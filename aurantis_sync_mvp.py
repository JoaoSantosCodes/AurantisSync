"""
AurantisSync – App GUI de Transcrição & Sincronização de Letras
Stack: Python 3.10+, PySide6, faster-whisper, librosa, matplotlib

Recursos neste MVP:
- Abrir áudio (.wav/.mp3)
- Plotar waveform
- Transcrever com faster-whisper (pt-BR por padrão)
- Editar linhas (início, fim, texto) numa tabela
- Exportar TXT, SRT, LRC, VTT e JSON

Para rodar:
  pip install -r requirements.txt
  # (Instale FFmpeg e deixe no PATH)
  python aurantis_sync.py

Requisitos (requirements.txt):
  PySide6
  faster-whisper
  librosa
  matplotlib
  numpy
  soundfile

Observação: FFmpeg deve estar instalado e no PATH do sistema.
"""

import sys
import os
import subprocess
from dataclasses import dataclass, asdict
from typing import List

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter
)
from PySide6.QtCore import Qt

import numpy as np
import matplotlib
matplotlib.use("QtAgg")  # Backend Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# --- MODELO ---
@dataclass
class Line:
    start: float
    end: float
    text: str

# --- EXPORTADORES ---
def export_txt(lines: List[Line], path: str):
    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            if ln.text.strip():
                f.write(ln.text.strip() + "\n")


def s_to_srt_time(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - int(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def export_srt(lines: List[Line], path: str):
    with open(path, "w", encoding="utf-8") as f:
        idx = 1
        for ln in lines:
            text = ln.text.strip()
            if not text:
                continue
            f.write(str(idx) + "\n")
            f.write(f"{s_to_srt_time(ln.start)} --> {s_to_srt_time(ln.end)}\n")
            f.write(text + "\n\n")
            idx += 1


def export_lrc(lines: List[Line], path: str):
    def s_to_lrc_time(t: float) -> str:
        if t < 0:
            t = 0
        m = int(t // 60)
        s = int(t % 60)
        cs = int((t - int(t)) * 100)  # centésimos
        return f"[{m:02d}:{s:02d}.{cs:02d}]"

    with open(path, "w", encoding="utf-8") as f:
        for ln in lines:
            text = ln.text.strip()
            if not text:
                continue
            f.write(s_to_lrc_time(ln.start) + text + "\n")


def export_vtt(lines: List[Line], path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for ln in lines:
            text = ln.text.strip()
            if not text:
                continue
            # VTT: hh:mm:ss.mmm
            def s_to_vtt_time(t: float) -> str:
                if t < 0:
                    t = 0
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t - int(t)) * 1000)
                return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

            f.write(f"{s_to_vtt_time(ln.start)} --> {s_to_vtt_time(ln.end)}\n")
            f.write(text + "\n\n")


def export_json(lines: List[Line], path: str):
    import json
    payload = [asdict(ln) for ln in lines if ln.text.strip()]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# --- WAVEFORM WIDGET ---
class WaveformWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 2), tight_layout=True)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Waveform")
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Amplitude")

    def plot_wave(self, y, sr):
        self.ax.clear()
        t = np.arange(len(y)) / float(sr)
        self.ax.plot(t, y, linewidth=0.8)
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("Waveform")
        self.ax.margins(x=0)
        self.draw()


# --- JANELA PRINCIPAL ---
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AurantisSync – Transcrição & Sincronização")
        self.resize(1100, 700)

        self.audio_path = None
        self.lines: List[Line] = []

        # Top controls
        top_bar = QHBoxLayout()

        self.btn_open = QPushButton("Abrir Áudio…")
        self.btn_open.clicked.connect(self.open_audio)
        top_bar.addWidget(self.btn_open)

        top_bar.addWidget(QLabel("Idioma:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["pt", "en", "es"])  # pode expandir
        self.lang_combo.setCurrentText("pt")
        top_bar.addWidget(self.lang_combo)

        top_bar.addWidget(QLabel("Modelo:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large-v3"])
        self.model_combo.setCurrentText("small")
        top_bar.addWidget(self.model_combo)

        self.btn_transcribe = QPushButton("Transcrever")
        self.btn_transcribe.clicked.connect(self.transcribe)
        top_bar.addWidget(self.btn_transcribe)

        self.btn_export_all = QPushButton("Exportar Tudo")
        self.btn_export_all.clicked.connect(self.export_all)
        top_bar.addWidget(self.btn_export_all)

        top_bar.addStretch(1)

        # Waveform + table
        self.wave = WaveformWidget()

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Início (s)", "Fim (s)", "Texto"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setWordWrap(True)
        self.table.setAlternatingRowColors(True)

        splitter = QSplitter(Qt.Vertical)
        wf_container = QWidget()
        wf_layout = QVBoxLayout(wf_container)
        wf_layout.addWidget(self.wave)
        splitter.addWidget(wf_container)
        splitter.addWidget(self.table)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        # Root layout
        root = QWidget()
        root_layout = QVBoxLayout(root)
        top_bar_w = QWidget(); top_bar_w.setLayout(top_bar)
        root_layout.addWidget(top_bar_w)
        root_layout.addWidget(splitter)
        self.setCentralWidget(root)

    # --- Funções ---
    def open_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Selecionar áudio", "", "Áudio (*.wav *.mp3 *.m4a *.flac)")
        if not path:
            return
        self.audio_path = path
        try:
            import soundfile as sf
            y, sr = sf.read(self.audio_path, always_2d=False)
            if y.ndim > 1:
                y = y.mean(axis=1)  # mono
            self.wave.plot_wave(y, sr)
        except Exception as e:
            QMessageBox.warning(self, "Waveform", f"Não foi possível carregar waveform:\n{e}")

    def ffmpeg_available(self) -> bool:
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True
        except Exception:
            return False

    def transcribe(self):
        if not self.audio_path:
            QMessageBox.information(self, "Transcrever", "Selecione um arquivo de áudio primeiro.")
            return
        if not self.ffmpeg_available():
            QMessageBox.warning(self, "FFmpeg", "FFmpeg não encontrado no PATH. Instale e tente novamente.")
            return

        lang = self.lang_combo.currentText()
        model_size = self.model_combo.currentText()

        self.setEnabled(False)
        QApplication.processEvents()

        try:
            from faster_whisper import WhisperModel
            model = WhisperModel(model_size, device="cpu")  # use "cuda" se tiver GPU
            segments, info = model.transcribe(self.audio_path, language=lang, beam_size=5)

            new_lines: List[Line] = []
            for seg in segments:
                st = float(seg.start) if seg.start is not None else 0.0
                ed = float(seg.end) if seg.end is not None else max(st + 0.5, st)
                txt = seg.text.strip()
                new_lines.append(Line(start=st, end=ed, text=txt))

            # Atualiza tabela
            self.lines = new_lines
            self.populate_table()
            QMessageBox.information(self, "Transcrição", f"Transcrição concluída. {len(self.lines)} linhas detectadas.")
        except Exception as e:
            QMessageBox.critical(self, "Transcrição", f"Erro ao transcrever:\n{e}")
        finally:
            self.setEnabled(True)

    def populate_table(self):
        self.table.setRowCount(0)
        for ln in self.lines:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(f"{ln.start:.2f}"))
            self.table.setItem(r, 1, QTableWidgetItem(f"{ln.end:.2f}"))
            self.table.setItem(r, 2, QTableWidgetItem(ln.text))

        # Permitir edição e salvar de volta
        self.table.itemChanged.connect(self._on_item_changed)

    def _on_item_changed(self, item: QTableWidgetItem):
        r = item.row()
        c = item.column()
        try:
            if c == 0:
                self.lines[r].start = float(item.text().replace(",", "."))
            elif c == 1:
                self.lines[r].end = float(item.text().replace(",", "."))
            elif c == 2:
                self.lines[r].text = item.text()
        except ValueError:
            pass

    def export_all(self):
        if not self.lines:
            QMessageBox.information(self, "Exportar", "Nenhuma linha para exportar.")
            return
        base, _ = QFileDialog.getSaveFileName(self, "Salvar base de arquivo", "letra", "Arquivos base (*.base)")
        if not base:
            return
        base = os.path.splitext(base)[0]
        try:
            export_txt(self.lines, base + ".txt")
            export_srt(self.lines, base + ".srt")
            export_lrc(self.lines, base + ".lrc")
            export_vtt(self.lines, base + ".vtt")
            export_json(self.lines, base + ".json")
            QMessageBox.information(self, "Exportar", "Arquivos TXT, SRT, LRC, VTT e JSON exportados com sucesso.")
        except Exception as e:
            QMessageBox.critical(self, "Exportar", f"Erro ao exportar arquivos:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

"""
Janela principal melhorada do aplicativo AurantisSync com funcionalidades do MVP.
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QPushButton, QComboBox, QLabel, 
    QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QKeySequence

import numpy as np
import matplotlib
matplotlib.use("QtAgg")  # Backend Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from app.core.sync_model import LyricLine
from app.core.transcriber import Transcriber
from app.core.exporters import Exporter


@dataclass
class Line:
    """Classe de linha simplificada (compatível com MVP)."""
    start: float
    end: float
    text: str


class TranscriptionThread(QThread):
    """Thread para transcrição em background."""
    progress = Signal(str)
    finished = Signal(list)
    error = Signal(str)
    
    def __init__(self, transcriber, audio_path, language, model_size):
        super().__init__()
        self.transcriber = transcriber
        self.audio_path = audio_path
        self.language = language
        self.model_size = model_size
    
    def run(self):
        try:
            self.progress.emit("Carregando modelo...")
            if not self.transcriber.load_model(self.model_size):
                self.error.emit("Falha ao carregar modelo do Whisper")
                return
            
            self.progress.emit("Transcrevendo áudio...")
            lines = self.transcriber.transcribe(self.audio_path, self.language, self.model_size)
            
            # Converter LyricLine para Line (compatível com MVP)
            mvp_lines = []
            for line in lines:
                mvp_lines.append(Line(
                    start=line.start,
                    end=line.end,
                    text=line.text
                ))
            
            self.progress.emit("Transcrição concluída!")
            self.finished.emit(mvp_lines)
            
        except Exception as e:
            self.error.emit(str(e))


class WaveformWidget(FigureCanvas):
    """Widget de waveform simplificado (compatível com MVP)."""
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


class MainWindow(QMainWindow):
    """Janela principal melhorada com funcionalidades do MVP."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AurantisSync – Transcrição & Sincronização")
        self.resize(1100, 700)

        self.audio_path = None
        self.lines: List[Line] = []
        self.transcriber = Transcriber()
        self.transcription_thread = None

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Configura a interface do usuário."""
        # Top controls
        top_bar = QHBoxLayout()

        self.btn_open = QPushButton("Abrir Áudio…")
        top_bar.addWidget(self.btn_open)

        top_bar.addWidget(QLabel("Idioma:"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["pt", "en", "es", "fr", "de", "it", "ja", "ko", "zh"])
        self.lang_combo.setCurrentText("pt")
        top_bar.addWidget(self.lang_combo)

        top_bar.addWidget(QLabel("Modelo:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large-v3"])
        self.model_combo.setCurrentText("small")
        top_bar.addWidget(self.model_combo)

        self.btn_transcribe = QPushButton("Transcrever")
        top_bar.addWidget(self.btn_transcribe)

        self.btn_export_all = QPushButton("Exportar Tudo")
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
        top_bar_w = QWidget()
        top_bar_w.setLayout(top_bar)
        root_layout.addWidget(top_bar_w)
        root_layout.addWidget(splitter)
        self.setCentralWidget(root)

    def setup_connections(self):
        """Configura as conexões dos sinais."""
        self.btn_open.clicked.connect(self.open_audio)
        self.btn_transcribe.clicked.connect(self.transcribe)
        self.btn_export_all.clicked.connect(self.export_all)
        self.table.itemChanged.connect(self._on_item_changed)

    def open_audio(self):
        """Abre arquivo de áudio e carrega waveform."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar áudio", "", 
            "Áudio (*.wav *.mp3 *.m4a *.flac *.ogg *.aac)"
        )
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
        """Verifica se FFmpeg está disponível."""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL, 
                         check=True)
            return True
        except Exception:
            return False

    def transcribe(self):
        """Inicia o processo de transcrição."""
        if not self.audio_path:
            QMessageBox.information(self, "Transcrever", "Selecione um arquivo de áudio primeiro.")
            return
        
        if not self.ffmpeg_available():
            QMessageBox.warning(self, "FFmpeg", 
                              "FFmpeg não encontrado no PATH. Instale e tente novamente.")
            return

        lang = self.lang_combo.currentText()
        model_size = self.model_combo.currentText()

        # Desabilitar controles durante transcrição
        self.setEnabled(False)
        QApplication.processEvents()

        # Criar e iniciar thread de transcrição
        self.transcription_thread = TranscriptionThread(
            self.transcriber, self.audio_path, lang, model_size
        )
        self.transcription_thread.progress.connect(self.on_transcription_progress)
        self.transcription_thread.finished.connect(self.on_transcription_finished)
        self.transcription_thread.error.connect(self.on_transcription_error)
        self.transcription_thread.start()

    def on_transcription_progress(self, message: str):
        """Chamado quando há progresso na transcrição."""
        # Aqui você pode atualizar uma barra de progresso ou status
        print(f"Transcrição: {message}")

    def on_transcription_finished(self, lines: List[Line]):
        """Chamado quando a transcrição é concluída."""
        self.lines = lines
        self.populate_table()
        QMessageBox.information(self, "Transcrição", 
                              f"Transcrição concluída. {len(self.lines)} linhas detectadas.")
        self.setEnabled(True)

    def on_transcription_error(self, error_message: str):
        """Chamado quando há erro na transcrição."""
        QMessageBox.critical(self, "Transcrição", f"Erro ao transcrever:\n{error_message}")
        self.setEnabled(True)

    def populate_table(self):
        """Popula a tabela com as linhas transcritas."""
        self.table.setRowCount(0)
        for ln in self.lines:
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(f"{ln.start:.2f}"))
            self.table.setItem(r, 1, QTableWidgetItem(f"{ln.end:.2f}"))
            self.table.setItem(r, 2, QTableWidgetItem(ln.text))

    def _on_item_changed(self, item: QTableWidgetItem):
        """Chamado quando um item da tabela é editado."""
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
        """Exporta para todos os formatos suportados."""
        if not self.lines:
            QMessageBox.information(self, "Exportar", "Nenhuma linha para exportar.")
            return
        
        base, _ = QFileDialog.getSaveFileName(
            self, "Salvar base de arquivo", "letra", "Arquivos base (*.base)"
        )
        if not base:
            return
        
        base = os.path.splitext(base)[0]
        try:
            # Converter Line para LyricLine para usar os exportadores existentes
            lyric_lines = []
            for line in self.lines:
                lyric_lines.append(LyricLine(
                    start=line.start,
                    end=line.end,
                    text=line.text
                ))
            
            # Exportar usando a classe Exporter
            exported_files = Exporter.export_all(lyric_lines, base)
            
            if exported_files:
                QMessageBox.information(
                    self, "Exportar", 
                    f"Arquivos exportados com sucesso:\n" + 
                    "\n".join(f"- {fmt}: {path}" for fmt, path in exported_files.items())
                )
            else:
                QMessageBox.warning(self, "Exportar", "Nenhum arquivo foi exportado.")
                
        except Exception as e:
            QMessageBox.critical(self, "Exportar", f"Erro ao exportar arquivos:\n{e}")

    def keyPressEvent(self, event):
        """Manipula eventos de teclado."""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Enter para próxima linha
            current_row = self.table.currentRow()
            if current_row < self.table.rowCount() - 1:
                self.table.setCurrentCell(current_row + 1, 0)
        elif event.key() == Qt.Key_Space:
            # Space para play/pause (implementar se necessário)
            pass
        else:
            super().keyPressEvent(event)

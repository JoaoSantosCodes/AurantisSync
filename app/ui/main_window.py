"""
Janela principal do aplicativo AurantisSync.
"""
import os
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QSplitter, QGroupBox, QPushButton, QComboBox, 
                               QLabel, QProgressBar, QTextEdit, QFileDialog, 
                               QMessageBox, QMenuBar, QMenu, QStatusBar, QApplication)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QAction, QKeySequence, QFont

from app.core.sync_model import SyncProject, LyricLine
from app.core.transcriber import Transcriber
from app.core.audio_player import AudioPlayer
from app.core.waveform import WaveformGenerator
from app.core.exporters import Exporter, ExportError
from app.core.project_io import ProjectIO
from app.widgets.waveform_widget import WaveformWidget
from app.widgets.lines_table import LinesTableWidget


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
            
            self.progress.emit("Transcrição concluída!")
            self.finished.emit(lines)
            
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Janela principal do aplicativo."""
    
    def __init__(self):
        super().__init__()
        self.project = SyncProject()
        self.transcriber = Transcriber()
        self.audio_player = AudioPlayer()
        self.waveform_generator = WaveformGenerator()
        self.project_io = ProjectIO()
        
        # Thread de transcrição
        self.transcription_thread = None
        
        # Estado da aplicação
        self.current_audio_path = ""
        self.is_playing = False
        self.guided_sync_mode = False
        
        self.setup_ui()
        self.setup_connections()
        self.setup_autosave()
        
        # Configurar callbacks do audio player
        self.audio_player.on_position_changed = self.on_audio_position_changed
        self.audio_player.on_playback_finished = self.on_playback_finished
    
    def setup_ui(self):
        """Configura a interface do usuário."""
        self.setWindowTitle("AurantisSync - Transcrição e Sincronização de Letras")
        self.setMinimumSize(1200, 800)
        
        # Menu
        self.setup_menu()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Painel esquerdo (áudio e waveform)
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Painel direito (controles e tabela)
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Definir proporções
        main_splitter.setSizes([800, 400])
        
        # Status bar
        self.setup_status_bar()
    
    def setup_menu(self):
        """Configura o menu da aplicação."""
        menubar = self.menuBar()
        
        # Menu Arquivo
        file_menu = menubar.addMenu("Arquivo")
        
        open_audio_action = QAction("Abrir Áudio", self)
        open_audio_action.setShortcut(QKeySequence.Open)
        open_audio_action.triggered.connect(self.open_audio)
        file_menu.addAction(open_audio_action)
        
        file_menu.addSeparator()
        
        new_project_action = QAction("Novo Projeto", self)
        new_project_action.setShortcut(QKeySequence.New)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)
        
        open_project_action = QAction("Abrir Projeto", self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
        
        save_project_action = QAction("Salvar Projeto", self)
        save_project_action.setShortcut(QKeySequence.Save)
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)
        
        save_as_action = QAction("Salvar Como...", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_menu = file_menu.addMenu("Exportar")
        
        export_txt_action = QAction("Texto (TXT)", self)
        export_txt_action.triggered.connect(lambda: self.export_format("txt"))
        export_menu.addAction(export_txt_action)
        
        export_srt_action = QAction("Legendas (SRT)", self)
        export_srt_action.triggered.connect(lambda: self.export_format("srt"))
        export_menu.addAction(export_srt_action)
        
        export_lrc_action = QAction("Letras (LRC)", self)
        export_lrc_action.triggered.connect(lambda: self.export_format("lrc"))
        export_menu.addAction(export_lrc_action)
        
        export_vtt_action = QAction("WebVTT (VTT)", self)
        export_vtt_action.triggered.connect(lambda: self.export_format("vtt"))
        export_menu.addAction(export_vtt_action)
        
        export_json_action = QAction("JSON", self)
        export_json_action.triggered.connect(lambda: self.export_format("json"))
        export_menu.addAction(export_json_action)
        
        export_all_action = QAction("Todos os Formatos", self)
        export_all_action.triggered.connect(self.export_all_formats)
        export_menu.addAction(export_all_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Sair", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Editar
        edit_menu = menubar.addMenu("Editar")
        
        undo_action = QAction("Desfazer", self)
        undo_action.setShortcut(QKeySequence.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Refazer", self)
        redo_action.setShortcut(QKeySequence.Redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        normalize_action = QAction("Normalizar Tempos", self)
        normalize_action.triggered.connect(self.normalize_times)
        edit_menu.addAction(normalize_action)
        
        # Menu Ferramentas
        tools_menu = menubar.addMenu("Ferramentas")
        
        guided_sync_action = QAction("Sincronização Guiada", self)
        guided_sync_action.triggered.connect(self.toggle_guided_sync)
        tools_menu.addAction(guided_sync_action)
        
        # Menu Ajuda
        help_menu = menubar.addMenu("Ajuda")
        
        about_action = QAction("Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_left_panel(self):
        """Cria o painel esquerdo com waveform."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Waveform widget
        self.waveform_widget = WaveformWidget()
        layout.addWidget(self.waveform_widget)
        
        return panel
    
    def create_right_panel(self):
        """Cria o painel direito com controles e tabela."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Grupo de controles de áudio
        audio_group = QGroupBox("Controles de Áudio")
        audio_layout = QVBoxLayout(audio_group)
        
        # Botão abrir áudio
        self.open_audio_btn = QPushButton("Abrir Áudio")
        self.open_audio_btn.clicked.connect(self.open_audio)
        audio_layout.addWidget(self.open_audio_btn)
        
        # Configurações de transcrição
        transcribe_layout = QHBoxLayout()
        
        transcribe_layout.addWidget(QLabel("Idioma:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["pt", "en", "es", "fr", "de", "it", "ja", "ko", "zh"])
        self.language_combo.setCurrentText("pt")
        transcribe_layout.addWidget(self.language_combo)
        
        transcribe_layout.addWidget(QLabel("Modelo:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large-v3"])
        self.model_combo.setCurrentText("base")
        self.model_combo.setToolTip("tiny: Rápido, Baixa qualidade\nbase: Equilibrado\nsmall: Boa qualidade\nmedium: Muito boa qualidade\nlarge-v3: Excelente qualidade")
        transcribe_layout.addWidget(self.model_combo)
        
        audio_layout.addLayout(transcribe_layout)
        
        # Botão transcrever
        self.transcribe_btn = QPushButton("Transcrever")
        self.transcribe_btn.clicked.connect(self.start_transcription)
        self.transcribe_btn.setEnabled(False)
        audio_layout.addWidget(self.transcribe_btn)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        audio_layout.addWidget(self.progress_bar)
        
        # Log de status
        self.status_log = QTextEdit()
        self.status_log.setMaximumHeight(100)
        self.status_log.setReadOnly(True)
        audio_layout.addWidget(self.status_log)
        
        layout.addWidget(audio_group)
        
        # Widget de tabela de linhas
        self.lines_table = LinesTableWidget()
        layout.addWidget(self.lines_table)
        
        # Controles de exportação
        export_group = QGroupBox("Exportação")
        export_layout = QVBoxLayout(export_group)
        
        export_buttons_layout = QHBoxLayout()
        
        self.export_txt_btn = QPushButton("TXT")
        self.export_txt_btn.clicked.connect(lambda: self.export_format("txt"))
        export_buttons_layout.addWidget(self.export_txt_btn)
        
        self.export_srt_btn = QPushButton("SRT")
        self.export_srt_btn.clicked.connect(lambda: self.export_format("srt"))
        export_buttons_layout.addWidget(self.export_srt_btn)
        
        self.export_lrc_btn = QPushButton("LRC")
        self.export_lrc_btn.clicked.connect(lambda: self.export_format("lrc"))
        export_buttons_layout.addWidget(self.export_lrc_btn)
        
        self.export_vtt_btn = QPushButton("VTT")
        self.export_vtt_btn.clicked.connect(lambda: self.export_format("vtt"))
        export_buttons_layout.addWidget(self.export_vtt_btn)
        
        self.export_json_btn = QPushButton("JSON")
        self.export_json_btn.clicked.connect(lambda: self.export_format("json"))
        export_buttons_layout.addWidget(self.export_json_btn)
        
        export_layout.addLayout(export_buttons_layout)
        
        self.export_all_btn = QPushButton("Exportar Tudo")
        self.export_all_btn.clicked.connect(self.export_all_formats)
        export_layout.addWidget(self.export_all_btn)
        
        layout.addWidget(export_group)
        
        return panel
    
    def setup_status_bar(self):
        """Configura a barra de status."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Labels de status
        self.audio_status_label = QLabel("Nenhum áudio carregado")
        self.device_status_label = QLabel("")
        self.project_status_label = QLabel("Projeto não salvo")
        
        self.status_bar.addWidget(self.audio_status_label)
        self.status_bar.addPermanentWidget(self.device_status_label)
        self.status_bar.addPermanentWidget(self.project_status_label)
        
        # Atualizar status do dispositivo
        device_info = self.transcriber.get_device_info()
        self.device_status_label.setText(device_info)
    
    def setup_connections(self):
        """Configura as conexões entre widgets."""
        # Waveform widget
        self.waveform_widget.play_pause_clicked.connect(self.toggle_playback)
        self.waveform_widget.seek_requested.connect(self.seek_audio)
        self.waveform_widget.position_changed.connect(self.on_position_changed)
        
        # Lines table
        self.lines_table.line_changed.connect(self.on_line_changed)
        self.lines_table.line_selected.connect(self.on_line_selected)
        self.lines_table.capture_start_requested.connect(self.capture_start_time)
        self.lines_table.capture_end_requested.connect(self.capture_end_time)
        self.lines_table.split_line_requested.connect(self.split_line)
        self.lines_table.merge_line_requested.connect(self.merge_line)
        
        # Audio player
        self.audio_player.on_position_changed = self.on_audio_position_changed
        self.audio_player.on_playback_finished = self.on_playback_finished
    
    def setup_autosave(self):
        """Configura o sistema de autosave."""
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
        self.autosave_timer.start(30000)  # 30 segundos
    
    def log_message(self, message: str):
        """Adiciona mensagem ao log."""
        self.status_log.append(f"[{self.get_current_time()}] {message}")
        self.status_log.ensureCursorVisible()
    
    def get_current_time(self) -> str:
        """Retorna tempo atual formatado."""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def open_audio(self):
        """Abre arquivo de áudio."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo de Áudio", "",
            "Arquivos de Áudio (*.wav *.mp3 *.m4a *.flac *.ogg);;Todos os Arquivos (*)"
        )
        
        if file_path:
            self.load_audio(file_path)
    
    def load_audio(self, file_path: str):
        """Carrega arquivo de áudio."""
        self.log_message(f"Carregando áudio: {os.path.basename(file_path)}")
        
        # Carregar no audio player
        if not self.audio_player.load_audio(file_path):
            QMessageBox.critical(self, "Erro", "Falha ao carregar arquivo de áudio")
            return
        
        # Gerar waveform
        if not self.waveform_generator.load_audio(file_path):
            QMessageBox.critical(self, "Erro", "Falha ao gerar waveform")
            return
        
        # Atualizar interface
        waveform_data, duration, sample_rate = self.waveform_generator.get_waveform_data()
        self.waveform_widget.load_waveform(waveform_data, duration, sample_rate)
        
        # Atualizar projeto
        self.project.audio_path = file_path
        self.current_audio_path = file_path
        
        # Atualizar status
        self.audio_status_label.setText(f"Áudio: {os.path.basename(file_path)}")
        self.transcribe_btn.setEnabled(True)
        
        self.log_message("Áudio carregado com sucesso!")
        self.mark_project_modified()
    
    def start_transcription(self):
        """Inicia processo de transcrição."""
        if not self.current_audio_path:
            QMessageBox.warning(self, "Aviso", "Nenhum áudio carregado")
            return
        
        # Verificar FFmpeg
        if not self.transcriber._check_ffmpeg():
            QMessageBox.critical(self, "FFmpeg não encontrado", 
                               self.transcriber.get_ffmpeg_instructions())
            return
        
        # Configurar interface
        self.transcribe_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminado
        
        # Obter configurações
        language = self.language_combo.currentText()
        model_size = self.model_combo.currentText()
        
        # Atualizar projeto
        self.project.language = language
        self.project.model_size = model_size
        
        # Iniciar thread de transcrição
        self.transcription_thread = TranscriptionThread(
            self.transcriber, self.current_audio_path, language, model_size
        )
        self.transcription_thread.progress.connect(self.log_message)
        self.transcription_thread.finished.connect(self.on_transcription_finished)
        self.transcription_thread.error.connect(self.on_transcription_error)
        self.transcription_thread.start()
    
    def on_transcription_finished(self, lines: list):
        """Chamado quando transcrição termina."""
        self.progress_bar.setVisible(False)
        self.transcribe_btn.setEnabled(True)
        
        # Atualizar projeto
        self.project.lines = lines
        
        # Atualizar tabela
        self.lines_table.set_lines(lines)
        
        # Atualizar waveform
        self.waveform_widget.update_lines(lines)
        
        self.log_message(f"Transcrição concluída! {len(lines)} linhas geradas.")
        self.mark_project_modified()
    
    def on_transcription_error(self, error_message: str):
        """Chamado quando há erro na transcrição."""
        self.progress_bar.setVisible(False)
        self.transcribe_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Erro na Transcrição", error_message)
        self.log_message(f"Erro: {error_message}")
    
    def toggle_playback(self):
        """Alterna entre play/pause."""
        if not self.audio_player.is_audio_loaded():
            return
        
        if self.is_playing:
            self.audio_player.pause()
            self.is_playing = False
        else:
            self.audio_player.play()
            self.is_playing = True
        
        self.waveform_widget.set_playing(self.is_playing)
    
    def seek_audio(self, position: float):
        """Vai para posição específica no áudio."""
        self.audio_player.seek(position)
    
    def on_audio_position_changed(self, position: float):
        """Chamado quando posição do áudio muda."""
        self.waveform_widget.set_position(position)
    
    def on_playback_finished(self):
        """Chamado quando reprodução termina."""
        self.is_playing = False
        self.waveform_widget.set_playing(False)
    
    def on_position_changed(self, position: float):
        """Chamado quando posição é alterada no waveform."""
        self.audio_player.seek(position)
    
    def on_line_changed(self, line_index: int, line: LyricLine):
        """Chamado quando linha é alterada."""
        if 0 <= line_index < len(self.project.lines):
            self.project.lines[line_index] = line
            self.waveform_widget.update_lines(self.project.lines)
            self.mark_project_modified()
    
    def on_line_selected(self, line_index: int):
        """Chamado quando linha é selecionada."""
        self.waveform_widget.highlight_line(line_index)
    
    def capture_start_time(self, line_index: int):
        """Captura tempo de início da linha atual."""
        current_position = self.audio_player.get_position()
        if 0 <= line_index < len(self.project.lines):
            self.project.lines[line_index].start = current_position
            self.lines_table.update_table()
            self.waveform_widget.update_lines(self.project.lines)
            self.mark_project_modified()
    
    def capture_end_time(self, line_index: int):
        """Captura tempo de fim da linha atual."""
        current_position = self.audio_player.get_position()
        if 0 <= line_index < len(self.project.lines):
            self.project.lines[line_index].end = current_position
            self.lines_table.update_table()
            self.waveform_widget.update_lines(self.project.lines)
            self.mark_project_modified()
    
    def split_line(self, line_index: int):
        """Divide uma linha."""
        if 0 <= line_index < len(self.project.lines):
            current_position = self.audio_player.get_position()
            self.project.split_line(line_index, current_position)
            self.lines_table.set_lines(self.project.lines)
            self.waveform_widget.update_lines(self.project.lines)
            self.mark_project_modified()
    
    def merge_line(self, line_index: int):
        """Une linha com a próxima."""
        if 0 <= line_index < len(self.project.lines) - 1:
            self.project.merge_lines(line_index)
            self.lines_table.set_lines(self.project.lines)
            self.waveform_widget.update_lines(self.project.lines)
            self.mark_project_modified()
    
    def normalize_times(self):
        """Normaliza tempos das linhas."""
        self.project._normalize_times()
        self.lines_table.set_lines(self.project.lines)
        self.waveform_widget.update_lines(self.project.lines)
        self.mark_project_modified()
        QMessageBox.information(self, "Normalização", "Tempos normalizados com sucesso!")
    
    def export_format(self, format_type: str):
        """Exporta para formato específico."""
        if not self.project.lines:
            QMessageBox.warning(self, "Aviso", "Nenhuma linha para exportar")
            return
        
        # Obter nome base do arquivo
        if self.project.audio_path:
            base_name = Path(self.project.audio_path).stem
        else:
            base_name = "letras"
        
        # Obter extensão
        extensions = {
            "txt": ".txt",
            "srt": ".srt", 
            "lrc": ".lrc",
            "vtt": ".vtt",
            "json": ".json"
        }
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Exportar {format_type.upper()}",
            f"{base_name}{extensions[format_type]}",
            f"Arquivos {format_type.upper()} (*{extensions[format_type]})"
        )
        
        if file_path:
            try:
                Exporter.export(self.project.lines, file_path, format_type)
                QMessageBox.information(self, "Sucesso", f"Arquivo exportado: {file_path}")
                self.log_message(f"Exportado {format_type.upper()}: {os.path.basename(file_path)}")
            except ExportError as e:
                QMessageBox.critical(self, "Erro na Exportação", str(e))
    
    def export_all_formats(self):
        """Exporta para todos os formatos."""
        if not self.project.lines:
            QMessageBox.warning(self, "Aviso", "Nenhuma linha para exportar")
            return
        
        # Obter diretório de saída
        output_dir = QFileDialog.getExistingDirectory(self, "Selecionar Diretório de Saída")
        if not output_dir:
            return
        
        # Obter nome base
        if self.project.audio_path:
            base_name = Path(self.project.audio_path).stem
        else:
            base_name = "letras"
        
        base_path = Path(output_dir) / base_name
        
        try:
            exported_files = Exporter.export_all(self.project.lines, str(base_path))
            
            if exported_files:
                message = "Arquivos exportados:\n"
                for fmt, path in exported_files.items():
                    message += f"• {fmt.upper()}: {os.path.basename(path)}\n"
                
                QMessageBox.information(self, "Exportação Concluída", message)
                self.log_message(f"Exportados {len(exported_files)} formatos para {output_dir}")
            else:
                QMessageBox.warning(self, "Aviso", "Nenhum arquivo foi exportado")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro na Exportação", str(e))
    
    def new_project(self):
        """Cria novo projeto."""
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Projeto não salvo",
                "Deseja salvar as alterações antes de criar um novo projeto?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                if not self.save_project():
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        # Limpar projeto
        self.project = SyncProject()
        self.current_audio_path = ""
        self.lines_table.clear_lines()
        self.waveform_widget.clear_highlights()
        
        # Resetar interface
        self.audio_status_label.setText("Nenhum áudio carregado")
        self.transcribe_btn.setEnabled(False)
        self.project_status_label.setText("Projeto não salvo")
        
        self.log_message("Novo projeto criado")
    
    def open_project(self):
        """Abre projeto existente."""
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Projeto não salvo",
                "Deseja salvar as alterações antes de abrir outro projeto?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                if not self.save_project():
                    return
            elif reply == QMessageBox.Cancel:
                return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Projeto", "",
            f"Projetos AurantisSync (*{ProjectIO.PROJECT_EXTENSION})"
        )
        
        if file_path:
            project = self.project_io.load_project(file_path)
            if project:
                self.load_project(project, file_path)
            else:
                QMessageBox.critical(self, "Erro", "Falha ao carregar projeto")
    
    def load_project(self, project: SyncProject, file_path: str):
        """Carrega projeto na interface."""
        self.project = project
        self.project_io.current_project_path = file_path
        
        # Carregar áudio se existir
        if project.audio_path and os.path.exists(project.audio_path):
            self.load_audio(project.audio_path)
        
        # Atualizar configurações
        self.language_combo.setCurrentText(project.language)
        self.model_combo.setCurrentText(project.model_size)
        
        # Atualizar linhas
        self.lines_table.set_lines(project.lines)
        self.waveform_widget.update_lines(project.lines)
        
        # Atualizar status
        self.project_status_label.setText(f"Projeto: {os.path.basename(file_path)}")
        
        self.log_message(f"Projeto carregado: {os.path.basename(file_path)}")
    
    def save_project(self) -> bool:
        """Salva projeto atual."""
        if not self.project_io.current_project_path:
            return self.save_project_as()
        
        success = self.project_io.save_project(self.project, self.project_io.current_project_path)
        if success:
            self.project_status_label.setText(f"Projeto: {os.path.basename(self.project_io.current_project_path)}")
            self.log_message("Projeto salvo com sucesso")
        else:
            QMessageBox.critical(self, "Erro", "Falha ao salvar projeto")
        
        return success
    
    def save_project_as(self) -> bool:
        """Salva projeto com novo nome."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Projeto", "",
            f"Projetos AurantisSync (*{ProjectIO.PROJECT_EXTENSION})"
        )
        
        if file_path:
            success = self.project_io.save_project(self.project, file_path)
            if success:
                self.project_status_label.setText(f"Projeto: {os.path.basename(file_path)}")
                self.log_message("Projeto salvo com sucesso")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao salvar projeto")
            return success
        
        return False
    
    def autosave(self):
        """Executa autosave."""
        if self.project_io.should_autosave() and self.project_io.current_project_path:
            self.project_io.create_autosave(self.project)
    
    def has_unsaved_changes(self) -> bool:
        """Verifica se há alterações não salvas."""
        return self.project_io.has_unsaved_changes
    
    def mark_project_modified(self):
        """Marca projeto como modificado."""
        self.project_io.mark_as_modified()
        self.project_status_label.setText("Projeto não salvo *")
    
    def toggle_guided_sync(self):
        """Alterna modo de sincronização guiada."""
        self.guided_sync_mode = not self.guided_sync_mode
        
        if self.guided_sync_mode:
            QMessageBox.information(
                self, "Sincronização Guiada",
                "Modo de sincronização guiada ativado.\n\n"
                "• Pressione Enter para capturar início da linha\n"
                "• Pressione Enter novamente para capturar fim\n"
                "• O áudio tocará automaticamente"
            )
        else:
            QMessageBox.information(self, "Sincronização Guiada", "Modo de sincronização guiada desativado.")
    
    def show_about(self):
        """Mostra diálogo sobre."""
        QMessageBox.about(
            self, "Sobre AurantisSync",
            "AurantisSync v1.0\n\n"
            "Aplicativo para transcrição e sincronização de letras de música.\n\n"
            "Desenvolvido com Python, PySide6 e faster-whisper.\n\n"
            "© 2024"
        )
    
    def keyPressEvent(self, event):
        """Trata eventos de teclado."""
        if event.key() == Qt.Key_Space:
            self.toggle_playback()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.guided_sync_mode:
                # Implementar lógica de sincronização guiada
                pass
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Trata evento de fechamento da janela."""
        if self.has_unsaved_changes():
            reply = QMessageBox.question(
                self, "Projeto não salvo",
                "Deseja salvar as alterações antes de sair?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Save:
                if not self.save_project():
                    event.ignore()
                    return
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        
        # Parar reprodução
        self.audio_player.stop()
        
        # Limpar autosave
        if self.project_io.current_project_path:
            self.project_io.delete_autosave(self.project_io.current_project_path)
        
        event.accept()

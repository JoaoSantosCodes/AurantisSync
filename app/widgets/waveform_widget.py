"""
Widget customizado para visualização de waveform.
"""
import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import matplotlib
matplotlib.use("QtAgg")  # Backend Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from app.core.sync_model import LyricLine


class WaveformWidget(QWidget):
    """Widget para visualização de waveform com controles de reprodução."""
    
    # Sinais
    position_changed = Signal(float)  # Posição do cursor alterada
    play_pause_clicked = Signal()     # Botão play/pause clicado
    seek_requested = Signal(float)    # Solicitação de seek
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.waveform_data = None
        self.duration = 0.0
        self.current_position = 0.0
        self.is_playing = False
        self.lines = []  # Lista de LyricLine para mostrar no waveform
        
        self.setup_ui()
        self.setup_plot()
        
        # Timer para atualizar posição
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_position)
        self.update_timer.start(100)  # Atualizar a cada 100ms
    
    def setup_ui(self):
        """Configura a interface do widget."""
        layout = QVBoxLayout(self)
        
        # Controles de reprodução
        controls_layout = QHBoxLayout()
        
        self.play_button = QPushButton("▶")
        self.play_button.clicked.connect(self.play_pause_clicked.emit)
        self.play_button.setFixedSize(40, 30)
        
        self.position_label = QLabel("00:00")
        self.position_label.setMinimumWidth(60)
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(1000)
        self.position_slider.valueChanged.connect(self.on_slider_changed)
        self.position_slider.sliderPressed.connect(self.on_slider_pressed)
        self.position_slider.sliderReleased.connect(self.on_slider_released)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setMinimumWidth(60)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setMaximumWidth(100)
        
        self.speed_combo = QPushButton("1.0x")
        self.speed_combo.setMaximumWidth(60)
        self.speed_combo.clicked.connect(self.cycle_speed)
        self.current_speed = 1.0
        
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.position_label)
        controls_layout.addWidget(self.position_slider)
        controls_layout.addWidget(self.duration_label)
        controls_layout.addWidget(QLabel("Vol:"))
        controls_layout.addWidget(self.volume_slider)
        controls_layout.addWidget(QLabel("Vel:"))
        controls_layout.addWidget(self.speed_combo)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Canvas do matplotlib
        self.figure = Figure(figsize=(12, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumHeight(150)
        layout.addWidget(self.canvas)
        
        # Conectar eventos do mouse
        self.canvas.mpl_connect('button_press_event', self.on_mouse_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
    
    def setup_plot(self):
        """Configura o plot do matplotlib."""
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel('Tempo (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.grid(True, alpha=0.3)
        
        # Linha do cursor
        self.cursor_line, = self.ax.plot([], [], 'r-', linewidth=2, alpha=0.8)
        
        # Retângulos para as linhas de letra
        self.line_rectangles = []
        
        self.figure.tight_layout()
    
    def load_waveform(self, waveform_data: np.ndarray, duration: float, sample_rate: int):
        """
        Carrega dados do waveform.
        
        Args:
            waveform_data: Dados do waveform
            duration: Duração em segundos
            sample_rate: Taxa de amostragem
        """
        self.waveform_data = waveform_data
        self.duration = duration
        self.sample_rate = sample_rate
        
        # Atualizar slider
        self.position_slider.setMaximum(int(duration * 1000))
        
        # Atualizar label de duração
        self.duration_label.setText(self.format_time(duration))
        
        # Plotar waveform
        self.plot_waveform()
    
    def plot_wave(self, y, sr):
        """Método simplificado para plotar waveform (compatível com MVP)."""
        self.ax.clear()
        t = np.arange(len(y)) / float(sr)
        self.ax.plot(t, y, linewidth=0.8)
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("Waveform")
        self.ax.margins(x=0)
        self.draw()
    
    def plot_waveform(self):
        """Plota o waveform no canvas."""
        if self.waveform_data is None:
            return
        
        self.ax.clear()
        
        # Criar array de tempo
        time = np.linspace(0, self.duration, len(self.waveform_data))
        
        # Plotar waveform
        self.ax.plot(time, self.waveform_data, 'b-', linewidth=0.5, alpha=0.7)
        self.ax.fill_between(time, self.waveform_data, alpha=0.3)
        
        # Configurar eixos
        self.ax.set_xlim(0, self.duration)
        self.ax.set_xlabel('Tempo (s)')
        self.ax.set_ylabel('Amplitude')
        self.ax.grid(True, alpha=0.3)
        
        # Adicionar linhas de letra se existirem
        self.plot_lyric_lines()
        
        # Adicionar cursor
        self.cursor_line, = self.ax.plot([], [], 'r-', linewidth=2, alpha=0.8)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_lyric_lines(self):
        """Plota as linhas de letra no waveform."""
        # Limpar retângulos anteriores
        for rect in self.line_rectangles:
            rect.remove()
        self.line_rectangles.clear()
        
        if not self.lines:
            return
        
        # Adicionar retângulos para cada linha
        for i, line in enumerate(self.lines):
            if not line.is_empty():
                # Cor alternada para melhor visualização
                color = 'lightblue' if i % 2 == 0 else 'lightgreen'
                alpha = 0.3
                
                rect = Rectangle(
                    (line.start, -1), 
                    line.end - line.start, 
                    2, 
                    facecolor=color, 
                    alpha=alpha,
                    edgecolor='blue',
                    linewidth=1
                )
                self.ax.add_patch(rect)
                self.line_rectangles.append(rect)
                
                # Adicionar texto da linha (se couber)
                if line.end - line.start > 2:  # Só se a linha for longa o suficiente
                    mid_time = (line.start + line.end) / 2
                    self.ax.text(mid_time, 0.8, line.text[:20] + "..." if len(line.text) > 20 else line.text,
                               ha='center', va='center', fontsize=8, rotation=0)
    
    def update_lines(self, lines: list):
        """Atualiza as linhas de letra exibidas."""
        self.lines = lines
        if self.waveform_data is not None:
            self.plot_waveform()
    
    def set_position(self, position: float):
        """Define a posição atual do cursor."""
        self.current_position = position
        
        # Atualizar slider (sem emitir sinal)
        self.position_slider.blockSignals(True)
        self.position_slider.setValue(int(position * 1000))
        self.position_slider.blockSignals(False)
        
        # Atualizar label
        self.position_label.setText(self.format_time(position))
        
        # Atualizar cursor no plot
        self.update_cursor()
    
    def update_cursor(self):
        """Atualiza a posição do cursor no plot."""
        if self.cursor_line is not None:
            self.cursor_line.set_data([self.current_position, self.current_position], [-1, 1])
            self.canvas.draw_idle()
    
    def set_playing(self, playing: bool):
        """Define se está tocando."""
        self.is_playing = playing
        self.play_button.setText("⏸" if playing else "▶")
    
    def update_position(self):
        """Atualiza a posição (chamado pelo timer)."""
        if self.is_playing:
            # A posição será atualizada pelo audio player
            pass
    
    def on_slider_changed(self, value):
        """Chamado quando o slider é movido."""
        position = value / 1000.0
        self.set_position(position)
        self.seek_requested.emit(position)
    
    def on_slider_pressed(self):
        """Chamado quando o slider é pressionado."""
        # Pausar reprodução durante o drag
        pass
    
    def on_slider_released(self):
        """Chamado quando o slider é solto."""
        # Retomar reprodução se estava tocando
        pass
    
    def on_mouse_click(self, event):
        """Chamado quando o mouse é clicado no plot."""
        if event.inaxes == self.ax and event.button == 1:  # Botão esquerdo
            position = event.xdata
            if position is not None:
                self.set_position(position)
                self.seek_requested.emit(position)
    
    def on_mouse_move(self, event):
        """Chamado quando o mouse se move sobre o plot."""
        if event.inaxes == self.ax:
            # Mostrar posição no tooltip ou status
            if event.xdata is not None:
                time_str = self.format_time(event.xdata)
                # Aqui você pode atualizar um tooltip ou status bar
                pass
    
    def cycle_speed(self):
        """Alterna entre velocidades de reprodução."""
        speeds = [0.75, 1.0, 1.25, 1.5, 2.0]
        current_index = speeds.index(self.current_speed)
        next_index = (current_index + 1) % len(speeds)
        self.current_speed = speeds[next_index]
        self.speed_combo.setText(f"{self.current_speed}x")
    
    def get_volume(self) -> float:
        """Retorna o volume atual (0.0 a 1.0)."""
        return self.volume_slider.value() / 100.0
    
    def get_speed(self) -> float:
        """Retorna a velocidade atual."""
        return self.current_speed
    
    def format_time(self, seconds: float) -> str:
        """Formata tempo em formato MM:SS."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"
    
    def highlight_line(self, line_index: int):
        """Destaca uma linha específica no waveform."""
        if 0 <= line_index < len(self.lines):
            line = self.lines[line_index]
            if not line.is_empty():
                # Destacar a linha
                self.ax.axvspan(line.start, line.end, alpha=0.5, color='yellow')
                self.canvas.draw()
    
    def clear_highlights(self):
        """Remove todos os destaques."""
        # Remover spans de destaque
        for span in self.ax.collections:
            if hasattr(span, '_highlight'):
                span.remove()
        self.canvas.draw()
    
    def zoom_to_line(self, line_index: int):
        """Faz zoom para uma linha específica."""
        if 0 <= line_index < len(self.lines):
            line = self.lines[line_index]
            if not line.is_empty():
                # Adicionar margem
                margin = (line.end - line.start) * 0.1
                self.ax.set_xlim(max(0, line.start - margin), 
                               min(self.duration, line.end + margin))
                self.canvas.draw()
    
    def reset_zoom(self):
        """Reseta o zoom para mostrar todo o waveform."""
        self.ax.set_xlim(0, self.duration)
        self.canvas.draw()

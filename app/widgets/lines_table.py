"""
Widget de tabela para edição de linhas de letra.
"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                               QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                               QHeaderView, QMessageBox, QMenu, QAbstractItemView)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QAction

from app.core.sync_model import LyricLine


class LinesTableWidget(QWidget):
    """Widget de tabela para edição de linhas de letra com timestamps."""
    
    # Sinais
    line_changed = Signal(int, LyricLine)      # Linha alterada
    line_selected = Signal(int)                # Linha selecionada
    capture_start_requested = Signal(int)      # Solicitação para capturar início
    capture_end_requested = Signal(int)        # Solicitação para capturar fim
    split_line_requested = Signal(int)         # Solicitação para dividir linha
    merge_line_requested = Signal(int)         # Solicitação para unir linha
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lines = []
        self.current_audio_position = 0.0
        self.setup_ui()
        self.setup_shortcuts()
    
    def setup_ui(self):
        """Configura a interface do widget."""
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Linhas de Letra")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title_label)
        
        # Controles superiores
        controls_layout = QHBoxLayout()
        
        self.capture_start_btn = QPushButton("Capturar Início")
        self.capture_start_btn.clicked.connect(self.capture_start)
        self.capture_start_btn.setEnabled(False)
        
        self.capture_end_btn = QPushButton("Capturar Fim")
        self.capture_end_btn.clicked.connect(self.capture_end)
        self.capture_end_btn.setEnabled(False)
        
        self.split_btn = QPushButton("Dividir Linha")
        self.split_btn.clicked.connect(self.split_line)
        self.split_btn.setEnabled(False)
        
        self.merge_btn = QPushButton("Unir com Próxima")
        self.merge_btn.clicked.connect(self.merge_line)
        self.merge_btn.setEnabled(False)
        
        self.normalize_btn = QPushButton("Normalizar Tempos")
        self.normalize_btn.clicked.connect(self.normalize_times)
        
        controls_layout.addWidget(self.capture_start_btn)
        controls_layout.addWidget(self.capture_end_btn)
        controls_layout.addWidget(self.split_btn)
        controls_layout.addWidget(self.merge_btn)
        controls_layout.addWidget(self.normalize_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Início (s)", "Fim (s)", "Texto", "▶"])
        
        # Configurar tabela
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Início
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Fim
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Texto
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Preview
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # Conectar sinais
        self.table.itemChanged.connect(self.on_item_changed)
        self.table.currentItemChanged.connect(self.on_item_changed)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.table)
        
        # Status
        self.status_label = QLabel("Nenhuma linha selecionada")
        layout.addWidget(self.status_label)
    
    def setup_shortcuts(self):
        """Configura atalhos de teclado."""
        # Enter para avançar para próxima linha
        # Space para play/pause (será tratado na janela principal)
        pass
    
    def set_lines(self, lines: list):
        """Define as linhas a serem exibidas."""
        self.lines = lines.copy()
        self.update_table()
    
    def update_table(self):
        """Atualiza a tabela com as linhas atuais."""
        self.table.blockSignals(True)
        self.table.setRowCount(len(self.lines))
        
        for i, line in enumerate(self.lines):
            # Início
            start_item = QTableWidgetItem(f"{line.start:.2f}")
            start_item.setData(Qt.UserRole, i)
            self.table.setItem(i, 0, start_item)
            
            # Fim
            end_item = QTableWidgetItem(f"{line.end:.2f}")
            end_item.setData(Qt.UserRole, i)
            self.table.setItem(i, 1, end_item)
            
            # Texto
            text_item = QTableWidgetItem(line.text)
            text_item.setData(Qt.UserRole, i)
            self.table.setItem(i, 2, text_item)
            
            # Botão de preview
            preview_btn = QPushButton("▶")
            preview_btn.setMaximumWidth(30)
            preview_btn.clicked.connect(lambda checked, idx=i: self.preview_line(idx))
            self.table.setCellWidget(i, 3, preview_btn)
        
        self.table.blockSignals(False)
        self.update_controls_state()
    
    def on_item_changed(self, item):
        """Chamado quando um item da tabela é alterado."""
        row = item.row()
        column = item.column()
        
        if 0 <= row < len(self.lines):
            line = self.lines[row]
            
            try:
                if column == 0:  # Início
                    line.start = float(item.text())
                elif column == 1:  # Fim
                    line.end = float(item.text())
                elif column == 2:  # Texto
                    line.text = item.text()
                
                # Emitir sinal de mudança
                self.line_changed.emit(row, line)
                self.update_status()
                
            except ValueError:
                # Reverter valor inválido
                if column == 0:
                    item.setText(f"{line.start:.2f}")
                elif column == 1:
                    item.setText(f"{line.end:.2f}")
                QMessageBox.warning(self, "Valor Inválido", 
                                  "Por favor, insira um número válido.")
    
    def on_row_changed(self, current_item, previous_item):
        """Chamado quando a linha selecionada muda."""
        self.update_controls_state()
        self.update_status()
        
        if current_item is not None:
            current_row = current_item.row()
            self.line_selected.emit(current_row)
    
    def update_controls_state(self):
        """Atualiza o estado dos controles baseado na seleção."""
        current_row = self.table.currentRow()
        has_selection = current_row >= 0
        has_lines = len(self.lines) > 0
        
        self.capture_start_btn.setEnabled(has_selection)
        self.capture_end_btn.setEnabled(has_selection)
        self.split_btn.setEnabled(has_selection and has_lines)
        self.merge_btn.setEnabled(has_selection and current_row < len(self.lines) - 1)
        self.normalize_btn.setEnabled(has_lines)
    
    def update_status(self):
        """Atualiza o label de status."""
        current_row = self.table.currentRow()
        
        if current_row >= 0 and current_row < len(self.lines):
            line = self.lines[current_row]
            duration = line.end - line.start
            self.status_label.setText(
                f"Linha {current_row + 1}: {line.start:.2f}s - {line.end:.2f}s "
                f"(duração: {duration:.2f}s)"
            )
        else:
            self.status_label.setText("Nenhuma linha selecionada")
    
    def capture_start(self):
        """Captura o tempo de início da linha atual."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.capture_start_requested.emit(current_row)
    
    def capture_end(self):
        """Captura o tempo de fim da linha atual."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.capture_end_requested.emit(current_row)
    
    def split_line(self):
        """Divide a linha atual."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.split_line_requested.emit(current_row)
    
    def merge_line(self):
        """Une a linha atual com a próxima."""
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.merge_line_requested.emit(current_row)
    
    def normalize_times(self):
        """Normaliza os tempos das linhas."""
        # Ordenar por tempo de início
        self.lines.sort(key=lambda x: x.start)
        
        # Ajustar sobreposições
        for i in range(len(self.lines) - 1):
            current = self.lines[i]
            next_line = self.lines[i + 1]
            
            if current.end > next_line.start:
                current.end = next_line.start
        
        self.update_table()
        QMessageBox.information(self, "Normalização", "Tempos normalizados com sucesso!")
    
    def preview_line(self, line_index: int):
        """Preview de uma linha específica."""
        if 0 <= line_index < len(self.lines):
            line = self.lines[line_index]
            # Emitir sinal para a janela principal tocar o trecho
            # Isso será implementado na janela principal
            pass
    
    def add_line(self, line: LyricLine = None):
        """Adiciona uma nova linha."""
        if line is None:
            line = LyricLine()
        
        self.lines.append(line)
        self.update_table()
        
        # Selecionar a nova linha
        self.table.selectRow(len(self.lines) - 1)
    
    def remove_line(self, line_index: int):
        """Remove uma linha."""
        if 0 <= line_index < len(self.lines):
            del self.lines[line_index]
            self.update_table()
    
    def insert_line(self, line_index: int, line: LyricLine = None):
        """Insere uma linha em uma posição específica."""
        if line is None:
            line = LyricLine()
        
        if 0 <= line_index <= len(self.lines):
            self.lines.insert(line_index, line)
            self.update_table()
            self.table.selectRow(line_index)
    
    def get_current_line(self) -> LyricLine:
        """Retorna a linha atualmente selecionada."""
        current_row = self.table.currentRow()
        if 0 <= current_row < len(self.lines):
            return self.lines[current_row]
        return None
    
    def set_current_line(self, line: LyricLine):
        """Define a linha atual."""
        current_row = self.table.currentRow()
        if 0 <= current_row < len(self.lines):
            self.lines[current_row] = line
            self.update_table()
    
    def update_audio_position(self, position: float):
        """Atualiza a posição atual do áudio."""
        self.current_audio_position = position
    
    def show_context_menu(self, position):
        """Mostra menu de contexto."""
        item = self.table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        menu = QMenu(self)
        
        # Ações do menu
        add_action = QAction("Adicionar Linha", self)
        add_action.triggered.connect(lambda: self.add_line())
        
        remove_action = QAction("Remover Linha", self)
        remove_action.triggered.connect(lambda: self.remove_line(row))
        
        insert_action = QAction("Inserir Linha", self)
        insert_action.triggered.connect(lambda: self.insert_line(row))
        
        menu.addAction(add_action)
        menu.addAction(remove_action)
        menu.addAction(insert_action)
        
        menu.exec_(self.table.mapToGlobal(position))
    
    def get_lines(self) -> list:
        """Retorna todas as linhas."""
        return self.lines.copy()
    
    def clear_lines(self):
        """Limpa todas as linhas."""
        self.lines.clear()
        self.update_table()
    
    def select_line(self, line_index: int):
        """Seleciona uma linha específica."""
        if 0 <= line_index < len(self.lines):
            self.table.selectRow(line_index)
    
    def highlight_line(self, line_index: int):
        """Destaca uma linha específica."""
        if 0 <= line_index < len(self.lines):
            # Destacar a linha na tabela
            for col in range(self.table.columnCount()):
                item = self.table.item(line_index, col)
                if item:
                    item.setBackground(Qt.yellow)
    
    def clear_highlights(self):
        """Remove todos os destaques."""
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(Qt.white)

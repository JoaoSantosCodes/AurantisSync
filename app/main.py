"""
Ponto de entrada principal do AurantisSync.
"""
import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont

from app.ui.main_window_improved import MainWindow


def check_dependencies():
    """Verifica se todas as dependências estão instaladas."""
    missing_deps = []
    
    try:
        import faster_whisper
    except ImportError:
        missing_deps.append("faster-whisper")
    
    try:
        import pydub
    except ImportError:
        missing_deps.append("pydub")
    
    try:
        import sounddevice
    except ImportError:
        missing_deps.append("sounddevice")
    
    try:
        import librosa
    except ImportError:
        missing_deps.append("librosa")
    
    try:
        import matplotlib
    except ImportError:
        missing_deps.append("matplotlib")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    try:
        import scipy
    except ImportError:
        missing_deps.append("scipy")
    
    if missing_deps:
        return False, missing_deps
    
    return True, []


def show_dependency_error(missing_deps):
    """Mostra erro de dependências faltando."""
    app = QApplication(sys.argv)
    
    message = "As seguintes dependências estão faltando:\n\n"
    for dep in missing_deps:
        message += f"• {dep}\n"
    
    message += "\nPara instalar, execute:\n"
    message += "pip install -r requirements.txt"
    
    QMessageBox.critical(None, "Dependências Faltando", message)
    sys.exit(1)


def create_splash_screen():
    """Cria tela de splash."""
    # Criar uma tela de splash simples
    pixmap = QPixmap(400, 300)
    pixmap.fill(Qt.darkBlue)
    
    splash = QSplashScreen(pixmap)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    
    # Adicionar texto
    splash.showMessage(
        "AurantisSync\nCarregando...",
        Qt.AlignCenter | Qt.AlignBottom,
        Qt.white
    )
    
    return splash


def main():
    """Função principal."""
    # Verificar dependências
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        show_dependency_error(missing_deps)
    
    # Criar aplicação
    app = QApplication(sys.argv)
    app.setApplicationName("AurantisSync")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("AurantisSync")
    
    # Configurar fonte padrão
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    
    # Criar e mostrar splash screen
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    
    # Simular carregamento
    QTimer.singleShot(2000, splash.close)
    
    try:
        # Criar janela principal
        main_window = MainWindow()
        
        # Fechar splash e mostrar janela principal
        def show_main_window():
            splash.close()
            main_window.show()
        
        QTimer.singleShot(2000, show_main_window)
        
        # Executar aplicação
        sys.exit(app.exec())
        
    except Exception as e:
        splash.close()
        QMessageBox.critical(
            None, "Erro Fatal",
            f"Erro ao inicializar aplicação:\n\n{str(e)}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

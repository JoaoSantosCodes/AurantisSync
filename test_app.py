"""
Script de teste para verificar se o aplicativo está funcionando corretamente.
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório app ao path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("Testando imports...")
    
    try:
        from core.sync_model import SyncProject, LyricLine
        print("✓ sync_model importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar sync_model: {e}")
        return False
    
    try:
        from core.transcriber import Transcriber
        print("✓ transcriber importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar transcriber: {e}")
        return False
    
    try:
        from core.audio_player import AudioPlayer
        print("✓ audio_player importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar audio_player: {e}")
        return False
    
    try:
        from core.waveform import WaveformGenerator
        print("✓ waveform importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar waveform: {e}")
        return False
    
    try:
        from core.exporters import Exporter
        print("✓ exporters importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar exporters: {e}")
        return False
    
    try:
        from core.project_io import ProjectIO
        print("✓ project_io importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar project_io: {e}")
        return False
    
    try:
        from widgets.waveform_widget import WaveformWidget
        print("✓ waveform_widget importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar waveform_widget: {e}")
        return False
    
    try:
        from widgets.lines_table import LinesTableWidget
        print("✓ lines_table importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar lines_table: {e}")
        return False
    
    try:
        from ui.main_window import MainWindow
        print("✓ main_window importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar main_window: {e}")
        return False
    
    return True


def test_core_functionality():
    """Testa funcionalidades básicas dos módulos core."""
    print("\nTestando funcionalidades core...")
    
    try:
        from core.sync_model import SyncProject, LyricLine
        
        # Testar LyricLine
        line = LyricLine(start=0.0, end=5.0, text="Teste")
        assert line.start == 0.0
        assert line.end == 5.0
        assert line.text == "Teste"
        assert not line.is_empty()
        print("✓ LyricLine funcionando")
        
        # Testar SyncProject
        project = SyncProject()
        project.add_line(line)
        assert len(project.lines) == 1
        print("✓ SyncProject funcionando")
        
    except Exception as e:
        print(f"✗ Erro na funcionalidade core: {e}")
        return False
    
    try:
        from core.exporters import Exporter
        
        # Testar exportação
        lines = [LyricLine(start=0.0, end=5.0, text="Teste")]
        formats = Exporter.get_supported_formats()
        assert len(formats) > 0
        print("✓ Exporters funcionando")
        
    except Exception as e:
        print(f"✗ Erro nos exporters: {e}")
        return False
    
    return True


def test_dependencies():
    """Testa se todas as dependências estão instaladas."""
    print("\nTestando dependências...")
    
    dependencies = [
        ('PySide6', 'PySide6'),
        ('faster_whisper', 'faster_whisper'),
        ('pydub', 'pydub'),
        ('sounddevice', 'sounddevice'),
        ('librosa', 'librosa'),
        ('matplotlib', 'matplotlib'),
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
    ]
    
    all_ok = True
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✓ {name} instalado")
        except ImportError:
            print(f"✗ {name} não encontrado")
            all_ok = False
    
    return all_ok


def test_ffmpeg():
    """Testa se FFmpeg está disponível."""
    print("\nTestando FFmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, check=True)
        print("✓ FFmpeg encontrado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ FFmpeg não encontrado")
        print("  Instale FFmpeg para usar o aplicativo")
        return False


def test_ui_creation():
    """Testa se a interface pode ser criada."""
    print("\nTestando criação da interface...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        # Criar aplicação (sem mostrar)
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Criar janela principal
        window = MainWindow()
        print("✓ Interface criada com sucesso")
        
        # Limpar
        window.close()
        return True
        
    except Exception as e:
        print(f"✗ Erro ao criar interface: {e}")
        return False


def main():
    """Função principal de teste."""
    print("=== Teste do AurantisSync ===\n")
    
    tests = [
        ("Dependências", test_dependencies),
        ("Imports", test_imports),
        ("Funcionalidades Core", test_core_functionality),
        ("FFmpeg", test_ffmpeg),
        ("Interface", test_ui_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "="*50)
    print("RESUMO DOS TESTES")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASSOU" if result else "FALHOU"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O aplicativo está pronto para uso.")
        print("\nPara executar:")
        print("  python app/main.py")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Verifique os erros acima.")
        print("\nPara instalar dependências faltando:")
        print("  pip install -r requirements.txt")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Teste do MVP do AurantisSync
"""
import sys
import os

def test_imports():
    """Testa se todos os imports necessários funcionam."""
    print("Testando imports...")
    
    try:
        from PySide6.QtWidgets import QApplication
        print("✓ PySide6 importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar PySide6: {e}")
        return False
    
    try:
        import faster_whisper
        print("✓ faster-whisper importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar faster-whisper: {e}")
        return False
    
    try:
        import librosa
        print("✓ librosa importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar librosa: {e}")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar matplotlib: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar numpy: {e}")
        return False
    
    try:
        import soundfile
        print("✓ soundfile importado com sucesso")
    except ImportError as e:
        print(f"✗ Erro ao importar soundfile: {e}")
        return False
    
    return True

def test_ffmpeg():
    """Testa se FFmpeg está disponível."""
    print("\nTestando FFmpeg...")
    
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✓ FFmpeg encontrado")
            return True
        else:
            print("✗ FFmpeg não encontrado")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar FFmpeg: {e}")
        return False

def test_mvp_file():
    """Testa se o arquivo MVP existe e pode ser importado."""
    print("\nTestando arquivo MVP...")
    
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("✗ Arquivo aurantis_sync_mvp.py não encontrado")
        return False
    
    try:
        # Tentar importar o módulo MVP
        import importlib.util
        spec = importlib.util.spec_from_file_location("mvp", "aurantis_sync_mvp.py")
        mvp_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mvp_module)
        print("✓ Arquivo MVP pode ser importado")
        return True
    except Exception as e:
        print(f"✗ Erro ao importar MVP: {e}")
        return False

def main():
    """Função principal de teste."""
    print("=== Teste do MVP AurantisSync ===\n")
    
    tests = [
        ("Imports", test_imports),
        ("FFmpeg", test_ffmpeg),
        ("Arquivo MVP", test_mvp_file)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print(f"\n=== Resultado dos Testes ===")
    print(f"Passou: {passed}/{total}")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O MVP está pronto para uso.")
        print("\nPara executar:")
        print("  python aurantis_sync_mvp.py")
        print("  ou")
        print("  start_app.bat (duplo clique)")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\nPara instalar dependências:")
        print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()

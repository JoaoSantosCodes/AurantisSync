#!/usr/bin/env python3
"""
Script para testar a aplicação estruturada
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from app.core.sync_model import LyricLine, SyncProject
        print("✅ app.core.sync_model - OK")
    except Exception as e:
        print(f"❌ app.core.sync_model - ERRO: {e}")
        return False
    
    try:
        from app.core.exporters import export_txt, export_srt, export_lrc, export_vtt, export_json
        print("✅ app.core.exporters - OK")
    except Exception as e:
        print(f"❌ app.core.exporters - ERRO: {e}")
        return False
    
    try:
        from app.core.transcriber import Transcriber
        print("✅ app.core.transcriber - OK")
    except Exception as e:
        print(f"❌ app.core.transcriber - ERRO: {e}")
        return False
    
    try:
        from app.widgets.waveform_widget import WaveformWidget
        print("✅ app.widgets.waveform_widget - OK")
    except Exception as e:
        print(f"❌ app.widgets.waveform_widget - ERRO: {e}")
        return False
    
    try:
        from app.widgets.lines_table import LinesTableWidget
        print("✅ app.widgets.lines_table - OK")
    except Exception as e:
        print(f"❌ app.widgets.lines_table - ERRO: {e}")
        return False
    
    try:
        from app.ui.main_window_improved import MainWindow
        print("✅ app.ui.main_window_improved - OK")
    except Exception as e:
        print(f"❌ app.ui.main_window_improved - ERRO: {e}")
        return False
    
    return True

def test_main_app():
    """Testa se a aplicação principal pode ser executada"""
    print("\n🚀 Testando aplicação principal...")
    
    try:
        # Importar sem executar
        from app.main import main, check_dependencies
        
        # Testar verificação de dependências
        deps_ok, missing_deps = check_dependencies()
        if deps_ok:
            print("✅ Dependências - OK")
        else:
            print(f"⚠️ Dependências faltando: {missing_deps}")
        
        print("✅ Aplicação principal - OK")
        return True
        
    except Exception as e:
        print(f"❌ Aplicação principal - ERRO: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 Testando aplicação estruturada AurantisSync")
    print("=" * 50)
    
    # Testar imports
    imports_ok = test_imports()
    
    # Testar aplicação principal
    app_ok = test_main_app()
    
    print("\n" + "=" * 50)
    if imports_ok and app_ok:
        print("🎉 Todos os testes passaram!")
        print("✅ Aplicação estruturada está funcionando")
        return True
    else:
        print("❌ Alguns testes falharam")
        print("🔧 Verifique os erros acima")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

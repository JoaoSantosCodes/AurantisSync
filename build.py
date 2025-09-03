"""
Script de build para criar executável com PyInstaller.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """Limpa arquivos de build anteriores."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removendo {dir_name}...")
            shutil.rmtree(dir_name)
    
    # Remover arquivos .spec
    for spec_file in Path('.').glob('*.spec'):
        print(f"Removendo {spec_file}...")
        spec_file.unlink()


def build_executable():
    """Cria executável com PyInstaller."""
    print("Criando executável com PyInstaller...")
    
    # Comando PyInstaller
    cmd = [
        'pyinstaller',
        '--noconsole',                    # Sem console
        '--onefile',                      # Arquivo único
        '--name', 'AurantisSync',         # Nome do executável
        '--distpath', 'dist',             # Pasta de saída
        '--workpath', 'build',            # Pasta de trabalho
        '--specpath', '.',                # Pasta para arquivo .spec
        
        # Incluir módulos necessários
        '--hidden-import', 'faster_whisper',
        '--hidden-import', 'pydub',
        '--hidden-import', 'sounddevice',
        '--hidden-import', 'librosa',
        '--hidden-import', 'matplotlib',
        '--hidden-import', 'numpy',
        '--hidden-import', 'scipy',
        '--hidden-import', 'PySide6',
        
        # Incluir dados se existirem
        '--add-data', 'examples;examples' if os.path.exists('examples') else '',
        
        # Ponto de entrada
        'app/main.py'
    ]
    
    # Remover elementos vazios
    cmd = [arg for arg in cmd if arg]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build concluído com sucesso!")
        print(f"Executável criado em: dist/AurantisSync{'exe' if sys.platform == 'win32' else ''}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro no build: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False


def create_installer_script():
    """Cria script de instalação."""
    if sys.platform == 'win32':
        # Script batch para Windows
        script_content = """@echo off
echo Instalando AurantisSync...
echo.
echo Verificando dependencias...

REM Verificar se FFmpeg esta instalado
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: FFmpeg nao encontrado!
    echo.
    echo Para instalar FFmpeg:
    echo 1. Baixe de https://ffmpeg.org/download.html
    echo 2. Extraia e adicione ao PATH do sistema
    echo 3. Ou use: winget install ffmpeg
    echo.
    pause
    exit /b 1
)

echo FFmpeg encontrado!
echo.
echo AurantisSync instalado com sucesso!
echo Execute: dist\\AurantisSync.exe
echo.
pause
"""
        with open('install.bat', 'w', encoding='utf-8') as f:
            f.write(script_content)
    
    else:
        # Script shell para Unix-like
        script_content = """#!/bin/bash
echo "Instalando AurantisSync..."
echo
echo "Verificando dependências..."

# Verificar se FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "ERRO: FFmpeg não encontrado!"
    echo
    echo "Para instalar FFmpeg:"
    echo "  macOS: brew install ffmpeg"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  CentOS/RHEL: sudo yum install ffmpeg"
    echo
    exit 1
fi

echo "FFmpeg encontrado!"
echo
echo "AurantisSync instalado com sucesso!"
echo "Execute: ./dist/AurantisSync"
echo
"""
        with open('install.sh', 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Tornar executável
        os.chmod('install.sh', 0o755)


def main():
    """Função principal do build."""
    print("=== Build do AurantisSync ===")
    print()
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"PyInstaller encontrado: {PyInstaller.__version__}")
    except ImportError:
        print("ERRO: PyInstaller não encontrado!")
        print("Instale com: pip install pyinstaller")
        return False
    
    # Limpar builds anteriores
    clean_build()
    
    # Criar executável
    if not build_executable():
        return False
    
    # Criar script de instalação
    create_installer_script()
    
    print()
    print("=== Build Concluído ===")
    print("Executável criado em: dist/")
    print("Script de instalação criado: install.bat (Windows) ou install.sh (Unix)")
    print()
    print("Para distribuir:")
    print("1. Copie a pasta 'dist' completa")
    print("2. Inclua o script de instalação")
    print("3. Instrua o usuário a instalar FFmpeg primeiro")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

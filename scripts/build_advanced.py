"""
Script avançado para build do AurantisSync com PyInstaller
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas."""
    print("Verificando dependências...")
    
    required_packages = [
        "PySide6", "faster-whisper", "librosa", 
        "matplotlib", "numpy", "soundfile"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"✗ {package}")
    
    if missing:
        print(f"\nInstalando dependências faltando: {', '.join(missing)}")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing)
    
    return len(missing) == 0

def clean_build():
    """Limpa arquivos de build anteriores."""
    print("Limpando builds anteriores...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removido: {dir_name}")
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            file.unlink()
            print(f"Removido: {file}")

def build_executable():
    """Constrói o executável."""
    print("Construindo executável...")
    
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--name", "AurantisSync",
        "--icon", "icon.ico" if os.path.exists("icon.ico") else None,
        "--add-data", "example_lines.json;." if os.path.exists("example_lines.json") else None,
        "aurantis_sync_mvp.py"
    ]
    
    # Remove argumentos None
    cmd = [arg for arg in cmd if arg is not None]
    
    print(f"Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Build concluído com sucesso!")
        print("Executável criado em: dist/AurantisSync.exe")
        return True
    else:
        print("✗ Erro no build:")
        print(result.stderr)
        return False

def create_portable_package():
    """Cria um pacote portável."""
    print("Criando pacote portável...")
    
    if not os.path.exists("dist/AurantisSync.exe"):
        print("✗ Executável não encontrado. Execute o build primeiro.")
        return False
    
    # Criar pasta do pacote
    package_dir = Path("AurantisSync_Portable")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Copiar executável
    shutil.copy("dist/AurantisSync.exe", package_dir)
    
    # Copiar arquivos de exemplo
    if os.path.exists("example_lines.json"):
        shutil.copy("example_lines.json", package_dir)
    
    # Criar README para o pacote
    readme_content = """# AurantisSync - Pacote Portável

## Como usar:
1. Execute AurantisSync.exe
2. Clique em "Abrir Áudio" para carregar um arquivo de música
3. Clique em "Transcrever" para gerar a letra
4. Edite os timestamps e texto na tabela
5. Clique em "Exportar Tudo" para salvar em múltiplos formatos

## Formatos suportados:
- TXT: Letra simples
- SRT: Legendas
- LRC: Letras sincronizadas
- VTT: WebVTT
- JSON: Dados estruturados

## Requisitos:
- FFmpeg deve estar instalado no sistema
- Windows 10/11 (64-bit)

## Suporte:
Para problemas, verifique se o FFmpeg está instalado e no PATH.
"""
    
    with open(package_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✓ Pacote portável criado em: {package_dir}")
    return True

def main():
    """Função principal."""
    print("=== Build Avançado do AurantisSync ===\n")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("✗ Arquivo aurantis_sync_mvp.py não encontrado!")
        print("Execute este script no diretório do projeto.")
        return 1
    
    # Verificar dependências
    if not check_dependencies():
        print("✗ Falha ao instalar dependências")
        return 1
    
    # Limpar builds anteriores
    clean_build()
    
    # Construir executável
    if not build_executable():
        print("✗ Falha no build")
        return 1
    
    # Criar pacote portável
    if not create_portable_package():
        print("✗ Falha ao criar pacote portável")
        return 1
    
    print("\n🎉 Build concluído com sucesso!")
    print("Arquivos criados:")
    print("- dist/AurantisSync.exe (executável)")
    print("- AurantisSync_Portable/ (pacote portável)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Script para criar executável do AurantisSync
Usa PyInstaller para gerar um .exe standalone
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("🔨 Criando executável do AurantisSync...")
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado")
    
    # Arquivo principal
    main_file = "aurantis_sync_mvp.py"
    if not os.path.exists(main_file):
        print(f"❌ Arquivo {main_file} não encontrado!")
        return False
    
    # Limpar builds anteriores
    if os.path.exists("build"):
        print("🧹 Limpando build anterior...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("🧹 Limpando dist anterior...")
        shutil.rmtree("dist")
    
    # Comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",           # Sem janela de console
        "--onefile",             # Arquivo único
        "--name", "AurantisSync", # Nome do executável
        "--clean",               # Limpar cache
        main_file
    ]
    
    print("🚀 Executando PyInstaller...")
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build concluído com sucesso!")
        
        # Verificar se o executável foi criado
        exe_path = Path("dist") / "AurantisSync.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executável criado: {exe_path}")
            print(f"📏 Tamanho: {size_mb:.1f} MB")
            print(f"📍 Localização: {exe_path.absolute()}")
            
            # Criar pasta de distribuição
            dist_folder = Path("AurantisSync_Portable")
            if dist_folder.exists():
                shutil.rmtree(dist_folder)
            
            dist_folder.mkdir()
            shutil.copy2(exe_path, dist_folder / "AurantisSync.exe")
            
            # Copiar arquivos necessários
            if os.path.exists("requirements.txt"):
                shutil.copy2("requirements.txt", dist_folder / "requirements.txt")
            
            if os.path.exists("README.md"):
                shutil.copy2("README.md", dist_folder / "README.md")
            
            print(f"📁 Pasta portável criada: {dist_folder.absolute()}")
            print("\n🎉 Executável pronto para distribuição!")
            print(f"Execute: {dist_folder / 'AurantisSync.exe'}")
            
        else:
            print("❌ Executável não foi criado!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Build concluído com sucesso!")
    else:
        print("\n❌ Build falhou!")
        sys.exit(1)

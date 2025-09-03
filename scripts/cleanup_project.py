#!/usr/bin/env python3
"""
Script para limpar arquivos desnecessários do projeto
"""

import os
import shutil
from pathlib import Path

def cleanup_pycache():
    """Remove arquivos __pycache__"""
    print("🧹 Removendo arquivos __pycache__...")
    
    for root, dirs, files in os.walk("."):
        for dir_name in dirs[:]:  # Use slice to avoid modifying list while iterating
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                print(f"  Removendo: {pycache_path}")
                shutil.rmtree(pycache_path)
                dirs.remove(dir_name)  # Remove from dirs to avoid further processing

def cleanup_build_files():
    """Remove arquivos de build"""
    print("🧹 Removendo arquivos de build...")
    
    build_dirs = ["build", "dist", "__pycache__"]
    
    for build_dir in build_dirs:
        if os.path.exists(build_dir):
            print(f"  Removendo: {build_dir}")
            shutil.rmtree(build_dir)

def cleanup_temp_files():
    """Remove arquivos temporários"""
    print("🧹 Removendo arquivos temporários...")
    
    temp_files = [
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.egg-info",
        ".coverage",
        ".pytest_cache",
        "*.log"
    ]
    
    for pattern in temp_files:
        for file_path in Path(".").rglob(pattern):
            if file_path.is_file():
                print(f"  Removendo: {file_path}")
                file_path.unlink()

def cleanup_duplicate_docs():
    """Remove documentação duplicada"""
    print("🧹 Verificando documentação duplicada...")
    
    # Arquivos que podem estar duplicados
    duplicate_candidates = [
        "EXECUTAVEL_GUIA.md",
        "GIT_PROBLEMA_SOLUCAO.md",
        "INSTRUCOES_FINAIS.md",
        "ATUALIZACOES_GITHUB.md"
    ]
    
    for file_name in duplicate_candidates:
        if os.path.exists(file_name):
            print(f"  Arquivo na raiz: {file_name}")
            print(f"  Verifique se há duplicata em docs/")

def show_project_structure():
    """Mostra a estrutura final do projeto"""
    print("\n📁 Estrutura final do projeto:")
    print("=" * 50)
    
    def print_tree(directory, prefix="", max_depth=3, current_depth=0):
        if current_depth >= max_depth:
            return
            
        try:
            items = sorted(Path(directory).iterdir())
            dirs = [item for item in items if item.is_dir() and not item.name.startswith('.')]
            files = [item for item in items if item.is_file() and not item.name.startswith('.')]
            
            # Print directories
            for i, item in enumerate(dirs):
                is_last_dir = i == len(dirs) - 1 and len(files) == 0
                current_prefix = "└── " if is_last_dir else "├── "
                print(f"{prefix}{current_prefix}{item.name}/")
                
                next_prefix = prefix + ("    " if is_last_dir else "│   ")
                print_tree(item, next_prefix, max_depth, current_depth + 1)
            
            # Print files
            for i, item in enumerate(files):
                is_last = i == len(files) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")
                
        except PermissionError:
            pass
    
    print_tree(".")

def main():
    """Função principal"""
    print("🧹 Limpeza do Projeto AurantisSync")
    print("=" * 50)
    
    # Verificar se estamos na pasta correta
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("❌ Execute este script na pasta raiz do projeto!")
        return False
    
    # Executar limpeza
    cleanup_pycache()
    cleanup_build_files()
    cleanup_temp_files()
    cleanup_duplicate_docs()
    
    print("\n✅ Limpeza concluída!")
    
    # Mostrar estrutura final
    show_project_structure()
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Projeto limpo e organizado!")
    else:
        print("\n❌ Erro na limpeza do projeto")

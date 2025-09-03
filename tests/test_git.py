#!/usr/bin/env python3
"""
Script para testar e diagnosticar problemas com Git
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    print(f"   Comando: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"   Return code: {result.returncode}")
        if result.stdout.strip():
            print(f"   STDOUT: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"   STDERR: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   EXCEPTION: {e}")
        return False

def main():
    print("🔍 Diagnosticando problemas com Git...")
    
    # Verificar se estamos na pasta correta
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("❌ Execute este script na pasta raiz do projeto!")
        return False
    
    # Testar comandos Git básicos
    commands = [
        ("git --version", "Verificar versão do Git"),
        ("git status", "Status do repositório"),
        ("git config --global user.name", "Nome do usuário"),
        ("git config --global user.email", "Email do usuário"),
        ("git remote -v", "Remotes configurados"),
        ("git branch -a", "Branches disponíveis"),
        ("git log --oneline -3", "Últimos commits"),
    ]
    
    for cmd, desc in commands:
        success = run_command(cmd, desc)
        print(f"   Resultado: {'✅' if success else '❌'}")
        print()
    
    return True

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para fazer upload do projeto AurantisSync para o GitHub
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso!")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
        else:
            print(f"❌ {description} - Erro!")
            if result.stderr.strip():
                print(f"   {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False
    return True

def main():
    print("🚀 Fazendo upload do AurantisSync para o GitHub...")
    
    # Verificar se estamos na pasta correta
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("❌ Execute este script na pasta raiz do projeto!")
        return False
    
    # Configurar Git se necessário
    commands = [
        ("git config --global user.name 'JoaoSantosCodes'", "Configurando nome do usuário"),
        ("git config --global user.email 'joao@example.com'", "Configurando email do usuário"),
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)
    
    # Inicializar repositório se necessário
    if not os.path.exists(".git"):
        commands = [
            ("git init", "Inicializando repositório Git"),
            ("git add .", "Adicionando arquivos"),
            ("git commit -m 'feat: Projeto AurantisSync completo e organizado'", "Fazendo commit inicial"),
            ("git remote add origin https://github.com/JoaoSantosCodes/AurantisSync.git", "Adicionando remote"),
            ("git branch -M main", "Renomeando branch para main"),
            ("git push -u origin main", "Fazendo push para GitHub"),
        ]
    else:
        commands = [
            ("git add .", "Adicionando arquivos"),
            ("git commit -m 'feat: Atualização do projeto AurantisSync com organização completa'", "Fazendo commit"),
            ("git push origin main", "Fazendo push para GitHub"),
        ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"❌ Falha em: {desc}")
            return False
    
    print("\n🎉 Upload concluído com sucesso!")
    print("📁 Repositório: https://github.com/JoaoSantosCodes/AurantisSync")
    print("🔗 Clone: git clone https://github.com/JoaoSantosCodes/AurantisSync.git")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Upload falhou!")
        sys.exit(1)
    else:
        print("\n✅ Projeto enviado para o GitHub com sucesso!")

"""
Script para fazer upload do projeto AurantisSync para o GitHub
"""
import os
import subprocess
import sys
from pathlib import Path

def check_git():
    """Verifica se o Git está instalado."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def init_git_repo():
    """Inicializa o repositório Git."""
    print("Inicializando repositório Git...")
    
    # Verificar se já é um repositório Git
    if os.path.exists(".git"):
        print("✓ Repositório Git já existe")
        return True
    
    try:
        subprocess.run(["git", "init"], check=True)
        print("✓ Repositório Git inicializado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao inicializar Git: {e}")
        return False

def add_remote():
    """Adiciona o remote do GitHub."""
    print("Configurando remote do GitHub...")
    
    try:
        # Verificar se o remote já existe
        result = subprocess.run(["git", "remote", "get-url", "origin"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Remote 'origin' já configurado")
            return True
        
        # Adicionar remote
        subprocess.run(["git", "remote", "add", "origin", 
                       "https://github.com/JoaoSantosCodes/AurantisSync.git"], 
                      check=True)
        print("✓ Remote 'origin' adicionado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao configurar remote: {e}")
        return False

def add_files():
    """Adiciona todos os arquivos ao Git."""
    print("Adicionando arquivos ao Git...")
    
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("✓ Arquivos adicionados")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao adicionar arquivos: {e}")
        return False

def commit_files():
    """Faz commit dos arquivos."""
    print("Fazendo commit dos arquivos...")
    
    try:
        subprocess.run(["git", "commit", "-m", 
                       "Initial commit: AurantisSync - Transcrição e Sincronização de Letras"], 
                      check=True)
        print("✓ Commit realizado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao fazer commit: {e}")
        return False

def push_to_github():
    """Faz push para o GitHub."""
    print("Fazendo push para o GitHub...")
    
    try:
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✓ Push realizado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao fazer push: {e}")
        return False

def create_readme():
    """Cria um README.md específico para o GitHub."""
    readme_content = """# 🎶 AurantisSync

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![PySide6](https://img.shields.io/badge/PySide6-6.5+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AurantisSync** é um aplicativo desktop em Python para **transcrever e sincronizar letras de músicas** automaticamente. Utiliza o modelo **faster-whisper** para transcrição e permite edição manual de timestamps com exportação para múltiplos formatos.

## ✨ Funcionalidades

- 🎵 **Carregamento de áudio** (.wav, .mp3, .m4a, .flac, .ogg, .aac)
- 📊 **Visualização de waveform** com matplotlib
- 🎤 **Transcrição automática** com faster-whisper
- 🌍 **Múltiplos idiomas** (pt, en, es, fr, de, it, ja, ko, zh)
- ⚡ **Múltiplos modelos** (tiny, base, small, medium, large-v3)
- ✏️ **Edição interativa** de timestamps e texto
- 📤 **Exportação múltipla** (TXT, SRT, LRC, VTT, JSON)
- 🖥️ **Interface moderna** com PySide6

## 🚀 Instalação

### Pré-requisitos
- Python 3.10+
- FFmpeg instalado e no PATH

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Verificar FFmpeg
```bash
ffmpeg -version
```

## ▶️ Como usar

### Opção 1: MVP Standalone (Recomendado)
```bash
python aurantis_sync_mvp.py
```

### Opção 2: Duplo clique (Windows)
- Clique duas vezes em `start_app.bat`

### Opção 3: Projeto estruturado
```bash
python run_structured_app.bat
```

## 🎯 Uso básico

1. **Abrir áudio**: Clique em "Abrir Áudio" e selecione um arquivo
2. **Transcrever**: Clique em "Transcrever" (escolha idioma e modelo)
3. **Editar**: Modifique os timestamps e texto na tabela
4. **Exportar**: Clique em "Exportar Tudo" para gerar todos os formatos

## 📋 Formatos de exportação

- **TXT**: Letra simples
- **SRT**: Legendas com formato hh:mm:ss,ms
- **LRC**: Letras sincronizadas com [mm:ss.cc]
- **VTT**: WebVTT para uso web
- **JSON**: Dados estruturados com timestamps

## 🛠️ Build executável

```bash
python build_advanced.py
```

## 🧪 Teste

```bash
python test_mvp.py
```

## 📁 Estrutura do projeto

```
AurantisSync/
├── aurantis_sync_mvp.py      # MVP standalone
├── app/                      # Projeto estruturado
│   ├── main.py
│   ├── core/                 # Lógica de negócio
│   ├── ui/                   # Interface
│   └── widgets/              # Componentes
├── requirements.txt
├── README.md
├── start_app.bat
├── build_exe.bat
└── example_lines.json
```

## 🔧 Tecnologias

- **Python 3.10+**
- **PySide6** - Interface gráfica
- **faster-whisper** - Transcrição de áudio
- **librosa** - Análise de áudio
- **matplotlib** - Visualização de waveform
- **numpy** - Computação numérica
- **soundfile** - Leitura de arquivos de áudio

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Fazer commit das mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Fazer push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📞 Suporte

Para problemas ou dúvidas:

- Abra uma [issue](https://github.com/JoaoSantosCodes/AurantisSync/issues)
- Verifique se o FFmpeg está instalado e no PATH
- Execute `python test_mvp.py` para diagnosticar problemas

## 🌟 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Modelo de transcrição
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Implementação otimizada
- [PySide6](https://doc.qt.io/qtforpython/) - Framework de interface gráfica

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✓ README.md criado")

def main():
    """Função principal."""
    print("=== Upload do AurantisSync para GitHub ===\n")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("aurantis_sync_mvp.py"):
        print("✗ Arquivo aurantis_sync_mvp.py não encontrado!")
        print("Execute este script no diretório do projeto.")
        return 1
    
    # Verificar Git
    if not check_git():
        print("✗ Git não encontrado!")
        print("Instale o Git: https://git-scm.com/downloads")
        return 1
    
    # Criar README específico para GitHub
    create_readme()
    
    # Inicializar repositório
    if not init_git_repo():
        return 1
    
    # Configurar remote
    if not add_remote():
        return 1
    
    # Adicionar arquivos
    if not add_files():
        return 1
    
    # Fazer commit
    if not commit_files():
        return 1
    
    # Fazer push
    if not push_to_github():
        return 1
    
    print("\n🎉 Upload concluído com sucesso!")
    print("Seu projeto está disponível em:")
    print("https://github.com/JoaoSantosCodes/AurantisSync")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

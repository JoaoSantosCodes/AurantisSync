# 🎶 AurantisSync

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

## 🚀 Instalação Rápida

### Windows (PowerShell)
```powershell
# Clone o repositório
git clone https://github.com/JoaoSantosCodes/AurantisSync.git
cd AurantisSync

# Execute o script de setup automático
.\scripts\Setup-And-Run-AurantisSync.ps1
```

### Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python aurantis_sync_mvp.py
```

## 📁 Estrutura do Projeto

```
AurantisSync/
├── README.md                    # 🎯 Visão geral
├── PROJECT_CONFIG.md            # ⚙️ Configuração
├── PROJECT_SUMMARY.md           # 📋 Resumo
├── aurantis_sync_mvp.py         # 🎮 App principal (MVP)
├── app/                         # 📦 Projeto estruturado
│   ├── main.py                 # Ponto de entrada
│   ├── config.py               # Configurações
│   ├── core/                   # Lógica de negócio
│   │   ├── sync_model.py       # Modelos de dados
│   │   ├── transcriber.py      # Transcrição
│   │   ├── exporters.py        # Exportação
│   │   ├── audio_player.py     # Player de áudio
│   │   ├── waveform.py         # Waveform
│   │   └── project_io.py       # I/O de projetos
│   ├── ui/                     # Interface gráfica
│   │   ├── main_window.py      # Janela principal
│   │   └── main_window_improved.py  # Janela melhorada
│   └── widgets/                # Componentes
│       ├── waveform_widget.py  # Widget de waveform
│       └── lines_table.py      # Tabela de linhas
├── scripts/                     # 🔧 Scripts de automação
│   ├── Setup-And-Run-AurantisSync.ps1  # Setup automático
│   ├── Create-Executable.ps1    # Criar executável
│   ├── Upload-To-GitHub.ps1     # Upload para GitHub
│   ├── upload_final.cmd         # Upload final
│   ├── fix_git_upload.bat       # Correção Git
│   ├── build_exe.py             # Build Python
│   ├── create_exe.bat           # Build Batch
│   ├── upload_github.py         # Upload Python
│   └── test_structured_app.py   # Teste estruturado
├── docs/                        # 📚 Documentação
│   ├── INDEX.md                # Índice da documentação
│   ├── README.md               # Documentação completa
│   ├── QUICKSTART.md           # Guia rápido
│   ├── POWERSHELL_SETUP.md     # Setup PowerShell
│   ├── CRIAR_EXECUTAVEL.md     # Guia executável
│   ├── SOLUCAO_PROBLEMAS_GIT.md # Solução Git
│   ├── GIT_PROBLEMA_SOLUCAO.md  # Problemas Git
│   ├── INSTRUCOES_FINAIS.md     # Instruções finais
│   ├── ATUALIZACOES_GITHUB.md   # Atualizações GitHub
│   ├── EXECUTAVEL_GUIA.md       # Guia executável
│   ├── ARCHITECTURE.md          # Arquitetura
│   └── CONTRIBUTING.md         # Como contribuir
├── examples/                    # 📝 Exemplos
│   ├── example_lines.json      # Arquivo de exemplo
│   └── sample_lines.json       # Linhas de exemplo
├── tests/                       # 🧪 Testes
│   ├── test_mvp.py             # Teste MVP
│   ├── test_app.py             # Teste app
│   └── test_git.py             # Teste Git
├── requirements.txt             # 📋 Dependências
├── pyproject.toml              # Configuração Python
├── LICENSE                      # 📄 Licença MIT
└── .gitignore                   # Arquivos ignorados
```

## 🎯 Como usar

### 1. **Abrir áudio**
Clique em "Abrir Áudio" e selecione um arquivo de música

### 2. **Transcrever**
Clique em "Transcrever" (escolha idioma e modelo)

### 3. **Editar**
Modifique os timestamps e texto na tabela

### 4. **Exportar**
Clique em "Exportar Tudo" para gerar todos os formatos

## 📋 Formatos de exportação

- **TXT**: Letra simples
- **SRT**: Legendas com formato hh:mm:ss,ms
- **LRC**: Letras sincronizadas com [mm:ss.cc]
- **VTT**: WebVTT para uso web
- **JSON**: Dados estruturados com timestamps

## 🛠️ Build executável

### 🎯 **Criar .exe (3 opções)**

#### **1. PowerShell (Mais Fácil)**
```powershell
.\scripts\Create-Executable.ps1
```

#### **2. Setup Automático**
```powershell
.\scripts\Setup-And-Run-AurantisSync.ps1 -BuildExe
```

#### **3. Manual**
```bash
# Python
python build_exe.py

# Batch
create_exe.bat

# PyInstaller direto
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py
```

### 📦 **Resultado**
- **`dist/AurantisSync.exe`** - Executável principal
- **`AurantisSync_Portable/`** - Pasta portável completa
- **Tamanho**: ~200-500 MB (com faster-whisper)

## 🔧 Tecnologias

- **Python 3.10+**
- **PySide6** - Interface gráfica
- **faster-whisper** - Transcrição de áudio
- **librosa** - Análise de áudio
- **matplotlib** - Visualização de waveform
- **numpy** - Computação numérica
- **soundfile** - Leitura de arquivos de áudio

## 📚 Documentação

- **[Guia Completo](docs/README.md)** - Documentação detalhada
- **[Quick Start](docs/QUICKSTART.md)** - Guia rápido
- **[Setup PowerShell](docs/POWERSHELL_SETUP.md)** - Setup automático
- **[Criar Executável](docs/CRIAR_EXECUTAVEL.md)** - Guia para gerar .exe
- **[Contribuindo](docs/CONTRIBUTING.md)** - Como contribuir

## 🧪 Testes

```bash
# Testar MVP
python tests/test_mvp.py

# Testar aplicação estruturada
python scripts/test_structured_app.py

# Testar estrutura do projeto
.\scripts\test_structure.ps1

# Testar configuração PowerShell
.\scripts\test_basic.ps1

# Testar Git
python tests/test_git.py
```

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🤝 Contribuição

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](docs/CONTRIBUTING.md) para detalhes.

## 📞 Suporte

- **GitHub Issues**: [Reportar problemas](https://github.com/JoaoSantosCodes/AurantisSync/issues)
- **GitHub Discussions**: [Perguntas e ideias](https://github.com/JoaoSantosCodes/AurantisSync/discussions)

## 🌟 Agradecimentos

- [OpenAI Whisper](https://github.com/openai/whisper) - Modelo de transcrição
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Implementação otimizada
- [PySide6](https://doc.qt.io/qtforpython/) - Framework de interface gráfica

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**

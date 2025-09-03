# ⚙️ Configuração do Projeto

## 📋 Informações do Projeto

- **Nome**: AurantisSync
- **Versão**: 1.0.0
- **Descrição**: Aplicativo desktop para transcrição e sincronização de letras de músicas
- **Linguagem**: Python 3.10+
- **Framework GUI**: PySide6
- **Licença**: MIT

## 🎯 Objetivos

- ✅ Transcrição automática de áudio com faster-whisper
- ✅ Edição manual de timestamps e texto
- ✅ Exportação para múltiplos formatos
- ✅ Interface gráfica moderna e intuitiva
- ✅ Cross-platform (Windows/macOS/Linux)
- ✅ Setup automático com scripts

## 📁 Estrutura Organizada

```
AurantisSync/
├── README.md                    # 🎯 Visão geral do projeto
├── PROJECT_CONFIG.md            # ⚙️ Este arquivo
├── aurantis_sync_mvp.py         # 🎮 App principal (MVP)
├── app/                         # 📦 Projeto estruturado
│   ├── main.py                 # Ponto de entrada
│   ├── core/                   # Lógica de negócio
│   │   ├── sync_model.py       # Modelos de dados
│   │   ├── transcriber.py      # Transcrição
│   │   ├── exporters.py        # Exportação
│   │   └── audio_player.py     # Player de áudio
│   ├── ui/                     # Interface gráfica
│   │   ├── main_window.py      # Janela principal
│   │   └── main_window_improved.py
│   └── widgets/                # Componentes
│       ├── waveform_widget.py  # Widget de waveform
│       └── lines_table.py      # Tabela de linhas
├── scripts/                    # 🔧 Scripts de automação
│   ├── Setup-And-Run-AurantisSync.ps1  # Setup automático
│   ├── build_advanced.py       # Build avançado
│   ├── upload_to_github.py     # Upload para GitHub
│   ├── test_*.ps1             # Testes PowerShell
│   └── *.bat                  # Scripts Windows
├── docs/                       # 📚 Documentação
│   ├── INDEX.md               # Índice da documentação
│   ├── README.md              # Documentação completa
│   ├── QUICKSTART.md          # Guia rápido
│   ├── POWERSHELL_SETUP.md    # Setup PowerShell
│   ├── CONTRIBUTING.md        # Como contribuir
│   └── CHANGELOG.md           # Histórico de versões
├── examples/                   # 📝 Exemplos
│   └── example_lines.json     # Arquivo de exemplo
├── tests/                      # 🧪 Testes
│   ├── test_mvp.py            # Teste do MVP
│   └── test_app.py            # Teste da app estruturada
├── .github/                    # 🔧 Configurações GitHub
│   ├── workflows/             # GitHub Actions
│   ├── ISSUE_TEMPLATE/        # Templates de issues
│   └── *.md                   # Configurações
├── .vscode/                    # 🔧 Configurações VS Code
│   ├── settings.json          # Configurações
│   ├── tasks.json             # Tarefas
│   ├── launch.json            # Debug
│   └── extensions.json        # Extensões recomendadas
├── requirements.txt            # 📋 Dependências Python
├── pyproject.toml             # 📦 Configuração do projeto
├── LICENSE                     # 📄 Licença MIT
└── .gitignore                 # 🚫 Arquivos ignorados pelo Git
```

## 🎮 Aplicações

### 1. MVP Standalone (`aurantis_sync_mvp.py`)
- **Propósito**: Versão simplificada e autocontida
- **Uso**: Para usuários finais e testes rápidos
- **Características**: Tudo em um arquivo, fácil de executar

### 2. Projeto Estruturado (`app/`)
- **Propósito**: Versão modular e extensível
- **Uso**: Para desenvolvedores e contribuições
- **Características**: Código organizado, fácil manutenção

## 🔧 Scripts de Automação

### PowerShell
- **`Setup-And-Run-AurantisSync.ps1`**: Setup automático completo
- **`test_*.ps1`**: Scripts de teste e verificação

### Python
- **`build_advanced.py`**: Build avançado com PyInstaller
- **`upload_to_github.py`**: Upload automático para GitHub

### Batch
- **`*.bat`**: Scripts Windows para execução e build

## 📚 Documentação

### Principal
- **`README.md`**: Visão geral e início rápido
- **`docs/README.md`**: Documentação completa
- **`docs/INDEX.md`**: Índice da documentação

### Guias
- **`docs/QUICKSTART.md`**: Guia de início rápido
- **`docs/POWERSHELL_SETUP.md`**: Setup automático
- **`docs/CONTRIBUTING.md`**: Como contribuir

## 🧪 Testes

- **`tests/test_mvp.py`**: Teste do MVP
- **`tests/test_app.py`**: Teste da app estruturada
- **`scripts/test_*.ps1`**: Testes PowerShell

## 🎯 Fluxo de Desenvolvimento

1. **Desenvolvimento**: Use `app/` para desenvolvimento
2. **Teste**: Execute `tests/test_*.py`
3. **Build**: Use `scripts/build_advanced.py`
4. **Distribuição**: Use `scripts/Setup-And-Run-AurantisSync.ps1`

## 🔄 Atualizações

- **Versão**: Atualize em `pyproject.toml`
- **Changelog**: Atualize `docs/CHANGELOG.md`
- **Documentação**: Mantenha `docs/` atualizado

## 📞 Suporte

- **GitHub Issues**: Para bugs e feature requests
- **GitHub Discussions**: Para perguntas e ideias
- **Documentação**: Consulte `docs/` para guias

---

⚙️ **Esta configuração garante que o projeto seja bem organizado e fácil de manter!**

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

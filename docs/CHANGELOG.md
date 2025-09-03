# Changelog - AurantisSync

## [1.0.0] - 2024-01-XX

### Adicionado
- Interface gráfica com PySide6
- Transcrição automática com faster-whisper
- Visualização de waveform com matplotlib
- Edição de linhas com timestamps
- Exportação para múltiplos formatos (TXT, SRT, LRC, VTT, JSON)
- Suporte a múltiplos idiomas
- Seleção de modelos Whisper (tiny, base, small, medium, large-v3)
- Verificação automática de FFmpeg
- Scripts de build com PyInstaller
- Arquivos de exemplo e documentação

### Funcionalidades
- **Carregamento de áudio**: Suporte a .wav, .mp3, .m4a, .flac, .ogg, .aac
- **Transcrição**: Integração com faster-whisper para reconhecimento de fala
- **Edição**: Tabela interativa para editar timestamps e texto
- **Exportação**: Múltiplos formatos de saída
- **Interface**: Design limpo e intuitivo

### Formatos de Exportação
- **TXT**: Letra simples, uma linha por vez
- **SRT**: Legendas com formato hh:mm:ss,ms
- **LRC**: Letras sincronizadas com [mm:ss.cc]
- **VTT**: WebVTT para uso web
- **JSON**: Dados estruturados com timestamps

### Requisitos
- Python 3.10+
- FFmpeg instalado e no PATH
- Dependências: PySide6, faster-whisper, librosa, matplotlib, numpy, soundfile

### Instalação
```bash
pip install -r requirements.txt
```

### Execução
```bash
python aurantis_sync_mvp.py
```

### Build
```bash
pyinstaller --noconsole --onefile --name "AurantisSync" aurantis_sync_mvp.py
```

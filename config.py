"""
Configurações do AurantisSync
"""
import os

# Configurações de transcrição
DEFAULT_LANGUAGE = "pt"
DEFAULT_MODEL = "small"
SUPPORTED_LANGUAGES = ["pt", "en", "es", "fr", "de", "it", "ja", "ko", "zh"]
SUPPORTED_MODELS = ["tiny", "base", "small", "medium", "large-v3"]

# Configurações de interface
WINDOW_TITLE = "AurantisSync – Transcrição & Sincronização"
WINDOW_SIZE = (1100, 700)

# Configurações de áudio
SUPPORTED_AUDIO_FORMATS = ["*.wav", "*.mp3", "*.m4a", "*.flac", "*.ogg", "*.aac"]

# Configurações de exportação
EXPORT_FORMATS = {
    "txt": "Texto Simples",
    "srt": "Legendas SRT", 
    "lrc": "Letras LRC",
    "vtt": "WebVTT",
    "json": "JSON"
}

# Configurações de FFmpeg
FFMPEG_REQUIRED = True
FFMPEG_INSTRUCTIONS = """
FFmpeg não encontrado! Para instalar:

Windows:
1. Baixe de https://ffmpeg.org/download.html
2. Extraia e adicione ao PATH do sistema
3. Ou use: winget install ffmpeg

macOS:
brew install ffmpeg

Linux:
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
"""

# Configurações de GPU
AUTO_DETECT_GPU = True
DEFAULT_DEVICE = "cpu"  # ou "cuda" se tiver GPU

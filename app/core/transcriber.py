"""
Módulo de transcrição usando faster-whisper.
"""
import os
import subprocess
import tempfile
from typing import List, Optional, Tuple
from pathlib import Path

from faster_whisper import WhisperModel
from pydub import AudioSegment

from app.core.sync_model import LyricLine


class Transcriber:
    """Classe para transcrição de áudio usando faster-whisper."""
    
    # Modelos disponíveis com informações de performance
    MODELS = {
        "tiny": {"size": "39 MB", "speed": "~32x", "quality": "Baixa"},
        "base": {"size": "74 MB", "speed": "~16x", "quality": "Média"},
        "small": {"size": "244 MB", "speed": "~6x", "quality": "Boa"},
        "medium": {"size": "769 MB", "speed": "~2x", "quality": "Muito Boa"},
        "large-v3": {"size": "1550 MB", "speed": "~1x", "quality": "Excelente"}
    }
    
    def __init__(self):
        self.model = None
        self.current_model_size = None
        self.device = "cuda" if self._check_cuda() else "cpu"
    
    def _check_cuda(self) -> bool:
        """Verifica se CUDA está disponível."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def _check_ffmpeg(self) -> bool:
        """Verifica se FFmpeg está instalado."""
        try:
            subprocess.run(["ffmpeg", "-version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_ffmpeg_instructions(self) -> str:
        """Retorna instruções para instalar FFmpeg."""
        return """
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
        """.strip()
    
    def load_model(self, model_size: str = "base") -> bool:
        """Carrega o modelo do Whisper."""
        try:
            if self.current_model_size != model_size:
                self.model = WhisperModel(
                    model_size, 
                    device=self.device,
                    compute_type="float16" if self.device == "cuda" else "int8"
                )
                self.current_model_size = model_size
            return True
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            return False
    
    def convert_to_wav(self, audio_path: str) -> str:
        """Converte áudio para WAV se necessário."""
        audio_path = Path(audio_path)
        
        # Se já é WAV, retorna o caminho original
        if audio_path.suffix.lower() == '.wav':
            return str(audio_path)
        
        # Verificar se FFmpeg está disponível
        if not self._check_ffmpeg():
            raise RuntimeError("FFmpeg não encontrado. " + self.get_ffmpeg_instructions())
        
        # Criar arquivo temporário WAV
        temp_dir = tempfile.gettempdir()
        wav_path = Path(temp_dir) / f"temp_audio_{os.getpid()}.wav"
        
        try:
            # Carregar com pydub e converter
            audio = AudioSegment.from_file(str(audio_path))
            audio.export(str(wav_path), format="wav")
            return str(wav_path)
        except Exception as e:
            raise RuntimeError(f"Erro ao converter áudio: {e}")
    
    def transcribe(self, audio_path: str, language: str = "pt", 
                   model_size: str = "base") -> List[LyricLine]:
        """
        Transcreve o áudio e retorna lista de linhas com timestamps.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            language: Código do idioma (ex: "pt", "en", "es")
            model_size: Tamanho do modelo ("tiny", "base", "small", "medium", "large-v3")
        
        Returns:
            Lista de LyricLine com timestamps e texto transcrito
        """
        # Verificar se FFmpeg está disponível
        if not self._check_ffmpeg():
            raise RuntimeError("FFmpeg não encontrado. " + self.get_ffmpeg_instructions())
        
        # Converter para WAV se necessário
        wav_path = self.convert_to_wav(audio_path)
        
        try:
            # Carregar modelo se necessário
            if not self.load_model(model_size):
                raise RuntimeError(f"Falha ao carregar modelo {model_size}")
            
            # Transcrever
            segments, info = self.model.transcribe(
                wav_path,
                language=language,
                beam_size=5,
                word_timestamps=True
            )
            
            # Converter segmentos para LyricLine
            lines = []
            for segment in segments:
                if segment.text.strip():  # Ignorar segmentos vazios
                    # Garantir que os tempos são válidos
                    start_time = float(segment.start) if segment.start is not None else 0.0
                    end_time = float(segment.end) if segment.end is not None else max(start_time + 0.5, start_time)
                    
                    line = LyricLine(
                        start=start_time,
                        end=end_time,
                        text=segment.text.strip()
                    )
                    lines.append(line)
            
            return lines
            
        except Exception as e:
            raise RuntimeError(f"Erro na transcrição: {e}")
        
        finally:
            # Limpar arquivo temporário se foi criado
            if wav_path != audio_path and os.path.exists(wav_path):
                try:
                    os.unlink(wav_path)
                except:
                    pass
    
    def get_model_info(self, model_size: str) -> dict:
        """Retorna informações sobre um modelo."""
        return self.MODELS.get(model_size, {})
    
    def get_available_models(self) -> List[str]:
        """Retorna lista de modelos disponíveis."""
        return list(self.MODELS.keys())
    
    def get_device_info(self) -> str:
        """Retorna informações sobre o dispositivo de processamento."""
        if self.device == "cuda":
            try:
                import torch
                gpu_name = torch.cuda.get_device_name(0)
                return f"GPU: {gpu_name}"
            except:
                return "GPU: CUDA disponível"
        else:
            return "CPU: Processamento em CPU (mais lento)"

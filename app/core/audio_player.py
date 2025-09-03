"""
Módulo de reprodução de áudio com controles avançados.
"""
import sounddevice as sd
import numpy as np
from typing import Optional, Callable
import threading
import time
from pathlib import Path

from pydub import AudioSegment


class AudioPlayer:
    """Player de áudio com controles de velocidade, volume e posicionamento."""
    
    def __init__(self):
        self.audio_data: Optional[np.ndarray] = None
        self.sample_rate: int = 44100
        self.current_position: float = 0.0
        self.duration: float = 0.0
        self.volume: float = 1.0
        self.speed: float = 1.0
        self.is_playing: bool = False
        self.is_paused: bool = False
        
        # Callbacks
        self.on_position_changed: Optional[Callable[[float], None]] = None
        self.on_playback_finished: Optional[Callable[[], None]] = None
        
        # Threading
        self._playback_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Configurar sounddevice
        sd.default.samplerate = self.sample_rate
        sd.default.channels = 2  # Estéreo
    
    def load_audio(self, audio_path: str) -> bool:
        """
        Carrega arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            True se carregado com sucesso, False caso contrário
        """
        try:
            # Parar reprodução atual
            self.stop()
            
            # Carregar com pydub
            audio = AudioSegment.from_file(audio_path)
            
            # Converter para numpy array
            self.audio_data = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                self.audio_data = self.audio_data.reshape((-1, 2))
            else:
                self.audio_data = self.audio_data.reshape((-1, 1))
                # Duplicar para estéreo
                self.audio_data = np.repeat(self.audio_data, 2, axis=1)
            
            self.sample_rate = audio.frame_rate
            self.duration = len(audio) / 1000.0  # Converter para segundos
            self.current_position = 0.0
            
            # Atualizar configuração do sounddevice
            sd.default.samplerate = self.sample_rate
            
            return True
            
        except Exception as e:
            print(f"Erro ao carregar áudio: {e}")
            return False
    
    def play(self) -> None:
        """Inicia ou retoma a reprodução."""
        if self.audio_data is None:
            return
        
        if self.is_paused:
            self.is_paused = False
            self._stop_event.clear()
        else:
            self.is_playing = True
            self._stop_event.clear()
            self._playback_thread = threading.Thread(target=self._playback_loop)
            self._playback_thread.daemon = True
            self._playback_thread.start()
    
    def pause(self) -> None:
        """Pausa a reprodução."""
        if self.is_playing:
            self.is_paused = True
            self._stop_event.set()
    
    def stop(self) -> None:
        """Para a reprodução e volta ao início."""
        self.is_playing = False
        self.is_paused = False
        self._stop_event.set()
        self.current_position = 0.0
        
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)
    
    def seek(self, position: float) -> None:
        """
        Vai para uma posição específica no áudio.
        
        Args:
            position: Posição em segundos
        """
        if self.audio_data is None:
            return
        
        # Limitar posição
        position = max(0.0, min(position, self.duration))
        self.current_position = position
        
        # Se estiver tocando, reiniciar reprodução da nova posição
        if self.is_playing and not self.is_paused:
            self._stop_event.set()
            if self._playback_thread and self._playback_thread.is_alive():
                self._playback_thread.join(timeout=1.0)
            
            self._playback_thread = threading.Thread(target=self._playback_loop)
            self._playback_thread.daemon = True
            self._playback_thread.start()
    
    def set_volume(self, volume: float) -> None:
        """
        Define o volume (0.0 a 1.0).
        
        Args:
            volume: Volume entre 0.0 e 1.0
        """
        self.volume = max(0.0, min(1.0, volume))
    
    def set_speed(self, speed: float) -> None:
        """
        Define a velocidade de reprodução.
        
        Args:
            speed: Velocidade (0.5 = metade, 1.0 = normal, 2.0 = dobro)
        """
        self.speed = max(0.25, min(4.0, speed))
    
    def get_position(self) -> float:
        """Retorna a posição atual em segundos."""
        return self.current_position
    
    def get_duration(self) -> float:
        """Retorna a duração total em segundos."""
        return self.duration
    
    def is_audio_loaded(self) -> bool:
        """Verifica se há áudio carregado."""
        return self.audio_data is not None
    
    def _playback_loop(self) -> None:
        """Loop principal de reprodução."""
        if self.audio_data is None:
            return
        
        # Calcular posição inicial em samples
        start_sample = int(self.current_position * self.sample_rate)
        total_samples = len(self.audio_data)
        
        # Ajustar velocidade alterando o sample rate efetivo
        effective_sample_rate = int(self.sample_rate * self.speed)
        
        # Buffer de reprodução
        buffer_size = 1024
        
        try:
            while (start_sample < total_samples and 
                   not self._stop_event.is_set() and 
                   self.is_playing):
                
                # Calcular tamanho do próximo chunk
                end_sample = min(start_sample + buffer_size, total_samples)
                chunk = self.audio_data[start_sample:end_sample]
                
                # Aplicar volume
                if self.volume != 1.0:
                    chunk = chunk * self.volume
                
                # Reproduzir chunk
                sd.play(chunk, samplerate=effective_sample_rate)
                sd.wait()
                
                # Atualizar posição
                samples_played = end_sample - start_sample
                time_played = samples_played / self.sample_rate
                self.current_position += time_played
                start_sample = end_sample
                
                # Notificar mudança de posição
                if self.on_position_changed:
                    self.on_position_changed(self.current_position)
                
                # Verificar se chegou ao fim
                if start_sample >= total_samples:
                    self.is_playing = False
                    if self.on_playback_finished:
                        self.on_playback_finished()
                    break
                    
        except Exception as e:
            print(f"Erro na reprodução: {e}")
            self.is_playing = False
    
    def get_audio_info(self) -> dict:
        """Retorna informações sobre o áudio carregado."""
        if not self.is_audio_loaded():
            return {}
        
        return {
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "channels": self.audio_data.shape[1] if len(self.audio_data.shape) > 1 else 1,
            "samples": len(self.audio_data)
        }

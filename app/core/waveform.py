"""
Módulo para geração e manipulação de waveform de áudio.
"""
import numpy as np
import librosa
from typing import Tuple, Optional, List
from pathlib import Path


class WaveformGenerator:
    """Classe para gerar waveform de arquivos de áudio."""
    
    def __init__(self, target_sample_rate: int = 22050):
        self.target_sample_rate = target_sample_rate
        self.waveform_data: Optional[np.ndarray] = None
        self.duration: float = 0.0
        self.sample_rate: int = 0
    
    def load_audio(self, audio_path: str) -> bool:
        """
        Carrega arquivo de áudio e gera waveform.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            True se carregado com sucesso, False caso contrário
        """
        try:
            # Carregar áudio com librosa
            y, sr = librosa.load(audio_path, sr=self.target_sample_rate)
            
            # Armazenar dados
            self.waveform_data = y
            self.sample_rate = sr
            self.duration = len(y) / sr
            
            return True
            
        except Exception as e:
            print(f"Erro ao carregar áudio para waveform: {e}")
            return False
    
    def get_waveform_data(self) -> Tuple[Optional[np.ndarray], float, int]:
        """
        Retorna dados do waveform.
        
        Returns:
            Tupla com (dados_waveform, duração, sample_rate)
        """
        return self.waveform_data, self.duration, self.sample_rate
    
    def get_waveform_segment(self, start_time: float, end_time: float) -> Optional[np.ndarray]:
        """
        Extrai segmento do waveform entre dois tempos.
        
        Args:
            start_time: Tempo de início em segundos
            end_time: Tempo de fim em segundos
            
        Returns:
            Array numpy com o segmento ou None se inválido
        """
        if self.waveform_data is None:
            return None
        
        # Converter tempos para índices
        start_idx = int(start_time * self.sample_rate)
        end_idx = int(end_time * self.sample_rate)
        
        # Limitar índices
        start_idx = max(0, start_idx)
        end_idx = min(len(self.waveform_data), end_idx)
        
        if start_idx >= end_idx:
            return None
        
        return self.waveform_data[start_idx:end_idx]
    
    def get_rms_energy(self, window_size: int = 1024) -> np.ndarray:
        """
        Calcula energia RMS do waveform em janelas.
        
        Args:
            window_size: Tamanho da janela em samples
            
        Returns:
            Array com energia RMS por janela
        """
        if self.waveform_data is None:
            return np.array([])
        
        # Calcular RMS em janelas
        rms = []
        for i in range(0, len(self.waveform_data), window_size):
            window = self.waveform_data[i:i + window_size]
            if len(window) > 0:
                rms.append(np.sqrt(np.mean(window**2)))
        
        return np.array(rms)
    
    def get_spectral_centroid(self, window_size: int = 1024) -> np.ndarray:
        """
        Calcula centroide espectral do waveform.
        
        Args:
            window_size: Tamanho da janela em samples
            
        Returns:
            Array com centroide espectral por janela
        """
        if self.waveform_data is None:
            return np.array([])
        
        centroids = []
        for i in range(0, len(self.waveform_data), window_size):
            window = self.waveform_data[i:i + window_size]
            if len(window) > 0:
                # Calcular FFT
                fft = np.fft.fft(window)
                freqs = np.fft.fftfreq(len(window), 1/self.sample_rate)
                
                # Calcular centroide espectral
                magnitude = np.abs(fft)
                if np.sum(magnitude) > 0:
                    centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
                    centroids.append(abs(centroid))
                else:
                    centroids.append(0)
        
        return np.array(centroids)
    
    def detect_silence(self, threshold: float = 0.01, min_duration: float = 0.1) -> List[Tuple[float, float]]:
        """
        Detecta períodos de silêncio no áudio.
        
        Args:
            threshold: Limiar de energia para considerar silêncio
            min_duration: Duração mínima para considerar um período de silêncio
            
        Returns:
            Lista de tuplas (início, fim) dos períodos de silêncio
        """
        if self.waveform_data is None:
            return []
        
        # Calcular energia RMS
        rms = self.get_rms_energy()
        
        # Detectar silêncio
        silence_mask = rms < threshold
        
        # Encontrar períodos contínuos de silêncio
        silence_periods = []
        in_silence = False
        silence_start = 0
        
        for i, is_silent in enumerate(silence_mask):
            if is_silent and not in_silence:
                # Início de silêncio
                in_silence = True
                silence_start = i
            elif not is_silent and in_silence:
                # Fim de silêncio
                in_silence = False
                silence_duration = (i - silence_start) * window_size / self.sample_rate
                if silence_duration >= min_duration:
                    start_time = silence_start * window_size / self.sample_rate
                    end_time = i * window_size / self.sample_rate
                    silence_periods.append((start_time, end_time))
        
        # Verificar se termina em silêncio
        if in_silence:
            silence_duration = (len(silence_mask) - silence_start) * window_size / self.sample_rate
            if silence_duration >= min_duration:
                start_time = silence_start * window_size / self.sample_rate
                end_time = len(self.waveform_data) / self.sample_rate
                silence_periods.append((start_time, end_time))
        
        return silence_periods
    
    def get_peak_positions(self, threshold: float = 0.5) -> List[float]:
        """
        Detecta posições de picos no waveform.
        
        Args:
            threshold: Limiar relativo para detectar picos (0.0 a 1.0)
            
        Returns:
            Lista de tempos em segundos onde ocorrem picos
        """
        if self.waveform_data is None:
            return []
        
        # Encontrar picos
        from scipy.signal import find_peaks
        
        # Normalizar waveform
        normalized = np.abs(self.waveform_data)
        max_val = np.max(normalized)
        threshold_abs = threshold * max_val
        
        # Encontrar picos
        peaks, _ = find_peaks(normalized, height=threshold_abs)
        
        # Converter índices para tempos
        peak_times = peaks / self.sample_rate
        
        return peak_times.tolist()
    
    def resample_waveform(self, target_length: int) -> np.ndarray:
        """
        Redimensiona waveform para um comprimento específico.
        
        Args:
            target_length: Comprimento desejado em samples
            
        Returns:
            Waveform redimensionado
        """
        if self.waveform_data is None:
            return np.array([])
        
        # Interpolar para o comprimento desejado
        from scipy.interpolate import interp1d
        
        original_length = len(self.waveform_data)
        original_indices = np.linspace(0, original_length - 1, original_length)
        target_indices = np.linspace(0, original_length - 1, target_length)
        
        f = interp1d(original_indices, self.waveform_data, kind='linear')
        resampled = f(target_indices)
        
        return resampled
    
    def get_waveform_stats(self) -> dict:
        """
        Retorna estatísticas do waveform.
        
        Returns:
            Dicionário com estatísticas
        """
        if self.waveform_data is None:
            return {}
        
        return {
            "duration": self.duration,
            "sample_rate": self.sample_rate,
            "samples": len(self.waveform_data),
            "max_amplitude": float(np.max(np.abs(self.waveform_data))),
            "rms": float(np.sqrt(np.mean(self.waveform_data**2))),
            "zero_crossings": int(np.sum(np.diff(np.sign(self.waveform_data)) != 0))
        }

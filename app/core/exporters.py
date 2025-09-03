"""
Módulo de exportação para diferentes formatos de legendas e letras.
"""
import json
from typing import List, Dict, Any
from pathlib import Path

from app.core.sync_model import LyricLine


class ExportError(Exception):
    """Exceção para erros de exportação."""
    pass


def format_time_srt(seconds: float) -> str:
    """Formata tempo para formato SRT (HH:MM:SS,mmm)."""
    if seconds < 0:
        seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


def format_time_vtt(seconds: float) -> str:
    """Formata tempo para formato VTT (HH:MM:SS.mmm)."""
    if seconds < 0:
        seconds = 0
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"


def format_time_lrc(seconds: float) -> str:
    """Formata tempo para formato LRC (MM:SS.xx)."""
    if seconds < 0:
        seconds = 0
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)  # centésimos
    return f"{minutes:02d}:{secs:02d}.{cs:02d}"


def export_txt(lines: List[LyricLine], path: str) -> None:
    """
    Exporta apenas o texto das letras para arquivo TXT.
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.text.strip():
                    f.write(line.text.strip() + '\n')
    except Exception as e:
        raise ExportError(f"Erro ao exportar TXT: {e}")


def export_srt(lines: List[LyricLine], path: str) -> None:
    """
    Exporta para formato SRT (legendas).
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            subtitle_index = 1
            for line in lines:
                text = line.text.strip()
                if not text:
                    continue
                start_time = format_time_srt(line.start)
                end_time = format_time_srt(line.end)
                
                f.write(f"{subtitle_index}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
                
                subtitle_index += 1
    except Exception as e:
        raise ExportError(f"Erro ao exportar SRT: {e}")


def export_lrc(lines: List[LyricLine], path: str) -> None:
    """
    Exporta para formato LRC (letras sincronizadas).
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                text = line.text.strip()
                if not text:
                    continue
                timestamp = format_time_lrc(line.start)
                f.write(f"[{timestamp}]{text}\n")
    except Exception as e:
        raise ExportError(f"Erro ao exportar LRC: {e}")


def export_vtt(lines: List[LyricLine], path: str) -> None:
    """
    Exporta para formato VTT (WebVTT).
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")
            
            for line in lines:
                text = line.text.strip()
                if not text:
                    continue
                start_time = format_time_vtt(line.start)
                end_time = format_time_vtt(line.end)
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
    except Exception as e:
        raise ExportError(f"Erro ao exportar VTT: {e}")


def export_json(lines: List[LyricLine], path: str) -> None:
    """
    Exporta para formato JSON com timestamps.
    
    Args:
        lines: Lista de linhas de letra
        path: Caminho do arquivo de saída
    """
    try:
        data = []
        for line in lines:
            if line.text.strip():
                data.append({
                    "start": line.start,
                    "end": line.end,
                    "text": line.text
                })
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ExportError(f"Erro ao exportar JSON: {e}")


class Exporter:
    """Classe principal para exportação de letras."""
    
    # Formatos suportados
    FORMATS = {
        "txt": {"name": "Texto Simples", "extension": ".txt", "function": export_txt},
        "srt": {"name": "Legendas SRT", "extension": ".srt", "function": export_srt},
        "lrc": {"name": "Letras LRC", "extension": ".lrc", "function": export_lrc},
        "vtt": {"name": "WebVTT", "extension": ".vtt", "function": export_vtt},
        "json": {"name": "JSON", "extension": ".json", "function": export_json}
    }
    
    @classmethod
    def get_supported_formats(cls) -> Dict[str, str]:
        """Retorna dicionário com formatos suportados."""
        return {fmt: info["name"] for fmt, info in cls.FORMATS.items()}
    
    @classmethod
    def export(cls, lines: List[LyricLine], path: str, format_type: str) -> None:
        """
        Exporta linhas para o formato especificado.
        
        Args:
            lines: Lista de linhas de letra
            path: Caminho do arquivo de saída
            format_type: Tipo de formato ("txt", "srt", "lrc", "vtt", "json")
        """
        if format_type not in cls.FORMATS:
            raise ExportError(f"Formato não suportado: {format_type}")
        
        # Adicionar extensão se não estiver presente
        path = Path(path)
        if not path.suffix:
            path = path.with_suffix(cls.FORMATS[format_type]["extension"])
        
        # Filtrar linhas vazias
        non_empty_lines = [line for line in lines if not line.is_empty()]
        
        if not non_empty_lines:
            raise ExportError("Nenhuma linha válida para exportar")
        
        # Exportar
        export_func = cls.FORMATS[format_type]["function"]
        export_func(non_empty_lines, str(path))
    
    @classmethod
    def export_all(cls, lines: List[LyricLine], base_path: str) -> Dict[str, str]:
        """
        Exporta para todos os formatos suportados.
        
        Args:
            lines: Lista de linhas de letra
            base_path: Caminho base (sem extensão)
            
        Returns:
            Dicionário com formato -> caminho do arquivo criado
        """
        base_path = Path(base_path)
        exported_files = {}
        
        for format_type, info in cls.FORMATS.items():
            try:
                file_path = base_path.with_suffix(info["extension"])
                cls.export(lines, str(file_path), format_type)
                exported_files[format_type] = str(file_path)
            except ExportError as e:
                print(f"Erro ao exportar {format_type}: {e}")
        
        return exported_files
    
    @classmethod
    def get_format_info(cls, format_type: str) -> Dict[str, Any]:
        """Retorna informações sobre um formato."""
        return cls.FORMATS.get(format_type, {})
    
    @classmethod
    def validate_lines(cls, lines: List[LyricLine]) -> List[str]:
        """
        Valida linhas e retorna lista de problemas encontrados.
        
        Args:
            lines: Lista de linhas para validar
            
        Returns:
            Lista de mensagens de erro
        """
        errors = []
        
        for i, line in enumerate(lines):
            if line.is_empty():
                continue
            
            # Verificar tempos válidos
            if line.start < 0:
                errors.append(f"Linha {i+1}: Tempo de início negativo ({line.start})")
            
            if line.end <= line.start:
                errors.append(f"Linha {i+1}: Tempo de fim deve ser maior que início ({line.start} -> {line.end})")
            
            # Verificar sobreposição com próxima linha
            if i < len(lines) - 1:
                next_line = lines[i + 1]
                if not next_line.is_empty() and line.end > next_line.start:
                    errors.append(f"Linha {i+1}: Sobreposição com próxima linha ({line.end} > {next_line.start})")
        
        return errors

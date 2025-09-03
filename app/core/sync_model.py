"""
Modelo de dados para sincronização de letras com timestamps.
"""
from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class LyricLine:
    """Representa uma linha de letra com timestamps de início e fim."""
    start: float = 0.0
    end: float = 0.0
    text: str = ""
    
    def __post_init__(self):
        """Validação básica após inicialização."""
        if self.start < 0:
            self.start = 0.0
        if self.end < self.start:
            self.end = self.start + 1.0
    
    def to_dict(self) -> dict:
        """Converte para dicionário."""
        return {
            "start": self.start,
            "end": self.end,
            "text": self.text
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LyricLine':
        """Cria instância a partir de dicionário."""
        return cls(
            start=data.get("start", 0.0),
            end=data.get("end", 0.0),
            text=data.get("text", "")
        )
    
    def is_empty(self) -> bool:
        """Verifica se a linha está vazia."""
        return not self.text.strip()
    
    def duration(self) -> float:
        """Retorna a duração da linha."""
        return self.end - self.start


@dataclass
class SyncProject:
    """Representa um projeto completo de sincronização."""
    audio_path: str = ""
    language: str = "pt"
    model_size: str = "base"
    lines: List[LyricLine] = field(default_factory=list)
    
    def add_line(self, line: LyricLine) -> None:
        """Adiciona uma linha ao projeto."""
        self.lines.append(line)
        self._normalize_times()
    
    def remove_line(self, index: int) -> None:
        """Remove uma linha pelo índice."""
        if 0 <= index < len(self.lines):
            del self.lines[index]
    
    def insert_line(self, index: int, line: LyricLine) -> None:
        """Insere uma linha em uma posição específica."""
        if 0 <= index <= len(self.lines):
            self.lines.insert(index, line)
            self._normalize_times()
    
    def split_line(self, index: int, split_time: float) -> None:
        """Divide uma linha em duas no tempo especificado."""
        if 0 <= index < len(self.lines):
            line = self.lines[index]
            if line.start < split_time < line.end:
                # Criar nova linha com a segunda parte
                new_line = LyricLine(
                    start=split_time,
                    end=line.end,
                    text=line.text
                )
                # Atualizar linha original
                line.end = split_time
                # Inserir nova linha
                self.insert_line(index + 1, new_line)
    
    def merge_lines(self, index: int) -> None:
        """Une a linha atual com a próxima."""
        if 0 <= index < len(self.lines) - 1:
            current_line = self.lines[index]
            next_line = self.lines[index + 1]
            
            # Combinar textos
            combined_text = f"{current_line.text} {next_line.text}".strip()
            
            # Atualizar linha atual
            current_line.text = combined_text
            current_line.end = next_line.end
            
            # Remover próxima linha
            self.remove_line(index + 1)
    
    def _normalize_times(self) -> None:
        """Garante que os tempos estejam em ordem crescente e sem sobreposição."""
        if not self.lines:
            return
        
        # Ordenar por tempo de início
        self.lines.sort(key=lambda x: x.start)
        
        # Ajustar sobreposições
        for i in range(len(self.lines) - 1):
            current = self.lines[i]
            next_line = self.lines[i + 1]
            
            if current.end > next_line.start:
                # Ajustar fim da linha atual
                current.end = next_line.start
    
    def get_non_empty_lines(self) -> List[LyricLine]:
        """Retorna apenas as linhas não vazias."""
        return [line for line in self.lines if not line.is_empty()]
    
    def to_dict(self) -> dict:
        """Converte projeto para dicionário."""
        return {
            "audio_path": self.audio_path,
            "language": self.language,
            "model_size": self.model_size,
            "lines": [line.to_dict() for line in self.lines]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SyncProject':
        """Cria projeto a partir de dicionário."""
        lines = [LyricLine.from_dict(line_data) for line_data in data.get("lines", [])]
        return cls(
            audio_path=data.get("audio_path", ""),
            language=data.get("language", "pt"),
            model_size=data.get("model_size", "base"),
            lines=lines
        )
    
    def to_json(self) -> str:
        """Converte para JSON."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SyncProject':
        """Cria projeto a partir de JSON."""
        data = json.loads(json_str)
        return cls.from_dict(data)

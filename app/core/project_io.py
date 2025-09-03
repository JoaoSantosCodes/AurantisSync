"""
Módulo para salvamento e carregamento de projetos.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from .sync_model import SyncProject


class ProjectIO:
    """Classe para operações de I/O de projetos."""
    
    PROJECT_EXTENSION = ".aurantisproj"
    AUTOSAVE_EXTENSION = ".autosave"
    
    def __init__(self, autosave_interval: int = 30):
        """
        Inicializa o sistema de I/O de projetos.
        
        Args:
            autosave_interval: Intervalo de autosave em segundos
        """
        self.autosave_interval = autosave_interval
        self.current_project_path: Optional[str] = None
        self.last_save_time: Optional[datetime] = None
        self.has_unsaved_changes = False
    
    def save_project(self, project: SyncProject, file_path: str) -> bool:
        """
        Salva projeto em arquivo.
        
        Args:
            project: Projeto a ser salvo
            file_path: Caminho do arquivo
            
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        try:
            # Adicionar extensão se necessário
            if not file_path.endswith(self.PROJECT_EXTENSION):
                file_path += self.PROJECT_EXTENSION
            
            # Preparar dados do projeto
            project_data = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "project": project.to_dict()
            }
            
            # Salvar arquivo
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            # Atualizar estado
            self.current_project_path = file_path
            self.last_save_time = datetime.now()
            self.has_unsaved_changes = False
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar projeto: {e}")
            return False
    
    def load_project(self, file_path: str) -> Optional[SyncProject]:
        """
        Carrega projeto de arquivo.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Projeto carregado ou None se houver erro
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar versão
            version = data.get("version", "1.0")
            if version != "1.0":
                print(f"Aviso: Versão do projeto ({version}) pode não ser compatível")
            
            # Carregar projeto
            project_data = data.get("project", {})
            project = SyncProject.from_dict(project_data)
            
            # Atualizar estado
            self.current_project_path = file_path
            self.last_save_time = datetime.now()
            self.has_unsaved_changes = False
            
            return project
            
        except Exception as e:
            print(f"Erro ao carregar projeto: {e}")
            return None
    
    def create_autosave(self, project: SyncProject) -> bool:
        """
        Cria arquivo de autosave.
        
        Args:
            project: Projeto a ser salvo
            
        Returns:
            True se salvo com sucesso, False caso contrário
        """
        if not self.current_project_path:
            return False
        
        try:
            # Criar caminho de autosave
            autosave_path = self._get_autosave_path(self.current_project_path)
            
            # Preparar dados
            project_data = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "modified": datetime.now().isoformat(),
                "is_autosave": True,
                "project": project.to_dict()
            }
            
            # Salvar autosave
            with open(autosave_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Erro ao criar autosave: {e}")
            return False
    
    def load_autosave(self, project_path: str) -> Optional[SyncProject]:
        """
        Carrega autosave de um projeto.
        
        Args:
            project_path: Caminho do projeto original
            
        Returns:
            Projeto do autosave ou None se não existir
        """
        autosave_path = self._get_autosave_path(project_path)
        
        if not os.path.exists(autosave_path):
            return None
        
        try:
            with open(autosave_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Verificar se é realmente um autosave
            if not data.get("is_autosave", False):
                return None
            
            # Carregar projeto
            project_data = data.get("project", {})
            project = SyncProject.from_dict(project_data)
            
            return project
            
        except Exception as e:
            print(f"Erro ao carregar autosave: {e}")
            return None
    
    def delete_autosave(self, project_path: str) -> bool:
        """
        Remove arquivo de autosave.
        
        Args:
            project_path: Caminho do projeto original
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        autosave_path = self._get_autosave_path(project_path)
        
        try:
            if os.path.exists(autosave_path):
                os.remove(autosave_path)
            return True
        except Exception as e:
            print(f"Erro ao remover autosave: {e}")
            return False
    
    def has_autosave(self, project_path: str) -> bool:
        """
        Verifica se existe autosave para um projeto.
        
        Args:
            project_path: Caminho do projeto
            
        Returns:
            True se existe autosave, False caso contrário
        """
        autosave_path = self._get_autosave_path(project_path)
        return os.path.exists(autosave_path)
    
    def get_autosave_info(self, project_path: str) -> Optional[Dict[str, Any]]:
        """
        Retorna informações sobre o autosave.
        
        Args:
            project_path: Caminho do projeto
            
        Returns:
            Dicionário com informações do autosave ou None
        """
        autosave_path = self._get_autosave_path(project_path)
        
        if not os.path.exists(autosave_path):
            return None
        
        try:
            with open(autosave_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return {
                "path": autosave_path,
                "modified": data.get("modified"),
                "size": os.path.getsize(autosave_path)
            }
            
        except Exception as e:
            print(f"Erro ao obter informações do autosave: {e}")
            return None
    
    def _get_autosave_path(self, project_path: str) -> str:
        """Gera caminho do arquivo de autosave."""
        project_path = Path(project_path)
        return str(project_path.with_suffix(self.AUTOSAVE_EXTENSION))
    
    def should_autosave(self) -> bool:
        """
        Verifica se deve fazer autosave baseado no tempo.
        
        Returns:
            True se deve fazer autosave, False caso contrário
        """
        if not self.last_save_time:
            return True
        
        time_since_save = (datetime.now() - self.last_save_time).total_seconds()
        return time_since_save >= self.autosave_interval
    
    def mark_as_modified(self) -> None:
        """Marca projeto como modificado."""
        self.has_unsaved_changes = True
    
    def mark_as_saved(self) -> None:
        """Marca projeto como salvo."""
        self.has_unsaved_changes = False
        self.last_save_time = datetime.now()
    
    def get_project_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Retorna informações sobre um arquivo de projeto.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            Dicionário com informações ou None se erro
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            project_data = data.get("project", {})
            
            return {
                "version": data.get("version", "1.0"),
                "created": data.get("created"),
                "modified": data.get("modified"),
                "audio_path": project_data.get("audio_path", ""),
                "language": project_data.get("language", "pt"),
                "model_size": project_data.get("model_size", "base"),
                "lines_count": len(project_data.get("lines", [])),
                "file_size": os.path.getsize(file_path),
                "is_autosave": data.get("is_autosave", False)
            }
            
        except Exception as e:
            print(f"Erro ao obter informações do projeto: {e}")
            return None
    
    def export_project_summary(self, project: SyncProject, output_path: str) -> bool:
        """
        Exporta resumo do projeto em formato legível.
        
        Args:
            project: Projeto a ser exportado
            output_path: Caminho do arquivo de saída
            
        Returns:
            True se exportado com sucesso, False caso contrário
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("=== RESUMO DO PROJETO AURANTIS SYNC ===\n\n")
                f.write(f"Arquivo de áudio: {project.audio_path}\n")
                f.write(f"Idioma: {project.language}\n")
                f.write(f"Modelo: {project.model_size}\n")
                f.write(f"Total de linhas: {len(project.lines)}\n")
                f.write(f"Linhas não vazias: {len(project.get_non_empty_lines())}\n\n")
                
                f.write("=== LINHAS ===\n")
                for i, line in enumerate(project.lines, 1):
                    if not line.is_empty():
                        f.write(f"{i:3d}. [{line.start:6.2f}s - {line.end:6.2f}s] {line.text}\n")
                
                f.write(f"\nGerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            return True
            
        except Exception as e:
            print(f"Erro ao exportar resumo: {e}")
            return False

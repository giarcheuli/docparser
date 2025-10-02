"""
Document Scanner - Core scanning functionality for directory traversal and file discovery
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileInfo:
    """Data class to store file information"""
    path: Path
    name: str
    extension: str
    size: int
    created: datetime
    modified: datetime
    project_name: Optional[str] = None
    relative_path: Optional[str] = None
    subfolder_path: Optional[str] = None
    is_readable: bool = True
    error_message: str = ""

class DocumentScanner:
    """Scans directories for supported document types and collects file metadata"""
    
    SUPPORTED_EXTENSIONS = {
        '.doc', '.docx',  # Word documents
        '.pdf',           # PDF files
        '.txt',           # Text files
        '.html', '.htm',  # HTML files
        '.md', '.markdown', # Markdown files
        '.xlsx', '.xls',  # Excel files
        '.xml'            # XML files
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scanned_files: List[FileInfo] = []
        self.root_directory: Optional[Path] = None
        self.projects: Dict[str, List[FileInfo]] = {}
        
    def scan_directory(self, directory_path: str) -> List[FileInfo]:
        """
        Scan a directory recursively for supported document types with project awareness
        
        Args:
            directory_path: Path to the directory to scan
            
        Returns:
            List of FileInfo objects for supported files
        """
        self.scanned_files = []
        self.projects = {}
        self.root_directory = Path(directory_path)
        
        if not self.root_directory.exists():
            self.logger.error(f"Directory does not exist: {directory_path}")
            return []
            
        if not self.root_directory.is_dir():
            self.logger.error(f"Path is not a directory: {directory_path}")
            return []
            
        self.logger.info(f"Starting project-aware scan of directory: {directory_path}")
        
        try:
            for root, dirs, files in os.walk(self.root_directory):
                for file in files:
                    file_path = Path(root) / file
                    if self._is_supported_file(file_path):
                        file_info = self._extract_file_info(file_path)
                        self.scanned_files.append(file_info)
                        
                        # Group by project
                        if file_info.project_name:
                            if file_info.project_name not in self.projects:
                                self.projects[file_info.project_name] = []
                            self.projects[file_info.project_name].append(file_info)
                        
        except Exception as e:
            self.logger.error(f"Error scanning directory: {e}")
            
        self.logger.info(f"Scan completed. Found {len(self.scanned_files)} files across {len(self.projects)} projects")
        return self.scanned_files
    
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if file extension is supported"""
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
    
    def _extract_file_info(self, file_path: Path) -> FileInfo:
        """Extract metadata from a file with project context"""
        try:
            stat = file_path.stat()
            
            # Extract project information from path hierarchy
            project_name, relative_path, subfolder_path = self._extract_project_info(file_path)
            
            return FileInfo(
                path=file_path,
                name=file_path.name,
                extension=file_path.suffix.lower(),
                size=stat.st_size,
                created=datetime.fromtimestamp(stat.st_ctime),
                modified=datetime.fromtimestamp(stat.st_mtime),
                project_name=project_name,
                relative_path=relative_path,
                subfolder_path=subfolder_path,
                is_readable=os.access(file_path, os.R_OK)
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting file info for {file_path}: {e}")
            return FileInfo(
                path=file_path,
                name=file_path.name,
                extension=file_path.suffix.lower(),
                size=0,
                created=datetime.now(),
                modified=datetime.now(),
                is_readable=False,
                error_message=str(e)
            )
    
    def _extract_project_info(self, file_path: Path) -> tuple[Optional[str], Optional[str], Optional[str]]:
        """Extract project name and relative path information"""
        if not self.root_directory:
            return None, None, None
            
        try:
            # Get relative path from root directory
            rel_path = file_path.relative_to(self.root_directory)
            path_parts = rel_path.parts
            
            if len(path_parts) >= 2:
                # Level 2 directory is the project name
                project_name = path_parts[0]
                
                # Full relative path from root
                relative_path = str(rel_path)
                
                # Subfolder path (everything between project and file)
                if len(path_parts) > 2:
                    subfolder_path = "/".join(path_parts[1:-1])
                else:
                    subfolder_path = ""
                    
                return project_name, relative_path, subfolder_path
            
            elif len(path_parts) == 1:
                # File is directly in root directory - treat root as single project
                project_name = self.root_directory.name
                relative_path = str(rel_path)
                subfolder_path = ""
                
                return project_name, relative_path, subfolder_path
                
        except ValueError:
            # File is not under root directory
            pass
            
        return None, None, None
    
    def get_summary_stats(self) -> Dict[str, int]:
        """Get summary statistics about scanned files"""
        stats = {}
        for file_info in self.scanned_files:
            ext = file_info.extension
            stats[ext] = stats.get(ext, 0) + 1
            
        stats['total_files'] = len(self.scanned_files)
        stats['total_size'] = sum(f.size for f in self.scanned_files)
        stats['total_projects'] = len(self.projects)
        
        return stats
    
    def get_projects(self) -> Dict[str, List[FileInfo]]:
        """Get files grouped by project"""
        return self.projects.copy()
    
    def get_project_stats(self) -> Dict[str, Dict]:
        """Get statistics for each project"""
        project_stats = {}
        
        for project_name, files in self.projects.items():
            stats = {
                'file_count': len(files),
                'total_size': sum(f.size for f in files),
                'extensions': {},
                'subfolders': set()
            }
            
            for file_info in files:
                # Count extensions
                ext = file_info.extension
                stats['extensions'][ext] = stats['extensions'].get(ext, 0) + 1
                
                # Collect subfolders
                if file_info.subfolder_path:
                    stats['subfolders'].add(file_info.subfolder_path)
            
            # Convert set to list for JSON serialization
            stats['subfolders'] = list(stats['subfolders'])
            project_stats[project_name] = stats
            
        return project_stats
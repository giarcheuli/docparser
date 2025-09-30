"""
Base analyzer interface for all document analyzers
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseAnalyzer(ABC):
    """Abstract base class for all document analyzers"""
    
    @abstractmethod
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from the document"""
        pass
    
    @abstractmethod
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from the document"""
        pass
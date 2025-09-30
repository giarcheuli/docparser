"""
Text file analyzer for .txt, .md, and .markdown files
"""

import logging
from pathlib import Path
from typing import Dict, Any
import chardet

from . import BaseAnalyzer

class TextAnalyzer(BaseAnalyzer):
    """Analyzer for plain text and markdown files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from text/markdown files"""
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding_result = chardet.detect(raw_data)
                encoding = encoding_result.get('encoding', 'utf-8')
            
            # Read with detected encoding
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
                
            return content
            
        except Exception as e:
            self.logger.error(f"Error reading text file {file_path}: {e}")
            return ""
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from text files"""
        try:
            stat = file_path.stat()
            
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding_result = chardet.detect(raw_data)
            
            # Count lines
            with open(file_path, 'r', encoding=encoding_result.get('encoding', 'utf-8'), errors='ignore') as f:
                lines = sum(1 for _ in f)
            
            metadata = {
                'file_type': 'text',
                'encoding': encoding_result.get('encoding', 'unknown'),
                'encoding_confidence': encoding_result.get('confidence', 0),
                'line_count': lines,
                'size_bytes': stat.st_size,
                'is_markdown': file_path.suffix.lower() in ['.md', '.markdown']
            }
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {'error': str(e)}
"""
Word document analyzer for .doc and .docx files
"""

import logging
from pathlib import Path
from typing import Dict, Any

try:
    from docx import Document
    import docx.oxml
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from . import BaseAnalyzer

class WordAnalyzer(BaseAnalyzer):
    """Analyzer for Word documents (.docx files, limited .doc support)"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not DOCX_AVAILABLE:
            self.logger.warning("python-docx not available. Word document analysis will be limited.")
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from Word documents"""
        if not DOCX_AVAILABLE:
            return "Word document analysis requires python-docx package"
        
        # Only support .docx files (not .doc)
        if file_path.suffix.lower() == '.doc':
            return "Legacy .doc files not supported. Please convert to .docx format."
        
        try:
            doc = Document(file_path)
            
            text_content = []
            
            # Extract paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        text_content.append(" | ".join(row_text))
            
            return "\n".join(text_content)
            
        except Exception as e:
            self.logger.error(f"Error reading Word document {file_path}: {e}")
            return f"Error reading Word document: {str(e)}"
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from Word documents"""
        if not DOCX_AVAILABLE:
            return {'error': 'python-docx not available'}
        
        if file_path.suffix.lower() == '.doc':
            return {'file_type': 'word_legacy', 'error': 'Legacy .doc format not supported'}
        
        try:
            doc = Document(file_path)
            
            metadata = {
                'file_type': 'word_docx',
                'paragraph_count': len(doc.paragraphs),
                'table_count': len(doc.tables),
            }
            
            # Extract core properties if available
            if hasattr(doc.core_properties, 'title') and doc.core_properties.title:
                metadata['title'] = doc.core_properties.title
            if hasattr(doc.core_properties, 'author') and doc.core_properties.author:
                metadata['author'] = doc.core_properties.author
            if hasattr(doc.core_properties, 'subject') and doc.core_properties.subject:
                metadata['subject'] = doc.core_properties.subject
            if hasattr(doc.core_properties, 'keywords') and doc.core_properties.keywords:
                metadata['keywords'] = doc.core_properties.keywords
            if hasattr(doc.core_properties, 'comments') and doc.core_properties.comments:
                metadata['comments'] = doc.core_properties.comments
            if hasattr(doc.core_properties, 'created') and doc.core_properties.created:
                metadata['created'] = str(doc.core_properties.created)
            if hasattr(doc.core_properties, 'modified') and doc.core_properties.modified:
                metadata['modified'] = str(doc.core_properties.modified)
            if hasattr(doc.core_properties, 'last_modified_by') and doc.core_properties.last_modified_by:
                metadata['last_modified_by'] = doc.core_properties.last_modified_by
            
            # Count different elements
            styles_used = set()
            for paragraph in doc.paragraphs:
                if paragraph.style:
                    styles_used.add(paragraph.style.name)
            
            metadata['styles_used'] = list(styles_used)
            metadata['style_count'] = len(styles_used)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting Word document metadata from {file_path}: {e}")
            return {'error': str(e)}
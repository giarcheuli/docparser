"""
PDF analyzer for extracting text and metadata from PDF files
"""

import logging
from pathlib import Path
from typing import Dict, Any

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from . import BaseAnalyzer

class PDFAnalyzer(BaseAnalyzer):
    """Analyzer for PDF files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not PDF_AVAILABLE:
            self.logger.warning("PyPDF2 not available. PDF analysis will be limited.")
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from PDF files"""
        if not PDF_AVAILABLE:
            return "PDF analysis requires PyPDF2 package"
        
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        self.logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        
            return text
            
        except Exception as e:
            self.logger.error(f"Error reading PDF file {file_path}: {e}")
            return f"Error reading PDF: {str(e)}"
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from PDF files"""
        if not PDF_AVAILABLE:
            return {'error': 'PyPDF2 not available'}
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                metadata = {
                    'file_type': 'pdf',
                    'page_count': len(pdf_reader.pages),
                    'is_encrypted': pdf_reader.is_encrypted,
                }
                
                # Extract document info if available
                if pdf_reader.metadata:
                    doc_info = pdf_reader.metadata
                    metadata.update({
                        'title': doc_info.get('/Title', ''),
                        'author': doc_info.get('/Author', ''),
                        'subject': doc_info.get('/Subject', ''),
                        'creator': doc_info.get('/Creator', ''),
                        'producer': doc_info.get('/Producer', ''),
                        'creation_date': str(doc_info.get('/CreationDate', '')),
                        'modification_date': str(doc_info.get('/ModDate', ''))
                    })
                
                return metadata
                
        except Exception as e:
            self.logger.error(f"Error extracting PDF metadata from {file_path}: {e}")
            return {'error': str(e)}
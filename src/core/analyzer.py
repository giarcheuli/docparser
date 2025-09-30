"""
Document Analyzer - Main analysis orchestrator that coordinates different analyzers
"""

import logging
from typing import List, Dict, Optional
from pathlib import Path
from dataclasses import dataclass, asdict

from .scanner import DocumentScanner, FileInfo

# Import analyzers with error handling
try:
    from ..analyzers.text_analyzer import TextAnalyzer
    from ..analyzers.pdf_analyzer import PDFAnalyzer
    from ..analyzers.word_analyzer import WordAnalyzer
    from ..analyzers.excel_analyzer import ExcelAnalyzer
    from ..analyzers.html_analyzer import HTMLAnalyzer
    from ..analyzers.xml_analyzer import XMLAnalyzer
except ImportError:
    # Fallback imports for when running directly
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from analyzers.text_analyzer import TextAnalyzer
    from analyzers.pdf_analyzer import PDFAnalyzer
    from analyzers.word_analyzer import WordAnalyzer
    from analyzers.excel_analyzer import ExcelAnalyzer
    from analyzers.html_analyzer import HTMLAnalyzer
    from analyzers.xml_analyzer import XMLAnalyzer

@dataclass
class AnalysisResult:
    """Result of document analysis"""
    file_info: FileInfo
    content_preview: str
    word_count: int
    metadata: Dict
    summary: str = ""
    ai_insights: str = ""
    error: str = ""

class DocumentAnalyzer:
    """Main analyzer that coordinates different file type analyzers"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scanner = DocumentScanner()
        
        # Initialize specific analyzers
        self.analyzers = {
            '.txt': TextAnalyzer(),
            '.md': TextAnalyzer(),
            '.markdown': TextAnalyzer(),
            '.pdf': PDFAnalyzer(),
            '.doc': WordAnalyzer(),
            '.docx': WordAnalyzer(),
            '.xlsx': ExcelAnalyzer(),
            '.xls': ExcelAnalyzer(),
            '.html': HTMLAnalyzer(),
            '.htm': HTMLAnalyzer(),
            '.xml': XMLAnalyzer()
        }
    
    def analyze_directory(self, directory_path: str, use_ai: bool = True) -> List[AnalysisResult]:
        """
        Analyze all supported documents in a directory
        
        Args:
            directory_path: Path to directory to analyze
            use_ai: Whether to use AI for content analysis
            
        Returns:
            List of AnalysisResult objects
        """
        self.logger.info(f"Starting analysis of directory: {directory_path}")
        
        # First, scan the directory
        files = self.scanner.scan_directory(directory_path)
        
        if not files:
            self.logger.warning("No supported files found in directory")
            return []
        
        results = []
        for file_info in files:
            try:
                result = self._analyze_file(file_info, use_ai)
                results.append(result)
                self.logger.info(f"Analyzed: {file_info.name}")
            except Exception as e:
                self.logger.error(f"Error analyzing {file_info.name}: {e}")
                error_result = AnalysisResult(
                    file_info=file_info,
                    content_preview="",
                    word_count=0,
                    metadata={},
                    error=str(e)
                )
                results.append(error_result)
        
        self.logger.info(f"Analysis completed. Processed {len(results)} files")
        return results
    
    def _analyze_file(self, file_info: FileInfo, use_ai: bool) -> AnalysisResult:
        """Analyze a single file using the appropriate analyzer"""
        
        if not file_info.is_readable:
            return AnalysisResult(
                file_info=file_info,
                content_preview="",
                word_count=0,
                metadata={},
                error=f"File not readable: {file_info.error_message}"
            )
        
        # Get the appropriate analyzer
        analyzer = self.analyzers.get(file_info.extension)
        
        if not analyzer:
            return AnalysisResult(
                file_info=file_info,
                content_preview="",
                word_count=0,
                metadata={},
                error=f"No analyzer available for {file_info.extension} files"
            )
        
        try:
            # Extract content and metadata
            content = analyzer.extract_text(file_info.path)
            metadata = analyzer.extract_metadata(file_info.path)
            
            # Calculate word count
            word_count = len(content.split()) if content else 0
            
            # Create preview (first 500 characters)
            preview = content[:500] + "..." if len(content) > 500 else content
            
            result = AnalysisResult(
                file_info=file_info,
                content_preview=preview,
                word_count=word_count,
                metadata=metadata
            )
            
            # Add AI analysis if requested
            if use_ai and content:
                try:
                    # Import with fallback
                    try:
                        from ..utils.ai_analyzer import AIAnalyzer
                    except ImportError:
                        import sys
                        import os
                        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
                        from utils.ai_analyzer import AIAnalyzer
                    
                    ai_analyzer = AIAnalyzer()
                    result.summary = ai_analyzer.summarize_content(
                        content, 
                        project_context=file_info.project_name
                    )
                    result.ai_insights = ai_analyzer.analyze_content(
                        content, 
                        file_info.name,
                        project_context=file_info.project_name,
                        subfolder_path=file_info.subfolder_path
                    )
                except Exception as e:
                    self.logger.warning(f"AI analysis failed for {file_info.name}: {e}")
                    result.ai_insights = "AI analysis unavailable"
            
            return result
            
        except Exception as e:
            return AnalysisResult(
                file_info=file_info,
                content_preview="",
                word_count=0,
                metadata={},
                error=f"Analysis failed: {str(e)}"
            )
    
    def get_directory_summary(self) -> Dict:
        """Get summary statistics for the last scanned directory"""
        return self.scanner.get_summary_stats()
    
    def get_projects(self) -> Dict:
        """Get files grouped by project"""
        return self.scanner.get_projects()
    
    def get_project_stats(self) -> Dict:
        """Get statistics for each project"""
        return self.scanner.get_project_stats()
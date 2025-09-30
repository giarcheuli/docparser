"""
Simple test runner for Document Analyzer
"""

import unittest
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestDocumentScanner(unittest.TestCase):
    """Basic tests for document scanner"""
    
    def test_scanner_import(self):
        """Test that scanner module can be imported"""
        try:
            from core.scanner import DocumentScanner
            scanner = DocumentScanner()
            self.assertIsNotNone(scanner)
        except ImportError as e:
            self.fail(f"Failed to import DocumentScanner: {e}")
    
    def test_supported_extensions(self):
        """Test supported file extensions"""
        from core.scanner import DocumentScanner
        scanner = DocumentScanner()
        
        expected_extensions = {'.doc', '.docx', '.pdf', '.txt', '.html', '.htm', 
                              '.md', '.markdown', '.xlsx', '.xls', '.xml'}
        
        self.assertEqual(scanner.SUPPORTED_EXTENSIONS, expected_extensions)

class TestAnalyzers(unittest.TestCase):
    """Basic tests for file analyzers"""
    
    def test_analyzer_imports(self):
        """Test that all analyzers can be imported"""
        analyzer_modules = [
            'analyzers.text_analyzer',
            'analyzers.pdf_analyzer', 
            'analyzers.word_analyzer',
            'analyzers.excel_analyzer',
            'analyzers.html_analyzer',
            'analyzers.xml_analyzer'
        ]
        
        for module_name in analyzer_modules:
            try:
                __import__(module_name)
            except ImportError as e:
                self.fail(f"Failed to import {module_name}: {e}")

class TestUtilities(unittest.TestCase):
    """Basic tests for utility modules"""
    
    def test_project_report_generator_import(self):
        """Test project report generator import"""
        try:
            from utils.project_report_generator import ProjectReportGenerator
            generator = ProjectReportGenerator()
            self.assertIsNotNone(generator)
        except ImportError as e:
            self.fail(f"Failed to import ProjectReportGenerator: {e}")
    
    def test_ai_analyzer_import(self):
        """Test AI analyzer import"""
        try:
            from utils.ai_analyzer import AIAnalyzer
            analyzer = AIAnalyzer()
            self.assertIsNotNone(analyzer)
        except ImportError as e:
            self.fail(f"Failed to import AIAnalyzer: {e}")

if __name__ == '__main__':
    print("Running Document Analyzer Tests...")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)
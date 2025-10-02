#!/usr/bin/env python3
"""
Test suite for configurable AI integration feature
"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.ai_config import AIConfig
from src.utils.ai_analyzer import AIAnalyzer

class TestAIConfig(unittest.TestCase):
    """Test AI configuration management"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.yaml")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration loading"""
        config = AIConfig(self.config_path)
        
        # Check default provider is set
        self.assertEqual(config.get_default_provider(), "replicate")
        
        # Check default providers exist
        providers = config.config.get("ai_providers", {})
        self.assertIn("replicate", providers)
        self.assertIn("openai", providers)
        self.assertIn("anthropic", providers)
        self.assertIn("gemini", providers)
    
    def test_provider_enablement(self):
        """Test enabling/disabling providers"""
        config = AIConfig(self.config_path)
        
        # Test enabling a provider
        config.set_provider_enabled("openai", True)
        self.assertTrue(config.is_provider_enabled("openai"))
        
        # Test disabling a provider
        config.set_provider_enabled("openai", False)
        self.assertFalse(config.is_provider_enabled("openai"))
    
    def test_credential_resolution(self):
        """Test API credential resolution"""
        config = AIConfig(self.config_path)
        
        # Test environment variable resolution
        os.environ["TEST_API_KEY"] = "test_key_123"
        config.update_provider_config("test_provider", {"api_key": "${TEST_API_KEY}"})
        
        credential = config.get_api_credential("test_provider")
        self.assertEqual(credential, "test_key_123")
        
        # Clean up
        del os.environ["TEST_API_KEY"]
    
    def test_config_validation(self):
        """Test configuration validation"""
        config = AIConfig(self.config_path)
        
        # Test with no enabled providers
        config.config["ai_providers"] = {"default": "none"}
        self.assertFalse(config.validate_config())
        
        # Test with enabled provider but no credential
        config.set_provider_enabled("replicate", True)
        self.assertFalse(config.validate_config())
    
    def test_save_load_config(self):
        """Test saving and loading configuration"""
        config = AIConfig(self.config_path)
        
        # Modify configuration
        config.set_default_provider("openai")
        config.set_provider_enabled("openai", True)
        config.save_config()
        
        # Load new config instance
        config2 = AIConfig(self.config_path)
        self.assertEqual(config2.get_default_provider(), "openai")
        self.assertTrue(config2.is_provider_enabled("openai"))

class TestAIAnalyzer(unittest.TestCase):
    """Test AI analyzer with new configuration system"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.yaml")
        
        # Create test config with mock provider
        config = AIConfig(self.config_path)
        config.config["ai_providers"]["mock"] = {
            "enabled": True,
            "api_key": "test_key"
        }
        config.save_config()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.temp_dir)
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization with config"""
        analyzer = AIAnalyzer(self.config_path)
        
        # Should have config loaded
        self.assertIsNotNone(analyzer.config)
        self.assertEqual(analyzer.config.config_path, self.config_path)
    
    def test_available_providers(self):
        """Test getting available providers"""
        analyzer = AIAnalyzer(self.config_path)
        
        # Should return list (may be empty if no credentials)
        providers = analyzer.get_available_providers()
        self.assertIsInstance(providers, list)
    
    def test_fallback_methods(self):
        """Test fallback methods when AI is unavailable"""
        analyzer = AIAnalyzer(self.config_path)
        
        # Test fallback summary
        content = "This is a test document with some content to summarize."
        summary = analyzer._fallback_summary(content, 50)
        self.assertIsNotNone(summary)
        self.assertTrue(len(summary) <= 53)  # Including "..."
        
        # Test fallback analysis
        analysis = analyzer._fallback_analysis(content, "test.txt")
        self.assertIn("Document Analysis", analysis)
        self.assertIn("TXT", analysis)
    
    def test_ai_availability(self):
        """Test AI availability checking"""
        analyzer = AIAnalyzer(self.config_path)
        
        # Should return boolean
        available = analyzer.is_available()
        self.assertIsInstance(available, bool)
    
    def test_content_processing(self):
        """Test content processing methods"""
        analyzer = AIAnalyzer(self.config_path)
        
        # Test with empty content
        result = analyzer.summarize_content("")
        self.assertEqual(result, "Content too short for meaningful summary")
        
        # Test with short content
        result = analyzer.analyze_content("Hi", "test.txt")
        self.assertEqual(result, "Content too short for analysis")

class TestConfigManager(unittest.TestCase):
    """Test the configuration manager script"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    
    def test_config_creation(self):
        """Test configuration file creation"""
        # Import and test the config manager
        import importlib.util
        script_path = Path(__file__).parent.parent / "ai_config_manager.py"
        
        spec = importlib.util.spec_from_file_location("ai_config_manager", script_path)
        manager = importlib.util.module_from_spec(spec)
        
        # This would test the create_sample_config function
        # But requires mocking to avoid actual file creation
        self.assertTrue(script_path.exists())

def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestAIConfig))
    suite.addTest(unittest.makeSuite(TestAIAnalyzer))
    suite.addTest(unittest.makeSuite(TestConfigManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
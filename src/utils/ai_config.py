"""
AI Configuration Module - Manages multi-provider AI settings
"""

# Load environment variables FIRST before any other imports
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)  # Override existing env vars
except ImportError:
    # dotenv not available, skip loading
    pass

import yaml
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class AIConfig:
    """Manages AI provider configuration"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config_path = config_path or "ai_config.yaml"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults"""
        
        # Default configuration
        default_config = {
            "ai_providers": {
                "default": "replicate",
                "replicate": {
                    "enabled": True,
                    "api_token": "${REPLICATE_API_TOKEN}",
                    "model": "meta/llama-2-7b-chat",
                    "max_tokens": 1000,
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                },
                "openai": {
                    "enabled": False,
                    "api_key": "${OPENAI_API_KEY}",
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000,
                    "temperature": 0.3
                },
                "anthropic": {
                    "enabled": False,
                    "api_key": "${ANTHROPIC_API_KEY}",
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 1000,
                    "temperature": 0.3
                },
                "gemini": {
                    "enabled": False,
                    "api_key": "${GEMINI_API_KEY}",
                    "model": "gemini-pro",
                    "max_tokens": 1000,
                    "temperature": 0.3
                }
            },
            "fallback": {
                "enabled": True,
                "order": ["replicate", "openai", "gemini", "anthropic"]
            }
        }
        
        # Try to load from file
        config_file = Path(self.config_path)
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        # Merge with defaults
                        default_config.update(file_config)
                        self.logger.info(f"Loaded AI configuration from {self.config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config file {self.config_path}: {e}")
                self.logger.info("Using default configuration")
        else:
            self.logger.info("No config file found, using defaults")
            
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider"""
        return self.config.get("ai_providers", {}).get(provider, {})
    
    def get_default_provider(self) -> str:
        """Get the default AI provider"""
        return self.config.get("ai_providers", {}).get("default", "replicate")
    
    def get_fallback_order(self) -> list:
        """Get the fallback provider order"""
        fallback_config = self.config.get("fallback", {})
        if fallback_config.get("enabled", True):
            return fallback_config.get("order", ["replicate"])
        return []
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a provider is enabled"""
        provider_config = self.get_provider_config(provider)
        return provider_config.get("enabled", False)
    
    def get_api_credential(self, provider: str) -> Optional[str]:
        """Get API credential for provider, resolving environment variables"""
        provider_config = self.get_provider_config(provider)
        
        # Determine credential key based on provider
        if provider == "replicate":
            credential_key = "api_token"
        else:
            credential_key = "api_key"
            
        credential = provider_config.get(credential_key, "")
        
        # Resolve environment variables
        if credential.startswith("${") and credential.endswith("}"):
            env_var = credential[2:-1]
            return os.getenv(env_var)
        
        return credential
    
    def set_provider_enabled(self, provider: str, enabled: bool):
        """Enable or disable a provider"""
        if "ai_providers" not in self.config:
            self.config["ai_providers"] = {}
        if provider not in self.config["ai_providers"]:
            self.config["ai_providers"][provider] = {}
            
        self.config["ai_providers"][provider]["enabled"] = enabled
        self.logger.info(f"Provider {provider} {'enabled' if enabled else 'disabled'}")
    
    def set_default_provider(self, provider: str):
        """Set the default provider"""
        if "ai_providers" not in self.config:
            self.config["ai_providers"] = {}
            
        self.config["ai_providers"]["default"] = provider
        self.logger.info(f"Default provider set to {provider}")
    
    def update_provider_config(self, provider: str, config_updates: Dict[str, Any]):
        """Update configuration for a specific provider"""
        if "ai_providers" not in self.config:
            self.config["ai_providers"] = {}
        if provider not in self.config["ai_providers"]:
            self.config["ai_providers"][provider] = {}
            
        self.config["ai_providers"][provider].update(config_updates)
        self.logger.info(f"Updated configuration for provider {provider}")
    
    def validate_config(self) -> bool:
        """Validate the current configuration"""
        try:
            # Check if at least one provider is enabled
            providers = self.config.get("ai_providers", {})
            enabled_providers = [p for p, cfg in providers.items() 
                               if isinstance(cfg, dict) and cfg.get("enabled", False)]
            
            if not enabled_providers:
                self.logger.warning("No AI providers are enabled")
                return False
            
            # Check if default provider is enabled
            default = self.get_default_provider()
            if default not in enabled_providers:
                self.logger.warning(f"Default provider '{default}' is not enabled")
                return False
            
            # Check if enabled providers have credentials
            for provider in enabled_providers:
                credential = self.get_api_credential(provider)
                if not credential:
                    self.logger.warning(f"Provider '{provider}' is enabled but has no API credential")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def get_available_providers(self) -> list:
        """Get list of available providers with credentials"""
        available = []
        providers = self.config.get("ai_providers", {})
        
        for provider, config in providers.items():
            if provider == "default":
                continue
                
            if isinstance(config, dict) and config.get("enabled", False):
                credential = self.get_api_credential(provider)
                if credential:
                    available.append(provider)
        
        return available
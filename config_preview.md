# DocParser Configuration (v2.1 Preview)

This file demonstrates the planned configuration system for DocParser v2.1.

## AI Provider Configuration

```yaml
# ai_config.yaml (planned for v2.1)
ai_providers:
  # Default provider (Replicate remains default for compatibility)
  default: replicate
  
  # Replicate Configuration (current default)
  replicate:
    enabled: true
    api_token: ${REPLICATE_API_TOKEN}
    model: "meta/llama-2-7b-chat"
    max_tokens: 1000
    temperature: 0.7
    
  # OpenAI Configuration
  openai:
    enabled: false
    api_key: ${OPENAI_API_KEY}
    model: "gpt-3.5-turbo"
    max_tokens: 1000
    temperature: 0.7
    
  # Anthropic Configuration
  anthropic:
    enabled: false
    api_key: ${ANTHROPIC_API_KEY}
    model: "claude-3-haiku-20240307"
    max_tokens: 1000
    temperature: 0.7
    
  # Google Gemini Configuration
  gemini:
    enabled: false
    api_key: ${GEMINI_API_KEY}
    model: "gemini-pro"
    max_tokens: 1000
    temperature: 0.7

# Fallback behavior
fallback:
  enabled: true
  order: ["replicate", "openai", "gemini", "anthropic"]
```

## Project Detection Configuration

```yaml
# project_config.yaml (planned for v2.1)
project_detection:
  # Directory level for project detection (current default: 2)
  level: 2
  
  # Example configurations for different organizational structures:
  
  # Standard structure: /Documents/Project/files
  # level: 2
  
  # Corporate structure: /Market/Industry/Company/Project/files  
  # level: 4
  
  # Temporal structure: /2025/Quarter/Project/files
  # level: 3
  
  # Flat structure: /Project/files
  # level: 1

# Auto-detection settings
auto_detection:
  enabled: true
  suggest_optimal_level: true
  min_projects_threshold: 2
  max_depth_scan: 6
```

## Command Line Overrides (Planned)

```bash
# Override AI provider
python3 docparser.py docs/ --ai-provider openai

# Override project detection level  
python3 docparser.py docs/ --project-level 3

# Use configuration file
python3 docparser.py docs/ --config custom_config.yaml

# Combined usage
python3 docparser.py docs/ --ai-provider gemini --project-level 4 --ai
```

## Environment Variable Support (Planned)

```bash
# AI Provider Selection
export DOCPARSER_AI_PROVIDER="openai"

# Project Detection Level
export DOCPARSER_PROJECT_LEVEL=3

# Configuration File Path
export DOCPARSER_CONFIG="/path/to/custom/config.yaml"

# API Keys (already supported)
export REPLICATE_API_TOKEN="your_token"
export OPENAI_API_KEY="your_key"
export ANTHROPIC_API_KEY="your_key"
export GEMINI_API_KEY="your_key"
```

## Migration from v2.0

Current v2.0 behavior will remain the default:
- Replicate as AI provider
- Level 2 project detection
- Environment variable configuration

Users can gradually adopt new configuration options without breaking existing workflows.

---

**Note**: This is a preview of planned v2.1 features. Current v2.0 does not support these configuration options yet.
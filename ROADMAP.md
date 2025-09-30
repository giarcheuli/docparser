# DocParser v2.1 - Feature Roadmap

## Planned Features for Next Release

### 1. Configurable AI Integration

**Feature**: Multi-provider AI configuration system

**Description**: 
Replace the current hard-coded Replicate integration with a flexible configuration system that supports multiple AI providers.

**Implementation Details**:
- **Configuration File**: `ai_config.yaml` or `ai_config.json`
- **Supported Providers**: 
  - Replicate (default) - API tokens
  - OpenAI - API keys  
  - Anthropic - API keys
  - Gemini - API keys
- **Default Behavior**: Replicate remains the default provider
- **Fallback Logic**: If primary provider fails, attempt secondary providers
- **Provider-Specific Parameters**: Model selection, temperature, max tokens, etc.

**Configuration Example**:
```yaml
ai_providers:
  default: replicate
  
  replicate:
    enabled: true
    api_token: ${REPLICATE_API_TOKEN}
    model: "meta/llama-2-7b-chat"
    max_tokens: 1000
    
  openai:
    enabled: false
    api_key: ${OPENAI_API_KEY}
    model: "gpt-3.5-turbo"
    max_tokens: 1000
    
  anthropic:
    enabled: false
    api_key: ${ANTHROPIC_API_KEY}
    model: "claude-3-haiku-20240307"
    max_tokens: 1000
    
  gemini:
    enabled: false
    api_key: ${GEMINI_API_KEY}
    model: "gemini-pro"
    max_tokens: 1000
```

**Benefits**:
- User choice in AI providers
- Better reliability with fallback options
- Provider-specific optimizations
- Easier testing and development

### 2. Configurable Project Detection Level

**Feature**: User-configurable project directory level detection

**Description**:
Allow users to specify which directory level should be considered as "projects" based on their specific directory structure needs.

**Implementation Details**:
- **Configuration Parameter**: `project_detection_level` (integer)
- **Default Value**: 2 (current behavior)
- **Range**: 1-6 (reasonable limits)
- **CLI Override**: `--project-level N` command line option

**Use Cases**:

1. **Level 3 Detection** (`/Market/Industry/Company/Project/`):
   ```
   Root/
   ├── TechMarket/           # Level 1
   │   ├── SaaS/             # Level 2  
   │   │   ├── CompanyA/     # Level 3
   │   │   │   ├── Project1/ # Level 4 ← PROJECT
   │   │   │   └── Project2/ # Level 4 ← PROJECT
   ```

2. **Level 4 Detection** (`/2025/Quarter/Company/Project/`):
   ```
   Root/
   ├── 2025/                 # Level 1
   │   ├── Q1/               # Level 2
   │   │   ├── ClientA/      # Level 3
   │   │   │   ├── Project1/ # Level 4 ← PROJECT
   │   │   │   └── Project2/ # Level 4 ← PROJECT
   ```

3. **Level 1 Detection** (Flat structure):
   ```
   Root/
   ├── Project1/             # Level 1 ← PROJECT
   ├── Project2/             # Level 1 ← PROJECT
   └── Project3/             # Level 1 ← PROJECT
   ```

**Configuration Options**:
- **Config File**: Add to main configuration
- **Environment Variable**: `DOCPARSER_PROJECT_LEVEL`
- **CLI Parameter**: `--project-level 3`
- **Auto-Detection**: Analyze directory structure and suggest optimal level

**Benefits**:
- Flexibility for different organizational structures
- Better project detection accuracy
- Supports various industry standards
- Maintains backward compatibility

## Implementation Priority

### Phase 1: Configurable Project Detection
- **Complexity**: Low-Medium
- **Impact**: High
- **Estimated Effort**: 1-2 weeks
- **Dependencies**: None

### Phase 2: Multi-Provider AI Integration
- **Complexity**: Medium-High  
- **Impact**: High
- **Estimated Effort**: 2-3 weeks
- **Dependencies**: Research provider APIs

## Technical Considerations

### Configuration Management
- **File Format**: YAML for human readability
- **Location**: `config/` directory or root level
- **Environment Variables**: Support for sensitive data
- **Validation**: Schema validation for configuration files
- **Backwards Compatibility**: Maintain existing behavior as defaults

### Testing Requirements
- **Unit Tests**: Configuration parsing and validation
- **Integration Tests**: Multi-provider AI functionality
- **Directory Structure Tests**: Various project level scenarios
- **Performance Tests**: Impact of configuration loading

### Documentation Updates
- **README**: Updated quick start with configuration options
- **USAGE**: Detailed configuration examples
- **Configuration Guide**: Dedicated configuration documentation
- **Migration Guide**: For users upgrading from v2.0

## Future Considerations

### Beyond v2.1
- **Custom Project Patterns**: Regex-based project detection
- **AI Provider Rotation**: Load balancing between providers
- **Configuration UI**: Web-based configuration interface
- **Template System**: Pre-defined configurations for common structures
- **Smart Detection**: Machine learning-based project boundary detection

---

**Created**: October 1, 2025  
**Target Release**: v2.1.0  
**Status**: Planning Phase
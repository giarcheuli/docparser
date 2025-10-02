# DocParser v2.0 - Project Specifications

## 🎯 Project Overview

# DocGuru v2.0 - Project Specifications

**Document Analysis Tool for macOS with Project-Aware Intelligence**

**DocGuru v2.0** is a **Project-Aware Document Analysis Tool** designed for intelligent analysis of multi-project directory structures with AI-powered insights.

### Core Mission
Transform complex document repositories into structured, actionable intelligence through project-aware analysis and AI-enhanced reporting.

## 📋 Current Specifications

### **Version**: 2.0.0
### **Platform**: macOS (Python 3.8+)
### **Architecture**: CLI-based with modular design
### **AI Integration**: Replicate API (Meta Llama-2-7b-chat)

## 🏗️ Architecture Overview

### **Core Components**

1. **Entry Point**: `docguru.py` - Main CLI application
2. **Core Engine**: 
   - `src/core/scanner.py` - Project-aware directory scanning
   - `src/core/analyzer.py` - Analysis orchestration
3. **File Analyzers**: 
   - 6 specialized analyzers for different file types
4. **AI Integration**: 
   - `src/utils/ai_analyzer.py` - Replicate API integration
5. **Report Generation**: 
   - `src/utils/project_report_generator.py` - Session-based reporting

### **Codebase Statistics**
- **Total Lines**: 2,238 lines of Python code
- **Modules**: 15 Python files
- **Test Coverage**: Basic unit tests included

## 🗂️ Project Detection Logic

### **Level-2 Directory Detection**
```
Root_Directory/                    # Level 1
├── Project_A/                     # Level 2 ← DETECTED AS PROJECT
│   ├── subfolder1/                # Level 3 (part of Project_A)
│   └── file.doc                   # Level 3 (part of Project_A)
├── Project_B/                     # Level 2 ← DETECTED AS PROJECT
│   └── docs/                      # Level 3 (part of Project_B)
└── standalone.pdf                 # Level 1 (not in project)
```

### **Project Context Features**
- **Hierarchical Analysis**: Documents analyzed within project context
- **Cross-Project Relationships**: Identifies patterns across projects
- **Project-Level AI Insights**: Context-aware analysis per project

## 📊 Report Generation System

### **4 Report Types**

1. **Comprehensive Report**
   - File: `{dir}_COMPREHENSIVE_AI_{timestamp}.md`
   - Content: Complete analysis organized by project
   - AI Insights: Full document and project analysis

2. **Overview Report**
   - File: `{dir}_OVERVIEW_AI_{timestamp}.md`
   - Content: Executive summary across all projects
   - AI Insights: Strategic overview and recommendations

3. **Individual Project Reports**
   - Files: `{dir}_{project}_PROJECT_{timestamp}.md`
   - Content: Dedicated analysis per project
   - AI Insights: Project-specific context and recommendations

4. **Cross-Project Analysis**
   - File: `{dir}_CROSS_PROJECT_ANALYSIS_{timestamp}.md`
   - Content: Inter-project relationships and patterns
   - AI Insights: Organizational-level insights

### **Session Management**
- **Location**: `Reports/{directory}_{dd}_{mm}_{yy}_{hh}_{mm}/`
- **Preservation**: All sessions preserved for historical comparison
- **Organization**: Timestamped folders prevent overwrites

## 🤖 AI Integration Specifications

### **Provider**: Replicate
### **Model**: Meta Llama-2-7b-chat
### **API Token**: `REPLICATE_API_TOKEN` environment variable

### **AI Analysis Capabilities**
1. **Document-Level Analysis**:
   - Content summarization
   - Theme identification
   - Insight extraction

2. **Project-Level Analysis**:
   - Project purpose assessment
   - Documentation quality evaluation
   - Strategic recommendations

3. **Cross-Project Analysis**:
   - Pattern identification
   - Relationship mapping
   - Organizational insights

## 📂 File Format Support

### **Supported Formats** (6 categories)
| Category | Extensions | Analyzer Module |
|----------|------------|-----------------|
| **Word Documents** | `.doc`, `.docx` | `word_analyzer.py` |
| **PDF Files** | `.pdf` | `pdf_analyzer.py` |
| **Text Files** | `.txt`, `.md`, `.markdown` | `text_analyzer.py` |
| **HTML Files** | `.html`, `.htm` | `html_analyzer.py` |
| **Excel Files** | `.xlsx`, `.xls` | `excel_analyzer.py` |
| **XML Files** | `.xml` | `xml_analyzer.py` |

### **Analysis Features Per Type**
- **Metadata Extraction**: File properties, creation dates, sizes
- **Content Extraction**: Text content, structure analysis
- **AI Analysis**: Content summaries and insights (when enabled)

## ⚙️ Technical Specifications

### **System Requirements**
- **OS**: macOS 10.14 or later
- **Python**: 3.8 or higher
- **Memory**: Optimized for streaming (minimal memory footprint)
- **Storage**: Generates reports in session folders

### **Dependencies** (requirements.txt)
- Core document processing libraries
- AI integration (replicate)
- File format handlers
- Logging and utilities

### **Performance Characteristics**
- **Small Projects** (< 50 files): 30-60 seconds with AI
- **Medium Projects** (50-200 files): 2-5 minutes with AI
- **Large Projects** (200+ files): 5-15 minutes with AI
- **Memory Usage**: Streaming processing, minimal memory footprint

## 🔧 Configuration Options

### **Command Line Interface**
```bash
python3 docguru.py <directory> [options]
```

### **Available Options**
| Option | Description | Default |
|--------|-------------|---------|
| `--ai` | Enable AI analysis | Disabled |
| `--verbose` | Detailed logging | Basic logging |
| `--analysis-mode` | Qualitative/Quantitative | Qualitative |
| `--no-summary` | Skip final summary | Show summary |
| `--list-only` | List files only | Full analysis |

### **Environment Variables**
- `REPLICATE_API_TOKEN`: Required for AI analysis
- Logging automatically to `docguru.log`

## 🧪 Testing & Quality Assurance

### **Test Suite**: `tests/test_basic.py`
- **Import Tests**: Verify all modules load correctly
- **Component Tests**: Basic functionality validation
- **Integration Tests**: End-to-end testing capability

### **Quality Metrics**
- ✅ All imports functional
- ✅ File analyzers operational
- ✅ AI integration working
- ✅ Report generation functional
- ✅ Error handling implemented

## 🔄 Development Workflow

### **Code Organization**
```
docguru/
├── docguru.py                   # CLI entry point
├── src/
│   ├── core/                      # Core logic
│   ├── analyzers/                 # File processors
│   └── utils/                     # AI & reporting
├── tests/                         # Test suite
├── README.md                      # Documentation
├── USAGE.md                       # User guide
└── requirements.txt               # Dependencies
```

### **Modular Design Principles**
- **Separation of Concerns**: Each module has single responsibility
- **Extensibility**: Easy to add new file types or AI providers
- **Error Resilience**: Graceful handling of failures
- **Logging**: Comprehensive debugging information

## 📈 Successful Implementation Examples

### **Real-World Test Case**: NBT_Confluence Analysis
- **Input**: 109 documents across 3 projects
- **Processing Time**: 234.2 seconds
- **Output**: 6 comprehensive reports with AI insights
- **Projects Detected**: Player Portal (28 files), Flutter Apps (32 files), Credit Platform (48 files)
- **AI Analysis**: Full content summaries and project insights

## 🚀 Production Readiness

### **Repository Status**: GitHub Ready ✅
- **Cleaned Codebase**: Removed all redundant files
- **Documentation**: Complete README and USAGE guides
- **Test Suite**: Basic functionality validated
- **Git Configuration**: Proper .gitignore in place
- **No Sensitive Data**: API keys externalized

### **Deployment Checklist**
- [x] Code cleanup completed
- [x] Documentation updated
- [x] Tests passing
- [x] .gitignore configured
- [x] Session folder management working
- [x] AI integration tested
- [x] Performance validated

## 🎯 Current Capabilities Summary

**DocGuru v2.0** successfully provides:

1. **Project-Aware Intelligence**: Automatically detects and analyzes projects within directory structures
2. **AI-Enhanced Insights**: Leverages Meta Llama-2-7b-chat for content analysis and strategic insights
3. **Comprehensive Reporting**: Generates 4 types of reports with session-based organization
4. **Multi-Format Support**: Handles 6 different document formats with specialized analyzers
5. **Production Reliability**: Error handling, logging, and performance optimization
6. **User-Friendly CLI**: Intuitive command-line interface with helpful options
7. **Session Management**: Organized output with historical preservation

## 🗺️ Future Development Roadmap

### **Version 2.1 Planned Features**

#### **1. Configurable AI Integration**
- **Multi-Provider Support**: Replicate, OpenAI, Anthropic, Gemini
- **YAML Configuration**: Flexible provider selection and parameters
- **Fallback Logic**: Automatic provider switching on failure
- **Backward Compatibility**: Replicate remains default

#### **2. Configurable Project Detection**
- **Variable Directory Levels**: User-defined project detection depth
- **Complex Structures**: Support for `/Market/Industry/Company/Project/` patterns
- **CLI Overrides**: Command-line project level specification
- **Auto-Detection**: Smart suggestions for optimal detection level

### **Long-term Vision**
- JSON output formats for programmatic integration
- Batch processing for multiple directory analysis
- Docker containerization for deployment flexibility
- Custom analysis templates and workflow support

**Detailed specifications available in [ROADMAP.md](ROADMAP.md)**

The tool is **production-ready** for deployment to GitHub and immediate use in real-world document analysis scenarios.

---

**Generated**: September 30, 2025  
**Updated**: October 1, 2025  
**Version**: 2.0.0  
**Status**: Production Ready ✅  
**Next Release**: v2.1.0 (Planned)
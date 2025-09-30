# DocParser v2.0 - Project-Aware Document Analysis Tool

A comprehensive command-line document analysis tool for macOS that provides **project-aware analysis** of directories containing various document formats and generates structured markdown reports with AI-powered insights.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![CLI](https://img.shields.io/badge/interface-CLI-orange.svg)

## ✨ Key Features

### �️ **Project-Aware Analysis**
- **Automatic Project Detection**: Identifies projects based on level-2 directory structure
- **Hierarchical Organization**: Understands document relationships within project contexts
- **Cross-Project Analysis**: Identifies patterns and relationships between projects

### 📊 **Comprehensive Reporting**
- **4 Report Types**: Comprehensive, Overview, Individual Project, and Cross-Project Analysis
- **Session-Based Organization**: Reports saved in timestamped session folders
- **Structured Output**: `Reports/{directory}_{timestamp}/` organization

### 🤖 **AI Integration**
- **Replicate API**: Integration with Meta Llama-2-7b-chat model
- **Content Summarization**: AI-powered document insights and analysis
- **Project Context**: AI analysis considers project hierarchy and relationships

### 📂 **Multi-Format Support**
- **Documents**: DOC, DOCX, PDF, TXT, HTML, Markdown
- **Spreadsheets**: XLSX, XLS  
- **Structured Data**: XML files
- **Metadata Extraction**: Comprehensive file analysis

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/giarcheuli/docparser.git
cd docparser

# Install dependencies
pip3 install -r requirements.txt

# Set up AI integration (optional)
export REPLICATE_API_TOKEN="your-replicate-api-key"

# Run analysis
python3 docparser.py /path/to/documents --ai
```

### Basic Usage

```bash
# Analyze a directory with project detection
python3 docparser.py documents/

# With AI-powered insights
python3 docparser.py documents/ --ai

# Verbose output for debugging
python3 docparser.py documents/ --verbose

# Just list supported files
python3 docparser.py documents/ --list-only
```

## 📋 Project Structure & Specifications

### **Project Detection Logic**
DocParser v2.0 uses **level-2 directory detection** for project identification:

```
Documents/
├── Project_A/           # ← Level 2: Detected as Project
│   ├── subfolder1/      # ← Level 3: Part of Project_A
│   └── subfolder2/      # ← Level 3: Part of Project_A
├── Project_B/           # ← Level 2: Detected as Project
│   └── docs/            # ← Level 3: Part of Project_B
└── standalone_file.pdf  # ← Level 1: Not in a project
```

### **Report Types Generated**

1. **Comprehensive Report**: Full analysis of all documents organized by project
2. **Overview Report**: Executive summary across all projects 
3. **Individual Project Reports**: Dedicated analysis for each detected project
4. **Cross-Project Analysis**: Relationships and patterns between projects

### **Session Organization**
```
Reports/
└── {directory_name}_{dd}_{mm}_{yy}_{hh}_{mm}/
    ├── {dir}_COMPREHENSIVE_AI_{timestamp}.md
    ├── {dir}_OVERVIEW_AI_{timestamp}.md  
    ├── {dir}_{project1}_PROJECT_{timestamp}.md
    ├── {dir}_{project2}_PROJECT_{timestamp}.md
    └── {dir}_CROSS_PROJECT_ANALYSIS_{timestamp}.md
```

## 💻 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- macOS 10.14 or later

### Quick Setup
```bash
# Clone repository
git clone https://github.com/giarcheuli/docparser.git
cd docparser

# Install dependencies
pip3 install -r requirements.txt

# Test installation
python3 docparser.py --help
```

### AI Integration Setup
To enable AI-powered analysis with Replicate:

```bash
# Set up Replicate API token
export REPLICATE_API_TOKEN="your-replicate-api-key"

# Verify setup
python3 docparser.py documents/ --ai --verbose
```

**Note**: DocParser v2.0 uses Replicate's Meta Llama-2-7b-chat model for AI analysis.

## 📖 Usage Examples

### Basic Project Analysis
```bash
# Analyze directory with project detection
python3 docparser.py ~/Documents/Projects

# Generate all 4 report types
python3 docparser.py ~/Technical_Documentation --ai

# Verbose output for troubleshooting
python3 docparser.py ~/Documents --verbose
```

### Real-World Examples
```bash
# Analyze Confluence export with AI insights
python3 docparser.py ~/Confluence_Export --ai

# Quick project overview without AI
python3 docparser.py ~/Client_Projects --no-summary

# List files in complex directory structure
python3 docparser.py ~/Multi_Project_Folder --list-only
```

### Command Line Options
```
usage: docparser.py [-h] [--ai] [--verbose] [--analysis-mode {qualitative,quantitative}] 
                    [--no-summary] [--list-only] directory

DocParser v2.0 - Project-Aware Document Analysis Tool

positional arguments:
  directory             Directory to analyze (required)

optional arguments:
  -h, --help            show this help message and exit
  --ai                  Enable AI-powered analysis and insights
  --verbose, -v         Enable verbose logging  
  --analysis-mode       Analysis approach: qualitative (insights) or quantitative (metrics)
  --no-summary          Skip showing the summary at the end
  --list-only           Only list supported files, don't analyze

Examples:
  docparser.py documents/                     # Project-aware analysis
  docparser.py documents/ --ai               # With AI insights
  docparser.py documents/ --verbose          # Verbose logging
```

### Supported File Types

| Format | Extensions | Features |
|--------|------------|----------|
| **Word Documents** | `.doc`, `.docx` | Text extraction, metadata, styles, tables |
| **PDF Files** | `.pdf` | Text extraction, page count, document properties |
| **Text Files** | `.txt`, `.md`, `.markdown` | Content analysis, encoding detection |
| **HTML Files** | `.html`, `.htm` | Text extraction, meta tags, links, images |
| **Excel Files** | `.xlsx`, `.xls` | Sheet analysis, data preview, metadata |
| **XML Files** | `.xml` | Structure analysis, namespaces, element counts |

### Sample Report Structure

Generated reports include:

#### **Comprehensive Report**
- **Project Overview**: All detected projects with file counts and structure
- **Document Analysis**: Detailed file-by-file analysis organized by project
- **AI Insights**: Project-level summaries and cross-project patterns
- **Statistics**: File types, sizes, and distribution metrics

#### **Overview Report**  
- **Executive Summary**: High-level analysis across all projects
- **Project Comparison**: Relative project sizes and characteristics
- **Key Findings**: Important insights and recommendations

#### **Individual Project Reports**
- **Project-Specific Analysis**: Deep dive into each detected project
- **Document Breakdown**: All files within the project context
- **Project Insights**: AI analysis specific to project content

#### **Cross-Project Analysis**
- **Relationship Analysis**: Common themes and patterns
- **Comparative Insights**: Differences and similarities between projects
- **Strategic Recommendations**: High-level organizational insights

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `REPLICATE_API_TOKEN` | Replicate API token for Meta Llama-2-7b-chat | Optional (for AI features) |

### Logging

The application automatically generates logs in `docparser.log` with:
- Project detection and analysis progress
- AI API interactions and responses  
- Error details and troubleshooting information
- File processing status and timing

## 🏗️ Architecture

```
docparser/
├── docparser.py                   # Main CLI application entry point
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore patterns
├── src/                          # Source code modules
│   ├── core/                     # Core analysis logic
│   │   ├── scanner.py            # Project-aware directory scanning
│   │   └── analyzer.py           # Main analysis orchestrator
│   ├── analyzers/                # File-specific analyzers
│   │   ├── text_analyzer.py      # Text and markdown files
│   │   ├── pdf_analyzer.py       # PDF documents
│   │   ├── word_analyzer.py      # Word documents (.doc/.docx)
│   │   ├── excel_analyzer.py     # Excel spreadsheets
│   │   ├── html_analyzer.py      # HTML files
│   │   └── xml_analyzer.py       # XML files
│   └── utils/                    # Utility modules
│       ├── ai_analyzer.py        # AI integration (Replicate/Llama)
│       └── project_report_generator.py # Session-based report generation
├── tests/                        # Unit tests
│   └── test_basic.py             # Basic functionality tests
└── Reports/                      # Generated session reports (auto-created)
    └── {session_folders}/        # Timestamped analysis sessions
```

## 🚀 Performance

DocParser v2.0 is optimized for project-aware analysis with:
- **Efficient Project Detection**: Fast hierarchy scanning and project identification
- **Memory Management**: Streaming content processing for large files
- **Concurrent Processing**: Parallel AI analysis where possible
- **Error Resilience**: Graceful handling of corrupted or inaccessible files

### Typical Performance

| Directory Size | File Count | Processing Time | Notes |
|----------------|------------|-----------------|--------|
| **Small Projects** | < 50 files | 10-30 seconds | Without AI analysis |
| **Medium Projects** | 50-200 files | 1-3 minutes | With basic AI analysis |  
| **Large Projects** | 200+ files | 3-10 minutes | Full AI analysis with all report types |

*Performance varies based on file sizes, complexity, and AI analysis depth*

### AI Analysis Performance
- **Document Analysis**: ~1-2 seconds per document
- **Project Analysis**: ~3-5 seconds per project  
- **Cross-Project Analysis**: ~5-10 seconds for final report
- **Total AI Overhead**: +2-5 minutes for comprehensive AI insights

## 🔧 Troubleshooting

### Common Issues

1. **"No projects detected" warning**
   ```bash
   # Ensure your directory has level-2 subdirectories
   Documents/
   ├── Project1/     # ← Level 2: Will be detected
   │   └── files...
   └── Project2/     # ← Level 2: Will be detected
       └── files...
   ```

2. **AI analysis fails**
   ```bash
   # Check API token
   echo $REPLICATE_API_TOKEN
   
   # Test with verbose logging
   python3 docparser.py documents/ --ai --verbose
   ```

3. **"No module named" errors**
   ```bash
   # Reinstall dependencies
   pip3 install -r requirements.txt
   ```

4. **Session folder creation fails**
   ```bash
   # Check write permissions in project directory
   ls -la Reports/
   chmod 755 Reports/
   ```

### Debug Mode

Enable comprehensive logging:
```bash
python3 docparser.py /path/to/docs --verbose
```

Check session logs:
```bash
tail -f docparser.log
```

## 🛠️ Development

### Setting up for Development

```bash
# Clone repository
git clone https://github.com/giarcheuli/docparser.git
cd docparser

# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 tests/test_basic.py

# Test with real data (need to create test directory)
mkdir test_data && python3 docparser.py test_data/ --verbose
```

### Adding New File Types

1. Create new analyzer in `src/analyzers/`
2. Inherit from appropriate base class
3. Implement `extract_text()` and `extract_metadata()` methods
4. Add file extension to `SUPPORTED_EXTENSIONS` in `core/scanner.py`
5. Register analyzer in `core/analyzer.py`

### Project Structure Guidelines

- **Level-2 Detection**: Projects are identified at 2 levels deep from root
- **Session Management**: All reports go to timestamped session folders
- **AI Integration**: Use project context for enhanced analysis
- **Error Handling**: Graceful degradation when AI/analysis fails

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with proper testing
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Contributing Guidelines

- Follow Python PEP 8 style guidelines
- Add tests for new functionality
- Update documentation for new features
- Ensure project-aware analysis remains intact
- Test with both AI and non-AI modes

## 📞 Support

For issues, questions, or contributions:

1. **Check Issues**: Search existing GitHub issues
2. **Create Issue**: Include logs, system info, and reproduction steps
3. **Debug Mode**: Use `--verbose` flag for detailed logs
4. **Documentation**: Check this README and code comments

## 🗺️ Roadmap

### Planned Features (v2.1)
- [ ] **Configurable AI Integration**: Multi-provider support (Replicate, OpenAI, Anthropic, Gemini)
- [ ] **Configurable Project Detection**: User-defined directory level for project identification
- [ ] **JSON Output Format**: Alternative to markdown reports
- [ ] **Batch Processing**: Multiple directory analysis
- [ ] **Custom Templates**: User-defined report formats
- [ ] **Watch Mode**: Monitor directories for changes
- [ ] **Docker Support**: Containerized deployment
- [ ] **Cloud Storage**: Direct integration with cloud services

### AI Enhancements
- [ ] **Multi-Provider Configuration**: Flexible AI provider selection with fallback support
- [ ] **Custom Prompts**: User-defined analysis templates
- [ ] **Workflow Analysis**: Document process understanding
- [ ] **Sentiment Analysis**: Document tone and sentiment

**See [ROADMAP.md](ROADMAP.md) for detailed feature specifications and implementation plans.**

---

**DocParser v2.0** - Built with ❤️ for intelligent, project-aware document analysis
# DocParser v2.0 - Usage Guide# DocParser v2.0 - Usage Guide



## Project-Aware Document Analysis Tool## Project-Aware Document Analysis Tool



DocParser v2.0 is designed for **intelligent, project-aware analysis** of directory structures containing multiple projects and document types.DocParser v2.0 is designed for **intelligent, project-aware analysis** of directory structures containing multiple projects and document types.



## 🗂️ Project Detection## 🗂️ Project Detection



### How Projects Are Identified### How Projects Are Identified



DocParser uses **level-2 directory detection**:DocParser uses **level-2 directory detection**:



``````

Root_Directory/Root_Directory/

├── Project_Alpha/          # ← Level 2: Detected as Project├── Project_Alpha/          # ← Level 2: Detected as Project

│   ├── docs/               # ← Level 3: Part of Project_Alpha  │   ├── docs/               # ← Level 3: Part of Project_Alpha  

│   ├── requirements/       # ← Level 3: Part of Project_Alpha│   ├── requirements/       # ← Level 3: Part of Project_Alpha

│   └── specs.pdf          # ← Level 3: Part of Project_Alpha│   └── specs.pdf          # ← Level 3: Part of Project_Alpha

├── Project_Beta/           # ← Level 2: Detected as Project├── Project_Beta/           # ← Level 2: Detected as Project

│   ├── design/             # ← Level 3: Part of Project_Beta│   ├── design/             # ← Level 3: Part of Project_Beta

│   └── implementation/     # ← Level 3: Part of Project_Beta│   └── implementation/     # ← Level 3: Part of Project_Beta

└── standalone.doc         # ← Level 1: Individual file (no project)└── standalone.doc         # ← Level 1: Individual file (no project)

``````



### Project Structure Examples## 🚀 Quick Start



**✅ Good Project Structure:**### 1. Install Dependencies

``````bash

Technical_Documentation/pip3 install -r requirements.txt

├── Player_Portal/          # Project 1```

│   ├── scrum/

│   ├── requirements/### 2. Set Up AI Integration (Optional)

│   └── planning/```bash

├── Flutter_Apps/           # Project 2  export REPLICATE_API_TOKEN="your-replicate-api-key"

│   ├── native_development/```

│   └── testing/

└── Credit_Platform/        # Project 3### 3. Run Analysis

    ├── architecture/```bash

    └── services/# Project-aware analysis

```python3 docparser.py /path/to/documents



**❌ Flat Structure (No Projects Detected):**# With AI insights

```python3 docparser.py /path/to/documents --ai

Documents/```

├── file1.doc

├── file2.pdf```bash

└── file3.xlsx# Analyze a directory

```python3 docparser.py ~/Documents



## 🚀 Quick Start# Analyze with AI insights (requires API key)

python3 docparser.py ~/Documents --ai

### 1. Install Dependencies

```bash# Custom output file

pip3 install -r requirements.txtpython3 docparser.py ~/Documents -o my_analysis.md

```

# Verbose output for debugging

### 2. Set Up AI Integration (Optional)python3 docparser.py ~/Documents --verbose

```bash

export REPLICATE_API_TOKEN="your-replicate-api-key"# Just list supported files without analysis

```python3 docparser.py ~/Documents --list-only

```

### 3. Run Analysis

```bash### Advanced Options

# Project-aware analysis

python3 docparser.py /path/to/documents```bash

# Skip the summary display

# With AI insightspython3 docparser.py ~/Documents --no-summary

python3 docparser.py /path/to/documents --ai

```# Future: JSON output format

python3 docparser.py ~/Documents --format json

## 📊 Report Types Generated

# Get help

### 1. Comprehensive Reportpython3 docparser.py --help

**File**: `{directory}_COMPREHENSIVE_AI_{timestamp}.md````



Complete analysis of all documents organized by project:## Supported File Types

- Project overview with file counts

- Document-by-document analysisThe CLI version analyzes the same file formats:

- AI insights for each file

- Cross-references and patterns| Format | Extensions | Analysis Features |

|--------|------------|-------------------|

### 2. Overview Report  | **Word Documents** | `.doc`, `.docx` | Text extraction, metadata, document properties |

**File**: `{directory}_OVERVIEW_AI_{timestamp}.md`| **PDF Files** | `.pdf` | Text extraction, page count, document info |

| **Text Files** | `.txt`, `.md`, `.markdown` | Full content analysis, encoding detection |

Executive summary across all projects:| **HTML Files** | `.html`, `.htm` | Text extraction, meta tags, links, images |

- High-level project comparison| **Excel Files** | `.xlsx`, `.xls` | Sheet analysis, data preview, workbook properties |

- Key statistics and metrics| **XML Files** | `.xml` | Structure analysis, element counts, namespaces |

- Strategic insights and recommendations

## AI Integration

### 3. Individual Project Reports

**Files**: `{directory}_{project_name}_PROJECT_{timestamp}.md`### Setting Up AI Analysis



Dedicated analysis for each detected project:Choose one of these providers:

- Project-specific document breakdown

- Context-aware AI analysis#### Google Gemini (Recommended - Free Tier)

- Project-level insights and recommendations```bash

export GEMINI_API_KEY="your-gemini-api-key"

### 4. Cross-Project Analysis```

**File**: `{directory}_CROSS_PROJECT_ANALYSIS_{timestamp}.md`- Get key from: https://aistudio.google.com/app/apikey

- Free tier: 15 requests/minute

Analysis of relationships between projects:

- Common themes and patterns#### OpenAI

- Inter-project dependencies```bash

- Organizational insightsexport OPENAI_API_KEY="your-openai-api-key"

```

## 🗂️ Session Organization- Get key from: https://platform.openai.com/api-keys

- Paid service

All reports are saved in timestamped session directories:

#### Anthropic

``````bash

Reports/export ANTHROPIC_API_KEY="your-anthropic-api-key"

└── NBT_Confluence_30_09_25_19_53/     # Session folder```

    ├── NBT_Confluence_COMPREHENSIVE_AI_19_53_30_09_25.md- Get key from: https://console.anthropic.com/

    ├── NBT_Confluence_OVERVIEW_AI_19_53_30_09_25.md- Paid service

    ├── NBT_Confluence_Player_Portal_PROJECT_19_53_30_09_25.md

    ├── NBT_Confluence_Flutter_Apps_PROJECT_19_53_30_09_25.md  ### Making API Keys Permanent

    ├── NBT_Confluence_Credit_Platform_PROJECT_19_53_30_09_25.md

    └── NBT_Confluence_CROSS_PROJECT_ANALYSIS_19_53_30_09_25.mdAdd to your shell profile (`~/.zshrc` or `~/.bash_profile`):

```

```bash

### Session Naming Convention# Add this line

`{directory_name}_{dd}_{mm}_{yy}_{hh}_{mm}/`export GEMINI_API_KEY="your-api-key-here"



Example: `NBT_Confluence_30_09_25_19_53/` means:# Reload the profile

- Directory: NBT_Confluencesource ~/.zshrc

- Date: September 30, 2025```

- Time: 19:53 (7:53 PM)

## Output and Reports

## 🤖 AI Integration

### Generated Report Structure

### Replicate API Setup

```markdown

DocParser v2.0 uses **Replicate's Meta Llama-2-7b-chat** model:# Document Analysis Report



```bash## Executive Summary

# Set API token- Total files processed

export REPLICATE_API_TOKEN="your-replicate-api-key"- Success/error counts  

- Key statistics

# Verify setup

echo $REPLICATE_API_TOKEN## Directory Overview

```- File type distribution

- Size analysis

### AI Analysis Features

## File Type Analysis

1. **Document Summaries**: AI-generated content summaries- Detailed analysis by format

2. **Project Analysis**: Context-aware project insights  - Word counts and statistics

3. **Cross-Project Patterns**: Relationship identification

4. **Strategic Insights**: High-level recommendations## Detailed File Analysis

- Individual file information

### AI vs Non-AI Mode- Content previews

- Metadata extraction

**With AI (`--ai` flag):**- AI summaries (if enabled)

- Rich content summaries

- Project-level strategic insights## Analysis Performance

- Cross-project pattern analysis- Processing time

- Enhanced recommendations- Technical details

```

**Without AI:**

- Basic metadata extraction### Sample Output

- File structure analysis

- Statistical summaries```

- Technical document properties============================================================

📄 DocParser v2.0 - CLI Edition

## 📖 Command Usage🔍 Comprehensive Document Analysis Tool

============================================================

### Basic Commands📁 Directory: /Users/username/Documents

🤖 AI Analysis: Enabled

```bash📄 Output: docparser_report.md

# Project-aware analysis (basic)📊 Format: markdown

python3 docparser.py /path/to/documents------------------------------------------------------------

📊 Scanning directory for supported files...

# Project-aware analysis with AI insights  ✅ Analysis complete in 2.3s

python3 docparser.py /path/to/documents --ai📈 Results: 15 successful, 0 failed

📝 Generating comprehensive report...

# Verbose logging for troubleshooting✅ Report saved to: docparser_report.md

python3 docparser.py /path/to/documents --verbose

📋 Analysis Summary:

# List files without analysis   ⏱️  Time taken: 2.3 seconds

python3 docparser.py /path/to/documents --list-only   📁 Total files: 15

```   📏 Total size: 2.1 MB



### Real-World Examples📊 File Types:

   .PDF: 8 files

```bash   .DOCX: 4 files

# Analyze Confluence export   .TXT: 2 files

python3 docparser.py ~/Downloads/Confluence_Export --ai   .MD: 1 files



# Analyze client project folders📈 Largest Files:

python3 docparser.py ~/Projects/Client_Work --ai --verbose   1. presentation.pdf (1.2 MB)

   2. manual.docx (456.7 KB)

# Quick overview of downloads folder   3. notes.txt (23.4 KB)

python3 docparser.py ~/Downloads --list-only

🎉 Analysis complete! Check 'docparser_report.md' for full details.

# Analyze without AI (faster)```

python3 docparser.py ~/Large_Document_Set --no-summary

```## Real-World Usage Examples



### Command Line Options### Document Organization

```bash

| Option | Description | Example |# Analyze your downloads folder

|--------|-------------|---------|python3 docparser.py ~/Downloads --list-only

| `directory` | Target directory (required) | `/path/to/docs` |

| `--ai` | Enable AI analysis | `--ai` |# Full analysis of project docs

| `--verbose` | Detailed logging | `--verbose` |python3 docparser.py ./project-docs --ai -o project-summary.md

| `--analysis-mode` | Analysis type | `--analysis-mode qualitative` |```

| `--no-summary` | Skip final summary | `--no-summary` |

| `--list-only` | List files only | `--list-only` |### Content Audit

```bash

## 📈 Performance Guidelines# Audit important documents with AI insights

python3 docparser.py ~/Important-Files --ai --verbose

### Optimal Performance

# Quick overview without detailed analysis

**Small Projects (< 50 files):**python3 docparser.py ~/Research --list-only

- Time: 30-60 seconds with AI```

- Recommendation: Use `--ai` for full insights

### Batch Processing

**Medium Projects (50-200 files):**  ```bash

- Time: 2-5 minutes with AI# Process multiple directories (using shell)

- Recommendation: Use `--verbose` for progress trackingfor dir in ~/Documents/*/; do

    python3 docparser.py "$dir" -o "analysis-$(basename "$dir").md"

**Large Projects (200+ files):**done

- Time: 5-15 minutes with AI  ```

- Recommendation: Consider running without AI first, then with AI if needed

## Troubleshooting

### Performance Tips

### Common Issues

1. **Directory Organization**: Ensure clear level-2 project structure

2. **File Accessibility**: Check file permissions before analysis**Command not found**

3. **AI Usage**: Use AI selectively for important document sets```bash

4. **Session Management**: Old sessions are preserved for comparison# Make sure you're in the right directory

cd /path/to/docparser

## 🔍 Supported File Typespython3 docparser.py --help

```

| Category | Extensions | AI Analysis |

|----------|------------|-------------|**No files found**

| **Documents** | `.doc`, `.docx` | ✅ Full content analysis |```bash

| **PDFs** | `.pdf` | ✅ Text extraction + analysis |# Check if directory exists and has supported files

| **Text Files** | `.txt`, `.md`, `.markdown` | ✅ Content + structure analysis |python3 docparser.py /path/to/docs --list-only

| **Web Files** | `.html`, `.htm` | ✅ Content extraction + analysis |```

| **Spreadsheets** | `.xlsx`, `.xls` | ✅ Data preview + insights |

| **Structured Data** | `.xml` | ✅ Structure + content analysis |**AI not working**

```bash

## 🚨 Troubleshooting# Check if API key is set

echo $GEMINI_API_KEY

### Common Issues

# Test without AI first

**"No projects detected"**python3 docparser.py /path/to/docs

```bash```

# Check directory structure - need level-2 folders

ls -la /path/to/directory**Permission errors**

``````bash

# Check file permissions

**"AI analysis failed"**  ls -la /path/to/directory

```bash

# Verify API token# Use absolute paths

echo $REPLICATE_API_TOKENpython3 docparser.py /Users/username/Documents

```

# Test with verbose logging

python3 docparser.py docs/ --ai --verbose### Debug Mode

```

For detailed troubleshooting:

**"Permission denied"**```bash

```bash# Enable verbose logging

# Check file permissionspython3 docparser.py ~/Documents --verbose

ls -la /path/to/directory

# Check the log file

# Fix if neededcat docparser.log

chmod -R 755 /path/to/directory```

```

## Performance Tips

### Debug Mode

### For Large Directories

For detailed troubleshooting:- Use `--list-only` first to see what will be processed

```bash- Disable AI analysis (`--no-ai`) for faster processing

# Enable comprehensive logging- Use `--no-summary` to skip summary display

python3 docparser.py /path/to/docs --verbose- Process subdirectories separately for better control



# Check log file### For Better Accuracy

tail -f docparser.log- Ensure files are not corrupted or password-protected

```- Use latest file formats when possible (.docx vs .doc)

- Check file permissions before analysis

## 💡 Best Practices

## Integration Examples

### Directory Preparation

1. **Organize by Project**: Use clear level-2 directory structure### With Other Tools

2. **Consistent Naming**: Use descriptive project folder names

3. **File Accessibility**: Ensure read permissions on all files```bash

# Count words across all documents

### Analysis Strategy  python3 docparser.py ~/docs --verbose | grep "word_count"

1. **Start Basic**: Run without AI first for large directories

2. **Use AI Selectively**: Enable AI for important document sets# Find largest files

3. **Review Sessions**: Compare multiple analysis sessions over timepython3 docparser.py ~/docs --list-only | sort -k3 -nr



### Report Management# Export to different location

1. **Session Organization**: Each analysis creates a new session folderpython3 docparser.py ~/docs -o ~/analysis-reports/latest.md

2. **Comparison**: Use different sessions to track document changes```

3. **Archival**: Sessions are preserved for historical analysis

### Automation

---

```bash

**DocParser v2.0** provides intelligent, project-aware document analysis for modern multi-project environments.# Create a daily analysis script
#!/bin/bash
DATE=$(date +%Y%m%d)
python3 docparser.py ~/Documents --ai -o ~/reports/daily-$DATE.md
```

## Support

- Use `--verbose` for detailed logs
- Check `docparser.log` for error details
- Ensure all dependencies are installed
- Verify API keys if using AI features

For more help: `python3 docparser.py --help`
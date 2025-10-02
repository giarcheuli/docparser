"""
Project-aware Report Generator - Creates comprehensive reports with project structure awareness
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Import with fallback for direct execution
try:
    from ..core.analyzer import AnalysisResult
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from core.analyzer import AnalysisResult

class ProjectReportGenerator:
    """Generates project-aware comprehensive and summary reports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session_dir = None
        
    def _get_session_directory(self, directory_path: str) -> Path:
        """Get or create session directory for this analysis run"""
        if self.session_dir is None:
            # Generate session directory name: root_dd_mm_yy_hh_mm
            root_name = Path(directory_path).name
            timestamp = datetime.now().strftime("%d_%m_%y_%H_%M")
            session_name = f"{root_name}_{timestamp}"
            
            # Create session directory under Reports
            reports_base = Path("Reports")
            reports_base.mkdir(exist_ok=True)
            
            self.session_dir = reports_base / session_name
            self.session_dir.mkdir(exist_ok=True)
            
            self.logger.info(f"Created session directory: {self.session_dir}")
        
        return self.session_dir
        
    def generate_comprehensive_report(self, results: List[AnalysisResult], 
                                    directory_path: str, projects: Dict,
                                    project_stats: Dict, analysis_mode: str = "comprehensive") -> str:
        """Generate comprehensive report organized by projects"""
        
        # Get root directory name for report naming
        root_name = Path(directory_path).name
        timestamp = datetime.now().strftime("%H_%M_%d_%m_%y")
        
        # Get session directory
        session_dir = self._get_session_directory(directory_path)
        
        # Generate filename
        filename = f"{root_name}_COMPREHENSIVE_AI_{timestamp}.md"
        filepath = session_dir / filename
        
        # Generate report content
        content = self._generate_comprehensive_content(
            results, directory_path, projects, project_stats, analysis_mode
        )
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Comprehensive report saved to: {filepath}")
        return str(filepath)
    
    def generate_overview_report(self, results: List[AnalysisResult], 
                               directory_path: str, projects: Dict,
                               project_stats: Dict) -> str:
        """Generate overview summary report"""
        
        root_name = Path(directory_path).name
        timestamp = datetime.now().strftime("%H_%M_%d_%m_%y")
        
        # Get session directory
        session_dir = self._get_session_directory(directory_path)
        
        filename = f"{root_name}_OVERVIEW_AI_{timestamp}.md"
        filepath = session_dir / filename
        
        content = self._generate_overview_content(
            results, directory_path, projects, project_stats
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Overview report saved to: {filepath}")
        return str(filepath)
    
    def generate_project_reports(self, results: List[AnalysisResult], 
                               directory_path: str, projects: Dict,
                               project_stats: Dict) -> List[str]:
        """Generate individual project reports"""
        
        root_name = Path(directory_path).name
        timestamp = datetime.now().strftime("%H_%M_%d_%m_%y")
        
        # Get session directory
        session_dir = self._get_session_directory(directory_path)
        
        generated_reports = []
        
        for project_name, project_files in projects.items():
            # Filter results for this project
            project_results = [r for r in results if r.file_info.project_name == project_name]
            
            filename = f"{root_name}_{project_name}_PROJECT_{timestamp}.md"
            filepath = session_dir / filename
            
            content = self._generate_project_content(
                project_results, project_name, project_stats.get(project_name, {}), directory_path
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            generated_reports.append(str(filepath))
            self.logger.info(f"Project report saved to: {filepath}")
        
        return generated_reports
    
    def generate_cross_project_report(self, results: List[AnalysisResult], 
                                    directory_path: str, projects: Dict,
                                    project_stats: Dict) -> str:
        """Generate cross-project analysis report"""
        
        root_name = Path(directory_path).name
        timestamp = datetime.now().strftime("%H_%M_%d_%m_%y")
        
        # Get session directory
        session_dir = self._get_session_directory(directory_path)
        
        filename = f"{root_name}_CROSS_PROJECT_ANALYSIS_{timestamp}.md"
        filepath = session_dir / filename
        
        content = self._generate_cross_project_content(
            results, directory_path, projects, project_stats
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Cross-project analysis report saved to: {filepath}")
        return str(filepath)
    
    def _generate_comprehensive_content(self, results: List[AnalysisResult], 
                                      directory_path: str, projects: Dict,
                                      project_stats: Dict, analysis_mode: str) -> str:
        """Generate comprehensive report content"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        root_name = Path(directory_path).name
        
        # Calculate overall stats
        total_files = len(results)
        successful_analyses = len([r for r in results if not r.error])
        total_words = sum(r.word_count for r in results)
        
        content = f"""# Comprehensive Document Analysis Report
## {root_name}

**Generated:** {timestamp}  
**Analysis Mode:** {analysis_mode.title()}  
**Directory:** `{directory_path}`

---

## Executive Summary

This comprehensive analysis covers **{len(projects)} projects** containing **{total_files} documents** with a total of **{total_words:,} words**.

### Projects Overview
"""
        
        # Add project summaries
        for project_name, project_files in projects.items():
            stats = project_stats.get(project_name, {})
            content += f"\n- **{project_name}:** {stats.get('file_count', 0)} files, {len(stats.get('subfolders', []))} sections\n"
        
        content += "\n---\n\n"
        
        # Add detailed project sections
        if projects:
            # Process organized projects
            for project_name, project_files in projects.items():
                project_results = [r for r in results if r.file_info.project_name == project_name]
                stats = project_stats.get(project_name, {})
                
                content += f"## Project: {project_name}\n\n"
                content += f"**Files:** {stats.get('file_count', 0)}  \n"
                content += f"**Sections:** {', '.join(stats.get('subfolders', ['root']))}\n"
                content += f"**File Types:** {', '.join(stats.get('extensions', {}).keys())}\n\n"
                
                # Add AI project analysis
                content += self._get_project_ai_analysis(project_name, project_files, stats)
                
                # Add file details
                content += f"### Documents in {project_name}\n\n"
                
                for result in project_results:
                    if result.error:
                        continue
                        
                    content += f"#### {result.file_info.name}\n"
                    content += f"**Location:** `{result.file_info.relative_path}`  \n"
                    content += f"**Type:** {result.file_info.extension.upper()}  \n"
                    content += f"**Size:** {self._format_size(result.file_info.size)}  \n"
                    content += f"**Words:** {result.word_count:,}\n\n"
                    
                    if result.summary:
                        content += f"**Summary:** {result.summary}\n\n"
                    
                    if result.ai_insights:
                        content += f"**Analysis:** {result.ai_insights}\n\n"
                    
                    content += "---\n\n"
        else:
            # Handle case where no projects were detected - show all files
            content += f"## Documents Analysis\n\n"
            content += f"**Total Files:** {total_files}  \n"
            content += f"**Successful Analyses:** {successful_analyses}  \n"
            content += f"**Total Words:** {total_words:,}\n\n"
            
            # Get file type distribution
            file_types = {}
            for result in results:
                ext = result.file_info.extension.upper()
                file_types[ext] = file_types.get(ext, 0) + 1
            
            content += f"**File Types:** {', '.join(f'{ext}({count})' for ext, count in file_types.items())}\n\n"
            
            # Add individual file details with AI insights
            content += f"### Document Details\n\n"
            
            for result in results:
                if result.error:
                    content += f"#### {result.file_info.name} (Error)\n"
                    content += f"**Error:** {result.error}\n\n"
                    content += "---\n\n"
                    continue
                    
                content += f"#### {result.file_info.name}\n"
                content += f"**Location:** `{result.file_info.relative_path}`  \n"
                content += f"**Type:** {result.file_info.extension.upper()}  \n"
                content += f"**Size:** {self._format_size(result.file_info.size)}  \n"
                content += f"**Words:** {result.word_count:,}\n\n"
                
                if result.summary:
                    content += f"**Summary:** {result.summary}\n\n"
                
                if result.ai_insights:
                    content += f"**AI Analysis:** {result.ai_insights}\n\n"
                
                content += "---\n\n"
        
        # Add technical appendix
        content += self._generate_technical_appendix(results, projects, project_stats)
        
        return content
    
    def _generate_overview_content(self, results: List[AnalysisResult], 
                                 directory_path: str, projects: Dict,
                                 project_stats: Dict) -> str:
        """Generate overview report content"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        root_name = Path(directory_path).name
        
        content = f"""# Portfolio Overview Report
## {root_name}

**Generated:** {timestamp}  
**Directory:** `{directory_path}`

---

## Portfolio Summary

### Quick Stats
- **Projects:** {len(projects)}
- **Total Documents:** {len(results)}
- **Total Words:** {sum(r.word_count for r in results):,}
- **File Types:** {len(set(r.file_info.extension for r in results))}

### Project Breakdown
"""
        
        for project_name, project_files in projects.items():
            stats = project_stats.get(project_name, {})
            project_results = [r for r in results if r.file_info.project_name == project_name]
            project_words = sum(r.word_count for r in project_results)
            
            content += f"\n#### {project_name}\n"
            content += f"- **Documents:** {stats.get('file_count', 0)}\n"
            content += f"- **Sections:** {len(stats.get('subfolders', []))}\n"
            content += f"- **Word Count:** {project_words:,}\n"
            content += f"- **File Types:** {', '.join(stats.get('extensions', {}).keys())}\n"
        
        # Add cross-project insights
        content += "\n---\n\n## Cross-Project Analysis\n\n"
        content += self._get_cross_project_ai_analysis(projects, project_stats)
        
        return content
    
    def _generate_project_content(self, project_results: List[AnalysisResult], 
                                project_name: str, project_stats: Dict,
                                directory_path: str) -> str:
        """Generate individual project report content"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# Project Report: {project_name}

**Generated:** {timestamp}  
**Parent Directory:** `{directory_path}`

---

## Project Overview

**Files:** {project_stats.get('file_count', 0)}  
**Sections:** {', '.join(project_stats.get('subfolders', ['root']))}  
**File Types:** {', '.join(project_stats.get('extensions', {}).keys())}  
**Total Words:** {sum(r.word_count for r in project_results):,}

## Project Analysis

"""
        
        # Add AI project analysis
        content += self._get_project_ai_analysis(project_name, project_results, project_stats)
        
        content += "\n## Document Details\n\n"
        
        # Group by subfolder
        by_subfolder = {}
        for result in project_results:
            subfolder = result.file_info.subfolder_path or "root"
            if subfolder not in by_subfolder:
                by_subfolder[subfolder] = []
            by_subfolder[subfolder].append(result)
        
        for subfolder, files in by_subfolder.items():
            content += f"### {subfolder.title()} Section\n\n"
            
            for result in files:
                if result.error:
                    continue
                    
                content += f"#### {result.file_info.name}\n"
                content += f"**Type:** {result.file_info.extension.upper()}  \n"
                content += f"**Words:** {result.word_count:,}  \n"
                
                if result.summary:
                    content += f"**Summary:** {result.summary}\n\n"
                
                if result.ai_insights:
                    content += f"**Insights:** {result.ai_insights}\n\n"
                
                content += "---\n\n"
        
        return content
    
    def _generate_cross_project_content(self, results: List[AnalysisResult], 
                                      directory_path: str, projects: Dict,
                                      project_stats: Dict) -> str:
        """Generate cross-project analysis content"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        root_name = Path(directory_path).name
        
        content = f"""# Cross-Project Analysis Report
## {root_name}

**Generated:** {timestamp}  
**Directory:** `{directory_path}`

---

## Portfolio Analysis

This report analyzes patterns, relationships, and insights across all {len(projects)} projects in the portfolio.

"""
        
        # Add cross-project AI analysis
        content += self._get_cross_project_ai_analysis(projects, project_stats)
        
        # Add comparative analysis
        content += "\n## Comparative Analysis\n\n"
        
        # Project size comparison
        content += "### Project Size Comparison\n\n"
        project_sizes = []
        for project_name, stats in project_stats.items():
            project_sizes.append((project_name, stats.get('file_count', 0)))
        
        project_sizes.sort(key=lambda x: x[1], reverse=True)
        
        for project_name, file_count in project_sizes:
            content += f"- **{project_name}:** {file_count} files\n"
        
        # File type distribution
        content += "\n### File Type Distribution\n\n"
        all_extensions = {}
        for stats in project_stats.values():
            for ext, count in stats.get('extensions', {}).items():
                all_extensions[ext] = all_extensions.get(ext, 0) + count
        
        for ext, count in sorted(all_extensions.items(), key=lambda x: x[1], reverse=True):
            content += f"- **{ext.upper()}:** {count} files\n"
        
        return content
    
    def _get_project_ai_analysis(self, project_name: str, project_files: list, project_stats: dict) -> str:
        """Get AI analysis for a project"""
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
            
            if ai_analyzer.is_available():
                analysis = ai_analyzer.analyze_project(project_name, project_files, project_stats)
                return f"### AI Project Analysis\n\n{analysis}\n\n"
            else:
                return "### Project Analysis\n\nAI analysis unavailable - requires API configuration.\n\n"
        except Exception as e:
            return f"### Project Analysis\n\nAnalysis error: {str(e)}\n\n"
    
    def _get_cross_project_ai_analysis(self, projects: Dict, project_stats: Dict) -> str:
        """Get AI cross-project analysis"""
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
            
            if ai_analyzer.is_available():
                # Prepare data structure for cross-project analysis
                projects_data = {}
                for project_name, files in projects.items():
                    projects_data[project_name] = {
                        'files': files,
                        'stats': project_stats.get(project_name, {})
                    }
                
                analysis = ai_analyzer.analyze_cross_project(projects_data)
                return analysis
            else:
                return "AI cross-project analysis unavailable - requires API configuration."
        except Exception as e:
            return f"Cross-project analysis error: {str(e)}"
    
    def _generate_technical_appendix(self, results: List[AnalysisResult], 
                                   projects: Dict, project_stats: Dict) -> str:
        """Generate technical appendix with detailed statistics"""
        
        content = "## Technical Appendix\n\n"
        
        # Error summary
        errors = [r for r in results if r.error]
        if errors:
            content += "### Processing Errors\n\n"
            for result in errors:
                content += f"- **{result.file_info.name}:** {result.error}\n"
            content += "\n"
        
        # Detailed statistics
        content += "### Detailed Statistics\n\n"
        
        for project_name, stats in project_stats.items():
            content += f"#### {project_name}\n"
            content += f"- Files: {stats.get('file_count', 0)}\n"
            content += f"- Total Size: {self._format_size(stats.get('total_size', 0))}\n"
            content += f"- Sections: {', '.join(stats.get('subfolders', ['root']))}\n"
            
            extensions = stats.get('extensions', {})
            if extensions:
                content += "- File Types:\n"
                for ext, count in extensions.items():
                    content += f"  - {ext.upper()}: {count}\n"
            content += "\n"
        
        return content
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        
        return f"{size_bytes:.1f} TB"
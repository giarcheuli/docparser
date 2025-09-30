#!/usr/bin/env python3
"""
DocParser - Enhanced Command Line Interface
A comprehensive document analysis tool for macOS

Features:
- Multi-format document support (DOC, DOCX, PDF, TXT, HTML, MD, XLSX, XML)
- Metadata extraction and content analysis
- Optional AI-powered insights
- Structured markdown report generation
- Progress tracking and detailed logging
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import List, Optional
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('docparser.log')
        ]
    )
    return logging.getLogger(__name__)

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("📄 DocParser v2.0 - CLI Edition")
    print("🔍 Comprehensive Document Analysis Tool")
    print("=" * 60)

def validate_directory(directory: str) -> Path:
    """Validate and return directory path"""
    path = Path(directory).resolve()
    if not path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {directory}")
    return path

def check_ai_availability() -> dict:
    """Check which AI providers are available"""
    available = {}
    
    # Check for API keys
    if os.getenv('OPENAI_API_KEY'):
        available['openai'] = True
    if os.getenv('ANTHROPIC_API_KEY'):
        available['anthropic'] = True
    if os.getenv('REPLICATE_API_TOKEN'):
        available['replicate'] = True
    
    return available

def analyze_directory(directory_path: Path, use_ai: bool, verbose: bool, logger: logging.Logger) -> tuple:
    """Run the document analysis with project awareness"""
    try:
        from core.analyzer import DocumentAnalyzer
        
        logger.info(f"Starting project-aware analysis of: {directory_path}")
        
        # Initialize analyzer
        analyzer = DocumentAnalyzer()
        
        # Show AI status
        if use_ai:
            ai_providers = check_ai_availability()
            if ai_providers:
                logger.info(f"AI providers available: {list(ai_providers.keys())}")
            else:
                logger.warning("AI analysis requested but no API keys found")
                print("⚠️  AI analysis enabled but no API keys detected")
                print("   Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or REPLICATE_API_TOKEN")
        
        # Run analysis with progress
        print("📊 Scanning directory for projects and supported files...")
        start_time = time.time()
        
        results = analyzer.analyze_directory(str(directory_path), use_ai=use_ai)
        directory_stats = analyzer.get_directory_summary()
        projects = analyzer.get_projects()
        project_stats = analyzer.get_project_stats()
        
        analysis_time = time.time() - start_time
        
        # Show results summary
        successful = len([r for r in results if not r.error])
        failed = len([r for r in results if r.error])
        
        print(f"✅ Analysis complete in {analysis_time:.1f}s")
        print(f"📈 Results: {successful} successful, {failed} failed")
        print(f"🗂️  Projects detected: {len(projects)}")
        
        if verbose and failed > 0:
            print("\n❌ Failed files:")
            for result in results:
                if result.error:
                    print(f"   {result.file_info.name}: {result.error}")
        
        return results, directory_stats, projects, project_stats, analysis_time
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise

def generate_all_reports(results: List, directory_path: Path, directory_stats: dict, 
                        projects: dict, project_stats: dict, analysis_time: float, use_ai: bool, 
                        analysis_mode: str, logger: logging.Logger) -> List[str]:
    """Generate all report types and return list of generated files"""
    try:
        from utils.project_report_generator import ProjectReportGenerator
        
        generated_files = []
        print("📝 Generating comprehensive report...")
        
        # Initialize project-aware report generator
        report_generator = ProjectReportGenerator()
        
        # 1. Generate comprehensive report (structured by projects)
        comprehensive_report = report_generator.generate_comprehensive_report(
            results, str(directory_path), projects, project_stats, analysis_mode
        )
        generated_files.append(comprehensive_report)
        logger.info(f"Comprehensive report generated: {comprehensive_report}")
        
        # 2. Generate overview report (one-pager summarizing all projects)
        print("📊 Generating overview report...")
        overview_report = report_generator.generate_overview_report(
            results, str(directory_path), projects, project_stats
        )
        generated_files.append(overview_report)
        logger.info(f"Overview report generated: {overview_report}")
        
        # 3. Generate individual project reports
        print("�️  Generating individual project reports...")
        project_reports = report_generator.generate_project_reports(
            results, str(directory_path), projects, project_stats
        )
        generated_files.extend(project_reports)
        logger.info(f"Generated {len(project_reports)} project reports")
        
        # 4. Generate cross-project analysis report
        print("🔀 Generating cross-project analysis...")
        cross_project_report = report_generator.generate_cross_project_report(
            results, str(directory_path), projects, project_stats
        )
        generated_files.append(cross_project_report)
        logger.info(f"Cross-project analysis generated: {cross_project_report}")
        
        return generated_files
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}", exc_info=True)
        raise

def show_summary(directory_stats: dict, projects: dict, results: List, analysis_time: float):
    """Show analysis summary with project information"""
    print(f"\n📋 Analysis Summary:")
    print(f"   ⏱️  Time taken: {analysis_time:.1f} seconds")
    print(f"   📁 Total files: {directory_stats.get('total_files', 0)}")
    print(f"   📏 Total size: {format_bytes(directory_stats.get('total_size', 0))}")
    print(f"   🗂️  Projects: {len(projects)}")
    
    print(f"\n📊 File Types:")
    for ext, count in directory_stats.items():
        if ext.startswith('.') and isinstance(count, int):
            print(f"   {ext.upper()}: {count} files")
    
    # Show projects
    print(f"\n🗂️  Projects:")
    for project_name, files in projects.items():
        print(f"   {project_name}: {len(files)} files")
    
    # Show largest files
    largest_files = sorted(
        [r for r in results if not r.error], 
        key=lambda x: x.file_info.size, 
        reverse=True
    )[:3]
    
    if largest_files:
        print(f"\n📈 Largest Files:")
        for i, result in enumerate(largest_files, 1):
            size = format_bytes(result.file_info.size)
            print(f"   {i}. {result.file_info.name} ({size})")

def format_bytes(bytes_size: int) -> str:
    """Format bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='DocParser v2.0 - Project-Aware Document Analysis Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s documents/                     # Analyze with project detection and generate all reports
  %(prog)s documents/ --ai               # With AI analysis for enhanced insights
  %(prog)s documents/ --verbose          # Verbose logging
  %(prog)s documents/ --verbose          # Verbose logging
  %(prog)s documents/ --format json      # JSON output format
        """
    )
    
    parser.add_argument('directory', 
                       help='Directory to analyze (required)')
    
    parser.add_argument('--ai', action='store_true',
                       help='Enable AI-powered analysis and insights')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    parser.add_argument('--analysis-mode', choices=['qualitative', 'quantitative'], default='qualitative',
                       help='Analysis approach: qualitative (insights/summaries) or quantitative (metrics/stats)')
    
    parser.add_argument('--no-summary', action='store_true',
                       help='Skip showing the summary at the end')
    
    parser.add_argument('--list-only', action='store_true',
                       help='Only list supported files, don\'t analyze')
    
    args = parser.parse_args()
    
    # Setup
    logger = setup_logging(args.verbose)
    print_banner()
    
    try:
        # Validate directory
        directory_path = validate_directory(args.directory)
        
        print(f"📁 Directory: {directory_path}")
        print(f"🤖 AI Analysis: {'Enabled' if args.ai else 'Disabled'}")
        print(f"📊 Analysis Mode: {args.analysis_mode.title()}")
        
        if args.list_only:
            # Just list files
            from core.scanner import DocumentScanner
            scanner = DocumentScanner()
            files = scanner.scan_directory(str(directory_path))
            
            print(f"\n🔍 Found {len(files)} supported files:")
            for file_info in sorted(files, key=lambda x: x.name.lower()):
                size = format_bytes(file_info.size)
                print(f"   {file_info.extension.upper()}: {file_info.name} ({size})")
            
            return 0
        
        print("-" * 60)
        
        # Run analysis
        results, directory_stats, projects, project_stats, analysis_time = analyze_directory(
            directory_path, args.ai, args.verbose, logger
        )
        
        if not results:
            print("❌ No supported files found in directory")
            return 1
        
        # Generate reports
        generated_files = generate_all_reports(
            results, directory_path, directory_stats, projects, project_stats,
            analysis_time, args.ai, args.analysis_mode, logger
        )
        
        print(f"✅ Reports saved to session directory:")
        if generated_files:
            # Extract session directory from first file path
            session_dir = str(Path(generated_files[0]).parent)
            print(f"   📁 {session_dir}")
            print(f"   📄 Generated {len(generated_files)} reports:")
            for file_path in generated_files:
                filename = Path(file_path).name
                print(f"      • {filename}")
        
        # Show summary unless disabled
        if not args.no_summary:
            show_summary(directory_stats, projects, results, analysis_time)
        
        print(f"\n🎉 Analysis complete! Generated {len(generated_files)} report(s).")
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️ Analysis interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
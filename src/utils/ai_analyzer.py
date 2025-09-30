"""
AI-powered content analysis using OpenAI, Anthropic, or Replicate APIs
"""

import logging
import os
from typing import Optional

class AIAnalyzer:
    """AI-powered content analyzer for summarization and insights"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.openai_client = None
        self.anthropic_client = None
        self.replicate_client = None
        
        # Initialize available AI clients
        self._init_ai_clients()
    
    def _init_ai_clients(self):
        """Initialize AI clients if API keys are available"""
        
        # Try OpenAI
        try:
            import openai
            if os.getenv('OPENAI_API_KEY'):
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                self.logger.info("OpenAI client initialized")
        except ImportError:
            self.logger.warning("OpenAI package not available")
        except Exception as e:
            self.logger.warning(f"Failed to initialize OpenAI client: {e}")
        
        # Try Anthropic
        try:
            import anthropic
            if os.getenv('ANTHROPIC_API_KEY'):
                self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
                self.logger.info("Anthropic client initialized")
        except ImportError:
            self.logger.warning("Anthropic package not available")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Anthropic client: {e}")
        
        # Try Replicate
        try:
            import replicate
            if os.getenv('REPLICATE_API_TOKEN'):
                self.replicate_client = replicate
                self.logger.info("Replicate client initialized")
        except ImportError:
            self.logger.warning("Replicate package not available")
        except Exception as e:
            self.logger.warning(f"Failed to initialize Replicate client: {e}")
    
    def summarize_content(self, content: str, max_length: int = 200, project_context: str = None) -> str:
        """Generate a summary of the content with optional project context"""
        
        if not content or len(content.strip()) < 50:
            return "Content too short for meaningful summary"
        
        # Truncate very long content
        if len(content) > 4000:
            content = content[:4000] + "..."
        
        context_info = ""
        if project_context:
            context_info = f"\nProject Context: This document belongs to the '{project_context}' project. "
        
        prompt = f"""Please provide a concise summary of the following content in {max_length} characters or less:{context_info}

{content}

Summary:"""
        
        try:
            if self.openai_client:
                return self._openai_completion(prompt, max_tokens=60)
            elif self.replicate_client:
                return self._replicate_completion(prompt, max_tokens=60)
            elif self.anthropic_client:
                return self._anthropic_completion(prompt, max_tokens=60)
            else:
                return self._fallback_summary(content, max_length)
        except Exception as e:
            self.logger.error(f"AI summarization failed: {e}")
            return self._fallback_summary(content, max_length)
    
    def analyze_content(self, content: str, filename: str, project_context: str = None, subfolder_path: str = None) -> str:
        """Analyze content and provide insights with project context"""
        
        if not content or len(content.strip()) < 20:
            return "Content too short for analysis"
        
        # Truncate very long content
        if len(content) > 4000:
            content = content[:4000] + "..."
        
        context_info = ""
        if project_context:
            context_info = f"\nProject Context: This document belongs to the '{project_context}' project"
            if subfolder_path:
                context_info += f" in the '{subfolder_path}' section"
            context_info += ". "
        
        prompt = f"""Analyze the following document content from file "{filename}" and provide insights about:
1. Document type and purpose
2. Key topics or themes  
3. Structure and organization
4. Notable characteristics{context_info}

Content:
{content}

Analysis:"""
        
        try:
            if self.openai_client:
                return self._openai_completion(prompt, max_tokens=150)
            elif self.replicate_client:
                return self._replicate_completion(prompt, max_tokens=150)
            elif self.anthropic_client:
                return self._anthropic_completion(prompt, max_tokens=150)
            else:
                return self._fallback_analysis(content, filename)
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return self._fallback_analysis(content, filename)
    
    def _openai_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    def _anthropic_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Anthropic"""
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            self.logger.error(f"Anthropic API error: {e}")
            raise
    
    def _replicate_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Replicate"""
        try:
            # Using Meta's Llama 2 7B Chat model
            output = self.replicate_client.run(
                "meta/llama-2-7b-chat",
                input={
                    "prompt": prompt,
                    "max_new_tokens": max_tokens,
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            )
            
            # Replicate returns an iterator, join the output
            result = "".join(output).strip()
            
            # Clean up the result - remove the original prompt if it's echoed back
            if result.startswith(prompt):
                result = result[len(prompt):].strip()
            
            return result if result else "No response generated"
            
        except Exception as e:
            self.logger.error(f"Replicate API error: {e}")
            raise
    
    def _gemini_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Google Gemini (legacy method - kept for compatibility)"""
        try:
            # Configure generation settings
            generation_config = {
                'max_output_tokens': max_tokens,
                'temperature': 0.3,
            }
            
            response = self.gemini_client.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            if response.text:
                return response.text.strip()
            else:
                raise Exception("Empty response from Gemini")
                
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise
    
    def _fallback_summary(self, content: str, max_length: int) -> str:
        """Fallback summary when AI is not available"""
        sentences = content.replace('\n', ' ').split('. ')
        if len(sentences) > 0:
            summary = sentences[0]
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            return summary
        return "No AI available for summarization"
    
    def analyze_project(self, project_name: str, project_files: list, project_stats: dict) -> str:
        """Generate analysis for a complete project"""
        
        if not project_files:
            return f"No files found for project '{project_name}'"
        
        # Prepare project summary
        file_types = ", ".join(project_stats.get('extensions', {}).keys())
        file_count = project_stats.get('file_count', 0)
        subfolders = project_stats.get('subfolders', [])
        
        project_overview = f"""Project: {project_name}
Files: {file_count} files ({file_types})
Structure: {len(subfolders)} subfolders: {', '.join(subfolders) if subfolders else 'root level only'}"""
        
        prompt = f"""Analyze the following project and provide insights:

{project_overview}

Based on the project structure and file types, provide:
1. Project purpose and scope assessment
2. Documentation quality and organization
3. Potential gaps or recommendations
4. Overall project characteristics

Analysis:"""
        
        try:
            if self.openai_client:
                return self._openai_completion(prompt, max_tokens=200)
            elif self.replicate_client:
                return self._replicate_completion(prompt, max_tokens=200)
            elif self.anthropic_client:
                return self._anthropic_completion(prompt, max_tokens=200)
            else:
                return f"Project '{project_name}' contains {file_count} files across {len(subfolders)} sections. Requires AI for detailed analysis."
        except Exception as e:
            self.logger.error(f"Project analysis failed: {e}")
            return f"Project '{project_name}' analysis unavailable due to error: {str(e)}"
    
    def analyze_cross_project(self, projects_data: dict) -> str:
        """Generate cross-project analysis comparing all projects"""
        
        if not projects_data:
            return "No projects found for cross-analysis"
        
        # Prepare cross-project summary
        project_summary = []
        total_files = 0
        
        for project_name, data in projects_data.items():
            stats = data.get('stats', {})
            file_count = stats.get('file_count', 0)
            total_files += file_count
            extensions = list(stats.get('extensions', {}).keys())
            subfolders = stats.get('subfolders', [])
            
            project_summary.append(f"- {project_name}: {file_count} files, {len(subfolders)} sections, types: {', '.join(extensions)}")
        
        summary_text = "\n".join(project_summary)
        
        prompt = f"""Perform cross-project analysis of the following projects:

Projects Overview:
{summary_text}

Total: {len(projects_data)} projects, {total_files} files

Provide insights on:
1. Project similarities and differences
2. Documentation patterns across projects
3. Potential standardization opportunities
4. Cross-project relationships or dependencies
5. Overall portfolio assessment

Cross-Project Analysis:"""
        
        try:
            if self.openai_client:
                return self._openai_completion(prompt, max_tokens=250)
            elif self.replicate_client:
                return self._replicate_completion(prompt, max_tokens=250)
            elif self.anthropic_client:
                return self._anthropic_completion(prompt, max_tokens=250)
            else:
                return f"Cross-project analysis of {len(projects_data)} projects with {total_files} total files. Requires AI for detailed insights."
        except Exception as e:
            self.logger.error(f"Cross-project analysis failed: {e}")
            return f"Cross-project analysis unavailable due to error: {str(e)}"

    def _fallback_analysis(self, content: str, filename: str) -> str:
        """Fallback analysis when AI is not available"""
        word_count = len(content.split())
        char_count = len(content)
        
        # Basic file type detection
        file_ext = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        analysis = f"Document Analysis (Basic):\n"
        analysis += f"- File type: {file_ext.upper()}\n"
        analysis += f"- Content length: {char_count} characters, {word_count} words\n"
        
        if 'table' in content.lower() or '|' in content:
            analysis += "- Contains structured data (tables)\n"
        
        if any(heading in content for heading in ['#', 'Chapter', 'Section']):
            analysis += "- Contains headings/sections\n"
        
        return analysis + "\nNote: Full AI analysis requires API configuration"
    
    def is_available(self) -> bool:
        """Check if AI analysis is available"""
        return (self.openai_client is not None or 
                self.anthropic_client is not None or 
                self.replicate_client is not None)
"""
AI-powered content analysis using multiple configurable AI providers
"""

# Ensure environment variables are loaded first
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

import logging
import os
from typing import Optional, Dict, Any, List
from .ai_config import AIConfig

class AIAnalyzer:
    """AI-powered content analyzer with configurable multi-provider support"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.config = AIConfig(config_path)
        self.clients = {}
        
        # Initialize available AI clients
        self._init_ai_clients()
    
    def _init_ai_clients(self):
        """Initialize AI clients for enabled providers with credentials"""
        available_providers = self.config.get_available_providers()
        
        for provider in available_providers:
            try:
                if provider == "openai":
                    self._init_openai()
                elif provider == "anthropic":
                    self._init_anthropic()
                elif provider == "replicate":
                    self._init_replicate()
                elif provider == "gemini":
                    self._init_gemini()
            except Exception as e:
                self.logger.warning(f"Failed to initialize {provider}: {e}")
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            api_key = self.config.get_api_credential("openai")
            if api_key:
                self.clients["openai"] = openai.OpenAI(api_key=api_key)
                self.logger.info("OpenAI client initialized")
        except ImportError:
            self.logger.warning("OpenAI package not available")
    
    def _init_anthropic(self):
        """Initialize Anthropic client"""
        try:
            import anthropic
            api_key = self.config.get_api_credential("anthropic")
            if api_key:
                self.clients["anthropic"] = anthropic.Anthropic(api_key=api_key)
                self.logger.info("Anthropic client initialized")
        except ImportError:
            self.logger.warning("Anthropic package not available")
    
    def _init_replicate(self):
        """Initialize Replicate client"""
        try:
            import replicate
            api_token = self.config.get_api_credential("replicate")
            if api_token:
                os.environ["REPLICATE_API_TOKEN"] = api_token
                self.clients["replicate"] = replicate
                self.logger.info("Replicate client initialized")
        except ImportError:
            self.logger.warning("Replicate package not available")
    
    def _init_gemini(self):
        """Initialize Google Gemini client"""
        try:
            import google.generativeai as genai
            api_key = self.config.get_api_credential("gemini")
            if api_key:
                genai.configure(api_key=api_key)
                self.clients["gemini"] = genai
                self.logger.info("Gemini client initialized")
        except ImportError:
            self.logger.warning("Google GenerativeAI package not available")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available and initialized providers"""
        return list(self.clients.keys())
    
    def _try_providers_with_fallback(self, method_name: str, *args, **kwargs) -> Optional[str]:
        """Try providers in fallback order until one succeeds"""
        
        # Get preferred provider order
        default_provider = self.config.get_default_provider()
        fallback_order = self.config.get_fallback_order()
        
        # Ensure default provider is first
        provider_order = [default_provider] if default_provider in self.clients else []
        for provider in fallback_order:
            if provider in self.clients and provider not in provider_order:
                provider_order.append(provider)
        
        if not provider_order:
            self.logger.error("No AI providers available")
            return None
        
        # Try each provider in order
        for provider in provider_order:
            try:
                method = getattr(self, f"_{provider}_{method_name}")
                result = method(*args, **kwargs)
                if result:
                    self.logger.info(f"Successfully used {provider} for {method_name}")
                    return result
            except Exception as e:
                self.logger.warning(f"{provider} failed for {method_name}: {e}")
                continue
        
        self.logger.error(f"All providers failed for {method_name}")
        return None
    
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
        
        result = self._try_providers_with_fallback("completion", prompt, max_tokens=60)
        return result or "Unable to generate summary - no AI providers available"
    
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
        
        result = self._try_providers_with_fallback("completion", prompt, max_tokens=150)
        return result or self._fallback_analysis(content, filename)
    
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
        
        result = self._try_providers_with_fallback("completion", prompt, max_tokens=200)
        return result or f"Project '{project_name}' analysis unavailable - no AI providers available"
    
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
        
        result = self._try_providers_with_fallback("completion", prompt, max_tokens=250)
        return result or f"Cross-project analysis of {len(projects_data)} projects with {total_files} total files. Requires AI for detailed insights."
    
    # Provider-specific completion methods
    def _openai_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from OpenAI"""
        try:
            config = self.config.get_provider_config("openai")
            response = self.clients["openai"].chat.completions.create(
                model=config.get("model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=min(max_tokens, config.get("max_tokens", 1000)),
                temperature=config.get("temperature", 0.3)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"OpenAI completion failed: {e}")
            raise
    
    def _anthropic_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Anthropic"""
        try:
            config = self.config.get_provider_config("anthropic")
            response = self.clients["anthropic"].messages.create(
                model=config.get("model", "claude-3-haiku-20240307"),
                max_tokens=min(max_tokens, config.get("max_tokens", 1000)),
                temperature=config.get("temperature", 0.3),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            self.logger.error(f"Anthropic completion failed: {e}")
            raise
    
    def _replicate_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Replicate"""
        try:
            config = self.config.get_provider_config("replicate")
            
            output = self.clients["replicate"].run(
                config.get("model", "meta/llama-2-7b-chat"),
                input={
                    "prompt": prompt,
                    "max_new_tokens": min(max_tokens, config.get("max_tokens", 1000)),
                    "temperature": config.get("temperature", 0.3),
                    "top_p": config.get("top_p", 0.9),
                    "repetition_penalty": config.get("repetition_penalty", 1.1)
                }
            )
            
            # Replicate returns a generator, collect the output
            result = ""
            for item in output:
                result += item
            
            return result.strip()
        except Exception as e:
            self.logger.error(f"Replicate completion failed: {e}")
            raise
    
    def _gemini_completion(self, prompt: str, max_tokens: int = 150) -> str:
        """Get completion from Google Gemini"""
        try:
            config = self.config.get_provider_config("gemini")
            model = self.clients["gemini"].GenerativeModel(config.get("model", "gemini-pro"))
            
            generation_config = self.clients["gemini"].types.GenerationConfig(
                max_output_tokens=min(max_tokens, config.get("max_tokens", 1000)),
                temperature=config.get("temperature", 0.3)
            )
            
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Gemini completion failed: {e}")
            raise
    
    def _fallback_summary(self, content: str, max_length: int) -> str:
        """Fallback summary when AI is not available"""
        # Simple text truncation
        sentences = content.split('. ')
        summary = sentences[0] if sentences else content
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        return summary or "Content summary unavailable"
    
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
        return len(self.clients) > 0
    
    def get_active_provider(self) -> Optional[str]:
        """Get the currently active provider"""
        default_provider = self.config.get_default_provider()
        if default_provider in self.clients:
            return default_provider
        return next(iter(self.clients.keys())) if self.clients else None
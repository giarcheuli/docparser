"""
HTML analyzer for .html and .htm files
"""

import logging
from pathlib import Path
from typing import Dict, Any

try:
    from bs4 import BeautifulSoup
    import requests
    HTML_AVAILABLE = True
except ImportError:
    HTML_AVAILABLE = False

from . import BaseAnalyzer

class HTMLAnalyzer(BaseAnalyzer):
    """Analyzer for HTML files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not HTML_AVAILABLE:
            self.logger.warning("BeautifulSoup not available. HTML analysis will be limited.")
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from HTML files"""
        if not HTML_AVAILABLE:
            return "HTML analysis requires beautifulsoup4 package"
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            self.logger.error(f"Error reading HTML file {file_path}: {e}")
            return f"Error reading HTML file: {str(e)}"
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from HTML files"""
        if not HTML_AVAILABLE:
            return {'error': 'beautifulsoup4 not available'}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            metadata = {
                'file_type': 'html',
            }
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text().strip()
            
            # Extract meta tags
            meta_tags = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name', meta.get('property', meta.get('http-equiv')))
                content = meta.get('content')
                if name and content:
                    meta_tags[name] = content
            
            if meta_tags:
                metadata['meta_tags'] = meta_tags
            
            # Count elements
            metadata['tag_counts'] = {}
            
            # Count common HTML elements
            common_tags = ['p', 'div', 'span', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                          'table', 'tr', 'td', 'ul', 'ol', 'li', 'form', 'input', 'button']
            
            for tag in common_tags:
                count = len(soup.find_all(tag))
                if count > 0:
                    metadata['tag_counts'][tag] = count
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().strip()
                if href and not href.startswith('#'):  # Skip anchor links
                    links.append({'url': href, 'text': text})
            
            if links:
                metadata['links'] = links[:20]  # Limit to first 20 links
                metadata['link_count'] = len(links)
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=True):
                src = img['src']
                alt = img.get('alt', '')
                images.append({'src': src, 'alt': alt})
            
            if images:
                metadata['images'] = images[:10]  # Limit to first 10 images
                metadata['image_count'] = len(images)
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting HTML metadata from {file_path}: {e}")
            return {'error': str(e)}
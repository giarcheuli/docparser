"""
XML analyzer for .xml files
"""

import logging
from pathlib import Path
from typing import Dict, Any
import xml.etree.ElementTree as ET

from . import BaseAnalyzer

class XMLAnalyzer(BaseAnalyzer):
    """Analyzer for XML files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_text(self, file_path: Path) -> str:
        """Extract text content from XML files"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            text_content = []
            text_content.append(f"Root element: {root.tag}")
            
            if root.attrib:
                text_content.append(f"Root attributes: {root.attrib}")
            
            # Extract all text content
            def extract_element_text(element, level=0):
                indent = "  " * level
                element_info = f"{indent}<{element.tag}"
                
                if element.attrib:
                    attrs = " ".join(f'{k}="{v}"' for k, v in element.attrib.items())
                    element_info += f" {attrs}"
                element_info += ">"
                
                text_content.append(element_info)
                
                if element.text and element.text.strip():
                    text_content.append(f"{indent}  {element.text.strip()}")
                
                for child in element:
                    extract_element_text(child, level + 1)
            
            extract_element_text(root)
            
            return "\n".join(text_content)
            
        except ET.ParseError as e:
            self.logger.error(f"XML parse error in {file_path}: {e}")
            return f"XML Parse Error: {str(e)}"
        except Exception as e:
            self.logger.error(f"Error reading XML file {file_path}: {e}")
            return f"Error reading XML file: {str(e)}"
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract metadata from XML files"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            metadata = {
                'file_type': 'xml',
                'root_element': root.tag,
                'root_attributes': dict(root.attrib) if root.attrib else {},
            }
            
            # Count elements by tag name
            tag_counts = {}
            all_elements = root.iter()
            
            for element in all_elements:
                tag_counts[element.tag] = tag_counts.get(element.tag, 0) + 1
            
            metadata['tag_counts'] = tag_counts
            metadata['total_elements'] = sum(tag_counts.values())
            metadata['unique_tags'] = len(tag_counts)
            
            # Extract namespaces
            namespaces = {}
            for elem in root.iter():
                if '}' in elem.tag:
                    namespace = elem.tag.split('}')[0] + '}'
                    namespaces[namespace] = namespaces.get(namespace, 0) + 1
            
            if namespaces:
                metadata['namespaces'] = namespaces
            
            # Calculate depth
            def get_max_depth(element, current_depth=0):
                if not list(element):
                    return current_depth
                return max(get_max_depth(child, current_depth + 1) for child in element)
            
            metadata['max_depth'] = get_max_depth(root)
            
            # Check for common XML document types
            if root.tag.lower() == 'html':
                metadata['document_type'] = 'HTML-like XML'
            elif 'rss' in root.tag.lower():
                metadata['document_type'] = 'RSS Feed'
            elif 'feed' in root.tag.lower():
                metadata['document_type'] = 'Atom Feed'
            elif root.tag.endswith('ml') or 'xml' in root.tag.lower():
                metadata['document_type'] = 'Markup Document'
            else:
                metadata['document_type'] = 'Generic XML'
            
            return metadata
            
        except ET.ParseError as e:
            self.logger.error(f"XML parse error in {file_path}: {e}")
            return {'error': f'XML Parse Error: {str(e)}'}
        except Exception as e:
            self.logger.error(f"Error extracting XML metadata from {file_path}: {e}")
            return {'error': str(e)}
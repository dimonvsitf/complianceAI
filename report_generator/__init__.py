# report_generator/__init__.py
from pathlib import Path
from typing import Dict, List
from .sections import get_section_generator
from .formatter import ReferenceManager, MarkdownFormatter

class ReportGenerator:
    def __init__(self, api_key: str, templates_dir: Path):
        """Initialize report generator with OpenAI API key and templates directory."""
        self.api_key = api_key
        self.templates_dir = templates_dir
        self.reference_manager = ReferenceManager()
        self.formatter = MarkdownFormatter()
    
    def generate_report(self, documents: Dict[str, List[dict]]) -> str:
        """Generate complete EDD report from processed documents."""
        # Generate each section
        sections = []
        section_types = ['business_description', 'ownership', 'compliance']
        
        for section_type in section_types:
            generator = get_section_generator(
                section_type,
                self.api_key,
                self.templates_dir
            )
            content = generator.generate(documents)
            sections.append(content)
        
        # Combine sections
        combined_content = "\n\n".join(sections)
        
        # Process references and format
        formatted_content = self.reference_manager.process_text(combined_content)
        final_content = self.formatter.format(formatted_content)
        return final_content
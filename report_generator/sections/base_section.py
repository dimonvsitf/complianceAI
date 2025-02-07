# report_generator/sections/base_section.py
from abc import ABC, abstractmethod
from typing import List, Dict
import openai
import json
from pathlib import Path

class BaseSection(ABC):
    """Base class for report sections."""
    
    def __init__(self, api_key: str, templates_dir: Path):
        self.client = openai.OpenAI(api_key=api_key)
        self.template_path = templates_dir / "prompts" / f"{self.section_name}.txt"
        with open(self.template_path) as f:
            self.template = f.read()
    
    @property
    @abstractmethod
    def section_name(self) -> str:
        """Returns the name of this section."""
        pass
    
    @property
    @abstractmethod
    def required_categories(self) -> List[str]:
        """Returns list of document categories needed for this section."""
        pass
    
    def generate(self, documents: Dict[str, List[dict]]) -> str:
        """Generates the section content using relevant documents."""
        # Filter documents to only those needed for this section
        relevant_docs = {
            cat: docs for cat, docs in documents.items() 
            if cat in self.required_categories
        }
        
        # Generate section using template and filtered documents
        prompt = self.template.format(documents=self._format_documents(relevant_docs))
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def _format_documents(self, documents: Dict[str, List[dict]]) -> str:
        """Format documents for inclusion in prompt."""
        formatted = []
        for category, docs in documents.items():
            formatted.append(f"\n### {category.replace('_', ' ').title()}")
            for i, doc in enumerate(docs, 1):
                formatted.append(f"\nDocument {i}:")
                formatted.append(json.dumps(doc, indent=2))
        return "\n".join(formatted)

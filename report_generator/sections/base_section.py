# report_generator/sections/base_section.py
from abc import ABC, abstractmethod
from typing import List, Dict
import openai
from pathlib import Path

class BaseSection(ABC):
    """Base class for report sections."""
    
    def __init__(self, templates_dir: Path):
        self.template_path = templates_dir / f"{self.section_name}.txt"
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
        prompt = self.template.format(documents=relevant_docs)
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
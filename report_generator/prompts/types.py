from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class PromptSection:
    """Represents a section of a prompt with title, content, and optional subsections."""
    title: str
    content: List[str]
    subsections: Optional[List['PromptSection']] = None

@dataclass
class PromptTemplate:
    """Represents a complete prompt template with sections and data requirements."""
    sections: List[PromptSection]
    required_data: List[str]  # List of required data fields
    description: str  # Description of what this prompt template is for
    
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate that all required data fields are present."""
        return all(field in data for field in self.required_data)

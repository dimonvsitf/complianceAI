from typing import List, Dict, Any
from .types import PromptSection, PromptTemplate

class PromptBuilder:
    """Utility class for building prompts from sections and templates."""
    
    @staticmethod
    def _build_section(section: PromptSection, data: Dict[str, Any], indent_level: int = 0) -> str:
        """
        Build a single section of the prompt, including its subsections.
        
        Args:
            section: The section to build
            data: Data to be used in the section
            indent_level: Current indentation level for formatting
        
        Returns:
            Formatted section text
        """
        # Build section header
        indent = "    " * indent_level
        lines = [f"{indent}# {section.title}"]
        
        # Add section content
        for line in section.content:
            # Replace any placeholders in the line with actual data
            for key, value in data.items():
                placeholder = f"{{{key}}}"
                if placeholder in line:
                    line = line.replace(placeholder, str(value))
            lines.append(f"{indent}{line}")
        
        # Add subsections if any
        if section.subsections:
            for subsection in section.subsections:
                subsection_text = PromptBuilder._build_section(
                    subsection, 
                    data, 
                    indent_level + 1
                )
                lines.append("")  # Add spacing between sections
                lines.append(subsection_text)
        
        return "\n".join(lines)
    
    @staticmethod
    def build_prompt(template: PromptTemplate, data: Dict[str, Any]) -> str:
        """
        Build a complete prompt from a template and data.
        
        Args:
            template: The prompt template to use
            data: Data to be used in the prompt
            
        Returns:
            Complete formatted prompt
        
        Raises:
            ValueError: If required data is missing
        """
        # Validate data
        if not template.validate_data(data):
            missing = [field for field in template.required_data if field not in data]
            raise ValueError(f"Missing required data fields: {', '.join(missing)}")
        
        # Build each section
        sections_text = []
        for section in template.sections:
            section_text = PromptBuilder._build_section(section, data)
            sections_text.append(section_text)
            sections_text.append("")  # Add spacing between main sections
        
        return "\n".join(sections_text)
    
    @staticmethod
    def create_section(
        title: str,
        content: List[str],
        subsections: List[PromptSection] = None
    ) -> PromptSection:
        """Utility method to create a prompt section."""
        return PromptSection(
            title=title,
            content=content,
            subsections=subsections
        )
    
    @staticmethod
    def create_template(
        sections: List[PromptSection],
        required_data: List[str],
        description: str
    ) -> PromptTemplate:
        """Utility method to create a prompt template."""
        return PromptTemplate(
            sections=sections,
            required_data=required_data,
            description=description
        )

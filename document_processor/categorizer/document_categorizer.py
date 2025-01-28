# document_processor/categorizer/document_categorizer.py
from pathlib import Path
import json
from typing import List
import openai
from ..models.document import DocumentSection

class DocumentCategorizer:
    """Categorizes document sections based on content."""
    
    def __init__(self, schema_dir: Path):
        """Initialize with directory containing category schemas."""
        self.schemas = self._load_schemas(schema_dir)
        self.categories = list(self.schemas.keys())
        
    def _load_schemas(self, schema_dir: Path) -> dict:
        schemas = {}
        for schema_file in schema_dir.glob("*.json"):
            with open(schema_file) as f:
                schemas[schema_file.stem] = json.load(f)
        return schemas
    
    def identify_sections(self, text: str) -> List[DocumentSection]:
        """Identifies distinct document sections in text."""
        # Split text into lines for line number tracking
        lines = text.split('\n')
        numbered_text = '\n'.join(f"{i+1}| {line}" for i, line in enumerate(lines))
        
        prompt = """
        Analyze the following text and identify distinct documents within it. Each line is numbered.
        For each document found, provide:
        1. The line numbers where it starts and ends
        2. A brief description of what the document is
        
        Text to analyze:
        {text}
        
        Return in JSON format:
        {{"sections": [
            {{"start_line": int,
              "end_line": int,
              "description": "string"}}
        ]}}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": prompt.format(text=numbered_text)
            }]
        )
        
        result = json.loads(response.choices[0].message.content)
        return [
            DocumentSection(
                content='\n'.join(lines[section["start_line"]-1:section["end_line"]]),
                start_line=section["start_line"],
                end_line=section["end_line"]
            ) 
            for section in result["sections"]
        ]
    
    def categorize_section(self, section: DocumentSection) -> str:
        """Determines the category of a document section."""
        prompt = f"""
        Analyze this document and determine which category it belongs to.
        
        Available categories:
        {self.categories}
        
        Document content:
        {section.content}
        
        Return only the category name that best matches this document.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        category = response.choices[0].message.content.strip()
        if category not in self.categories:
            raise ValueError(f"Invalid category returned by API: {category}")
        
        return category

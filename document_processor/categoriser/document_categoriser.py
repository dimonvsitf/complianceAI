# document_processor/categorizer/document_categorizer.py
from pathlib import Path
import json
from typing import List
import openai
from ..models.document import DocumentSection, ProcessedDocument

class DocumentCategorizer:
    """Categorizes document sections based on content."""
    
    def __init__(self, schema_dir: Path):
        """Initialize with directory containing category schemas."""
        self.schemas = self._load_schemas(schema_dir)
        
    def _load_schemas(self, schema_dir: Path) -> dict:
        schemas = {}
        for schema_file in schema_dir.glob("*.json"):
            with open(schema_file) as f:
                schemas[schema_file.stem] = json.load(f)
        return schemas
    
    def identify_sections(self, text: str) -> List[DocumentSection]:
        """Identifies distinct document sections in text."""
        prompt = """
        Identify distinct documents in this text. For each document found, provide:
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
        
        # Use OpenAI to identify sections
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user", 
                "content": prompt.format(text=text)
            }]
        )
        
        result = json.loads(response.choices[0].message.content)
        return [DocumentSection(
            content=self._extract_section_text(text, section["start_line"], section["end_line"]),
            start_line=section["start_line"],
            end_line=section["end_line"]
        ) for section in result["sections"]]
    
    def categorize_section(self, section: DocumentSection) -> str:
        """Determines the category of a document section."""
        # Implementation details for categorization...
        pass
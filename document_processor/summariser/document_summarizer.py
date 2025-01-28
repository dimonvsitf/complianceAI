# document_processor/summarizer/document_summarizer.py
import openai
import json
from pathlib import Path
from ..models.document import DocumentSection

class DocumentSummarizer:
    """Extracts structured data from document sections based on their category schema."""
    
    def __init__(self, api_key: str, schema_dir: Path):
        """Initialize with OpenAI API key and schema directory."""
        self.api_key = api_key
        openai.api_key = api_key
        self.schemas = self._load_schemas(schema_dir)
    
    def _load_schemas(self, schema_dir: Path) -> dict:
        schemas = {}
        for schema_file in schema_dir.glob("*.json"):
            with open(schema_file) as f:
                schemas[schema_file.stem] = json.load(f)
        return schemas
    
    def summarize_section(self, section: DocumentSection) -> dict:
        """Extract structured data from a document section based on its category schema."""
        if not section.category or section.category not in self.schemas:
            raise ValueError(f"Invalid category: {section.category}")
        
        schema = self.schemas[section.category]
        
        prompt = f"""
        Extract structured information from this document according to the following JSON schema:
        {json.dumps(schema, indent=2)}
        
        Document content:
        {section.content}
        
        Return a JSON object that follows the schema exactly.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse and validate against schema
        result = json.loads(response.choices[0].message.content)
        
        # TODO: Add proper JSON schema validation
        return result
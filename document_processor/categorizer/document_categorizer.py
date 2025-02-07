# document_processor/categorizer/document_categorizer.py
from pathlib import Path
import json
from typing import List
from openai import OpenAI
from ..models.document import DocumentSection

class DocumentCategorizer:
    """Categorizes document sections based on content."""
    
    def __init__(self, schema_dir: Path):
        """Initialize with directory containing category schemas."""
        self.client = OpenAI()
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
        """
        
        messages = [{
            "role": "user", 
            "content": prompt.format(text=numbered_text)
        }]
        print("\nSending to OpenAI (identify_sections):")
        print("Messages:", json.dumps(messages, indent=2))
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            response_format={
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "sections": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "start_line": {"type": "integer"},
                                    "end_line": {"type": "integer"},
                                    "description": {"type": "string"}
                                },
                                "required": ["start_line", "end_line", "description"]
                            }
                        }
                    },
                    "required": ["sections"]
                }
            }
        )
        print("\nOpenAI Response:")
        print(json.dumps(response.model_dump(), indent=2))
        
        try:
            result = json.loads(response.choices[0].message.content)
            if not isinstance(result, dict) or 'sections' not in result:
                return [DocumentSection(content=text, start_line=1, end_line=len(text.split('\n')))]
        except json.JSONDecodeError:
            # If we can't parse the response, treat the entire text as one section
            return [DocumentSection(content=text, start_line=1, end_line=len(text.split('\n')))]
        
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
        
        Available categories (use EXACTLY one of these names):
        {', '.join(self.categories)}
        
        Document content:
        {section.content}
        """
        
        messages = [{"role": "user", "content": prompt}]
        print("\nSending to OpenAI (categorize_section):")
        print("Messages:", json.dumps(messages, indent=2))
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            response_format={
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": self.categories
                        }
                    },
                    "required": ["category"]
                }
            }
        )
        print("\nOpenAI Response:")
        print(json.dumps(response.model_dump(), indent=2))
        
        try:
            result = json.loads(response.choices[0].message.content)
            category = result.get('category', '').strip().lower()
            
            if category not in self.categories:
                # Default to most appropriate category based on content
                if any(keyword in section.content.lower() for keyword in ['license', 'certificate', 'registration']):
                    return 'company_formation'
                elif any(keyword in section.content.lower() for keyword in ['invoice', 'contract', 'agreement']):
                    return 'business_activities'
                elif any(keyword in section.content.lower() for keyword in ['compliance', 'check', 'verification']):
                    return 'compliance_checks'
                elif any(keyword in section.content.lower() for keyword in ['financial', 'statement', 'balance']):
                    return 'financial_documents'
                else:
                    return 'ownership_control'  # default category
            
            return category
        except Exception as e:
            # Default to ownership_control if anything goes wrong
            print(f"\nError parsing category: {e}")
            return 'ownership_control'

# document_processor/__init__.py
from pathlib import Path
from typing import Dict, List
from .extractors import get_extractor #not defined yet
from .categorizer import DocumentCategorizer 
from .summarizer import DocumentSummarizer 
from .models.document import ProcessedDocument 

class DocumentProcessor:
    def __init__(self, api_key: str, schema_dir: Path):
        """Initialize document processor with OpenAI API key and schema directory."""
        self.api_key = api_key
        self.categorizer = DocumentCategorizer(schema_dir)
        self.summarizer = DocumentSummarizer(api_key, schema_dir)

    def process_document(self, file_path: Path) -> ProcessedDocument:
        """Process a single document file."""
        # Get appropriate extractor for file type
        extractor = get_extractor(file_path, self.api_key)
        
        # Extract text
        text = extractor.extract_text(file_path)
        
        # Identify document sections
        sections = self.categorizer.identify_sections(text)
        
        # Categorize each section
        for section in sections:
            section.category = self.categorizer.categorize_section(section)
        
        return ProcessedDocument(
            file_path=str(file_path),
            raw_text=text,
            sections=sections,
            processed_date=datetime.now(),
            original_format=file_path.suffix.lower()[1:]  # Remove the dot from extension
        )

    def extract_structured_data(self, section: DocumentSection) -> dict:
        """Extract structured data from a document section based on its category."""
        return self.summarizer.summarize_section(section)


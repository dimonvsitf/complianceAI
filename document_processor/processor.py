import os
import json
from pathlib import Path
from typing import Dict, List, Optional
from .data_loader import DataLoader
from .categorizer.document_categorizer import DocumentCategorizer
from .summariser.document_summarizer import DocumentSummarizer
from .extractors.pdf_extractor import PDFExtractor
from .extractors.image_extractor import ImageExtractor
from .extractors.text_extractor import TextExtractor
from .extractors.base_extractor import BaseExtractor

class DocumentProcessor:
    """Main class for processing documents through the pipeline."""
    
    def __init__(self, api_key: str, data_dir: Path, schema_dir: Path):
        """Initialize the document processor with necessary components."""
        self.data_dir = data_dir
        self.schema_dir = schema_dir
        self.api_key = api_key
        
        # Initialize components
        self.categorizer = DocumentCategorizer(schema_dir)
        self.summarizer = DocumentSummarizer(api_key, schema_dir)
        self.data_loader = DataLoader(data_dir)
        
        # Initialize extractors
        self.extractors: List[BaseExtractor] = [
            PDFExtractor(api_key),
            ImageExtractor(api_key),
            TextExtractor()
        ]
        
        # Create output directories
        self.text_output_dir = data_dir / 'text_output'
        self.json_output_dir = data_dir / 'json_output'
        self.text_output_dir.mkdir(parents=True, exist_ok=True)
        self.json_output_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_extractor(self, file_path: Path) -> Optional[BaseExtractor]:
        """Get appropriate extractor for the file type."""
        return next(
            (e for e in self.extractors if e.can_handle(file_path)),
            None
        )
    
    def _save_text_output(self, file_path: Path, text: str) -> Path:
        """Save extracted text to output file."""
        output_path = self.text_output_dir / f"{file_path.stem}.txt"
        with open(output_path, 'w') as f:
            f.write(text)
        print(f"Saved text to: {output_path}")
        return output_path
    
    def _save_json_output(self, file_path: Path, data: dict) -> Path:
        """Save processed data to JSON file."""
        output_path = self.json_output_dir / f"{file_path.stem}.json"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved JSON to: {output_path}")
        return output_path
    
    def _load_existing_results(self, file_path: Path) -> Optional[dict]:
        """Load existing processing results if available."""
        text_path = self.text_output_dir / f"{file_path.stem}.txt"
        json_path = self.json_output_dir / f"{file_path.stem}.json"
        
        if text_path.exists() and json_path.exists():
            try:
                with open(json_path) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading JSON for {file_path}")
        return None
    
    def process_file(self, file_path: Path) -> Optional[dict]:
        """Process a single file through the pipeline."""
        # Skip JSON files
        if file_path.suffix.lower() == '.json':
            print(f"Skipping JSON file: {file_path}")
            return None
        
        # Check for existing results
        existing = self._load_existing_results(file_path)
        if existing:
            print(f"Using existing results for: {file_path}")
            return existing
        
        # Get appropriate extractor
        extractor = self._get_extractor(file_path)
        if not extractor:
            print(f"No extractor found for: {file_path}")
            return None
        
        try:
            print(f"\nProcessing: {file_path}")
            
            # Extract text
            text = extractor.extract_text(file_path)
            self._save_text_output(file_path, text)
            
            # Identify and process sections
            sections = self.categorizer.identify_sections(text)
            processed_sections = []
            
            for section in sections:
                # Categorize and summarize section
                category = self.categorizer.categorize_section(section)
                summary = self.summarizer.summarize_section(section)
                
                processed_sections.append({
                    "category": category,
                    "content": summary,
                    "text": section.content,
                    "metadata": {
                        "start_line": section.start_line,
                        "end_line": section.end_line
                    }
                })
            
            # Save results
            result = {
                "source_file": str(file_path),
                "sections": processed_sections
            }
            self._save_json_output(file_path, result)
            return result
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None
    
    def process_directory(self, input_dir: Optional[Path] = None) -> Dict[str, List[dict]]:
        """Process all documents in the input directory."""
        print("Processing documents...")
        
        # Load structured data first
        self.data_loader.load_all()
        
        # Use default input directory if none provided
        if input_dir is None:
            input_dir = self.data_dir / 'input_documents'
        
        if not input_dir.exists():
            raise Exception(f"Input directory not found: {input_dir}")
        
        # Process each file
        processed_docs: Dict[str, List[dict]] = {}
        for file_path in input_dir.glob('*.*'):
            result = self.process_file(file_path)
            if result and 'sections' in result:
                for section in result['sections']:
                    category = section['category']
                    if category not in processed_docs:
                        processed_docs[category] = []
                    processed_docs[category].append(section['content'])
        
        return processed_docs

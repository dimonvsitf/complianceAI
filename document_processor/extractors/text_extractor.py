# document_processor/extractors/text_extractor.py
from pathlib import Path
from .base_extractor import BaseExtractor

class TextExtractor(BaseExtractor):
    """Handles plain text documents."""
    
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in ['.txt', '.md']
    
    def extract_text(self, file_path: Path) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


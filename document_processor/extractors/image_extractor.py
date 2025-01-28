# document_processor/extractors/image_extractor.py
from pathlib import Path
from .base_extractor import BaseExtractor
from .ocr_extractor import OCRExtractor

class ImageExtractor(BaseExtractor):
    """Handles image files using OCR."""
    
    def __init__(self, api_key: str):
        self.ocr_extractor = OCRExtractor(api_key)
    
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']
    
    def extract_text(self, file_path: Path) -> str:
        return self.ocr_extractor.extract_text(file_path)

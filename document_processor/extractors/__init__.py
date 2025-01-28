# document_processor/extractors/__init__.py
from pathlib import Path
from .base_extractor import BaseExtractor
from .text_extractor import TextExtractor
from .pdf_extractor import PDFExtractor
from .image_extractor import ImageExtractor

def get_extractor(file_path: Path, api_key: str) -> BaseExtractor:
    """Factory function to get appropriate extractor for file type."""
    suffix = file_path.suffix.lower()
    
    if suffix == '.pdf':
        return PDFExtractor(api_key)
    elif suffix in ['.jpg', '.jpeg', '.png']:
        return ImageExtractor(api_key)
    elif suffix in ['.txt', '.md']:
        return TextExtractor()
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

# document_processor/extractors/base_extractor.py
from abc import ABC, abstractmethod
from pathlib import Path

class BaseExtractor(ABC):
    """Base class for all document extractors."""
    
    @abstractmethod
    def can_handle(self, file_path: Path) -> bool:
        """Determines if this extractor can handle the given file type."""
        pass
    
    @abstractmethod
    def extract_text(self, file_path: Path) -> str:
        """Extracts text content from the document."""
        pass

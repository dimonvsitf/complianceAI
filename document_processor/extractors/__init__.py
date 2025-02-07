from pathlib import Path
from typing import Type
from .base_extractor import BaseExtractor
from .pdf_extractor import PDFExtractor
from .image_extractor import ImageExtractor
from .text_extractor import TextExtractor

def get_extractor(file_path: Path, api_key: str) -> BaseExtractor:
    """Get appropriate extractor for file type."""
    suffix = file_path.suffix.lower()
    
    if suffix == '.pdf':
        return PDFExtractor(api_key)
    elif suffix in ['.jpg', '.jpeg', '.png']:
        return ImageExtractor(api_key)
    elif suffix in ['.txt', '.md']:
        return TextExtractor()
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

__all__ = ['get_extractor', 'BaseExtractor', 'PDFExtractor', 'ImageExtractor', 'TextExtractor']

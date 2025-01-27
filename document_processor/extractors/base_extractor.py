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
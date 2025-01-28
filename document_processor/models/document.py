# document_processor/models/document.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class DocumentSection:
    """Represents a distinct document section found within a file."""
    content: str
    start_line: int
    end_line: int
    category: Optional[str] = None
    
@dataclass
class ProcessedDocument:
    """Represents a processed document with extracted text and metadata."""
    file_path: str
    raw_text: str
    sections: List[DocumentSection]
    processed_date: datetime
    original_format: str  # pdf, image, text, etc.



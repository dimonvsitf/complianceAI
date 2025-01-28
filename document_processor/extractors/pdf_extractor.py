# document_processor/extractors/pdf_extractor.py
import fitz  # PyMuPDF
from pathlib import Path
from .base_extractor import BaseExtractor
import pytesseract
from PIL import Image
import io

class PDFExtractor(BaseExtractor):
    """Handles PDF documents, including those with images."""
    
    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.pdf'
    
    def extract_text(self, file_path: Path) -> str:
        doc = fitz.open(file_path)
        text_content = []
        
        for page in doc:
            # Extract text directly
            text = page.get_text()
            
            # If page has little to no text, try OCR on the page image
            if len(text.strip()) < 50:  # Arbitrary threshold
                # Convert page to image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                # Perform OCR
                ocr_text = pytesseract.image_to_string(img)
                text_content.append(ocr_text)
            else:
                text_content.append(text)
        
        return "\n\n".join(text_content)
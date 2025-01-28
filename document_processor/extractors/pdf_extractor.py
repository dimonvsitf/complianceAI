# document_processor/extractors/pdf_extractor.py
import fitz
from pathlib import Path
from .base_extractor import BaseExtractor
from .ocr_extractor import OCRExtractor
import io
from PIL import Image

class PDFExtractor(BaseExtractor):
    def __init__(self, api_key: str):
        self.ocr_extractor = OCRExtractor(api_key)
    
    def extract_text(self, file_path: Path) -> str:
        doc = fitz.open(file_path)
        full_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get text directly from PDF
            text = page.get_text()
            
            # If page has little text, it might be an image/scan
            if len(text.strip()) < 50:
                # Convert page to image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Save to temporary file
                temp_img_path = Path(f"temp_page_{page_num}.png")
                img.save(temp_img_path)
                
                # Extract text using OpenAI Vision
                ocr_text = self.ocr_extractor.extract_text(temp_img_path)
                
                # Clean up temp file
                temp_img_path.unlink()
                
                full_text.append(ocr_text)
            else:
                full_text.append(text)
        
        return "\n\n".join(full_text)
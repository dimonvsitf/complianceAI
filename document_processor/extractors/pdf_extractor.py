# document_processor/extractors/pdf_extractor.py
import pdfplumber
from pdf2image import convert_from_path
from pathlib import Path
from .base_extractor import BaseExtractor
from .ocr_extractor import OCRExtractor
import tempfile
import os
from tqdm import tqdm

class PDFExtractor(BaseExtractor):
    def __init__(self, api_key: str):
        self.ocr_extractor = OCRExtractor(api_key)
        
    def can_handle(self, file_path: Path) -> bool:
        """Check if this extractor can handle the given file."""
        return file_path.suffix.lower() == '.pdf'
    
    def extract_text(self, file_path: Path) -> str:
        try:
            # First try extracting with pdfplumber
            with pdfplumber.open(file_path) as pdf:
                pages_text = []
                for page in tqdm(pdf.pages, desc=f"Extracting text from {file_path.name}"):
                    text = page.extract_text() or ""
                    pages_text.append(text)
                
                text = "\n\n".join(pages_text)
            
            # If we got very little text, the PDF might be scanned/image-based
            if len(text.strip()) < 50:
                print(f"\nLittle text found in {file_path.name}, attempting OCR...")
                # Create a temporary directory for image extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Convert PDF to images
                    images = convert_from_path(file_path)
                    
                    # Save images and process with OCR
                    ocr_texts = []
                    for i, image in enumerate(tqdm(images, desc="Processing pages with OCR")):
                        img_path = Path(temp_dir) / f"page_{i+1}.png"
                        image.save(img_path)
                        ocr_text = self.ocr_extractor.extract_text(img_path)
                        ocr_texts.append(ocr_text)
                    
                    text = "\n\n".join(ocr_texts)
            
            return text
            
        except Exception as e:
            print(f"\nError extracting text from PDF: {e}")
            # If pdfplumber fails, fall back to OCR
            return self.ocr_extractor.extract_text(file_path)

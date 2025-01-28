# document_processor/extractors/ocr_extractor.py
import base64
from pathlib import Path
import openai
from PIL import Image
import io

class OCRExtractor:
    """Uses OpenAI's Vision model for text extraction from images."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def image_to_base64(self, image_path: Path) -> str:
        """Convert image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_text(self, image_path: Path) -> str:
        """Extract text from image using OpenAI's Vision model."""
        base64_image = self.image_to_base64(image_path)
        
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract and transcribe ALL text from this image. Include any tables, headers, and footnotes. Maintain the original formatting structure as much as possible."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        
        return response.choices[0].message.content
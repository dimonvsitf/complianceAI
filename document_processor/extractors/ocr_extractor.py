# document_processor/extractors/ocr_extractor.py
import base64
import json
from pathlib import Path
from openai import OpenAI
from PIL import Image
import io

class OCRExtractor:
    """Uses OpenAI's Vision model for text extraction from images."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def image_to_base64(self, image_path: Path) -> str:
        """Convert image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_text(self, image_path: Path) -> str:
        """Extract text from image using OpenAI's Vision model."""
        base64_image = self.image_to_base64(image_path)
        
        messages = [
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
        print(f"\nSending to OpenAI Vision (extract_text for {image_path.name}):")
        print("Messages:", json.dumps([{**msg, "content": [
            content if isinstance(content, str) else {**content, "image_url": {"url": "[BASE64_IMAGE]"}}
            for content in msg["content"]
        ]} for msg in messages], indent=2))
        
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=4096
        )
        print("\nOpenAI Response:")
        print(json.dumps({**response.model_dump(), "choices": [{
            **choice,
            "message": {**choice["message"], "content": choice["message"]["content"][:500] + "..." if len(choice["message"]["content"]) > 500 else choice["message"]["content"]}
        } for choice in response.choices]}, indent=2))
        
        return response.choices[0].message.content

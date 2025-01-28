# report_generator/formatter/reference_manager.py
import re
from typing import Dict, List, Tuple

class ReferenceManager:
    """Manages document references and footnotes in the report."""
    
    def __init__(self):
        self.references: Dict[str, int] = {}
        self.footnotes: List[Tuple[int, str]] = []
    
    def process_text(self, text: str) -> str:
        """
        Processes text to standardize references and create footnotes.
        Converts all document references to numbered footnotes.
        """
        def replace_reference(match):
            doc_ref = match.group(1)
            if doc_ref not in self.references:
                self.references[doc_ref] = len(self.references) + 1
                self.footnotes.append((self.references[doc_ref], doc_ref))
            return f"[^{self.references[doc_ref]}]"
        
        # Replace all document references with footnote numbers
        processed_text = re.sub(r'\[ref:(.*?)\]', replace_reference, text)
        
        # Add footnotes section
        footnotes_text = "\n\n## Footnotes\n\n"
        for number, reference in sorted(self.footnotes):
            footnotes_text += f"[^{number}]: {reference}\n"
        
        return processed_text + footnotes_text
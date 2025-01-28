# report_generator/sections/ownership_section.py
from typing import List
from pathlib import Path
from .base_section import BaseSection

class OwnershipSection(BaseSection):
    @property
    def section_name(self) -> str:
        return "ownership"
    
    @property
    def required_categories(self) -> List[str]:
        return [
            "ownership_control",
            "identity_verification"
        ]

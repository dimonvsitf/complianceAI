# report_generator/sections/compliance_section.py
from typing import List
from pathlib import Path
from .base_section import BaseSection

class ComplianceSection(BaseSection):
    @property
    def section_name(self) -> str:
        return "compliance"
    
    @property
    def required_categories(self) -> List[str]:
        return [
            "compliance_checks",
            "financial_documents"
        ]

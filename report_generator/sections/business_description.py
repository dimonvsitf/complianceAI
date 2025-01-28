# report_generator/sections/business_description.py
from typing import List
from pathlib import Path
from .base_section import BaseSection

class BusinessDescriptionSection(BaseSection):
    @property
    def section_name(self) -> str:
        return "business_description"
    
    @property
    def required_categories(self) -> List[str]:
        return [
            "company_formation",
            "business_activities",
            "financial_documents"
        ]

# report_generator/sections/__init__.py
from .business_description import BusinessDescriptionSection
from .ownership_section import OwnershipSection
from .compliance_section import ComplianceSection

def get_section_generator(section_type: str, api_key: str, templates_dir: Path):
    """Factory function to get appropriate section generator."""
    generators = {
        'business_description': BusinessDescriptionSection,
        'ownership': OwnershipSection,
        'compliance': ComplianceSection
    }
    
    if section_type not in generators:
        raise ValueError(f"Unknown section type: {section_type}")
    
    return generators[section_type](api_key, templates_dir)

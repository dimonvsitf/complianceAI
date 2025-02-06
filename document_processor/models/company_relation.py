from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from .company import Company

@dataclass
class CompanyRelation:
    """Model representing relationships between companies."""
    id: str
    parent_company: Company
    child_company: Company
    relationship_type: str
    notes: Optional[str] = None
    
    @classmethod
    def from_json(cls, data: dict, companies: dict[str, Company]) -> Optional['CompanyRelation']:
        """
        Create a CompanyRelation instance from JSON data.
        
        Args:
            data: The JSON data for the relation
            companies: Dictionary of company_id -> Company objects
        
        Returns:
            CompanyRelation instance if both companies exist, None otherwise
        """
        parent_id = data.get('parentCompanyId')
        child_id = data.get('childCompanyId')
        
        # Skip if either company is missing
        if not (parent_id and child_id):
            return None
            
        parent = companies.get(parent_id)
        child = companies.get(child_id)
        
        # Skip if either company is not found
        if not (parent and child):
            return None
                
        return cls(
            id=data.get('_id', ''),
            parent_company=parent,
            child_company=child,
            relationship_type=data.get('relationshipType', ''),
            notes=data.get('notes')
        )

from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime
from .company import Company
from .person import Person

@dataclass
class Share:
    """Base model for share ownership."""
    id: str
    company_id: str
    percentage: float
    share_type: str
    acquisition_date: Optional[datetime] = None
    notes: Optional[str] = None

@dataclass
class CompanyShare(Share):
    """Model representing shares owned by a company."""
    owner: Company
    
    @classmethod
    def from_json(cls, data: dict, owner: Company) -> 'CompanyShare':
        """Create a CompanyShare instance from JSON data."""
        acquisition_date = None
        if data.get('acquisitionDate'):
            try:
                acquisition_date = datetime.fromisoformat(data['acquisitionDate'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            id=data.get('_id', ''),
            company_id=data.get('companyId', ''),
            percentage=float(data.get('percentage', 0)),
            share_type=data.get('shareType', ''),
            acquisition_date=acquisition_date,
            notes=data.get('notes'),
            owner=owner
        )

@dataclass
class PersonShare(Share):
    """Model representing shares owned by a person."""
    owner: Person
    
    @classmethod
    def from_json(cls, data: dict, owner: Person) -> 'PersonShare':
        """Create a PersonShare instance from JSON data."""
        acquisition_date = None
        if data.get('acquisitionDate'):
            try:
                acquisition_date = datetime.fromisoformat(data['acquisitionDate'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            id=data.get('_id', ''),
            company_id=data.get('companyId', ''),
            percentage=float(data.get('percentage', 0)),
            share_type=data.get('shareType', ''),
            acquisition_date=acquisition_date,
            notes=data.get('notes'),
            owner=owner
        )

def create_share(data: dict, owner: Union[Company, Person]) -> Union[CompanyShare, PersonShare]:
    """Factory function to create appropriate share type based on owner."""
    if isinstance(owner, Company):
        return CompanyShare.from_json(data, owner)
    elif isinstance(owner, Person):
        return PersonShare.from_json(data, owner)
    else:
        raise ValueError(f"Invalid owner type: {type(owner)}")

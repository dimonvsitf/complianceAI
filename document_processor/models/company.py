from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Company:
    """Model representing a company entity."""
    id: str
    name: str
    registration_number: Optional[str] = None
    registration_date: Optional[datetime] = None
    country: Optional[str] = None
    address: Optional[str] = None
    business_type: Optional[str] = None
    status: Optional[str] = None
    
    @classmethod
    def from_json(cls, data: dict) -> 'Company':
        """Create a Company instance from JSON data."""
        registration_date = None
        if data.get('registrationDate'):
            try:
                registration_date = datetime.fromisoformat(data['registrationDate'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            id=data.get('_id', ''),
            name=data.get('name', ''),
            registration_number=data.get('registrationNumber'),
            registration_date=registration_date,
            country=data.get('country'),
            address=data.get('address'),
            business_type=data.get('businessType'),
            status=data.get('status')
        )

from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Person:
    """Model representing an individual person."""
    id: str
    first_name: str
    last_name: str
    nationality: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    passport_number: Optional[str] = None
    address: Optional[str] = None
    position: Optional[str] = None
    
    @classmethod
    def from_json(cls, data: dict) -> 'Person':
        """Create a Person instance from JSON data."""
        date_of_birth = None
        if data.get('dateOfBirth'):
            try:
                date_of_birth = datetime.fromisoformat(data['dateOfBirth'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass
                
        return cls(
            id=data.get('_id', ''),
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', ''),
            nationality=data.get('nationality'),
            date_of_birth=date_of_birth,
            passport_number=data.get('passportNumber'),
            address=data.get('address'),
            position=data.get('position')
        )

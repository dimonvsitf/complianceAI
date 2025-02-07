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
        # Get ID from MongoDB ObjectId format
        person_id = str(data.get('_id', {}).get('$oid', '')) if isinstance(data.get('_id'), dict) else str(data.get('_id', ''))
        
        # Get date of birth
        date_of_birth = None
        if data.get('dob', {}).get('$date'):
            try:
                if isinstance(data['dob']['$date'], dict) and '$numberLong' in data['dob']['$date']:
                    # Handle timestamp in milliseconds
                    timestamp_ms = int(data['dob']['$date']['$numberLong'])
                    date_of_birth = datetime.fromtimestamp(timestamp_ms / 1000)
                else:
                    # Handle ISO date string
                    date_of_birth = datetime.fromisoformat(data['dob']['$date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError, TypeError):
                pass

        # Get address from addresses array if available
        address = None
        if data.get('addresses'):
            personal_address = next((addr for addr in data['addresses'] if addr.get('type') == 'personal'), None)
            if personal_address:
                address_parts = [
                    personal_address.get('streetAddress1', ''),
                    personal_address.get('streetAddress2', ''),
                    personal_address.get('town', ''),
                    personal_address.get('country', ''),
                    personal_address.get('postcode', '')
                ]
                address = ', '.join(part for part in address_parts if part)

        # Get position from roles
        position = None
        if data.get('roles'):
            position = ', '.join(data['roles'])

        # Get passport number from document data
        passport_number = None
        if data.get('passportOrIdDocument', {}).get('documentNumber'):
            passport_number = data['passportOrIdDocument']['documentNumber']
        elif data.get('videoIdentDocument', {}).get('documentNumber'):
            passport_number = data['videoIdentDocument']['documentNumber']

        return cls(
            id=person_id,
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', ''),
            nationality=data.get('citizenship'),  # Using citizenship as nationality
            date_of_birth=date_of_birth,
            passport_number=passport_number,
            address=address,
            position=position
        )

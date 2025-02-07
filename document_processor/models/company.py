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
        if data.get('companyRegDate', {}).get('$date'):
            try:
                registration_date = datetime.fromisoformat(data['companyRegDate']['$date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                pass

        # Get address from addresses array if available
        address = None
        if data.get('addresses'):
            legal_address = next((addr for addr in data['addresses'] if addr.get('type') == 'legal'), None)
            if legal_address:
                address_parts = [
                    legal_address.get('streetAddress1', ''),
                    legal_address.get('streetAddress2', ''),
                    legal_address.get('town', ''),
                    legal_address.get('country', ''),
                    legal_address.get('postcode', '')
                ]
                address = ', '.join(part for part in address_parts if part)

        # Get ID from MongoDB ObjectId format
        company_id = str(data.get('_id', {}).get('$oid', '')) if isinstance(data.get('_id'), dict) else str(data.get('_id', ''))
                
        return cls(
            id=company_id,
            name=data.get('companyName', ''),
            registration_number=data.get('regNumber'),
            registration_date=registration_date,
            country=data.get('country'),
            address=address,
            business_type=data.get('businessType'),
            status=data.get('status')
        )

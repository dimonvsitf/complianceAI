from pathlib import Path
from typing import Dict, List, Any, Optional
from .generator import ReportGenerator

class ReportProcessor:
    """Main class for generating reports from processed documents."""
    
    def __init__(self, api_key: str, templates_dir: Path, output_dir: Path):
        """Initialize the report processor."""
        self.generator = ReportGenerator(api_key, templates_dir)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _prepare_company_info(self, company_data: Any) -> dict:
        """Prepare company information for report generation."""
        return {
            "name": company_data.name if hasattr(company_data, 'name') else company_data["name"],
            "legal_structure": company_data.legal_structure if hasattr(company_data, 'legal_structure') else company_data["legal_structure"],
            "incorporation_date": company_data.registration_date if hasattr(company_data, 'registration_date') else company_data["incorporation_date"],
            "incorporation_place": company_data.country if hasattr(company_data, 'country') else company_data["incorporation_place"],
            "registration_numbers": [company_data.registration_number] if hasattr(company_data, 'registration_number') and company_data.registration_number else [],
            "address": company_data.address if hasattr(company_data, 'address') else company_data["address"],
            "business_activities": [],  # Populated from processed documents
            "client_information": {
                "typical_clients": [],
                "locations": [],
                "acquisition": ""
            },
            "operations_details": {
                "international": [],
                "local": {},
                "suppliers": []
            },
            "regulatory_status": {
                "licenses": [],
                "certifications": [],
                "tax_status": {}
            }
        }
    
    def _prepare_person_info(self, persons: List[Any]) -> List[dict]:
        """Prepare person information for report generation."""
        return [{
            "name": f"{p.first_name} {p.last_name}",
            "role": p.position,
            "nationality": p.nationality,
            "identification": p.passport_number
        } for p in persons] if persons else []
    
    def _prepare_transaction_info(self, transactions: List[dict]) -> List[dict]:
        """Prepare transaction information for report generation."""
        return [{
            "type": t.get("type", ""),
            "amount": t.get("amount", 0),
            "currency": t.get("currency", ""),
            "date": t.get("date", ""),
            "counterparty": t.get("counterparty", "")
        } for t in transactions]
    
    def prepare_report_data(
        self,
        processed_docs: Dict[str, List[dict]],
        company_data: Any,
        persons: List[Any],
        transactions: List[dict]
    ) -> dict:
        """Prepare all data needed for report generation."""
        # Prepare basic information
        company_info = self._prepare_company_info(company_data)
        person_info = self._prepare_person_info(persons)
        transaction_info = self._prepare_transaction_info(transactions)
        
        # Enhance with processed document information
        if processed_docs.get('business_activities'):
            company_info['business_activities'] = processed_docs['business_activities']
        
        # TODO: Add more document information processing
        
        return {
            "company_data": company_info,
            "person_data": person_info,
            "transaction_data": transaction_info
        }
    
    def generate_report(
        self,
        processed_docs: Dict[str, List[dict]],
        company_data: Any,
        persons: List[Any],
        transactions: List[dict]
    ) -> Dict[str, str]:
        """Generate a complete report with all sections."""
        print("\nGenerating EDD report...")
        
        # Prepare report data
        report_data = self.prepare_report_data(
            processed_docs,
            company_data,
            persons,
            transactions
        )
        
        # Generate report sections
        sections = self.generator.generate_full_report(
            report_data["company_data"],
            report_data["person_data"],
            report_data["transaction_data"],
            self.output_dir
        )
        
        print("\nReport generation complete!")
        return sections

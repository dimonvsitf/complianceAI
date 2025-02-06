import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from .models.company import Company
from .models.person import Person
from .models.share import CompanyShare, PersonShare, create_share
from .models.company_relation import CompanyRelation

class DataLoader:
    """Handles loading and processing of structured data files."""
    
    def __init__(self, data_dir: Path):
        """Initialize with directory containing data files."""
        self.data_dir = data_dir
        self.companies: Dict[str, Company] = {}
        self.persons: Dict[str, Person] = {}
        self.company_shares: List[CompanyShare] = []
        self.person_shares: List[PersonShare] = []
        self.transactions: List[dict] = []
        self.company_relations: List[CompanyRelation] = []
        
    def _load_json(self, filename: str) -> List[dict]:
        """Load and parse a JSON file."""
        file_path = self.data_dir / filename
        if not file_path.exists():
            return []
        with open(file_path, 'r') as f:
            return json.load(f)
            
    def load_all(self) -> None:
        """Load all data files and process them."""
        # Load companies first
        company_data = self._load_json('backoffice_prod.companies.json')
        for data in company_data:
            company = Company.from_json(data)
            self.companies[company.id] = company
            
        # Load persons
        person_data = self._load_json('backoffice_prod.companyPersons.json')
        for data in person_data:
            person = Person.from_json(data)
            self.persons[person.id] = person
            
        # Load company shares
        company_share_data = self._load_json('backoffice_prod.companyShares.json')
        for data in company_share_data:
            owner_id = data.get('ownerId')
            if owner_id and owner_id in self.companies:
                share = create_share(data, self.companies[owner_id])
                self.company_shares.append(share)
                
        # Load person shares
        person_share_data = self._load_json('backoffice_prod.companyPersonShares.json')
        for data in person_share_data:
            owner_id = data.get('ownerId')
            if owner_id and owner_id in self.persons:
                share = create_share(data, self.persons[owner_id])
                self.person_shares.append(share)
                
        # Load transactions
        self.transactions = self._load_json('backoffice_prod.companyTransactions.json')
        
        # Load company relations
        relation_data = self._load_json('backoffice_prod.companyRelations.json')
        for data in relation_data:
            relation = CompanyRelation.from_json(data, self.companies)
            if relation:
                self.company_relations.append(relation)
        
    def get_company_by_id(self, company_id: str) -> Optional[Company]:
        """Get a company by its ID."""
        return self.companies.get(company_id)
        
    def get_person_by_id(self, person_id: str) -> Optional[Person]:
        """Get a person by their ID."""
        return self.persons.get(person_id)
        
    def get_shares_for_company(self, company_id: str) -> List[Union[CompanyShare, PersonShare]]:
        """Get all shares (both company and person) for a given company."""
        return [
            *[share for share in self.company_shares if share.company_id == company_id],
            *[share for share in self.person_shares if share.company_id == company_id]
        ]
        
    def get_transactions_for_company(self, company_id: str) -> List[dict]:
        """Get all transactions for a given company."""
        return [
            transaction for transaction in self.transactions 
            if transaction.get('companyId') == company_id
        ]
        
    def get_company_relations(self, company_id: str) -> Dict[str, List[CompanyRelation]]:
        """Get all parent and child relations for a given company."""
        return {
            'parent_relations': [
                relation for relation in self.company_relations 
                if relation.child_company.id == company_id
            ],
            'child_relations': [
                relation for relation in self.company_relations 
                if relation.parent_company.id == company_id
            ]
        }

# main.py
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from document_processor.data_loader import DataLoader
from report_generator.generator import ReportGenerator
from typing import Dict, List, Any
import json

def process_documents(input_dir: Path, processor: DocumentProcessor, data_loader: DataLoader) -> Dict[str, List[dict]]:
    """Process all documents in the input directory."""
    processed_docs: Dict[str, List[dict]] = {}
    
    # Load structured data first
    data_loader.load_all()
    
    # Process each file in the input directory
    for file_path in input_dir.glob("*.*"):
        try:
            # Skip non-supported files
            if file_path.suffix.lower() not in ['.pdf', '.txt', '.jpg', '.jpeg', '.png']:
                continue
            
            print(f"Processing {file_path.name}...")
            
            # Process document
            doc = processor.process_document(file_path)
            
            # Extract structured data from each section
            for section in doc.sections:
                if section.category:
                    if section.category not in processed_docs:
                        processed_docs[section.category] = []
                    
                    structured_data = processor.extract_structured_data(section)
                    structured_data['source_file'] = str(file_path)
                    processed_docs[section.category].append(structured_data)
        
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
            continue
    
    return processed_docs

def prepare_report_data(
    processed_docs: Dict[str, List[dict]],
    data_loader: DataLoader
) -> Dict[str, Dict[str, Any]]:
    """Prepare data for report generation."""
    # Get company data
    company_data = next(iter(data_loader.companies.values()))  # Get first company for now
    company_info = {
        "name": company_data.name,
        "legal_structure": "Limited Liability Company",  # This should come from actual data
        "incorporation_date": company_data.registration_date,
        "incorporation_place": company_data.country,
        "registration_numbers": [company_data.registration_number] if company_data.registration_number else [],
        "address": company_data.address,
        "website": "",  # Should come from actual data
        "business_activities": processed_docs.get("business_activities", []),
        "international_operations": [],  # Should come from actual data
        "local_operations": {},  # Should come from actual data
        "suppliers": []  # Should come from actual data
    }
    
    # Get person data
    person_info = {
        "key_personnel": [
            {
                "name": f"{person.first_name} {person.last_name}",
                "role": person.position,
                "nationality": person.nationality
            }
            for person in data_loader.persons.values()
        ]
    }
    
    # Get transaction data
    transaction_info = {
        "transactions": data_loader.transactions
    }
    
    return {
        "company_data": company_info,
        "person_data": person_info,
        "transaction_data": transaction_info
    }

async def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Setup paths
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input_documents"
    schema_dir = base_dir / "document_processor" / "categorizer" / "schemas"
    templates_dir = base_dir / "report_generator" / "templates"
    output_dir = base_dir / "output"
    data_dir = base_dir / "data"  # Directory for JSON data files
    
    # Create directories if they don't exist
    for directory in [input_dir, output_dir, data_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    processor = DocumentProcessor(api_key, schema_dir)
    data_loader = DataLoader(data_dir)
    report_generator = ReportGenerator(api_key, templates_dir)
    
    try:
        # Process all documents
        print("Processing documents...")
        processed_docs = process_documents(input_dir, processor, data_loader)
        
        # Save processed data for review
        with open(output_dir / "processed_data.json", "w") as f:
            json.dump(processed_docs, f, indent=2)
        
        # Prepare data for report generation
        report_data = prepare_report_data(processed_docs, data_loader)
        
        # Generate report
        print("Generating EDD report...")
        sections = await report_generator.generate_full_report(
            report_data["company_data"],
            report_data["person_data"],
            report_data["transaction_data"],
            output_dir
        )
        
        print("Report generated successfully!")
        print(f"Output files are in: {output_dir}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())

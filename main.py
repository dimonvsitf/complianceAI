import os
from pathlib import Path
from dotenv import load_dotenv
from document_processor.processor import DocumentProcessor
from report_generator.report_processor import ReportProcessor

def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    # Initialize paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / 'data'
    schema_dir = base_dir / 'document_processor' / 'categorizer' / 'schemas'
    templates_dir = base_dir / 'report_generator' / 'templates'
    output_dir = data_dir / 'output'
    
    try:
        # Initialize processors
        doc_processor = DocumentProcessor(api_key, data_dir, schema_dir)
        report_processor = ReportProcessor(api_key, templates_dir, output_dir)
        
        # Process documents
        processed_docs = doc_processor.process_directory()
        
        # Generate report
        sections = report_processor.generate_report(
            processed_docs,
            next(iter(doc_processor.data_loader.companies.values())) if doc_processor.data_loader.companies else {
                "name": "INPLACE SOFTWARE MIDDLE EAST",
                "legal_structure": "Limited Liability Company",
                "incorporation_date": None,
                "incorporation_place": "UAE",
                "registration_number": None,
                "address": None
            },
            list(doc_processor.data_loader.persons.values()),
            doc_processor.data_loader.transactions
        )
        
        return sections
        
    except Exception as e:
        print(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()

# main.py
import os
from pathlib import Path
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from report_generator import ReportGenerator
from typing import Dict, List
import json

def process_documents(input_dir: Path, processor: DocumentProcessor) -> Dict[str, List[dict]]:
    """Process all documents in the input directory."""
    processed_docs: Dict[str, List[dict]] = {}
    
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

def main():
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
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Initialize processors
    processor = DocumentProcessor(api_key, schema_dir)
    report_generator = ReportGenerator(api_key, templates_dir)
    
    try:
        # Process all documents
        print("Processing documents...")
        processed_docs = process_documents(input_dir, processor)
        
        # Save processed data for review
        with open(output_dir / "processed_data.json", "w") as f:
            json.dump(processed_docs, f, indent=2)
        
        # Generate report
        print("Generating EDD report...")
        report = report_generator.generate_report(processed_docs)
        
        # Save report
        with open(output_dir / "edd_report.md", "w") as f:
            f.write(report)
        
        print("Report generated successfully!")
        print(f"Output files are in: {output_dir}")
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    main()
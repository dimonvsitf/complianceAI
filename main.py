# main.py
from pathlib import Path
from document_processor import DocumentProcessor
from report_generator import ReportGenerator

def process_documents(input_dir: Path) -> Dict[str, List[dict]]:
    """Process all documents in the input directory."""
    processor = DocumentProcessor()
    processed_docs = {}
    
    for file_path in input_dir.glob("*"):
        # Process each document
        doc = processor.process_document(file_path)
        
        # Group processed sections by category
        for section in doc.sections:
            if section.category not in processed_docs:
                processed_docs[section.category] = []
            processed_docs[section.category].append(
                processor.extract_structured_data(section)
            )
    
    return processed_docs

def generate_report(processed_docs: Dict[str, List[dict]], output_path: Path):
    """Generate the EDD report from processed documents."""
    generator = ReportGenerator()
    report = generator.generate_report(processed_docs)
    
    # Save the report
    output_path.write_text(report)

if __name__ == "__main__":
    input_dir = Path("input_documents")
    output_path = Path("output/edd_report.md")
    
    # Process all documents
    processed_docs = process_documents(input_dir)
    
    # Generate report
    generate_report(processed_docs, output_path)
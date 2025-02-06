# Enhanced Due Diligence Report Generator

A Python implementation of an Enhanced Due Diligence (EDD) report generator that processes various document types and generates structured reports using AI.

## Features

- Document processing for multiple file types (PDF, images, text)
- OCR capabilities for scanned documents using OpenAI's Vision API
- Structured data extraction and categorization
- AI-powered report generation using GPT-4
- Modular prompt engineering system
- Asynchronous processing for improved performance

## Project Structure

```
python-version/
├── document_processor/          # Document processing components
│   ├── categorizer/            # Document categorization
│   ├── extractors/             # File type specific extractors
│   ├── models/                 # Data models
│   └── summariser/             # Document summarization
├── report_generator/           # Report generation components
│   ├── prompts/               # Prompt engineering system
│   ├── sections/              # Report section generators
│   └── templates/             # Report templates
├── input_documents/           # Directory for input files
├── output/                    # Generated reports and data
└── data/                      # Structured data files
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

## Usage

1. Place input documents in the `input_documents` directory

2. Run the processor:
   ```bash
   python main.py
   ```

3. Find generated reports in the `output` directory

## Document Processing Pipeline

1. **Document Loading**
   - Supports PDF, images (JPG, PNG), and text files
   - OCR for scanned documents using OpenAI's Vision API

2. **Data Extraction**
   - Text extraction from various file types
   - Structured data parsing from JSON files
   - Company and person information processing

3. **Document Categorization**
   - AI-powered document type identification
   - Category-specific data extraction
   - Structured data organization

4. **Report Generation**
   - Template-based report structure
   - AI-powered content generation
   - Markdown formatting
   - Source citation and footnotes

## Prompt Engineering System

The project uses a sophisticated prompt engineering system that:

1. Builds structured prompts from modular components
2. Maintains consistent formatting and style
3. Ensures comprehensive data inclusion
4. Handles citations and references
5. Validates output quality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

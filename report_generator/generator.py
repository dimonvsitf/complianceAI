import json
from pathlib import Path
from typing import Dict, Any, Optional
from openai import OpenAI
from .prompts.builder import PromptBuilder
from .prompts.types import PromptTemplate
from .prompts.sections import business_description

class ReportGenerator:
    """Handles generation of report sections using OpenAI's API."""
    
    def __init__(self, api_key: str, templates_dir: Path):
        """
        Initialize the report generator.
        
        Args:
            api_key: OpenAI API key
            templates_dir: Directory containing templates and prompts
        """
        self.client = OpenAI(api_key=api_key)
        self.templates_dir = templates_dir
        
    async def _generate_content(self, prompt: str, model: str = "gpt-4") -> str:
        """
        Generate content using OpenAI's API.
        
        Args:
            prompt: The complete prompt to send
            model: The model to use (default: gpt-4)
            
        Returns:
            Generated content
        """
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a compliance and due diligence expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")
    
    def _prepare_business_description_data(
        self,
        company_data: Dict[str, Any],
        person_data: Dict[str, Any],
        transaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare data for business description template."""
        return {
            "company_name": company_data.get("name", ""),
            "legal_structure": company_data.get("legal_structure", ""),
            "incorporation_details": {
                "date": company_data.get("incorporation_date", ""),
                "place": company_data.get("incorporation_place", "")
            },
            "registration_numbers": company_data.get("registration_numbers", []),
            "address": company_data.get("address", ""),
            "website": company_data.get("website", ""),
            "business_activities": company_data.get("business_activities", []),
            "client_information": {
                "typical_clients": company_data.get("typical_clients", []),
                "locations": company_data.get("client_locations", []),
                "acquisition": company_data.get("client_acquisition", "")
            },
            "operations_details": {
                "international": company_data.get("international_operations", []),
                "local": company_data.get("local_operations", {}),
                "suppliers": company_data.get("suppliers", [])
            },
            "regulatory_status": {
                "licenses": company_data.get("licenses", []),
                "certifications": company_data.get("certifications", []),
                "tax_status": company_data.get("tax_status", {})
            }
        }
    
    async def generate_business_description(
        self,
        company_data: Dict[str, Any],
        person_data: Dict[str, Any],
        transaction_data: Dict[str, Any],
        output_path: Optional[Path] = None
    ) -> str:
        """
        Generate the business description section.
        
        Args:
            company_data: Company information
            person_data: Person information
            transaction_data: Transaction information
            output_path: Optional path to save the output
            
        Returns:
            Generated business description
        """
        # Prepare data
        data = self._prepare_business_description_data(
            company_data,
            person_data,
            transaction_data
        )
        
        # Get template and build prompt
        template = business_description.create_business_description_template()
        prompt = PromptBuilder.build_prompt(template, data)
        
        # Generate content
        content = await self._generate_content(prompt)
        
        # Save if output path provided
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(content)
        
        return content
    
    async def generate_full_report(
        self,
        company_data: Dict[str, Any],
        person_data: Dict[str, Any],
        transaction_data: Dict[str, Any],
        output_dir: Path
    ) -> Dict[str, str]:
        """
        Generate a complete report with all sections.
        
        Args:
            company_data: Company information
            person_data: Person information
            transaction_data: Transaction information
            output_dir: Directory to save report sections
            
        Returns:
            Dictionary mapping section names to their content
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        sections = {}
        
        # Generate business description
        sections['business_description'] = await self.generate_business_description(
            company_data,
            person_data,
            transaction_data,
            output_dir / 'business_description.md'
        )
        
        # TODO: Add other section generators (ownership, compliance, etc.)
        
        # Save full report
        full_report = "\n\n".join(sections.values())
        with open(output_dir / 'full_report.md', 'w') as f:
            f.write(full_report)
        
        return sections

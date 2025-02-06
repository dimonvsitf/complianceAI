from typing import List
from ..types import PromptSection, PromptTemplate
from ..builder import PromptBuilder
from .. import common

def create_business_description_structure() -> PromptSection:
    """Create the business description structure section."""
    return PromptBuilder.create_section(
        title="Structure the Business Description",
        content=["Document should have a title 'Business Activity'"],
        subsections=[
            PromptBuilder.create_section(
                title="Introduction",
                content=[
                    "Format the following in a table of key-value pairs, with the first column containing the following keys",
                    "",
                    "- **Company's Full Legal Name**",
                    "- **Legal Structure:** (Corporation, LLC, Partnership, etc.)",
                    "- **Date and Place of Incorporation**",
                    "- **Registration Number(s)**",
                    "- **Regulatory License(s)**",
                    "- **Registered Address and Contact Information**",
                    "- **Company Website**",
                    "",
                    "and the second column containing values specific to the applicant company"
                ]
            ),
            PromptBuilder.create_section(
                title="Business Description",
                content=[
                    "**Primary Business Activities:**",
                    "- Detailed description of products or services",
                    "- Industry sector and sub-sector(s)",
                    "",
                    "**Client Information:**",
                    "- Typical clients and their locations",
                    "- Client acquisition strategy",
                    "- Payment patterns and transaction types",
                    "",
                    "**Operations:**",
                    "- International operations and presence",
                    "- Local operations and economic substance",
                    "- Key suppliers and contractors",
                    "",
                    "**Regulatory and Compliance:**",
                    "- Applicable regulations and licenses",
                    "- Industry standards and certifications",
                    "- Tax compliance status",
                    "",
                    "**Account Purpose:**",
                    "- Purpose of opening account",
                    "- Expected transaction patterns",
                    "- Business expansion plans",
                    "",
                    "Note: Do NOT mention the assigned risk level or score in this section."
                ]
            )
        ]
    )

def create_business_description_template() -> PromptTemplate:
    """Create the complete business description template."""
    sections = [
        PromptBuilder.create_section(
            title="Instructions",
            content=[
                "As an AI assistant specializing in compliance and due diligence, your task is to",
                "**generate the Business Description section of an Enhanced Due Diligence (EDD) report**",
                "for a specific applicant company. This section should provide a comprehensive,",
                "accurate, and engaging overview of the company, based on the provided data and documents."
            ]
        ),
        common.create_data_integration(),
        create_business_description_structure(),
        common.create_writing_guidelines(),
        common.create_data_verification(),
        common.create_footnotes(),
        common.create_final_review(),
        common.create_reminder("Business Description"),
        common.create_important_notes()
    ]
    
    required_data = [
        "company_name",
        "legal_structure",
        "incorporation_details",
        "registration_numbers",
        "address",
        "website",
        "business_activities",
        "client_information",
        "operations_details",
        "regulatory_status"
    ]
    
    return PromptTemplate(
        sections=sections,
        required_data=required_data,
        description="Template for generating the business description section of an EDD report"
    )

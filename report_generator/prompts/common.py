from typing import List
from .types import PromptSection
from .builder import PromptBuilder

def create_writing_guidelines() -> PromptSection:
    """Create the writing guidelines section."""
    return PromptBuilder.create_section(
        title="Writing Guidelines",
        content=[
            "**Formatting:**",
            "- Use markdown formatting.",
            "- For document title use heading 2 (`##`), and subsequent headings for subsections",
            "- Do not provide numbers for headings",
            "",
            "**Clarity and Precision:**",
            "- Use clear, concise, and professional language.",
            "- Avoid vague statements; provide specific details.",
            "",
            "**Consistency:**",
            "- Ensure names, dates, and figures are consistent throughout.",
            "",
            "**Objectivity:**",
            "- Present factual information without personal opinions or biases.",
            "",
            "**Professional Tone:**",
            "- Maintain a formal writing style suitable for compliance reports.",
            "",
            "**Confidentiality:**",
            "- Handle all information securely, respecting data protection regulations."
        ]
    )

def create_data_integration() -> PromptSection:
    """Create the data integration guidelines section."""
    return PromptBuilder.create_section(
        title="Data Integration Guidelines",
        content=[
            "When analyzing and integrating the provided data:",
            "",
            "- Cross-reference information from different sources",
            "- Identify and resolve any inconsistencies",
            "- Ensure all key information is included",
            "- Maintain data accuracy and completeness",
            "- Follow a logical flow of information"
        ]
    )

def create_data_verification() -> PromptSection:
    """Create the data verification requirements section."""
    return PromptBuilder.create_section(
        title="Data Verification Requirements",
        content=[
            "Before finalizing the section:",
            "",
            "- Verify all facts and figures",
            "- Check consistency of names and dates",
            "- Ensure all required information is included",
            "- Validate any calculations or numerical data",
            "- Confirm source document references"
        ]
    )

def create_footnotes() -> PromptSection:
    """Create the footnotes handling section."""
    return PromptBuilder.create_section(
        title="Footnotes and References",
        content=[
            "For citations and references:",
            "",
            "- Use footnotes for source citations",
            "- Reference specific documents when stating facts",
            "- Include document names and dates in footnotes",
            "- Maintain consistent footnote formatting",
            "- Ensure all key statements are properly sourced"
        ]
    )

def create_final_review() -> PromptSection:
    """Create the final review checklist section."""
    return PromptBuilder.create_section(
        title="Final Review Checklist",
        content=[
            "Before submitting, verify:",
            "",
            "- All required information is included",
            "- Formatting is consistent and correct",
            "- All statements are properly sourced",
            "- No confidential information is exposed",
            "- Language is clear and professional",
            "- No spelling or grammatical errors"
        ]
    )

def create_data_provided(data: dict) -> PromptSection:
    """Create the data provided section."""
    content = ["The following data is provided for analysis:"]
    for key, value in data.items():
        content.append(f"- {key}: {value}")
    
    return PromptBuilder.create_section(
        title="Data Provided",
        content=content
    )

def create_important_notes() -> PromptSection:
    """Create the important notes section."""
    return PromptBuilder.create_section(
        title="Important Notes",
        content=[
            "Remember to:",
            "",
            "- Focus on factual information",
            "- Maintain professional tone",
            "- Be specific and detailed",
            "- Avoid speculation or assumptions",
            "- Highlight any significant gaps in information"
        ]
    )

def create_reminder(section_name: str) -> PromptSection:
    """Create a section-specific reminder."""
    return PromptBuilder.create_section(
        title=f"{section_name} Reminder",
        content=[
            f"When creating the {section_name}:",
            "",
            "- Follow all formatting guidelines",
            "- Include all required information",
            "- Maintain professional language",
            "- Ensure factual accuracy",
            "- Provide proper citations"
        ]
    )

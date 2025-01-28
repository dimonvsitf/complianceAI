# report_generator/formatter/markdown_formatter.py
class MarkdownFormatter:
    """Handles markdown formatting and cleanup."""
    
    def format(self, content: str) -> str:
        """Format and clean up markdown content."""
        # Ensure consistent header formatting
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Fix header formatting
            if line.strip().startswith('#'):
                # Remove extra spaces after #
                parts = line.split('#')
                level = len(parts[0]) + 1
                text = parts[-1].strip()
                formatted_lines.append(f"{'#' * level} {text}")
            else:
                formatted_lines.append(line)
        
        # Ensure single blank line between sections
        content = '\n'.join(formatted_lines)
        while '\n\n\n' in content:
            content = content.replace('\n\n\n', '\n\n')
        
        return content

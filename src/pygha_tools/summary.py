import os
from typing import TextIO, Optional, List, Union, TYPE_CHECKING
from .enums import TextStyle, HeadingKind

if TYPE_CHECKING:
    from .text import Text
    from .link import Link


class Summary:
    """Handles GitHub Actions step summary output using builder pattern."""
    
    def __init__(self):
        """Initialize Summary by opening the GITHUB_STEP_SUMMARY file."""
        summary_path = os.environ.get('GITHUB_STEP_SUMMARY')
        if not summary_path:
            raise ValueError("GITHUB_STEP_SUMMARY environment variable is not set")
        
        self.doc: TextIO = open(summary_path, 'a')
        self._lines: List[str] = []
    
    def addText(self, text: str, style: TextStyle, id: Optional[str] = None) -> 'Summary':
        """
        Add styled text to the summary buffer.
        
        Args:
            text: The text content to add
            style: The style to apply (BOLD, ITALIC, or UNDERLINED)
            id: Optional HTML id attribute for the text
        
        Returns:
            Self for method chaining
        """
        if style == TextStyle.BOLD:
            markdown_text = f"**{text}**"
        elif style == TextStyle.ITALIC:
            markdown_text = f"*{text}*"
        elif style == TextStyle.UNDERLINED:
            markdown_text = f"<u>{text}</u>"
        else:
            markdown_text = text
        
        if id:
            markdown_text = f'<span id="{id}">{markdown_text}</span>'
        
        self._lines.append(markdown_text)
        return self
    
    def addHeading(self, text: str, kind: HeadingKind, id: Optional[str] = None) -> 'Summary':
        """
        Add a heading to the summary buffer.
        
        Args:
            text: The heading text
            kind: The heading level (H1 through H6, or SETEXT1/SETEXT2)
            id: Optional HTML id attribute for the heading
        
        Returns:
            Self for method chaining
        """
        if kind == HeadingKind.SETEXT1:
            markdown_heading = f"{text}\n{'=' * len(text)}"
        elif kind == HeadingKind.SETEXT2:
            markdown_heading = f"{text}\n{'-' * len(text)}"
        else:
            heading_prefix = '#' * kind.value
            markdown_heading = f"{heading_prefix} {text}"
        
        if id:
            # For setext headers, wrap the entire block
            if kind in (HeadingKind.SETEXT1, HeadingKind.SETEXT2):
                lines = markdown_heading.split('\n')
                markdown_heading = f'<span id="{id}">\n{lines[0]}\n{lines[1]}\n</span>'
            else:
                markdown_heading = f'<span id="{id}">{markdown_heading}</span>'
        
        self._lines.append(markdown_heading)
        return self
    
    def addCode(self, code: str, language: Optional[str] = None) -> 'Summary':
        """
        Add a code block to the summary buffer.
        
        Args:
            code: The code content
            language: Optional language identifier for syntax highlighting
        
        Returns:
            Self for method chaining
        """
        lang = language if language else ""
        markdown_code = f"```{lang}\n{code}\n```"
        self._lines.append(markdown_code)
        return self
    
    def addLink(self, text: str, url: str, title: Optional[str] = None, style: Optional[TextStyle] = None) -> 'Summary':
        """
        Add a link to the summary buffer.
        
        Args:
            text: The link text to display
            url: The URL to link to
            title: Optional title attribute for the link
            style: Optional style to apply to the link text (BOLD, ITALIC, or UNDERLINED)
        
        Returns:
            Self for method chaining
        """
        # Apply styling to the link text if style is provided
        styled_text = text
        if style == TextStyle.BOLD:
            styled_text = f"**{text}**"
        elif style == TextStyle.ITALIC:
            styled_text = f"*{text}*"
        elif style == TextStyle.UNDERLINED:
            styled_text = f"<u>{text}</u>"
        
        if title:
            markdown_link = f'[{styled_text}]({url} "{title}")'
        else:
            markdown_link = f'[{styled_text}]({url})'
        
        self._lines.append(markdown_link)
        return self
    
    def addTable(self, data: List[List[Union[str, 'Text', 'Link']]]) -> 'Summary':
        """
        Add a table to the summary buffer.
        
        Args:
            data: List of lists where first row is the header and subsequent rows are data.
                  All rows must have the same number of columns.
                  Cells can be strings, Text objects, or Link objects.
        
        Returns:
            Self for method chaining
        
        Raises:
            ValueError: If data is empty or if rows have inconsistent column counts
        """
        if not data:
            raise ValueError("Table data cannot be empty")
        
        if len(data) < 1:
            raise ValueError("Table must have at least a header row")
        
        # Get the number of columns from the header row
        header = data[0]
        num_columns = len(header)
        
        if num_columns == 0:
            raise ValueError("Header row cannot be empty")
        
        # Validate that all rows have the same number of columns
        for i, row in enumerate(data):
            if len(row) != num_columns:
                raise ValueError(
                    f"Row {i} has {len(row)} columns, but header has {num_columns} columns. "
                    "All rows must have the same number of columns."
                )
        
        # Build the markdown table
        table_lines = []
        
        # Helper function to render cell content
        def render_cell(cell):
            if hasattr(cell, 'render'):
                return cell.render()
            return str(cell)
        
        # Add header row
        table_lines.append("| " + " | ".join(render_cell(cell) for cell in header) + " |")
        
        # Add separator row
        table_lines.append("| " + " | ".join(["---"] * num_columns) + " |")
        
        # Add data rows
        for row in data[1:]:
            table_lines.append("| " + " | ".join(render_cell(cell) for cell in row) + " |")
        
        # Join all lines and add to buffer
        markdown_table = "\n".join(table_lines)
        self._lines.append(markdown_table)
        return self
    
    def addNewLine(self) -> 'Summary':
        """
        Add a blank line to the summary buffer.
        
        Returns:
            Self for method chaining
        """
        self._lines.append("")
        return self
    
    def addDivider(self) -> 'Summary':
        """
        Add a horizontal divider line to the summary buffer.
        
        Returns:
            Self for method chaining
        """
        self._lines.append("---")
        return self
    
    def write(self) -> 'Summary':
        """
        Write all accumulated lines to the summary file.
        
        Returns:
            Self for method chaining
        """
        if self._lines:
            content = '\n'.join(self._lines) + '\n'
            self.doc.write(content)
            self.doc.flush()
        return self
    
    def __del__(self):
        """Clean up by closing the file if it's open."""
        if hasattr(self, 'doc') and not self.doc.closed:
            self.doc.close()
    
    def close(self):
        """Explicitly close the summary file."""
        if hasattr(self, 'doc') and not self.doc.closed:
            self.doc.close()
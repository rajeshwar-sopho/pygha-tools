from typing import Optional
from .enums import TextStyle


class Text:
    """Represents styled text that can be rendered as markdown."""
    
    def __init__(self, text: str, style: Optional[TextStyle] = None, id: Optional[str] = None):
        """
        Initialize a Text object.
        
        Args:
            text: The text content
            style: Optional style to apply (BOLD, ITALIC, or UNDERLINED)
            id: Optional HTML id attribute
        """
        self.text = text
        self.style = style
        self.id = id
    
    def render(self) -> str:
        """
        Render the text as markdown.
        
        Returns:
            Markdown formatted string
        """
        result = self.text
        
        # Apply styling
        if self.style == TextStyle.BOLD:
            result = f"**{result}**"
        elif self.style == TextStyle.ITALIC:
            result = f"*{result}*"
        elif self.style == TextStyle.UNDERLINED:
            result = f"<u>{result}</u>"
        
        # Apply id if present
        if self.id:
            result = f'<span id="{self.id}">{result}</span>'
        
        return result
    
    def __add__(self, other):
        """
        Concatenate Text with string or another Text/Link object.
        
        Args:
            other: String or renderable object to concatenate
        
        Returns:
            String result of concatenation
        """
        if isinstance(other, str):
            return self.render() + other
        elif hasattr(other, 'render'):
            return self.render() + other.render()
        return NotImplemented
    
    def __radd__(self, other):
        """
        Right-hand addition to support str + Text or renderable + Text.
        
        Args:
            other: String or renderable object to prepend
        
        Returns:
            String result of concatenation
        """
        if isinstance(other, str):
            return other + self.render()
        elif hasattr(other, 'render'):
            return other.render() + self.render()
        return NotImplemented
from typing import Optional
from .enums import TextStyle


class Link:
    """Represents a hyperlink that can be rendered as markdown."""
    
    def __init__(self, text: str, href: str, title: Optional[str] = None, style: Optional[TextStyle] = None):
        """
        Initialize a Link object.
        
        Args:
            text: The link text to display
            href: The URL to link to
            title: Optional title attribute for the link
            style: Optional style to apply to the link text
        """
        self.text = text
        self.href = href
        self.title = title
        self.style = style
    
    def render(self) -> str:
        """
        Render the link as markdown.
        
        Returns:
            Markdown formatted link string
        """
        styled_text = self.text
        
        # Apply styling to the link text
        if self.style == TextStyle.BOLD:
            styled_text = f"**{styled_text}**"
        elif self.style == TextStyle.ITALIC:
            styled_text = f"*{styled_text}*"
        elif self.style == TextStyle.UNDERLINED:
            styled_text = f"<u>{styled_text}</u>"
        
        # Create the markdown link
        if self.title:
            return f'[{styled_text}]({self.href} "{self.title}")'
        else:
            return f'[{styled_text}]({self.href})'
    
    def __add__(self, other):
        """
        Concatenate Link with string or another Text/Link object.
        
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
        Right-hand addition to support str + Link or renderable + Link.
        
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
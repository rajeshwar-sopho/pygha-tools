from enum import Enum


class TextStyle(Enum):
    """Enum for text styling options."""
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINED = "underlined"


class HeadingKind(Enum):
    """Enum for heading levels."""
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6
    SETEXT1 = "setext1"
    SETEXT2 = "setext2"
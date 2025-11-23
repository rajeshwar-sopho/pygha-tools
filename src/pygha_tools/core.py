from .summary import Summary


class Core:
    """Main class to control GitHub Actions environment interactions."""
    
    def __init__(self):
        """Initialize Core with a Summary object."""
        self.summary: Summary = Summary()
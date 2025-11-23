# GitHub Actions Summary

A Python library for creating rich markdown summaries in GitHub Actions.

## Installation
```bash
pip install github-actions-summary
```

## Usage
```python
from github_actions_summary import Summary, Text, Link, TextStyle, HeadingKind

summary = Summary()
summary.addHeading('Test Results', HeadingKind.H1)\
       .addCodeBlock('console.log("hello")', 'js')\
       .addTable([
           ['File', 'Status'],
           [Text('foo.js', style=TextStyle.BOLD), '✅ Pass'],
           ['bar.js', '❌ Fail']
       ])\
       .addLink('View report', 'https://example.com/report')\
       .write()
```

## Features

- Builder pattern for fluent API
- Rich text formatting (bold, italic, underlined)
- Headings (H1-H6, Setext)
- Code blocks with syntax highlighting
- Tables with styled cells
- Links with optional styling
- Horizontal dividers
- Blank lines for spacing

## License

MIT
import os
import pytest
from pathlib import Path


def test_summary_initialization_and_file_handling(tmp_path):
    """Test Summary class initialization with GITHUB_STEP_SUMMARY environment variable."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    
    # Set the environment variable
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        # Import here to ensure environment variable is set
        from pygha_tools import Summary
        
        # Create Summary object
        summary = Summary()
        
        # Check if doc is loaded properly
        assert summary.doc is not None, "doc should be initialized"
        assert not summary.doc.closed, "doc should be open"
        assert summary.doc.mode == 'a', "doc should be opened in append mode"
        assert summary.doc.name == str(summary_file), "doc should point to the correct file"
        
        # Verify the file was created
        assert summary_file.exists(), "Summary file should be created"
        
        # Cleanup: Close the file
        summary.close()
        assert summary.doc.closed, "doc should be closed after calling close()"
        
    finally:
        # Cleanup: Remove the environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        # Cleanup: Remove the temporary file if it exists
        if summary_file.exists():
            summary_file.unlink()


def test_summary_missing_environment_variable():
    """Test Summary class raises error when GITHUB_STEP_SUMMARY is not set."""
    # Ensure environment variable is not set
    if 'GITHUB_STEP_SUMMARY' in os.environ:
        del os.environ['GITHUB_STEP_SUMMARY']
    
    from pygha_tools import Summary
    
    # Should raise ValueError when environment variable is missing
    with pytest.raises(ValueError, match="GITHUB_STEP_SUMMARY environment variable is not set"):
        Summary()


def test_addText_with_different_styles(tmp_path):
    """Test addText method with bold, italic, and underlined styles."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add text with different styles
        summary.addText("Bold text", TextStyle.BOLD)
        summary.addText("Italic text", TextStyle.ITALIC)
        summary.addText("Underlined text", TextStyle.UNDERLINED)
        
        # Check internal list for correct markdown strings
        assert len(summary._lines) == 3, "Should have 3 lines in buffer"
        assert summary._lines[0] == "**Bold text**", "Bold markdown should be correct"
        assert summary._lines[1] == "*Italic text*", "Italic markdown should be correct"
        assert summary._lines[2] == "<u>Underlined text</u>", "Underlined markdown should be correct"
        
        # Cleanup
        summary.close()
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_write_method_outputs_to_file(tmp_path):
    """Test write method correctly writes accumulated lines to file."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add multiple texts
        summary.addText("First line", TextStyle.BOLD)
        summary.addText("Second line", TextStyle.ITALIC)
        summary.addText("Third line", TextStyle.UNDERLINED)
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = "**First line**\n*Second line*\n<u>Third line</u>\n"
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addHeading_with_all_levels(tmp_path):
    """Test addHeading method with all heading levels H1 through H6."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, HeadingKind
        
        # Create Summary object
        summary = Summary()
        
        # Add all heading levels
        summary.addHeading("Heading 1", HeadingKind.H1)
        summary.addHeading("Heading 2", HeadingKind.H2)
        summary.addHeading("Heading 3", HeadingKind.H3)
        summary.addHeading("Heading 4", HeadingKind.H4)
        summary.addHeading("Heading 5", HeadingKind.H5)
        summary.addHeading("Heading 6", HeadingKind.H6)
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "# Heading 1\n"
            "## Heading 2\n"
            "### Heading 3\n"
            "#### Heading 4\n"
            "##### Heading 5\n"
            "###### Heading 6\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addHeading_setext_headers(tmp_path):
    """Test addHeading method with Setext header styles."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, HeadingKind
        
        # Create Summary object
        summary = Summary()
        
        # Add Setext headers
        summary.addHeading("Setext Header 1", HeadingKind.SETEXT1)
        summary.addHeading("Setext Header 2", HeadingKind.SETEXT2)
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "Setext Header 1\n"
            "===============\n"
            "Setext Header 2\n"
            "---------------\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addText_with_id_parameter(tmp_path):
    """Test addText method with id parameter."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add text with ids
        summary.addText("Bold text with id", TextStyle.BOLD, id="bold-text")
        summary.addText("Italic text with id", TextStyle.ITALIC, id="italic-text")
        summary.addText("Underlined text with id", TextStyle.UNDERLINED, id="underlined-text")
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            '<span id="bold-text">**Bold text with id**</span>\n'
            '<span id="italic-text">*Italic text with id*</span>\n'
            '<span id="underlined-text"><u>Underlined text with id</u></span>\n'
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addHeading_with_id_parameter(tmp_path):
    """Test addHeading method with id parameter for different heading types."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, HeadingKind
        
        # Create Summary object
        summary = Summary()
        
        # Add headings with ids
        summary.addHeading("H1 with id", HeadingKind.H1, id="h1-heading")
        summary.addHeading("H2 with id", HeadingKind.H2, id="h2-heading")
        summary.addHeading("Setext1 with id", HeadingKind.SETEXT1, id="setext1-heading")
        summary.addHeading("Setext2 with id", HeadingKind.SETEXT2, id="setext2-heading")
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            '<span id="h1-heading"># H1 with id</span>\n'
            '<span id="h2-heading">## H2 with id</span>\n'
            '<span id="setext1-heading">\n'
            'Setext1 with id\n'
            '===============\n'
            '</span>\n'
            '<span id="setext2-heading">\n'
            'Setext2 with id\n'
            '---------------\n'
            '</span>\n'
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addCode_with_and_without_language(tmp_path):
    """Test addCode method with and without language specification."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary
        
        # Create Summary object
        summary = Summary()
        
        # Add code blocks
        summary.addCode("def hello():\n    print('Hello, World!')", language="python")
        summary.addCode("console.log('Hello, World!');", language="javascript")
        summary.addCode("echo 'Hello, World!'")  # No language specified
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "```python\n"
            "def hello():\n"
            "    print('Hello, World!')\n"
            "```\n"
            "```javascript\n"
            "console.log('Hello, World!');\n"
            "```\n"
            "```\n"
            "echo 'Hello, World!'\n"
            "```\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addLink_with_and_without_title(tmp_path):
    """Test addLink method with and without title attribute."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add links with different styles
        summary.addLink("GitHub", "https://github.com")
        summary.addLink("Google", "https://google.com", title="Search Engine")
        summary.addLink("Bold Link", "https://example.com", style=TextStyle.BOLD)
        summary.addLink("Italic Link", "https://example.com", title="With Title", style=TextStyle.ITALIC)
        summary.addLink("Underlined Link", "https://example.com", style=TextStyle.UNDERLINED)
        
        # Write to file
        summary.write()
        
        # Close to ensure flush
        summary.close()
        
        # Read the file and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "[GitHub](https://github.com)\n"
            '[Google](https://google.com "Search Engine")\n'
            "[**Bold Link**](https://example.com)\n"
            '[*Italic Link*](https://example.com "With Title")\n'
            "[<u>Underlined Link</u>](https://example.com)\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addTable_with_valid_and_invalid_data(tmp_path):
    """Test addTable method with valid data and validate error handling for mismatched columns."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary
        
        # Test with valid table data
        summary = Summary()
        
        table_data = [
            ["Name", "Age", "City"],
            ["Alice", "30", "New York"],
            ["Bob", "25", "Los Angeles"],
            ["Charlie", "35", "Chicago"]
        ]
        
        summary.addTable(table_data) # type: ignore
        summary.write()
        summary.close()
        
        # Read and verify the table
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "| Name | Age | City |\n"
            "| --- | --- | --- |\n"
            "| Alice | 30 | New York |\n"
            "| Bob | 25 | Los Angeles |\n"
            "| Charlie | 35 | Chicago |\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
        # Test with mismatched columns - should raise ValueError
        summary2 = Summary()
        
        invalid_data = [
            ["Name", "Age", "City"],
            ["Alice", "30", "New York"],
            ["Bob", "25"]  # Missing column
        ]
        
        with pytest.raises(ValueError, match="Row 2 has 2 columns, but header has 3 columns"):
            summary2.addTable(invalid_data) # type: ignore
        
        summary2.close()
        
        # Test with empty data
        summary3 = Summary()
        with pytest.raises(ValueError, match="Table data cannot be empty"):
            summary3.addTable([])
        summary3.close()
        
        # Test with empty header
        summary4 = Summary()
        with pytest.raises(ValueError, match="Header row cannot be empty"):
            summary4.addTable([[]])
        summary4.close()
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addNewLine(tmp_path):
    """Test addNewLine method adds blank lines correctly."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add content with new lines
        summary.addText("First line", TextStyle.BOLD)
        summary.addNewLine()
        summary.addText("Second line after blank", TextStyle.ITALIC)
        summary.addNewLine()
        summary.addNewLine()
        summary.addText("Third line after two blanks", TextStyle.UNDERLINED)
        
        # Write to file
        summary.write()
        summary.close()
        
        # Read and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "**First line**\n"
            "\n"
            "*Second line after blank*\n"
            "\n"
            "\n"
            "<u>Third line after two blanks</u>\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_addDivider(tmp_path):
    """Test addDivider method adds horizontal dividers correctly."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, HeadingKind, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Add content with dividers
        summary.addHeading("Section 1", HeadingKind.H2)
        summary.addText("Content for section 1", TextStyle.BOLD)
        summary.addDivider()
        summary.addHeading("Section 2", HeadingKind.H2)
        summary.addText("Content for section 2", TextStyle.ITALIC)
        summary.addDivider()
        summary.addText("Final content", TextStyle.UNDERLINED)
        
        # Write to file
        summary.write()
        summary.close()
        
        # Read and verify contents
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "## Section 1\n"
            "**Content for section 1**\n"
            "---\n"
            "## Section 2\n"
            "*Content for section 2*\n"
            "---\n"
            "<u>Final content</u>\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()


def test_text_class_render_and_concatenation():
    """Test Text class rendering and concatenation with + operator."""
    from pygha_tools import Text, TextStyle
    
    # Test basic rendering
    plain_text = Text("Hello")
    assert plain_text.render() == "Hello"
    
    bold_text = Text("Bold", style=TextStyle.BOLD)
    assert bold_text.render() == "**Bold**"
    
    italic_text = Text("Italic", style=TextStyle.ITALIC)
    assert italic_text.render() == "*Italic*"
    
    underlined_text = Text("Underlined", style=TextStyle.UNDERLINED)
    assert underlined_text.render() == "<u>Underlined</u>"
    
    # Test with id
    text_with_id = Text("IDText", style=TextStyle.BOLD, id="my-id")
    assert text_with_id.render() == '<span id="my-id">**IDText**</span>'
    
    # Test concatenation with string (Text + str)
    result = bold_text + " World"
    assert result == "**Bold** World"
    
    # Test concatenation with string (str + Text)
    result = "Hello " + bold_text
    assert result == "Hello **Bold**"
    
    # Test concatenation with another Text (Text + Text)
    result = bold_text + italic_text
    assert result == "**Bold***Italic*"
    
    # Test chaining with multiple objects
    result = bold_text + " and " + italic_text + " text"
    assert result == "**Bold** and *Italic* text"


def test_link_class_render_and_concatenation():
    """Test Link class rendering and concatenation with + operator."""
    from pygha_tools import Link, Text, TextStyle
    
    # Test basic rendering
    simple_link = Link("GitHub", "https://github.com")
    assert simple_link.render() == "[GitHub](https://github.com)"
    
    # Test with title
    link_with_title = Link("Google", "https://google.com", title="Search")
    assert link_with_title.render() == '[Google](https://google.com "Search")'
    
    # Test with styling
    bold_link = Link("Bold Link", "https://example.com", style=TextStyle.BOLD)
    assert bold_link.render() == "[**Bold Link**](https://example.com)"
    
    italic_link = Link("Italic Link", "https://example.com", style=TextStyle.ITALIC)
    assert italic_link.render() == "[*Italic Link*](https://example.com)"
    
    # Test concatenation with string (Link + str)
    result = simple_link + " is cool"
    assert result == "[GitHub](https://github.com) is cool"
    
    # Test concatenation with string (str + Link)
    result = "Visit " + simple_link
    assert result == "Visit [GitHub](https://github.com)"
    
    # Test concatenation with another Link
    result = simple_link + bold_link
    assert result == "[GitHub](https://github.com)[**Bold Link**](https://example.com)"
    
    # Test concatenation with Text object
    bold_text = Text("Bold", style=TextStyle.BOLD)
    result = bold_text + simple_link
    assert result == "**Bold**[GitHub](https://github.com)"
    
    result = simple_link + bold_text
    assert result == "[GitHub](https://github.com)**Bold**"


def test_table_with_text_and_link_objects(tmp_path):
    """Test addTable method with Text and Link objects in cells."""
    # Setup: Create a temporary file path
    summary_file = tmp_path / "github_step_summary.log"
    os.environ['GITHUB_STEP_SUMMARY'] = str(summary_file)
    
    try:
        from pygha_tools import Summary, Text, Link, TextStyle
        
        # Create Summary object
        summary = Summary()
        
        # Create table with styled content
        table_data = [
            ["Name", "Status", "Link"],
            [
                Text("Alice", style=TextStyle.BOLD),
                Text("Passed", style=TextStyle.ITALIC),
                Link("Profile", "https://example.com/alice")
            ],
            [
                Text("Bob", style=TextStyle.BOLD),
                Text("Failed", style=TextStyle.UNDERLINED),
                Link("Details", "https://example.com/bob", title="View Details", style=TextStyle.ITALIC)
            ],
            [
                "Charlie",  # Mix of regular strings
                Text("Pending", style=TextStyle.ITALIC),
                Link("Report", "https://example.com/charlie", style=TextStyle.BOLD)
            ]
        ]
        
        summary.addTable(table_data)
        summary.write()
        summary.close()
        
        # Read and verify the table
        with open(summary_file, 'r') as f:
            content = f.read()
        
        expected_content = (
            "| Name | Status | Link |\n"
            "| --- | --- | --- |\n"
            "| **Alice** | *Passed* | [Profile](https://example.com/alice) |\n"
            '| **Bob** | <u>Failed</u> | [*Details*](https://example.com/bob "View Details") |\n'
            "| Charlie | *Pending* | [**Report**](https://example.com/charlie) |\n"
        )
        assert content == expected_content, f"File content should match expected. Got: {repr(content)}"
        
    finally:
        # Cleanup environment variable
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            del os.environ['GITHUB_STEP_SUMMARY']
        
        if summary_file.exists():
            summary_file.unlink()

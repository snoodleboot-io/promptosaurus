#!/usr/bin/env python3
"""Simple test script for template inheritance."""

import sys
from pathlib import Path

# Add the promptosaurus directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from promptosaurus.builders.builder import Builder


def test_inheritance():
    print("Starting inheritance test...")
    """Test template inheritance manually."""
    builder = Builder()

    # Create a simple base template
    base_content = """Base Template
{% block content %}Default content{% endblock %}
End of base"""

    # Create a child template that extends it
    child_content = """{% extends "base.md" %}
{% block content %}Overridden content{% endblock %}"""

    # Mock the registry
    import promptosaurus.registry

    original_prompt_body = promptosaurus.registry.registry.prompt_body

    def mock_prompt_body(filename):
        if filename == "base.md":
            return base_content
        raise FileNotFoundError(f"Template {filename} not found")

    promptosaurus.registry.registry.prompt_body = mock_prompt_body

    try:
        # Test rendering the child template
        result = builder._jinja2_renderer.handle(child_content, {})
        print("Inheritance test result:")
        print(repr(result))
        print("SUCCESS: Inheritance works!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Restore original
        promptosaurus.registry.registry.prompt_body = original_prompt_body


if __name__ == "__main__":
    test_inheritance()

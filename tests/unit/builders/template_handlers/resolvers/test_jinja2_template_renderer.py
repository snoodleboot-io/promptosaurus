"""Unit tests for the Jinja2TemplateRenderer class inheritance functionality."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add the promptosaurus directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import jinja2
import pytest

from promptosaurus.builders.template_handlers.resolvers.jinja2_template_renderer import (
    Jinja2TemplateRenderer,
)
from promptosaurus.builders.template_handlers.resolvers.template_rendering_error import (
    TemplateRenderingError,
)


class TestJinja2TemplateRendererInheritance:
    """Test inheritance functionality in Jinja2TemplateRenderer."""

    @pytest.fixture
    def mock_environment(self):
        """Create a mock Jinja2 environment for testing."""
        env = Mock(spec=jinja2.Environment)
        env.from_string = Mock()
        return env

    @pytest.fixture
    def renderer(self, mock_environment):
        """Create a Jinja2TemplateRenderer instance for testing."""
        return Jinja2TemplateRenderer(mock_environment)

    def test_detect_inheritance_no_inheritance(self, renderer):
        """Test _detect_inheritance returns None when no inheritance is used."""
        template = "Simple template without inheritance"
        result = renderer._detect_inheritance(template)
        assert result is None

    def test_detect_inheritance_with_extends(self, renderer):
        """Test _detect_inheritance detects extends directive."""
        template = """{% extends "base-template.md" %}
{% block content %}Child content{% endblock %}"""
        result = renderer._detect_inheritance(template)
        assert result == "base-template.md"

    def test_detect_inheritance_with_quotes_variations(self, renderer):
        """Test _detect_inheritance works with different quote styles."""
        # Double quotes
        template1 = """{% extends "base.md" %}"""
        assert renderer._detect_inheritance(template1) == "base.md"

        # Single quotes
        template2 = """{% extends 'base.md' %}"""
        assert renderer._detect_inheritance(template2) == "base.md"

    def test_detect_inheritance_with_whitespace(self, renderer):
        """Test _detect_inheritance handles whitespace around extends."""
        template = """   {% extends "base.md" %}   """
        result = renderer._detect_inheritance(template)
        assert result == "base.md"

    def test_extract_blocks_simple(self, renderer):
        """Test _extract_blocks extracts simple blocks correctly."""
        template = """Base content
{% block header %}Default Header{% endblock %}
More content
{% block footer %}Default Footer{% endblock %}"""

        blocks = renderer._extract_blocks(template)

        assert "header" in blocks
        assert "footer" in blocks
        assert blocks["header"] == "Default Header"
        assert blocks["footer"] == "Default Footer"

    def test_extract_blocks_nested(self, renderer):
        """Test _extract_blocks handles nested blocks correctly."""
        template = """{% block outer %}
Outer start
{% block inner %}Inner content{% endblock %}
Outer end
{% endblock %}"""

        blocks = renderer._extract_blocks(template)

        assert "outer" in blocks
        assert "inner" in blocks
        assert "Inner content" in blocks["inner"]
        assert (
            "Outer start\n{% block inner %}Inner content{% endblock %}\nOuter end"
            in blocks["outer"]
        )

    def test_extract_blocks_malformed_syntax(self, renderer):
        """Test _extract_blocks raises error for malformed block syntax."""
        # Missing closing %}
        template = """{% block content %}Content{% endblock"""

        with pytest.raises(TemplateRenderingError) as exc_info:
            renderer._extract_blocks(template)
        assert "Malformed block syntax" in str(exc_info.value)

    def test_extract_blocks_invalid_declaration(self, renderer):
        """Test _extract_blocks raises error for invalid block declaration."""
        template = """{% block %}Content{% endblock %}"""

        with pytest.raises(TemplateRenderingError) as exc_info:
            renderer._extract_blocks(template)
        assert "Invalid block declaration" in str(exc_info.value)

    def test_extract_blocks_unclosed_block(self, renderer):
        """Test _extract_blocks raises error for unclosed blocks."""
        template = """{% block content %}Content without endblock"""

        with pytest.raises(TemplateRenderingError) as exc_info:
            renderer._extract_blocks(template)
        assert "Unclosed block" in str(exc_info.value)

    def test_resolve_inheritance_chain_no_inheritance(self, renderer):
        """Test _resolve_inheritance_chain returns template as-is when no inheritance."""
        template = "Simple template"
        content, blocks = renderer._resolve_inheritance_chain(template)

        assert content == template
        assert isinstance(blocks, dict)

    @patch("promptosaurus.registry.registry.prompt_body")
    def test_resolve_inheritance_chain_single_level(self, mock_prompt_body, renderer):
        """Test _resolve_inheritance_chain resolves single-level inheritance."""
        base_template = """Base
{% block content %}Default{% endblock %}"""

        child_template = """{% extends "base.md" %}
{% block content %}Overridden{% endblock %}"""

        mock_prompt_body.return_value = base_template

        content, blocks = renderer._resolve_inheritance_chain(child_template)

        assert content == base_template
        assert "content" in blocks
        assert blocks["content"] == "Overridden"

    @patch("promptosaurus.registry.registry.prompt_body")
    def test_resolve_inheritance_chain_multi_level(self, mock_prompt_body, renderer):
        """Test _resolve_inheritance_chain resolves multi-level inheritance."""
        grandparent = """Grandparent
{% block header %}Default Header{% endblock %}
{% block content %}Grandparent Content{% endblock %}"""

        parent = """{% extends "grandparent.md" %}
{% block header %}Parent Header{% endblock %}"""

        child = """{% extends "parent.md" %}
{% block content %}Child Content{% endblock %}"""

        def mock_body(filename):
            if filename == "grandparent.md":
                return grandparent
            elif filename == "parent.md":
                return parent
            else:
                raise FileNotFoundError()

        mock_prompt_body.side_effect = mock_body

        content, blocks = renderer._resolve_inheritance_chain(child)

        assert content == grandparent
        assert blocks["header"] == "Parent Header"
        assert blocks["content"] == "Child Content"

    def test_resolve_inheritance_chain_circular_dependency(self, renderer):
        """Test _resolve_inheritance_chain detects circular dependencies."""
        # This would require mocking the registry to create a circular reference
        # For now, we'll test the detection logic by manually calling with visited set
        template = """{% extends "self.md" %}"""

        with pytest.raises(TemplateRenderingError) as exc_info:
            renderer._resolve_inheritance_chain(template, visited_templates={"self.md"})

        assert "Circular template inheritance detected" in str(exc_info.value)

    def test_resolve_inheritance_chain_depth_limit(self, renderer):
        """Test _resolve_inheritance_chain enforces depth limit."""
        # Create a deep inheritance chain that exceeds the limit
        templates = {}
        for i in range(12):  # More than max_depth of 10
            templates[f"template{i}.md"] = f"""{{% extends "template{i + 1}.md" %}}"""

        # Mock the registry to return these templates
        with patch("promptosaurus.registry.registry.prompt_body") as mock_body:
            mock_body.side_effect = lambda name: templates.get(name, "")

            deep_template = """{% extends "template0.md" %}"""

            with pytest.raises(TemplateRenderingError) as exc_info:
                renderer._resolve_inheritance_chain(deep_template)

            assert "inheritance depth limit" in str(exc_info.value)

    @patch("promptosaurus.registry.registry.prompt_body")
    def test_merge_templates_basic(self, mock_prompt_body, renderer):
        """Test _merge_templates merges basic inheritance."""
        base = """Base
{% block content %}Default{% endblock %}"""

        child = """{% extends "base.md" %}
{% block content %}Overridden{% endblock %}"""

        mock_prompt_body.return_value = base

        result = renderer._merge_templates(child)

        # Should contain base content with child block substituted
        assert "Base" in result
        assert "Overridden" in result
        assert "Default" not in result

    @patch("promptosaurus.registry.registry.prompt_body")
    def test_merge_templates_with_super(self, mock_prompt_body, renderer):
        """Test _merge_templates handles {% super() %} calls."""
        base = """Base
{% block content %}Default content{% endblock %}"""

        child = """{% extends "base.md" %}
{% block content %}Child content {{ super() }}{% endblock %}"""

        mock_prompt_body.return_value = base

        result = renderer._merge_templates(child)

        # Should contain both child and parent content
        assert "Base" in result
        assert "Child content" in result
        assert "Default content" in result

    @patch("promptosaurus.registry.registry.prompt_body")
    def test_merge_templates_missing_base(self, mock_prompt_body, renderer):
        """Test _merge_templates handles missing base templates."""
        child = """{% extends "missing.md" %}
{% block content %}Content{% endblock %}"""

        mock_prompt_body.side_effect = FileNotFoundError("Template not found")

        with pytest.raises(TemplateRenderingError) as exc_info:
            renderer._merge_templates(child)

        assert "Failed to load base template" in str(exc_info.value)

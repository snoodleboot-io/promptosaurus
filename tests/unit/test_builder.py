"""Unit tests for the Builder class template substitution functionality."""

import sys
from pathlib import Path

# Add the promptosaurus directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from promptosaurus.builders.builder import Builder


def test_basic_substitution():
    """Test basic template substitution functionality."""
    # Create a builder instance
    builder = Builder()

    # Test content with template variables
    content = """
    Language: {{config.language}}
    Runtime: {{config.runtime}}
    Package Manager: {{config.package_manager}}
    Linter: {{config.linter}}
    Formatter: {{config.formatter}}
    Abstract Class Style: {{config.abstract_class_style}}
    Testing Framework: {{config.test_framework}}
    Test Runner: {{config.test_runner}}
    Line Coverage: {{config.coverage.line}}%
    Branch Coverage: {{config.coverage.branch}}%
    Function Coverage: {{config.coverage.function}}%
    Statement Coverage: {{config.coverage.statement}}%
    Mutation Coverage: {{config.coverage.mutation}}%
    Path Coverage: {{config.coverage.path}}%
    """

    # Test config
    config = {
        "spec": {
            "language": "python",
            "runtime": "CPython 3.11",
            "package_manager": "uv",
            "linter": "ruff",
            "formatter": "ruff",
            "abstract_class_style": "interface",
            "test_framework": "pytest",
            "test_runner": "pytest",
            "coverage": {
                "line": 80,
                "branch": 70,
                "function": 90,
                "statement": 85,
                "mutation": 80,
                "path": 60,
            },
        }
    }

    # Perform substitution
    result = builder._substitute_template_variables(content, config)

    # Check that substitutions worked
    assert "Language: python" in result
    assert "Runtime: CPython 3.11" in result
    assert "Package Manager: uv" in result
    assert "Linter: ruff" in result
    assert "Formatter: ruff" in result
    assert "Abstract Class Style: interface" in result
    assert "Testing Framework: pytest" in result
    assert "Test Runner: pytest" in result
    assert "Line Coverage: 80%" in result
    assert "Branch Coverage: 70%" in result
    assert "Function Coverage: 90%" in result
    assert "Statement Coverage: 85%" in result
    assert "Mutation Coverage: 80%" in result
    assert "Path Coverage: 60%" in result


def test_coverage_presets():
    """Test coverage preset functionality."""
    builder = Builder()

    content = "Line: {{config.coverage.line}}%, Branch: {{config.coverage.branch}}%"

    # Test strict preset with explicit values
    config_strict = {
        "spec": {
            "coverage": {
                "line": 90,
                "branch": 80,
                "function": 95,
                "statement": 90,
                "mutation": 85,
                "path": 70,
            }
        }
    }
    result_strict = builder._substitute_template_variables(content, config_strict)
    assert "Line: 90%" in result_strict
    assert "Branch: 80%" in result_strict

    # Test standard preset with explicit values
    config_standard = {
        "spec": {
            "coverage": {
                "line": 80,
                "branch": 70,
                "function": 90,
                "statement": 85,
                "mutation": 80,
                "path": 60,
            }
        }
    }
    result_standard = builder._substitute_template_variables(content, config_standard)
    assert "Line: 80%" in result_standard
    assert "Branch: 70%" in result_standard

    # Test minimal preset with explicit values
    config_minimal = {
        "spec": {
            "coverage": {
                "line": 70,
                "branch": 60,
                "function": 80,
                "statement": 75,
                "mutation": 70,
                "path": 50,
            }
        }
    }
    result_minimal = builder._substitute_template_variables(content, config_minimal)
    assert "Line: 70%" in result_minimal
    assert "Branch: 60%" in result_minimal


def test_multilanguage_config():
    """Test multi-language configuration handling."""
    builder = Builder()

    content = "Language: {{config.language}}"

    # Multi-language config (list)
    config_multi = {"spec": [{"language": "python"}, {"language": "javascript"}]}
    result = builder._substitute_template_variables(content, config_multi)
    # Should use the first language in the list
    assert "Language: python" in result


def test_no_config():
    """Test behavior with empty config - missing keys raise UndefinedError."""
    import pytest
    from promptosaurus.builders.template_handlers.resolvers.template_rendering_error import (
        TemplateRenderingError,
    )

    builder = Builder()

    content = "Language: {{config.language}}"
    # Accessing a missing key in Jinja2 raises an error
    with pytest.raises(TemplateRenderingError, match="language"):
        builder._substitute_template_variables(content, {"spec": {}})


def test_extensibility():
    """Test that custom config values work through the config object."""
    builder = Builder()
    content = "Custom: {{config.custom_var}}"
    config = {"spec": {"custom_var": "custom_value"}}
    result = builder._substitute_template_variables(content, config)
    assert "Custom: custom_value" in result

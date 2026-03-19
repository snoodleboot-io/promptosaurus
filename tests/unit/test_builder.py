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
    Language: {{LANGUAGE}}
    Runtime: {{RUNTIME}}
    Package Manager: {{PACKAGE_MANAGER}}
    Linter: {{LINTER}}
    Formatter: {{FORMATTER}}
    Abstract Class Style: {{ABSTRACT_CLASS_STYLE}}
    Testing Framework: {{TESTING_FRAMEWORK}}
    Test Runner: {{TEST_RUNNER}}
    Line Coverage: {{LINE_COVERAGE_%}}%
    Branch Coverage: {{BRANCH_COVERAGE_%}}%
    Function Coverage: {{FUNCTION_COVERAGE_%}}%
    Statement Coverage: {{STATEMENT_COVERAGE_%}}%
    Mutation Coverage: {{MUTATION_COVERAGE_%}}%
    Path Coverage: {{PATH_COVERAGE_%}}%
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
                "path": 60
            }
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

    content = "Line: {{LINE_COVERAGE_%}}%, Branch: {{BRANCH_COVERAGE_%}}%"

    # Test strict preset
    config_strict = {
        "spec": {
            "coverage": "strict"
        }
    }
    result_strict = builder._substitute_template_variables(content, config_strict)
    assert "Line: 90%" in result_strict
    assert "Branch: 80%" in result_strict

    # Test standard preset
    config_standard = {
        "spec": {
            "coverage": "standard"
        }
    }
    result_standard = builder._substitute_template_variables(content, config_standard)
    assert "Line: 80%" in result_standard
    assert "Branch: 70%" in result_standard

    # Test minimal preset
    config_minimal = {
        "spec": {
            "coverage": "minimal"
        }
    }
    result_minimal = builder._substitute_template_variables(content, config_minimal)
    assert "Line: 70%" in result_minimal
    assert "Branch: 60%" in result_minimal


def test_multilanguage_config():
    """Test multi-language configuration handling."""
    builder = Builder()

    content = "Language: {{LANGUAGE}}"

    # Multi-language config (list)
    config_multi = {
        "spec": [
            {"language": "python"},
            {"language": "javascript"}
        ]
    }
    result = builder._substitute_template_variables(content, config_multi)
    # Should use the first language in the list
    assert "Language: python" in result


def test_no_config():
    """Test behavior with no config."""
    builder = Builder()

    content = "Language: {{LANGUAGE}}"
    result = builder._substitute_template_variables(content, None)
    # Should substitute with empty string
    assert "Language: " in result


def test_extensibility():
    """Test that the new extensibility mechanism works."""
    # Create a subclass that adds a custom template variable
    class TestBuilder(Builder):
        def _get_template_substitutions(self, defaults, format_value):
            # Get base substitutions
            substitutions = super()._get_template_substitutions(defaults, format_value)
            # Add a custom one
            substitutions["{{CUSTOM_VAR}}"] = "custom_value"
            return substitutions

    builder = TestBuilder()
    content = "Custom: {{CUSTOM_VAR}}"
    config = {"spec": {}}
    result = builder._substitute_template_variables(content, config)
    assert "Custom: custom_value" in result

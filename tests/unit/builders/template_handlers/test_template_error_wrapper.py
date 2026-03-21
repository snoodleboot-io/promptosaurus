"""Tests for TemplateErrorWrapper context-preserving error handling."""

import pytest
import jinja2

from promptosaurus.builders.template_handlers.template_error_wrapper import (
    TemplateErrorWrapper,
    wrap_template_operation,
    default_error_wrapper,
)
from promptosaurus.builders.template_handlers.template_exceptions import (
    TemplateError,
    TemplateSyntaxError,
    TemplateRenderingError,
    TemplateValidationError,
    TemplateSecurityError,
    TemplateComplexityError,
)


class TestTemplateErrorWrapper:
    """Test suite for TemplateErrorWrapper functionality."""

    @pytest.fixture
    def wrapper(self) -> TemplateErrorWrapper:
        """Create a test wrapper instance."""
        return TemplateErrorWrapper(max_context_lines=2, max_variable_preview=50)

    @pytest.fixture
    def sample_template(self) -> str:
        """Sample template for testing."""
        return """Hello {{name}}!

{% for item in items %}
- {{ item }}
{% endfor %}

{% if show_footer %}
Footer content here.
{% endif %}
"""

    @pytest.fixture
    def sample_variables(self) -> dict:
        """Sample variables for testing."""
        return {
            "name": "Alice",
            "items": ["apple", "banana", "cherry"],
            "show_footer": True,
            "secret_key": "sensitive_data_that_should_not_be_logged",
            "large_object": {"nested": {"deeply": {"buried": "value"}}},
        }

    def test_initialization(self, wrapper):
        """Test wrapper initialization with custom parameters."""
        assert wrapper.max_context_lines == 2
        assert wrapper.max_variable_preview == 50

    def test_wrap_rendering_operation_success(self, wrapper, sample_template, sample_variables):
        """Test successful operation wrapping."""
        def mock_render(template_content, variables, template_name=None):
            # Simulate successful rendering
            return template_content.replace("{{name}}", variables["name"])

        result = wrapper.wrap_rendering_operation(
            mock_render,
            sample_template,
            sample_variables,
            template_name="test_template"
        )

        assert "Hello Alice!" in result

    def test_jinja2_syntax_error_enhancement(self, wrapper, sample_variables):
        """Test enhancement of Jinja2 TemplateSyntaxError."""
        malformed_template = "Hello {{name"  # Missing closing brace

        def mock_render(template_content, variables, template_name=None):
            env = jinja2.Environment()
            env.from_string(template_content)  # This should raise TemplateSyntaxError

        with pytest.raises(TemplateSyntaxError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                malformed_template,
                sample_variables
            )

        error = exc_info.value
        assert isinstance(error, TemplateSyntaxError)
        assert "Jinja2 syntax error" in str(error)
        assert error.template_content == malformed_template
        assert error.line_number is not None
        assert "template_snippet" in error.context

    def test_jinja2_undefined_error_enhancement(self, wrapper, sample_variables):
        """Test enhancement of Jinja2 UndefinedError."""
        template_with_undefined = "Hello {{undefined_var}}!"

        def mock_render(template_content, variables, template_name=None):
            env = jinja2.Environment()
            template = env.from_string(template_content)
            template.render(variables)  # This should raise UndefinedError

        with pytest.raises(TemplateRenderingError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                template_with_undefined,
                sample_variables
            )

        error = exc_info.value
        assert isinstance(error, TemplateRenderingError)
        assert "Undefined variable" in str(error)
        assert error.variables == sample_variables  # Should include full variables for undefined error
        assert "available_variables" in error.context
        assert "undefined_variable" in error.context

    def test_jinja2_runtime_error_enhancement(self, wrapper, sample_variables):
        """Test enhancement of Jinja2 TemplateRuntimeError."""
        template_with_runtime_error = "Hello {{name | nonexistent_filter}}!"

        def mock_render(template_content, variables, template_name=None):
            env = jinja2.Environment()
            template = env.from_string(template_content)
            template.render(variables)  # This should raise TemplateRuntimeError

        with pytest.raises(TemplateRenderingError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                template_with_runtime_error,
                sample_variables
            )

        error = exc_info.value
        assert isinstance(error, TemplateRenderingError)
        assert "Template runtime error" in str(error)
        assert "variable_snapshot" in error.context
        assert "error_location" in error.context

    def test_generic_exception_enhancement(self, wrapper, sample_variables):
        """Test enhancement of generic exceptions."""
        def mock_render(template_content, variables, template_name=None):
            raise ValueError("Custom error occurred")

        with pytest.raises(TemplateError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                "some template",
                sample_variables
            )

        error = exc_info.value
        assert isinstance(error, TemplateError)
        assert "Unexpected error during template processing" in str(error)
        assert "original_error_type" in error.context
        assert "original_error_message" in error.context
        assert "stack_trace" in error.context

    def test_existing_custom_error_preservation(self, wrapper, sample_variables):
        """Test that existing custom template errors are preserved with additional context."""
        def mock_render(template_content, variables, template_name=None):
            raise TemplateValidationError(
                message="Custom validation error",
                template_content=template_content,
                context={"custom_field": "custom_value"}
            )

        with pytest.raises(TemplateValidationError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                "some template",
                sample_variables
            )

        error = exc_info.value
        assert isinstance(error, TemplateValidationError)
        assert "Custom validation error" in str(error)
        assert error.context["custom_field"] == "custom_value"
        assert error.context["enhanced_by_wrapper"] is True

    def test_variable_snapshot_creation(self, wrapper, sample_variables):
        """Test safe variable snapshot creation."""
        snapshot = wrapper._create_variable_snapshot(sample_variables)

        # Should include safe previews
        assert "name" in snapshot
        assert snapshot["name"] == "Alice"  # String value preserved

        assert "items" in snapshot
        assert snapshot["items"] == "list(3 items)"  # Collection summarized

        assert "secret_key" in snapshot
        assert "sensitive_data_that_should_not_be_logged" in snapshot["secret_key"]  # Safe for short strings

        assert "large_object" in snapshot
        assert snapshot["large_object"] == "<dict object>"  # Complex object summarized

    def test_template_snippet_extraction(self, wrapper):
        """Test template snippet extraction around error locations."""
        template = """line 1
line 2
line 3
line 4
line 5"""

        # Test snippet around line 3
        snippet = wrapper._extract_template_snippet(template, 3)
        assert snippet is not None
        lines = snippet.split('\n')
        assert len(lines) == 3  # Should include context lines
        assert '--> line 3' in snippet  # Error line should be marked

    def test_template_snippet_edge_cases(self, wrapper):
        """Test template snippet extraction edge cases."""
        # Empty template
        assert wrapper._extract_template_snippet("", 1) is None

        # Invalid line number
        template = "single line"
        assert wrapper._extract_template_snippet(template, 0) is None
        assert wrapper._extract_template_snippet(template, 10) is None

    def test_location_formatting(self, wrapper):
        """Test location information formatting."""
        assert wrapper._format_location(None, None) == "unknown location"
        assert wrapper._format_location(5, None) == "line 5"
        assert wrapper._format_location(5, 10) == "line 5, column 10"

    def test_context_manager_functionality(self, wrapper, sample_variables):
        """Test context manager functionality."""
        template = "Hello {{name}}!"
        collected_context = None

        def mock_operation_with_context(context):
            nonlocal collected_context
            collected_context = context
            return "Hello Alice!"

        with wrapper.wrap_rendering_context(template, sample_variables) as context:
            result = mock_operation_with_context(context)

        assert result == "Hello Alice!"
        assert collected_context["template_content"] == template
        assert collected_context["variables"] == sample_variables
        assert collected_context["error_wrapper"] is wrapper

    def test_context_manager_error_handling(self, wrapper, sample_variables):
        """Test context manager error handling."""
        template = "Hello {{name}}!"

        with pytest.raises(TemplateError):
            with wrapper.wrap_rendering_context(template, sample_variables) as context:
                raise ValueError("Test error in context")

    def test_decorator_functionality(self, wrapper, sample_variables):
        """Test decorator functionality."""
        @wrap_template_operation("Hello {{name}}!", sample_variables, wrapper=wrapper)
        def mock_decorated_render(template_content, variables, template_name=None):
            return "Hello Alice!"

        result = mock_decorated_render()
        assert result == "Hello Alice!"

    def test_decorator_error_handling(self, wrapper, sample_variables):
        """Test decorator error handling."""
        @wrap_template_operation("Hello {{name}}!", sample_variables, wrapper=wrapper)
        def mock_decorated_render(template_content, variables, template_name=None):
            raise RuntimeError("Decorator test error")

        with pytest.raises(TemplateError) as exc_info:
            mock_decorated_render()

        error = exc_info.value
        assert isinstance(error, TemplateError)
        assert "Decorator test error" in error.context["original_error_message"]

    def test_default_wrapper_instance(self):
        """Test that default wrapper instance exists and works."""
        assert default_error_wrapper is not None
        assert isinstance(default_error_wrapper, TemplateErrorWrapper)

        # Test that it can be used
        result = default_error_wrapper.wrap_rendering_operation(
            lambda: "success",
            "template",
            {}
        )
        assert result == "success"

    def test_error_chaining(self, wrapper, sample_variables):
        """Test that error chaining preserves original exception."""
        def mock_render(template_content, variables, template_name=None):
            raise ValueError("Original error")

        with pytest.raises(TemplateError) as exc_info:
            wrapper.wrap_rendering_operation(
                mock_render,
                "template",
                sample_variables
            )

        error = exc_info.value
        # The __cause__ should be set to the original error
        assert error.__cause__ is not None
        assert isinstance(error.__cause__, ValueError)
        assert str(error.__cause__) == "Original error"

    def test_logging_integration(self, wrapper, sample_variables, caplog):
        """Test that errors are logged appropriately."""
        import logging
        caplog.set_level(logging.DEBUG)

        def mock_render(template_content, variables, template_name=None):
            raise ValueError("Test logging error")

        with pytest.raises(TemplateError):
            wrapper.wrap_rendering_operation(
                mock_render,
                "template",
                sample_variables,
                template_name="test_template"
            )

        # Should have debug log about error enhancement
        assert any("Template error enhanced" in record.message for record in caplog.records)

    def test_large_template_handling(self, wrapper):
        """Test handling of very large templates."""
        large_template = "\n".join([f"line {i}" for i in range(1000)])
        variables = {"test": "value"}

        # Should handle large templates without issues
        result = wrapper.wrap_rendering_operation(
            lambda template_content, variables, template_name=None: "processed",
            large_template,
            variables
        )
        assert result == "processed"

    def test_complex_variable_types(self, wrapper):
        """Test handling of complex variable types in snapshots."""
        complex_vars = {
            "string": "hello",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "none": None,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "tuple": (1, 2, 3),
            "set": {1, 2, 3},
            "custom_object": object(),  # Should be handled gracefully
        }

        snapshot = wrapper._create_variable_snapshot(complex_vars)

        # Verify different types are handled appropriately
        assert snapshot["string"] == "hello"
        assert snapshot["number"] == "42"
        assert snapshot["float"] == "3.14"
        assert snapshot["boolean"] == "True"
        assert snapshot["none"] == "None"
        assert "list(3 items)" in snapshot["list"]
        assert "dict(1 keys)" in snapshot["dict"]
        assert "tuple(3 items)" in snapshot["tuple"]
        assert "set(3 items)" in snapshot["set"]
        assert "<object object>" in snapshot["custom_object"]
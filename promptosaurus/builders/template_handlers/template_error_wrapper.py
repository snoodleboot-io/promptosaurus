"""Context-preserving error wrapper for template rendering operations.

This module provides a wrapper that enhances template rendering error handling
by capturing comprehensive context when errors occur, including template source,
variables provided, execution context, line numbers, and template snippets.
"""

import logging
from contextlib import contextmanager
from typing import Any, Dict, Generator, Optional, Callable, TypeVar

import jinja2

from .template_exceptions import (
    TemplateError,
    TemplateSyntaxError,
    TemplateRenderingError,
    TemplateValidationError,
    TemplateSecurityError,
    TemplateComplexityError,
)

logger = logging.getLogger(__name__)

# Type variables for generic wrapper
T = TypeVar('T')


class TemplateErrorWrapper:
    """Wrapper that captures comprehensive context when template errors occur.

    This class provides methods to wrap template rendering operations and ensure
    that any errors are caught and re-raised with enhanced context preservation,
    including line numbers, variable state, template snippets, and proper error
    chaining for root cause analysis.
    """

    def __init__(self, max_context_lines: int = 3, max_variable_preview: int = 100):
        """Initialize the error wrapper.

        Args:
            max_context_lines: Maximum number of lines to include in error context
            max_variable_preview: Maximum length for variable value previews
        """
        self.max_context_lines = max_context_lines
        self.max_variable_preview = max_variable_preview

    def wrap_rendering_operation(
        self,
        operation: Callable[..., T],
        template_content: str,
        variables: Dict[str, Any],
        template_name: Optional[str] = None,
        **operation_kwargs
    ) -> T:
        """Wrap a template rendering operation with comprehensive error handling.

        Args:
            operation: The rendering operation to wrap (function/callable)
            template_content: The template source content
            variables: Variables provided for rendering
            template_name: Optional name/identifier for the template
            **operation_kwargs: Additional arguments to pass to the operation

        Returns:
            The result of the operation if successful

        Raises:
            TemplateError: Enhanced with comprehensive context
        """
        try:
            return operation(
                template_content=template_content,
                variables=variables,
                template_name=template_name,
                **operation_kwargs
            )
        except Exception as original_error:
            # Catch any exception and enhance it with context
            enhanced_error = self._enhance_error(
                original_error,
                template_content,
                variables,
                template_name
            )
            logger.debug(
                f"Template error enhanced with context: {enhanced_error}",
                extra={
                    'template_name': template_name,
                    'error_type': type(original_error).__name__,
                    'enhanced_error_type': type(enhanced_error).__name__,
                }
            )
            raise enhanced_error from original_error

    @contextmanager
    def wrap_rendering_context(
        self,
        template_content: str,
        variables: Dict[str, Any],
        template_name: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """Context manager for wrapping template rendering operations.

        Use this context manager around template rendering code to automatically
        catch and enhance any errors that occur within the context.

        Args:
            template_content: The template source content
            variables: Variables provided for rendering
            template_name: Optional name/identifier for the template

        Yields:
            Dictionary containing context information that can be used by
            the wrapped operation.

        Raises:
            TemplateError: Enhanced with comprehensive context
        """
        context_info = {
            'template_content': template_content,
            'variables': variables,
            'template_name': template_name,
            'error_wrapper': self,
        }

        try:
            yield context_info
        except Exception as original_error:
            enhanced_error = self._enhance_error(
                original_error,
                template_content,
                variables,
                template_name
            )
            logger.debug(
                f"Template error enhanced in context: {enhanced_error}",
                extra={
                    'template_name': template_name,
                    'error_type': type(original_error).__name__,
                    'enhanced_error_type': type(enhanced_error).__name__,
                }
            )
            raise enhanced_error from original_error

    def _enhance_error(
        self,
        original_error: Exception,
        template_content: str,
        variables: Dict[str, Any],
        template_name: Optional[str] = None,
    ) -> TemplateError:
        """Enhance an original error with comprehensive context.

        Args:
            original_error: The original exception that occurred
            template_content: The template source content
            variables: Variables provided for rendering
            template_name: Optional name/identifier for the template

        Returns:
            Enhanced TemplateError with comprehensive context
        """
        # Extract line number and position information from Jinja2 errors
        line_number, column = self._extract_location_info(original_error)

        # Create variable snapshot (avoid exposing sensitive data)
        variable_snapshot = self._create_variable_snapshot(variables)

        # Extract template snippet around the error location
        template_snippet = self._extract_template_snippet(
            template_content, line_number
        )

        # Create appropriate enhanced error based on original error type
        if isinstance(original_error, jinja2.TemplateSyntaxError):
            return TemplateSyntaxError(
                message=f"Jinja2 syntax error: {original_error.message}",
                template_content=template_content,
                template_name=template_name,
                line_number=line_number or original_error.lineno,
                column=column or getattr(original_error, 'pos', None),
                context={
                    'jinja2_error': str(original_error),
                    'template_snippet': template_snippet,
                    'variable_snapshot': variable_snapshot,
                    'error_location': self._format_location(line_number, column),
                }
            )

        elif isinstance(original_error, jinja2.UndefinedError):
            return TemplateRenderingError(
                message=f"Undefined variable in template: {original_error.message}",
                template_content=template_content,
                template_name=template_name,
                variables=variables,  # Include full variables for undefined error
                context={
                    'jinja2_error': str(original_error),
                    'template_snippet': template_snippet,
                    'available_variables': list(variables.keys()),
                    'error_location': self._format_location(line_number, column),
                    'undefined_variable': getattr(original_error, 'name', 'unknown'),
                }
            )

        elif isinstance(original_error, jinja2.TemplateRuntimeError):
            return TemplateRenderingError(
                message=f"Template runtime error: {original_error}",
                template_content=template_content,
                template_name=template_name,
                variables=variable_snapshot,  # Use snapshot to avoid sensitive data
                context={
                    'jinja2_error': str(original_error),
                    'template_snippet': template_snippet,
                    'error_location': self._format_location(line_number, column),
                    'runtime_context': self._extract_runtime_context(original_error),
                }
            )

        elif isinstance(original_error, (TemplateValidationError, TemplateSecurityError, TemplateComplexityError)):
            # These are already our custom errors, just add more context
            original_error.context.update({
                'template_snippet': template_snippet,
                'variable_snapshot': variable_snapshot,
                'error_location': self._format_location(line_number, column),
                'enhanced_by_wrapper': True,
            })
            return original_error

        else:
            # Generic template error for unexpected exceptions
            return TemplateError(
                message=f"Unexpected error during template processing: {type(original_error).__name__}",
                template_content=template_content,
                template_name=template_name,
                context={
                    'original_error_type': type(original_error).__name__,
                    'original_error_message': str(original_error),
                    'template_snippet': template_snippet,
                    'variable_snapshot': variable_snapshot,
                    'error_location': self._format_location(line_number, column),
                    'stack_trace': self._extract_stack_trace(original_error),
                }
            )

    def _extract_location_info(self, error: Exception) -> tuple[Optional[int], Optional[int]]:
        """Extract line number and column information from an error.

        Args:
            error: The exception to analyze

        Returns:
            Tuple of (line_number, column) or (None, None) if not available
        """
        line_number = None
        column = None

        # Check for Jinja2-specific attributes
        if hasattr(error, 'lineno') and error.lineno is not None:
            line_number = error.lineno

        if hasattr(error, 'pos') and error.pos is not None:
            column = error.pos

        return line_number, column

    def _create_variable_snapshot(self, variables: Dict[str, Any]) -> Dict[str, str]:
        """Create a safe snapshot of variables for error reporting.

        This creates previews of variable values without exposing sensitive data.
        Large values are truncated and complex objects are summarized.

        Args:
            variables: The original variables dictionary

        Returns:
            Dictionary with variable names and safe preview values
        """
        snapshot = {}

        for name, value in variables.items():
            try:
                preview = self._create_value_preview(value)
                snapshot[name] = preview
            except Exception:
                # If preview creation fails, use a safe fallback
                snapshot[name] = f"<error creating preview: {type(value).__name__}>"

        return snapshot

    def _create_value_preview(self, value: Any) -> str:
        """Create a safe preview of a variable value.

        Args:
            value: The value to preview

        Returns:
            String representation safe for error reporting
        """
        if value is None:
            return "None"

        value_type = type(value).__name__

        # For primitive types, show actual values
        if isinstance(value, (str, int, float, bool)):
            str_value = str(value)
            if len(str_value) <= self.max_variable_preview:
                return str_value
            else:
                return str_value[:self.max_variable_preview] + "..."

        # For collections, show type and size
        elif isinstance(value, (list, tuple, set)):
            return f"{value_type}({len(value)} items)"

        elif isinstance(value, dict):
            return f"{value_type}({len(value)} keys)"

        # For other objects, just show type
        else:
            return f"<{value_type} object>"

    def _extract_template_snippet(
        self,
        template_content: str,
        line_number: Optional[int]
    ) -> Optional[str]:
        """Extract a snippet of template content around an error location.

        Args:
            template_content: The full template content
            line_number: The line number where the error occurred (1-indexed)

        Returns:
            Template snippet or None if extraction fails
        """
        if not line_number or line_number < 1:
            return None

        try:
            lines = template_content.splitlines()

            # Convert to 0-indexed
            error_line_idx = line_number - 1

            if error_line_idx >= len(lines):
                return None

            # Extract context lines around the error
            start_line = max(0, error_line_idx - self.max_context_lines)
            end_line = min(len(lines), error_line_idx + self.max_context_lines + 1)

            snippet_lines = []
            for i in range(start_line, end_line):
                line_content = lines[i]
                marker = " --> " if i == error_line_idx else "     "
                snippet_lines.append("2d")

            return "\n".join(snippet_lines)

        except Exception:
            # If snippet extraction fails, return None
            return None

    def _format_location(self, line_number: Optional[int], column: Optional[int]) -> str:
        """Format location information for display.

        Args:
            line_number: Line number (1-indexed)
            column: Column number (0-indexed)

        Returns:
            Formatted location string
        """
        if line_number is None:
            return "unknown location"

        if column is not None:
            return f"line {line_number}, column {column}"
        else:
            return f"line {line_number}"

    def _extract_runtime_context(self, error: Exception) -> Dict[str, Any]:
        """Extract additional runtime context from a TemplateRuntimeError.

        Args:
            error: The runtime error to analyze

        Returns:
            Dictionary with additional context information
        """
        context = {}

        # Try to extract any additional information from the error
        for attr in ['name', 'obj', 'filename', 'message']:
            if hasattr(error, attr):
                value = getattr(error, attr)
                if value is not None:
                    context[attr] = str(value)

        return context

    def _extract_stack_trace(self, error: Exception) -> Optional[str]:
        """Extract a simplified stack trace from an exception.

        Args:
            error: The exception to analyze

        Returns:
            Simplified stack trace or None
        """
        import traceback

        try:
            # Get the full traceback
            tb_lines = traceback.format_exception(type(error), error, error.__traceback__)

            # Keep only the last few frames to avoid overwhelming output
            # Skip the first frame (this function) and keep up to 5 frames
            relevant_frames = tb_lines[-6:-1] if len(tb_lines) > 6 else tb_lines[1:]

            return "".join(relevant_frames).strip()

        except Exception:
            return None


# Global instance for convenience
default_error_wrapper = TemplateErrorWrapper()


def wrap_template_operation(
    template_content: str,
    variables: Dict[str, Any],
    template_name: Optional[str] = None,
    wrapper: Optional[TemplateErrorWrapper] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator to wrap template operations with error enhancement.

    Args:
        template_content: The template source content
        variables: Variables provided for rendering
        template_name: Optional name/identifier for the template
        wrapper: The error wrapper to use (default: global instance)

    Returns:
        Decorator function

    Example:
        @wrap_template_operation(template_content, variables, template_name)
        def render_template(template_content, variables, template_name):
            # Your rendering logic here
            return result
    """
    if wrapper is None:
        wrapper = default_error_wrapper

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper_func(*args, **kwargs):
            return wrapper.wrap_rendering_operation(
                func,
                template_content,
                variables,
                template_name,
                **kwargs
            )
        return wrapper_func
    return decorator
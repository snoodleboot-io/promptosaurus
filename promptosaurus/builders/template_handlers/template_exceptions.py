"""Custom exception hierarchy for template processing errors.

This module defines a comprehensive exception hierarchy for template-related operations,
providing typed errors with context preservation for better error handling and debugging.
"""

from typing import Optional, Dict, Any


class TemplateError(Exception):
    """Base exception for all template processing errors.

    This is the root exception class for template-related errors. All template
    exceptions inherit from this class to provide consistent error handling.

    Attributes:
        message: Human-readable error message
        template_content: The template content that caused the error (if available)
        template_name: Name/identifier of the template (if available)
        context: Additional context information about the error
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the template error.

        Args:
            message: Human-readable error message
            template_content: The template content that caused the error
            template_name: Name/identifier of the template
            context: Additional context information
        """
        super().__init__(message)
        self.message = message
        self.template_content = template_content
        self.template_name = template_name
        self.context = context or {}

    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [self.message]

        if self.template_name:
            parts.append(f"Template: {self.template_name}")

        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            parts.append(f"Context: {context_str}")

        return " | ".join(parts)


class TemplateSyntaxError(TemplateError):
    """Exception raised when template syntax is invalid.

    This exception is raised when Jinja2 or other template engines detect
    syntax errors in template content, such as unmatched braces, invalid
    statements, or malformed expressions.

    Examples:
        - Unmatched {{ or }}
        - Invalid {% statements %}
        - Malformed expressions like {{var.attr.nonexistent}}
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        line_number: Optional[int] = None,
        column: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the syntax error.

        Args:
            message: Description of the syntax error
            template_content: The template content with syntax error
            template_name: Name of the template
            line_number: Line number where error occurred
            column: Column number where error occurred
            context: Additional context information
        """
        super().__init__(message, template_content, template_name, context)
        self.line_number = line_number
        self.column = column

        # Add location info to context if provided
        if line_number is not None:
            self.context["line"] = line_number
        if column is not None:
            self.context["column"] = column

    def __str__(self) -> str:
        """Return a string representation with location info."""
        base_str = super().__str__()

        location_parts = []
        if self.line_number is not None:
            location_parts.append(f"line {self.line_number}")
        if self.column is not None:
            location_parts.append(f"column {self.column}")

        if location_parts:
            return f"{base_str} | Location: {', '.join(location_parts)}"

        return base_str


class TemplateRenderingError(TemplateError):
    """Exception raised when template rendering fails at runtime.

    This exception is raised when template rendering fails due to runtime
    issues like undefined variables, type errors, or execution problems
    during the rendering process.

    Examples:
        - Undefined variables in strict mode
        - Type errors during expression evaluation
        - Runtime errors in template filters/macros
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the rendering error.

        Args:
            message: Description of the rendering error
            template_content: The template content that failed to render
            template_name: Name of the template
            variables: Variables that were provided for rendering
            context: Additional context information
        """
        super().__init__(message, template_content, template_name, context)
        self.variables = variables or {}

        # Add variable info to context
        if self.variables:
            self.context["available_variables"] = list(self.variables.keys())


class TemplateValidationError(TemplateError):
    """Exception raised when template validation fails.

    This exception is raised when pre-rendering validation detects issues
    that would prevent successful template processing, such as missing
    required variables or security violations.

    Examples:
        - Missing required variables in strict validation
        - Template complexity exceeding limits
        - Validation rule violations
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        validation_type: Optional[str] = None,
        validation_details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the validation error.

        Args:
            message: Description of the validation failure
            template_content: The template content that failed validation
            template_name: Name of the template
            validation_type: Type of validation that failed (e.g., 'variables', 'security')
            validation_details: Detailed information about validation failure
            context: Additional context information
        """
        super().__init__(message, template_content, template_name, context)
        self.validation_type = validation_type
        self.validation_details = validation_details or {}

        # Add validation info to context
        if self.validation_type:
            self.context["validation_type"] = self.validation_type
        if self.validation_details:
            self.context.update(self.validation_details)


class TemplateSecurityError(TemplateValidationError):
    """Exception raised when template contains security violations.

    This exception is raised when template analysis detects potentially
    dangerous constructs that could lead to code execution, unauthorized
    access, or other security issues.

    Examples:
        - Access to Python internals (__class__, __globals__, etc.)
        - Dangerous method calls (eval, exec, open)
        - Template injection attempts
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        violations: Optional[list[str]] = None,
        severity: str = "high",
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the security error.

        Args:
            message: Description of the security violation
            template_content: The template content with security issues
            template_name: Name of the template
            violations: List of specific security violations detected
            severity: Severity level ('low', 'medium', 'high', 'critical')
            context: Additional context information
        """
        super().__init__(
            message,
            template_content,
            template_name,
            validation_type="security",
            context=context,
        )
        self.violations = violations or []
        self.severity = severity

        # Add security info to context
        self.context["severity"] = self.severity
        if self.violations:
            self.context["violations"] = self.violations

    def __str__(self) -> str:
        """Return a string representation with security details."""
        base_str = super().__str__()

        if self.violations:
            violations_str = ", ".join(self.violations)
            return f"{base_str} | Violations: {violations_str}"

        return base_str


class TemplateComplexityError(TemplateValidationError):
    """Exception raised when template exceeds complexity limits.

    This exception is raised when template analysis determines the template
    is too complex to process safely, based on metrics like nesting depth,
    expression count, or computational complexity.

    Examples:
        - Excessive nesting levels
        - Too many expressions or filters
        - Complex conditional logic
    """

    def __init__(
        self,
        message: str,
        template_content: Optional[str] = None,
        template_name: Optional[str] = None,
        complexity_metrics: Optional[Dict[str, Any]] = None,
        limits: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the complexity error.

        Args:
            message: Description of the complexity issue
            template_content: The template content that's too complex
            template_name: Name of the template
            complexity_metrics: Measured complexity metrics
            limits: Complexity limits that were exceeded
            context: Additional context information
        """
        super().__init__(
            message,
            template_content,
            template_name,
            validation_type="complexity",
            context=context,
        )
        self.complexity_metrics = complexity_metrics or {}
        self.limits = limits or {}

        # Add complexity info to context
        if self.complexity_metrics:
            self.context["metrics"] = self.complexity_metrics
        if self.limits:
            self.context["limits"] = self.limits
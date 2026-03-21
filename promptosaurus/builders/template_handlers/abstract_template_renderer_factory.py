"""Abstract factory interfaces for template renderer dependency injection.

This module defines the factory interfaces and protocols for integrating
template renderers with sweet_tea's dependency injection framework.
"""

from typing import Protocol, TypeVar

from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer

# Type variable for template renderer implementations
TTemplateRenderer = TypeVar('TTemplateRenderer', bound=Jinja2TemplateRenderer)


class AbstractTemplateRendererFactory(Protocol[TTemplateRenderer]):
    """Abstract factory interface for creating template renderer instances.

    This interface defines the contract for factories that create template
    renderer instances, compatible with sweet_tea's AbstractFactory pattern.

    The factory is responsible for:
    - Creating configured template renderer instances
    - Managing dependencies and configuration
    - Providing type-safe factory methods

    Type Parameters:
        TTemplateRenderer: The specific template renderer type this factory creates
    """

    def create(self) -> TTemplateRenderer:
        """Create a new template renderer instance.

        Returns:
            A fully configured template renderer instance ready for use

        Raises:
            FactoryError: If the renderer cannot be created due to configuration
                         or dependency issues
        """
        ...


class TemplateRendererProvider(Protocol):
    """Protocol for components that provide template renderer instances.

    This protocol defines the interface for objects that can provide access
    to template renderer instances, either through direct creation or factory
    delegation. It supports sweet_tea's AbstractInverterFactory pattern for
    dependency resolution.

    Providers are typically used in dependency injection containers to:
    - Resolve template renderer dependencies
    - Provide factory-based instance creation
    - Support multiple renderer configurations
    """

    def get_renderer(self) -> Jinja2TemplateRenderer:
        """Get a template renderer instance.

        Returns:
            A configured template renderer instance

        Raises:
            ProviderError: If no suitable renderer can be provided
        """
        ...


class FactoryError(Exception):
    """Exception raised when factory operations fail."""

    def __init__(self, message: str, factory_type: str | None = None) -> None:
        """Initialize the factory error.

        Args:
            message: Error message describing what went wrong
            factory_type: The type of factory that failed (optional)
        """
        super().__init__(message)
        self.factory_type = factory_type

    def __str__(self) -> str:
        """String representation with factory context."""
        if self.factory_type:
            return f"Factory error in {self.factory_type}: {super().__str__()}"
        return f"Factory error: {super().__str__()}"


class ProviderError(Exception):
    """Exception raised when provider operations fail."""

    def __init__(self, message: str, provider_type: str | None = None) -> None:
        """Initialize the provider error.

        Args:
            message: Error message describing what went wrong
            provider_type: The type of provider that failed (optional)
        """
        super().__init__(message)
        self.provider_type = provider_type

    def __str__(self) -> str:
        """String representation with provider context."""
        if self.provider_type:
            return f"Provider error in {self.provider_type}: {super().__str__()}"
        return f"Provider error: {super().__str__()}"
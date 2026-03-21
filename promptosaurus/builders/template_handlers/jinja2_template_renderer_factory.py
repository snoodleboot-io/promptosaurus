"""Concrete factory implementation for Jinja2 template renderers.

This module provides concrete factory implementations that work with sweet_tea's
AbstractFactory and AbstractInverterFactory patterns for dependency injection
of Jinja2 template renderers.
"""

import jinja2

from promptosaurus.builders.template_handlers.abstract_template_renderer_factory import (
    AbstractTemplateRendererFactory,
    TemplateRendererProvider,
    FactoryError,
    ProviderError,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer


class Jinja2TemplateRendererFactory(AbstractTemplateRendererFactory[Jinja2TemplateRenderer]):
    """Concrete factory for creating Jinja2TemplateRenderer instances.

    This factory implements the AbstractTemplateRendererFactory protocol and provides
    concrete creation logic for Jinja2TemplateRenderer instances with proper
    dependency injection support.

    The factory creates renderer instances with configured Jinja2 environments,
    supporting different configuration scenarios for template processing.
    """

    def __init__(self, template_loader: jinja2.BaseLoader | None = None,
                 environment_options: dict[str, object] | None = None) -> None:
        """Initialize the Jinja2 template renderer factory.

        Args:
            template_loader: Optional Jinja2 template loader for custom loading strategies
            environment_options: Optional dictionary of Jinja2 environment configuration options
        """
        self._template_loader = template_loader
        self._environment_options = environment_options or {}

    def create(self) -> Jinja2TemplateRenderer:
        """Create a new Jinja2TemplateRenderer instance.

        Returns:
            A fully configured Jinja2TemplateRenderer instance ready for use

        Raises:
            FactoryError: If the renderer cannot be created due to configuration issues
        """
        try:
            # Create Jinja2 environment with provided options
            environment = jinja2.Environment(
                loader=self._template_loader,
                **self._environment_options
            )

            # Create and return the renderer
            return Jinja2TemplateRenderer(environment)

        except jinja2.TemplateError as e:
            raise FactoryError(
                f"Failed to create Jinja2 environment: {e}",
                factory_type=self.__class__.__name__
            ) from e
        except Exception as e:
            raise FactoryError(
                f"Unexpected error creating template renderer: {type(e).__name__}",
                factory_type=self.__class__.__name__
            ) from e


class DefaultTemplateRendererProvider(TemplateRendererProvider):
    """Default provider implementation for template renderer instances.

    This provider implements the TemplateRendererProvider protocol and provides
    access to template renderer instances through factory delegation. It supports
    sweet_tea's AbstractInverterFactory pattern for dependency resolution.

    The provider maintains a reference to a factory and delegates instance creation
    to support dependency injection patterns.
    """

    def __init__(self, factory: AbstractTemplateRendererFactory[Jinja2TemplateRenderer]) -> None:
        """Initialize the template renderer provider.

        Args:
            factory: The factory to use for creating renderer instances
        """
        self._factory = factory

    def get_renderer(self) -> Jinja2TemplateRenderer:
        """Get a template renderer instance.

        Returns:
            A configured template renderer instance

        Raises:
            ProviderError: If no suitable renderer can be provided
        """
        try:
            return self._factory.create()
        except FactoryError as e:
            raise ProviderError(
                f"Failed to provide template renderer: {e}",
                provider_type=self.__class__.__name__
            ) from e
        except Exception as e:
            raise ProviderError(
                f"Unexpected error providing template renderer: {type(e).__name__}",
                provider_type=self.__class__.__name__
            ) from e
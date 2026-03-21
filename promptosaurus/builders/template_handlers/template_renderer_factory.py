"""Template renderer factory for dependency injection.

This module provides the main factory class for creating and managing template
renderer instances using sweet_tea's dependency injection framework.
"""

from sweet_tea.abstract_factory import AbstractFactory
from sweet_tea.registry import Registry

from promptosaurus.builders.template_handlers.abstract_template_renderer_factory import (
    AbstractTemplateRendererFactory,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer_factory import (
    Jinja2TemplateRendererFactory,
    DefaultTemplateRendererProvider,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer
from promptosaurus.builders.template_handlers.dependency_resolver import DependencyResolver


# Register template renderer factory components with sweet_tea Registry
Registry.register(
    "jinja2_template_renderer_factory",
    Jinja2TemplateRendererFactory,
    library="promptosaurus"
)
Registry.register(
    "default_template_renderer_provider",
    DefaultTemplateRendererProvider,
    library="promptosaurus"
)


class TemplateRendererFactory:
    """Factory for creating template renderer instances via sweet_tea.

    This factory provides a clean interface for obtaining template renderer
    instances and providers, using sweet_tea's AbstractFactory for dependency
    injection. It supports different renderer types and configuration options.

    The factory handles:
    - Renderer instance creation
    - Provider instantiation
    - Configuration management
    - Error handling and logging
    - Automatic dependency resolution and injection
    """

    @staticmethod
    def create_renderer() -> Jinja2TemplateRenderer:
        """Create a new template renderer instance.

        Returns:
            A fully configured template renderer instance ready for use

        Raises:
            FactoryError: If the renderer cannot be created
        """
        factory = AbstractFactory[Jinja2TemplateRenderer]
        return factory.create("jinja2_template_renderer_factory")

    @staticmethod
    def create_renderer_with_config(
        template_loader=None,
        environment_options=None
    ) -> Jinja2TemplateRenderer:
        """Create a template renderer with custom configuration.

        Args:
            template_loader: Optional Jinja2 template loader
            environment_options: Optional dictionary of Jinja2 environment options

        Returns:
            A configured template renderer instance

        Raises:
            FactoryError: If the renderer cannot be created with the given config
        """
        concrete_factory = Jinja2TemplateRendererFactory(
            template_loader=template_loader,
            environment_options=environment_options
        )
        return concrete_factory.create()

    @staticmethod
    def create_provider(
        factory: AbstractTemplateRendererFactory[Jinja2TemplateRenderer] | None = None
    ):
        """Create a template renderer provider.

        Args:
            factory: Optional factory to use for provider creation.
                    If None, uses the default registered factory.

        Returns:
            A template renderer provider instance

        Raises:
            FactoryError: If the provider cannot be created
        """
        if factory is None:
            # Use the default registered factory
            provider_factory = AbstractFactory[DefaultTemplateRendererProvider]
            provider = provider_factory.create("default_template_renderer_provider")

            # Configure the provider with the default renderer factory
            renderer_factory = AbstractFactory[Jinja2TemplateRenderer]
            default_factory = renderer_factory.create("jinja2_template_renderer_factory")
            provider._factory = default_factory

            return provider
        else:
            # Use the provided factory
            provider_factory = AbstractFactory[DefaultTemplateRendererProvider]
            provider = provider_factory.create("default_template_renderer_provider")
            provider._factory = factory
            return provider

    @staticmethod
    def create_renderer_with_dependency_injection() -> Jinja2TemplateRenderer:
        """Create a template renderer using automatic dependency injection.

        This method uses the DependencyResolver to automatically discover and
        inject dependencies required by the template renderer. Components are
        resolved through sweet_tea's AbstractInverterFactory for seamless
        dependency management.

        Returns:
            A fully configured template renderer with injected dependencies

        Raises:
            DependencyResolverError: If dependency resolution fails
        """
        resolver = DependencyResolver.create_template_renderer_resolver()

        # Resolve the renderer using dependency injection
        renderer = resolver.resolve(Jinja2TemplateRenderer, "jinja2_template_renderer")

        # Inject any additional dependencies the renderer might need
        resolver.inject_dependencies(renderer)

        return renderer

    @staticmethod
    def create_provider_with_dependency_injection() -> DefaultTemplateRendererProvider:
        """Create a template renderer provider using automatic dependency injection.

        This method creates a provider instance with its dependencies automatically
        resolved and injected through the DependencyResolver.

        Returns:
            A configured template renderer provider with injected dependencies

        Raises:
            DependencyResolverError: If dependency resolution or injection fails
        """
        resolver = DependencyResolver.create_template_renderer_resolver()

        # Resolve the provider
        provider = resolver.resolve(DefaultTemplateRendererProvider, "default_template_renderer_provider")

        # Inject dependencies into the provider
        resolver.inject_dependencies(provider)

        # Ensure the provider has access to a renderer factory
        if not hasattr(provider, '_factory') or provider._factory is None:
            renderer_factory = resolver.resolve(AbstractTemplateRendererFactory[Jinja2TemplateRenderer], "jinja2_template_renderer_factory")
            provider._factory = renderer_factory

        return provider

    @staticmethod
    def resolve_component(component_type: type, name: str | None = None):
        """Resolve a component using automatic dependency injection.

        This method provides direct access to the dependency resolver for
        resolving any registered component in the template rendering system.

        Args:
            component_type: The type of component to resolve
            name: Optional component name for named resolution

        Returns:
            The resolved component instance

        Raises:
            DependencyResolverError: If component resolution fails
        """
        resolver = DependencyResolver.create_template_renderer_resolver()
        return resolver.resolve(component_type, name)

    @staticmethod
    def inject_dependencies_into(target: object) -> None:
        """Inject dependencies into an arbitrary target object.

        This method allows dependency injection into any object that requires
        template rendering components or other registered dependencies.

        Args:
            target: The object to inject dependencies into

        Raises:
            DependencyResolverError: If dependency injection fails
        """
        resolver = DependencyResolver.create_template_renderer_resolver()
        resolver.inject_dependencies(target)

    @staticmethod
    def create_provider_with_config(
        template_loader=None,
        environment_options=None
    ):
        """Create a provider with custom renderer configuration.

        Args:
            template_loader: Optional Jinja2 template loader
            environment_options: Optional dictionary of Jinja2 environment options

        Returns:
            A configured template renderer provider

        Raises:
            FactoryError: If the provider cannot be created
        """
        # Create a custom factory with the provided configuration
        custom_factory = Jinja2TemplateRendererFactory(
            template_loader=template_loader,
            environment_options=environment_options
        )

        # Create provider and inject the custom factory
        provider_factory = AbstractFactory[DefaultTemplateRendererProvider]
        provider = provider_factory.create("default_template_renderer_provider")
        provider._factory = custom_factory

        return provider
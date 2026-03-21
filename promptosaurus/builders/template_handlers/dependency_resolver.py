"""Dependency resolver for automatic component discovery and injection.

This module provides a dependency resolver that integrates with sweet_tea's
AbstractInverterFactory to enable automatic component discovery and dependency
injection for template rendering components.
"""

from typing import TypeVar, Generic, Protocol

from sweet_tea.abstract_inverter_factory import AbstractInverterFactory
from sweet_tea.registry import Registry
from sweet_tea.sweet_tea_error import SweetTeaError

try:
    from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer
except ImportError:
    Jinja2TemplateRenderer = None  # type: ignore

try:
    from promptosaurus.builders.template_handlers.template_error_wrapper import TemplateErrorWrapper
except ImportError:
    TemplateErrorWrapper = None  # type: ignore


# Type variables for generic dependency resolution
T = TypeVar('T')


class DependencyResolverError(Exception):
    """Exception raised for dependency resolution errors."""

    def __init__(self, message: str, resolver_type: str | None = None) -> None:
        super().__init__(message)
        self.resolver_type = resolver_type or "DependencyResolver"


class Injectable(Protocol[T]):
    """Protocol for components that can be injected as dependencies."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the injectable component."""
        ...


class DependencyResolver:
    """Dependency resolver using sweet_tea's AbstractInverterFactory.

    This resolver enables automatic component discovery and dependency injection
    by leveraging sweet_tea's inversion of control container. It provides a clean
    interface for resolving dependencies and managing component lifecycles.

    The resolver automatically discovers registered components and can inject
    dependencies into components that require them.
    """

    def __init__(self) -> None:
        """Initialize the dependency resolver."""
        self._inverter_factory = AbstractInverterFactory()

    def resolve(self, component_type: type[T], name: str | None = None) -> T:
        """Resolve a dependency by type and optional name.

        Args:
            component_type: The type of component to resolve
            name: Optional component name for named resolution

        Returns:
            The resolved component instance

        Raises:
            DependencyResolverError: If the dependency cannot be resolved
        """
        try:
            if name is not None:
                return self._inverter_factory.resolve_named(component_type, name)
            else:
                return self._inverter_factory.resolve(component_type)
        except SweetTeaError as e:
            raise DependencyResolverError(
                f"Failed to resolve dependency {component_type.__name__}: {e}",
                resolver_type=self.__class__.__name__
            ) from e
        except Exception as e:
            raise DependencyResolverError(
                f"Unexpected error resolving dependency {component_type.__name__}: {type(e).__name__}",
                resolver_type=self.__class__.__name__
            ) from e

    def inject_dependencies(self, target: object) -> None:
        """Inject dependencies into a target object.

        This method analyzes the target object's dependencies and automatically
        injects them using the resolver.

        Args:
            target: The object to inject dependencies into

        Raises:
            DependencyResolverError: If dependency injection fails
        """
        try:
            # Use the inverter factory to inject dependencies
            self._inverter_factory.inject(target)
        except SweetTeaError as e:
            raise DependencyResolverError(
                f"Failed to inject dependencies into {type(target).__name__}: {e}",
                resolver_type=self.__class__.__name__
            ) from e
        except Exception as e:
            raise DependencyResolverError(
                f"Unexpected error injecting dependencies into {type(target).__name__}: {type(e).__name__}",
                resolver_type=self.__class__.__name__
            ) from e

    def register_component(self, component_type: type, name: str, library: str = "promptosaurus") -> None:
        """Register a component with the dependency resolver.

        Args:
            component_type: The component type to register
            name: The registration name (snake_case)
            library: The library namespace for registration

        Raises:
            DependencyResolverError: If registration fails
        """
        try:
            Registry.register(name, component_type, library=library)
        except SweetTeaError as e:
            raise DependencyResolverError(
                f"Failed to register component {component_type.__name__} as '{name}': {e}",
                resolver_type=self.__class__.__name__
            ) from e
        except Exception as e:
            raise DependencyResolverError(
                f"Unexpected error registering component {component_type.__name__}: {type(e).__name__}",
                resolver_type=self.__class__.__name__
            ) from e

    def has_component(self, component_type: type[T], name: str | None = None) -> bool:
        """Check if a component is registered and available for resolution.

        Args:
            component_type: The component type to check
            name: Optional component name to check

        Returns:
            True if the component is available, False otherwise
        """
        try:
            if name is not None:
                return self._inverter_factory.can_resolve_named(component_type, name)
            else:
                return self._inverter_factory.can_resolve(component_type)
        except Exception:
            # If checking fails, assume component is not available
            return False

    @staticmethod
    def create_template_renderer_resolver() -> 'DependencyResolver':
        """Create a dependency resolver configured for template rendering.

        Returns:
            A pre-configured dependency resolver for template rendering components
        """
        resolver = DependencyResolver()

        # Register core template rendering components
        resolver.register_component(Jinja2TemplateRenderer, "jinja2_template_renderer")
        resolver.register_component(TemplateErrorWrapper, "template_error_wrapper")

        return resolver
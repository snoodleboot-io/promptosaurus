"""Tests for TemplateRendererFactory dependency injection integration."""

import pytest
from unittest.mock import Mock, patch

from promptosaurus.builders.template_handlers.template_renderer_factory import (
    TemplateRendererFactory,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer_factory import (
    Jinja2TemplateRendererFactory,
    DefaultTemplateRendererProvider,
)
from promptosaurus.builders.template_handlers.abstract_template_renderer_factory import (
    FactoryError,
    ProviderError,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer
from sweet_tea.registry import Registry
from sweet_tea.abstract_factory import AbstractFactory


class TestTemplateRendererFactory:
    """Test cases for TemplateRendererFactory static methods."""

    @patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory')
    def test_create_renderer_success(self, mock_abstract_factory):
        """Test successful renderer creation through AbstractFactory."""
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_renderer = Mock(spec=Jinja2TemplateRenderer)
        mock_factory.create.return_value = mock_renderer

        mock_abstract_factory.return_value.create.return_value = mock_factory

        renderer = TemplateRendererFactory.create_renderer()

        mock_abstract_factory.assert_called_once()
        mock_abstract_factory.return_value.create.assert_called_once_with("jinja2_template_renderer_factory")
        mock_factory.create.assert_called_once()
        assert renderer is mock_renderer

    @patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory')
    def test_create_renderer_with_config_success(self, mock_abstract_factory):
        """Test renderer creation with custom configuration."""
        mock_renderer = Mock(spec=Jinja2TemplateRenderer)

        # Mock the concrete factory creation
        with patch('promptosaurus.builders.template_handlers.template_renderer_factory.Jinja2TemplateRendererFactory') as mock_concrete_factory:
            mock_factory_instance = Mock(spec=Jinja2TemplateRendererFactory)
            mock_factory_instance.create.return_value = mock_renderer
            mock_concrete_factory.return_value = mock_factory_instance

            renderer = TemplateRendererFactory.create_renderer_with_config(
                template_loader=None,
                environment_options={"autoescape": True}
            )

            mock_concrete_factory.assert_called_once_with(
                template_loader=None,
                environment_options={"autoescape": True}
            )
            mock_factory_instance.create.assert_called_once()
            assert renderer is mock_renderer

    @patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory')
    def test_create_provider_success(self, mock_abstract_factory):
        """Test successful provider creation with default factory."""
        mock_provider = Mock(spec=DefaultTemplateRendererProvider)
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_renderer = Mock(spec=Jinja2TemplateRenderer)

        # Setup the mock chain
        mock_abstract_factory.return_value.create.side_effect = [mock_provider, mock_factory]
        mock_factory.create.return_value = mock_renderer

        provider = TemplateRendererFactory.create_provider()

        # Verify AbstractFactory was used correctly
        assert mock_abstract_factory.call_count == 2
        # First call for provider, second for default factory
        mock_abstract_factory.return_value.create.assert_any_call("default_template_renderer_provider")
        mock_abstract_factory.return_value.create.assert_any_call("jinja2_template_renderer_factory")

        # Verify provider was configured with factory
        assert provider._factory is mock_factory

    def test_create_provider_with_custom_factory(self):
        """Test provider creation with custom factory."""
        mock_custom_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_provider = Mock(spec=DefaultTemplateRendererProvider)

        with patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory') as mock_abstract_factory:
            mock_abstract_factory.return_value.create.return_value = mock_provider

            provider = TemplateRendererFactory.create_provider(mock_custom_factory)

            mock_abstract_factory.assert_called_once()
            mock_abstract_factory.return_value.create.assert_called_once_with("default_template_renderer_provider")
            assert provider._factory is mock_custom_factory

    def test_create_provider_with_config(self):
        """Test provider creation with custom configuration."""
        mock_provider = Mock(spec=DefaultTemplateRendererProvider)
        mock_renderer = Mock(spec=Jinja2TemplateRenderer)

        with patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory') as mock_abstract_factory, \
             patch('promptosaurus.builders.template_handlers.template_renderer_factory.Jinja2TemplateRendererFactory') as mock_concrete_factory:

            mock_abstract_factory.return_value.create.return_value = mock_provider
            mock_factory_instance = Mock(spec=Jinja2TemplateRendererFactory)
            mock_factory_instance.create.return_value = mock_renderer
            mock_concrete_factory.return_value = mock_factory_instance

            provider = TemplateRendererFactory.create_provider_with_config(
                template_loader=None,
                environment_options={"trim_blocks": True}
            )

            # Verify custom factory was created with config
            mock_concrete_factory.assert_called_once_with(
                template_loader=None,
                environment_options={"trim_blocks": True}
            )

            # Verify provider was created and configured
            mock_abstract_factory.assert_called_once()
            mock_abstract_factory.return_value.create.assert_called_once_with("default_template_renderer_provider")
            assert provider._factory is mock_factory_instance


class TestRegistryIntegration:
    """Test cases for Registry integration and component registration."""

    def test_registry_components_registered(self):
        """Test that factory components are registered with sweet_tea Registry."""
        # Verify that the registry has the expected registrations
        # This tests the module-level registration in template_renderer_factory.py

        # Check that the factory is registered
        factory_entry = Registry._components.get("jinja2_template_renderer_factory")
        assert factory_entry is not None
        assert factory_entry["component"] == Jinja2TemplateRendererFactory
        assert factory_entry["library"] == "promptosaurus"

        # Check that the provider is registered
        provider_entry = Registry._components.get("default_template_renderer_provider")
        assert provider_entry is not None
        assert provider_entry["component"] == DefaultTemplateRendererProvider
        assert provider_entry["library"] == "promptosaurus"

    def test_abstract_factory_integration(self):
        """Test that AbstractFactory can resolve registered components."""
        # This tests the integration between Registry and AbstractFactory

        # Create abstract factories for our registered components
        factory_factory = AbstractFactory[Jinja2TemplateRendererFactory]
        provider_factory = AbstractFactory[DefaultTemplateRendererProvider]

        # Verify we can create instances through AbstractFactory
        factory_instance = factory_factory.create("jinja2_template_renderer_factory")
        assert isinstance(factory_instance, Jinja2TemplateRendererFactory)

        provider_instance = provider_factory.create("default_template_renderer_provider")
        assert isinstance(provider_instance, DefaultTemplateRendererProvider)


class TestFactoryErrorHandling:
    """Test cases for error handling in factory operations."""

    @patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory')
    def test_create_renderer_factory_error(self, mock_abstract_factory):
        """Test handling of FactoryError during renderer creation."""
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_factory.create.side_effect = FactoryError(
            "Factory creation failed",
            factory_type="TestFactory"
        )

        mock_abstract_factory.return_value.create.return_value = mock_factory

        with pytest.raises(FactoryError) as exc_info:
            TemplateRendererFactory.create_renderer()

        assert "Factory creation failed" in str(exc_info.value)
        assert exc_info.value.factory_type == "TestFactory"

    @patch('promptosaurus.builders.template_handlers.template_renderer_factory.AbstractFactory')
    def test_create_provider_registry_error(self, mock_abstract_factory):
        """Test handling of registry resolution errors in provider creation."""
        mock_abstract_factory.return_value.create.side_effect = KeyError("Component not found")

        with pytest.raises(KeyError):
            TemplateRendererFactory.create_provider()


class TestEndToEndIntegration:
    """End-to-end integration tests for the complete factory system."""

    def test_complete_factory_workflow(self):
        """Test complete workflow from factory creation to renderer usage."""
        # Create a renderer through the factory
        renderer = TemplateRendererFactory.create_renderer()
        assert isinstance(renderer, Jinja2TemplateRenderer)

        # Create a provider
        provider = TemplateRendererFactory.create_provider()
        assert isinstance(provider, DefaultTemplateRendererProvider)

        # Get renderer through provider
        provided_renderer = provider.get_renderer()
        assert isinstance(provided_renderer, Jinja2TemplateRenderer)

    def test_custom_config_workflow(self):
        """Test complete workflow with custom configuration."""
        custom_options = {"autoescape": True, "trim_blocks": True}

        # Create renderer with custom config
        renderer = TemplateRendererFactory.create_renderer_with_config(
            environment_options=custom_options
        )
        assert isinstance(renderer, Jinja2TemplateRenderer)
        assert renderer.environment.autoescape is True
        assert renderer.environment.trim_blocks is True

        # Create provider with same config
        provider = TemplateRendererFactory.create_provider_with_config(
            environment_options=custom_options
        )
        assert isinstance(provider, DefaultTemplateRendererProvider)

        # Verify provider returns renderer with same config
        provided_renderer = provider.get_renderer()
        assert isinstance(provided_renderer, Jinja2TemplateRenderer)
        assert provided_renderer.environment.autoescape is True
        assert provided_renderer.environment.trim_blocks is True
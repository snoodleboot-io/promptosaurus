"""Tests for Jinja2 template renderer factory implementation."""

import pytest
from unittest.mock import Mock, patch
import jinja2

from promptosaurus.builders.template_handlers.jinja2_template_renderer_factory import (
    Jinja2TemplateRendererFactory,
    DefaultTemplateRendererProvider,
)
from promptosaurus.builders.template_handlers.abstract_template_renderer_factory import (
    FactoryError,
    ProviderError,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer


class TestJinja2TemplateRendererFactory:
    """Test cases for Jinja2TemplateRendererFactory."""

    def test_create_with_default_options(self):
        """Test factory creates renderer with default Jinja2 options."""
        factory = Jinja2TemplateRendererFactory()

        renderer = factory.create()

        assert isinstance(renderer, Jinja2TemplateRenderer)
        assert renderer.environment is not None
        assert isinstance(renderer.environment, jinja2.Environment)

    def test_create_with_custom_loader(self):
        """Test factory creates renderer with custom template loader."""
        mock_loader = Mock(spec=jinja2.BaseLoader)

        factory = Jinja2TemplateRendererFactory(template_loader=mock_loader)

        renderer = factory.create()

        assert renderer.environment.loader is mock_loader

    def test_create_with_environment_options(self):
        """Test factory creates renderer with custom environment options."""
        custom_options = {
            "trim_blocks": True,
            "lstrip_blocks": True,
            "autoescape": True
        }

        factory = Jinja2TemplateRendererFactory(environment_options=custom_options)

        renderer = factory.create()

        assert renderer.environment.trim_blocks is True
        assert renderer.environment.lstrip_blocks is True
        assert renderer.environment.autoescape is True

    def test_create_handles_template_error(self):
        """Test factory handles Jinja2 TemplateError during creation."""
        with patch("jinja2.Environment", side_effect=jinja2.TemplateError("Invalid template")):
            factory = Jinja2TemplateRendererFactory()

            with pytest.raises(FactoryError) as exc_info:
                factory.create()

            assert "Failed to create Jinja2 environment" in str(exc_info.value)
            assert exc_info.value.factory_type == "Jinja2TemplateRendererFactory"

    def test_create_handles_unexpected_error(self):
        """Test factory handles unexpected errors during creation."""
        with patch("jinja2.Environment", side_effect=ValueError("Unexpected error")):
            factory = Jinja2TemplateRendererFactory()

            with pytest.raises(FactoryError) as exc_info:
                factory.create()

            assert "Unexpected error creating template renderer" in str(exc_info.value)
            assert exc_info.value.factory_type == "Jinja2TemplateRendererFactory"


class TestDefaultTemplateRendererProvider:
    """Test cases for DefaultTemplateRendererProvider."""

    def test_get_renderer_success(self):
        """Test provider successfully returns renderer from factory."""
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_renderer = Mock(spec=Jinja2TemplateRenderer)
        mock_factory.create.return_value = mock_renderer

        provider = DefaultTemplateRendererProvider(mock_factory)

        renderer = provider.get_renderer()

        assert renderer is mock_renderer
        mock_factory.create.assert_called_once()

    def test_get_renderer_handles_factory_error(self):
        """Test provider handles FactoryError from factory."""
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_factory.create.side_effect = FactoryError(
            "Factory creation failed",
            factory_type="TestFactory"
        )

        provider = DefaultTemplateRendererProvider(mock_factory)

        with pytest.raises(ProviderError) as exc_info:
            provider.get_renderer()

        assert "Failed to provide template renderer" in str(exc_info.value)
        assert exc_info.value.provider_type == "DefaultTemplateRendererProvider"

    def test_get_renderer_handles_unexpected_error(self):
        """Test provider handles unexpected errors."""
        mock_factory = Mock(spec=Jinja2TemplateRendererFactory)
        mock_factory.create.side_effect = RuntimeError("Unexpected runtime error")

        provider = DefaultTemplateRendererProvider(mock_factory)

        with pytest.raises(ProviderError) as exc_info:
            provider.get_renderer()

        assert "Unexpected error providing template renderer" in str(exc_info.value)
        assert exc_info.value.provider_type == "DefaultTemplateRendererProvider"


class TestFactoryIntegration:
    """Integration tests for factory and provider interaction."""

    def test_factory_provider_integration(self):
        """Test complete factory-to-provider integration."""
        # Create factory with custom options
        custom_options = {"autoescape": True}
        factory = Jinja2TemplateRendererFactory(environment_options=custom_options)

        # Create provider with the factory
        provider = DefaultTemplateRendererProvider(factory)

        # Get renderer through provider
        renderer = provider.get_renderer()

        # Verify renderer was created correctly
        assert isinstance(renderer, Jinja2TemplateRenderer)
        assert renderer.environment.autoescape is True

    def test_multiple_renderer_instances_are_independent(self):
        """Test that multiple renderer instances are independent."""
        factory = Jinja2TemplateRendererFactory()

        renderer1 = factory.create()
        renderer2 = factory.create()

        # They should be different instances but with equivalent environments
        assert renderer1 is not renderer2
        assert isinstance(renderer1.environment, jinja2.Environment)
        assert isinstance(renderer2.environment, jinja2.Environment)
        # Environments might be shared or separate depending on Jinja2 behavior,
        # but renderers should be independent instances

    def test_provider_with_different_factories(self):
        """Test provider works with different factory configurations."""
        # Factory with loader
        mock_loader = Mock(spec=jinja2.BaseLoader)
        factory1 = Jinja2TemplateRendererFactory(template_loader=mock_loader)

        # Factory with options
        factory2 = Jinja2TemplateRendererFactory(environment_options={"trim_blocks": True})

        # Provider with first factory
        provider = DefaultTemplateRendererProvider(factory1)
        renderer1 = provider.get_renderer()
        assert renderer1.environment.loader is mock_loader

        # Change provider's factory (normally not recommended, but for testing)
        provider._factory = factory2
        renderer2 = provider.get_renderer()
        assert renderer2.environment.trim_blocks is True
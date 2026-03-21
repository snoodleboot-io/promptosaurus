"""Tests for abstract template renderer factory interfaces."""

import pytest
from unittest.mock import Mock

from promptosaurus.builders.template_handlers.abstract_template_renderer_factory import (
    AbstractTemplateRendererFactory,
    TemplateRendererProvider,
    FactoryError,
    ProviderError,
)
from promptosaurus.builders.template_handlers.jinja2_template_renderer import Jinja2TemplateRenderer


class TestAbstractTemplateRendererFactory:
    """Test the abstract factory interface."""

    def test_abstract_factory_is_protocol(self):
        """Test that AbstractTemplateRendererFactory is a protocol."""
        # This test ensures the interface is correctly defined as a Protocol
        # Concrete implementations should be tested separately
        assert hasattr(AbstractTemplateRendererFactory, '__protocol__')
        assert AbstractTemplateRendererFactory.__protocol__ is not None

    def test_factory_create_method_signature(self):
        """Test that the create method has the correct signature."""
        # This is a structural test to ensure the protocol is defined correctly
        # The actual create method will be implemented by concrete factories
        method = getattr(AbstractTemplateRendererFactory, 'create', None)
        assert method is not None
        assert callable(method) is False  # Protocols have non-callable methods


class TestTemplateRendererProvider:
    """Test the provider protocol."""

    def test_provider_is_protocol(self):
        """Test that TemplateRendererProvider is a protocol."""
        assert hasattr(TemplateRendererProvider, '__protocol__')
        assert TemplateRendererProvider.__protocol__ is not None

    def test_provider_get_renderer_method_signature(self):
        """Test that the get_renderer method has the correct signature."""
        method = getattr(TemplateRendererProvider, 'get_renderer', None)
        assert method is not None
        assert callable(method) is False  # Protocols have non-callable methods


class TestFactoryError:
    """Test the FactoryError exception."""

    def test_factory_error_initialization(self):
        """Test FactoryError initialization."""
        error = FactoryError("Test factory error")
        assert str(error) == "Factory error: Test factory error"
        assert error.factory_type is None

    def test_factory_error_with_factory_type(self):
        """Test FactoryError with factory type."""
        error = FactoryError("Test factory error", "TestFactory")
        assert str(error) == "Factory error in TestFactory: Test factory error"
        assert error.factory_type == "TestFactory"


class TestProviderError:
    """Test the ProviderError exception."""

    def test_provider_error_initialization(self):
        """Test ProviderError initialization."""
        error = ProviderError("Test provider error")
        assert str(error) == "Provider error: Test provider error"
        assert error.provider_type is None

    def test_provider_error_with_provider_type(self):
        """Test ProviderError with provider type."""
        error = ProviderError("Test provider error", "TestProvider")
        assert str(error) == "Provider error in TestProvider: Test provider error"
        assert error.provider_type == "TestProvider"


# TODO: Add integration tests when concrete implementations are available
# These will test actual factory creation and dependency injection scenarios
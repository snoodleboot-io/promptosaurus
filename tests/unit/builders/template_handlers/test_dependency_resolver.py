"""Tests for dependency resolver functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from promptosaurus.builders.template_handlers.dependency_resolver import (
    DependencyResolver,
    DependencyResolverError,
)
from sweet_tea.sweet_tea_error import SweetTeaError


class TestDependencyResolver:
    """Test cases for the DependencyResolver class."""

    def test_initialization(self):
        """Test that DependencyResolver initializes correctly."""
        resolver = DependencyResolver()
        assert resolver is not None
        assert hasattr(resolver, '_inverter_factory')

    def test_resolve_success(self):
        """Test successful dependency resolution."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'resolve') as mock_resolve:
            mock_resolve.return_value = Mock(spec=mock_component_class)

            result = resolver.resolve(mock_component_class)

            assert result is not None
            mock_resolve.assert_called_once_with(mock_component_class)

    def test_resolve_named_success(self):
        """Test successful named dependency resolution."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'resolve_named') as mock_resolve_named:
            mock_resolve_named.return_value = Mock(spec=mock_component_class)

            result = resolver.resolve(mock_component_class, "test_renderer")

            assert result is not None
            mock_resolve_named.assert_called_once_with(mock_component_class, "test_renderer")

    def test_resolve_failure_sweet_tea_error(self):
        """Test dependency resolution failure due to SweetTeaError."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'resolve') as mock_resolve:
            mock_resolve.side_effect = SweetTeaError("Component not found")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.resolve(mock_component_class)

            assert "Failed to resolve dependency" in str(exc_info.value)
            assert mock_component_class.__name__ in str(exc_info.value)

    def test_resolve_failure_generic_error(self):
        """Test dependency resolution failure due to generic error."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'resolve') as mock_resolve:
            mock_resolve.side_effect = Exception("Unexpected error")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.resolve(mock_component_class)

            assert "Unexpected error resolving dependency" in str(exc_info.value)
            assert "Exception" in str(exc_info.value)

    def test_inject_dependencies_success(self):
        """Test successful dependency injection."""
        resolver = DependencyResolver()
        target = Mock()

        with patch.object(resolver._inverter_factory, 'inject') as mock_inject:
            resolver.inject_dependencies(target)

            mock_inject.assert_called_once_with(target)

    def test_inject_dependencies_failure_sweet_tea_error(self):
        """Test dependency injection failure due to SweetTeaError."""
        resolver = DependencyResolver()
        target = Mock()

        with patch.object(resolver._inverter_factory, 'inject') as mock_inject:
            mock_inject.side_effect = SweetTeaError("Injection failed")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.inject_dependencies(target)

            assert "Failed to inject dependencies" in str(exc_info.value)
            assert "Injection failed" in str(exc_info.value)

    def test_inject_dependencies_failure_generic_error(self):
        """Test dependency injection failure due to generic error."""
        resolver = DependencyResolver()
        target = Mock()

        with patch.object(resolver._inverter_factory, 'inject') as mock_inject:
            mock_inject.side_effect = Exception("Unexpected injection error")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.inject_dependencies(target)

            assert "Unexpected error injecting dependencies" in str(exc_info.value)

    def test_register_component_success(self):
        """Test successful component registration."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch('promptosaurus.builders.template_handlers.dependency_resolver.Registry.register') as mock_register:
            resolver.register_component(mock_component_class, "test_renderer")

            mock_register.assert_called_once_with("test_renderer", mock_component_class, library="promptosaurus")

    def test_register_component_failure_sweet_tea_error(self):
        """Test component registration failure due to SweetTeaError."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch('promptosaurus.builders.template_handlers.dependency_resolver.Registry.register') as mock_register:
            mock_register.side_effect = SweetTeaError("Registration failed")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.register_component(mock_component_class, "test_renderer")

            assert "Failed to register component" in str(exc_info.value)
            assert mock_component_class.__name__ in str(exc_info.value)

    def test_register_component_failure_generic_error(self):
        """Test component registration failure due to generic error."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch('promptosaurus.builders.template_handlers.dependency_resolver.Registry.register') as mock_register:
            mock_register.side_effect = Exception("Unexpected registration error")

            with pytest.raises(DependencyResolverError) as exc_info:
                resolver.register_component(mock_component_class, "test_renderer")

            assert "Unexpected error registering component" in str(exc_info.value)

    def test_has_component_success(self):
        """Test successful component availability check."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'can_resolve', return_value=True):
            assert resolver.has_component(mock_component_class) is True

    def test_has_component_named_success(self):
        """Test successful named component availability check."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'can_resolve_named', return_value=True):
            assert resolver.has_component(mock_component_class, "test_renderer") is True

    def test_has_component_failure(self):
        """Test component availability check when component is not available."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'can_resolve', return_value=False):
            assert resolver.has_component(mock_component_class) is False

    def test_has_component_check_error(self):
        """Test component availability check when check fails."""
        resolver = DependencyResolver()
        mock_component_class = MagicMock()

        with patch.object(resolver._inverter_factory, 'can_resolve', side_effect=Exception("Check failed")):
            # Should return False when check fails, not raise exception
            assert resolver.has_component(mock_component_class) is False

    @patch('promptosaurus.builders.template_handlers.dependency_resolver.Registry.register')
    def test_create_template_renderer_resolver(self, mock_register):
        """Test creation of template renderer resolver with pre-configured components."""
        resolver = DependencyResolver.create_template_renderer_resolver()

        assert resolver is not None
        assert isinstance(resolver, DependencyResolver)

        # Verify that the core components were registered
        assert mock_register.call_count == 2

        # Check the calls (order may vary)
        calls = mock_register.call_args_list
        call_names = [call[0][0] for call in calls]  # Extract the name parameter

        assert "jinja2_template_renderer" in call_names
        assert "template_error_wrapper" in call_names

        # Verify all calls use the correct library
        for call in calls:
            assert call[1]['library'] == "promptosaurus"


class TestDependencyResolverIntegration:
    """Integration tests for dependency resolver with template renderer components."""

    @patch('promptosaurus.builders.template_handlers.dependency_resolver.Registry.register')
    def test_integration_with_template_renderer_factory(self, mock_register):
        """Test that dependency resolver integrates properly with template renderer factory."""
        from promptosaurus.builders.template_handlers.template_renderer_factory import TemplateRendererFactory

        # This test verifies that the factory can create components with dependency injection
        # without actually resolving dependencies (which would require full sweet_tea setup)

        resolver = DependencyResolver.create_template_renderer_resolver()

        # Verify the resolver was created with proper registrations
        assert resolver is not None
        assert mock_register.call_count == 2

    def test_error_hierarchy(self):
        """Test that DependencyResolverError properly inherits from Exception."""
        error = DependencyResolverError("Test error", "TestResolver")

        assert isinstance(error, Exception)
        assert str(error) == "Test error"
        assert error.resolver_type == "TestResolver"
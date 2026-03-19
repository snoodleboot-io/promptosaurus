"""Base Builder class for all output builders.

This module provides the Builder abstract base class that defines the interface
for all AI tool-specific output builders. Each builder transforms the prompt
registry into the specific format required by different AI assistant tools.

Classes:
    Builder: Abstract base class for output builders.

Example:
    >>> from promptosaurus.builders.builder import Builder
    >>> # Subclass to create a new builder
    >>> class MyToolBuilder(Builder):
    ...     def build(self, output, config=None, dry_run=False):
    ...         # Implementation
    ...         return ["Created config files"]
    """

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Callable, Optional

from promptosaurus.builders.template_handlers.template_handler import TemplateHandler

from promptosaurus.registry import registry


@runtime_checkable
class TemplateVariableHandler(Protocol):
    """Protocol for template variable handlers."""

    def can_handle(self, variable_name: str) -> bool:
        """Determine if this handler can process the given variable.

        Args:
            variable_name: The name of the template variable (without braces)

        Returns:
            True if this handler can process the variable, False otherwise
        """
        ...

    def handle(self, variable_name: str, config: Dict[str, Any]) -> str:
        """Handle the template variable substitution.

        Args:
            variable_name: The name of the template variable (without braces)
            config: The configuration dictionary

        Returns:
            The substituted value for the template variable
        """
        ...


class TemplateHandlerRegistry:
    """Registry for template variable handlers."""

    def __init__(self):
        self._handlers: List[TemplateVariableHandler] = []

    def register_handler(self, handler: TemplateVariableHandler) -> None:
        """Register a template variable handler.

        Args:
            handler: The handler to register
        """
        self._handlers.append(handler)

    def unregister_handler(self, handler: TemplateVariableHandler) -> None:
        """Unregister a template variable handler.

        Args:
            handler: The handler to unregister
        """
        if handler in self._handlers:
            self._handlers.remove(handler)

    def get_handlers(self) -> List[TemplateVariableHandler]:
        """Get all registered handlers.

        Returns:
            List of registered template variable handlers
        """
        return self._handlers.copy()

    def get_handler_for_variable(self, variable_name: str) -> Optional[TemplateVariableHandler]:
        """Get the first handler that can handle the given variable.

        Args:
            variable_name: The name of the template variable (without braces)

        Returns:
            The handler that can process the variable, or None if no handler can
        """
        for handler in self._handlers:
            if handler.can_handle(variable_name):
                return handler
        return None


class Builder:
    """Base class for all builders that generate output configs.

    This abstract class defines the interface that all tool-specific builders
    must implement. Subclasses should override the build() method to generate
    the appropriate output format for their target AI tool.

    Attributes:
        _base_files: List of core prompt files included in all builds.

    Methods:
        build: Generate output configuration files.
        _build_concatenated: Create concatenated rules file content.
        _substitute_template_variables: Replace {{VARIABLE}} templates with values from config.
        _copy: Copy a source file to destination with optional template substitution.
    """

    _base_files = [
        "agents/core/core-system.md",
        "agents/core/core-conventions.md",
        "agents/core/core-session.md",
    ]

    def __init__(self, template_handler_factory: Callable[[], List[TemplateHandler]] = None):
        """Initialize the builder with a template handler factory.

        Args:
            template_handler_factory: Optional factory that returns a list of TemplateHandler instances.
                                      If None, uses default factory with standard handlers.
        """
        self._template_handler_factory = template_handler_factory or self._get_default_template_handler_factory()
        self._template_handlers = self._template_handler_factory()

    def build(
        self, output: Path, config: dict[str, Any] | None = None, dry_run: bool = False
    ) -> list[str]:
        """Build output configs.

        This method should be overridden by subclasses to generate tool-specific
        configuration files.

        Args:
            output: Directory to write output into.
            config: Optional configuration dict with template variables.
            dry_run: If True, preview what would be written without touching filesystem.

        Returns:
            List of messages describing what was done (or would have been done).
        """
        raise NotImplementedError

    def build(
        self, output: Path, config: dict[str, Any] | None = None, dry_run: bool = False
    ) -> list[str]:
        """Build output configs.

        This method should be overridden by subclasses to generate tool-specific
        configuration files.

        Args:
            output: Directory to write output into.
            config: Optional configuration dict with template variables.
            dry_run: If True, preview what would be written without touching filesystem.

        Returns:
            List of messages describing what was done (or would have been done).
        """
        raise NotImplementedError

    def _build_concatenated_content(
        cls, tool_comment: str, config: dict[str, Any] | None = None
    ) -> str:
        """Create concatenated rules file content.

        This method creates the content for a concatenated rules file by
        combining all the prompt files in the registry's concat_order.

        Args:
            tool_comment: Comment string to identify the tool (e.g., '# .clinerules').
            config: Optional configuration dict with template variables.

        Returns:
            Complete concatenated rules file content as a string.

        Example:
            >>> content = cls._build_concatenated('# .clinerules')
            >>> print(content[:100])
            # .clinerules
            # Auto-generated by prompt CLI...
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines: list[str] = [
            tool_comment,
            "# Auto-generated by prompt CLI — edit files in prompts/ then rebuild",
            f"# Last built: {now}",
            "",
        ]

        for label, filename in registry.concat_order:
            try:
                body = registry.prompt_body(filename)
                # Apply template substitution if config is provided
                if config:
                    # Create a temporary instance to access the instance method
                    temp_instance = cls()
                    body = temp_instance._substitute_template_variables(body, config)
            except FileNotFoundError:
                lines.append(f"## {label} — MISSING: {filename}")
                lines.append("")
                continue

            lines.append("---")
            lines.append(f"## {label}")
            lines.append("")
            lines.append(body.rstrip())
            lines.append("")

        return "\n".join(lines) + "\n"

    def _substitute_template_variables(self, content: str, config: dict[str, Any] | None = None) -> str:
        """Replace {{VARIABLE}} templates with values from config.

        This method performs template variable substitution on content,
        replacing placeholders like {{LANGUAGE}} with actual values
        from the configuration. It uses registered template variable handlers
        to determine how to substitute each variable.

        Args:
            content: The template content with {{VARIABLE}} placeholders.
            config: Optional configuration dict containing spec values.

        Returns:
            Content with all template variables replaced.
        """
        if config is None:
            config = {}

        # Handle both single-language (dict) and multi-language (list) configs
        if isinstance(config.get("spec"), list):
            # Multi-language monorepo: get config from first folder
            config = config.get("spec", [{}])[0] if config.get("spec") else {}
        else:
            config = config.get("spec", {})

        # Import regex here to avoid top-level import if not used
        import re

        # Find all template variables in the content
        template_pattern = r'\{\{([A-Z_][A-Z0-9_]*)\}\}'
        matches = re.findall(template_pattern, content)

        # Process each unique template variable
        substitutions = {}
        for var_name in set(matches):
            template_var = f"{{{{{var_name}}}}}"
            value = self._get_variable_value(var_name, config)
            if value is not None:  # Only substitute if we have a value
                substitutions[template_var] = value

        # Perform substitutions
        for template_var, value in substitutions.items():
            content = content.replace(template_var, value)

        return content

    def _get_variable_value(self, variable_name: str, config: Dict[str, Any]) -> str:
        """Get the value for a template variable by consulting registered handlers.

        Args:
            variable_name: The name of the template variable (without braces)
            config: The configuration dictionary

        Returns:
            The substituted value, or None if no handler can process the variable
        """
        handler = self._template_handler_registry.get_handler_for_variable(variable_name)
        if handler:
            return handler.handle(variable_name, config)
        return None

    def register_template_handler(self, handler: TemplateVariableHandler) -> None:
        """Register a custom template variable handler.

        Args:
            handler: The handler to register
        """
        self._template_handler_registry.register_handler(handler)

    def unregister_template_handler(self, handler: TemplateVariableHandler) -> None:
        """Unregister a template variable handler.

        Args:
            handler: The handler to unregister
        """
        self._template_handler_registry.unregister_handler(handler)

    def _get_default_template_handler_registry(self) -> TemplateHandlerRegistry:
        """Get the default template variable handler registry by dynamically loading them.

        Returns:
            TemplateHandlerRegistry with default template variable handlers
        """
        registry = TemplateHandlerRegistry()

        # Import and instantiate all handler classes from the template_handlers package
        try:
            import pkg_resources
            from promptosaurus.builders.template_handlers import (
                language_handler,
                runtime_handler,
                package_manager_handler,
                linter_handler,
                formatter_handler,
                abstract_class_style_handler,
                mocking_library_handler,
                coverage_tool_handler,
                mutation_tool_handler,
                framework_handler,
                e2e_tool_handler,
                testing_framework_handler,
                test_runner_handler,
                coverage_handler
            )

            # Get all handler classes from the modules
            handler_classes = []

            # Language handler
            if hasattr(language_handler, 'LanguageHandler'):
                handler_classes.append(language_handler.LanguageHandler)

            # Runtime handler
            if hasattr(runtime_handler, 'RuntimeHandler'):
                handler_classes.append(runtime_handler.RuntimeHandler)

            # Package manager handler
            if hasattr(package_manager_handler, 'PackageManagerHandler'):
                handler_classes.append(package_manager_handler.PackageManagerHandler)

            # Linter handler
            if hasattr(linter_handler, 'LinterHandler'):
                handler_classes.append(linter_handler.LinterHandler)

            # Formatter handler
            if hasattr(formatter_handler, 'FormatterHandler'):
                handler_classes.append(formatter_handler.FormatterHandler)

            # Abstract class style handler
            if hasattr(abstract_class_style_handler, 'AbstractClassStyleHandler'):
                handler_classes.append(abstract_class_style_handler.AbstractClassStyleHandler)

            # Mocking library handler
            if hasattr(mocking_library_handler, 'MockingLibraryHandler'):
                handler_classes.append(mocking_library_handler.MockingLibraryHandler)

            # Coverage tool handler
            if hasattr(coverage_tool_handler, 'CoverageToolHandler'):
                handler_classes.append(coverage_tool_handler.CoverageToolHandler)

            # Mutation tool handler
            if hasattr(mutation_tool_handler, 'MutationToolHandler'):
                handler_classes.append(mutation_tool_handler.MutationToolHandler)

            # Framework handler
            if hasattr(framework_handler, 'FrameworkHandler'):
                handler_classes.append(framework_handler.FrameworkHandler)

            # E2E tool handler
            if hasattr(e2e_tool_handler, 'E2EToolHandler'):
                handler_classes.append(e2e_tool_handler.E2EToolHandler)

            # Testing framework handler
            if hasattr(testing_framework_handler, 'TestingFrameworkHandler'):
                handler_classes.append(testing_framework_handler.TestingFrameworkHandler)

            # Test runner handler
            if hasattr(test_runner_handler, 'TestRunnerHandler'):
                handler_classes.append(test_runner_handler.TestRunnerHandler)

            # Coverage handler
            if hasattr(coverage_handler, 'CoverageHandler'):
                handler_classes.append(coverage_handler.CoverageHandler)

            # Instantiate all handler classes and register them
            for cls in handler_classes:
                registry.register_handler(cls())

        except ImportError as e:
            # Fallback to original handlers if dynamic loading fails
            fallback_handlers = [
                LanguageHandler(),
                RuntimeHandler(),
                PackageManagerHandler(),
                LinterHandler(),
                FormatterHandler(),
                AbstractClassStyleHandler(),
                TestingFrameworkHandler(),
                TestRunnerHandler(),
                CoverageHandler()
            ]
            for handler in fallback_handlers:
                registry.register_handler(handler)

        return registry

    def _copy(
        self,
        source_path: Path,
        destination: Path,
        dry_run: bool,
        config: dict[str, Any] | None = None,
    ) -> str:
        """Copy a source file to destination with optional template substitution.

        Internal helper that handles file copying with support for
        template variable substitution in files that need it.

        Args:
            source_path: Source file path to copy from.
            destination: Destination file path to copy to.
            dry_run: If True, return preview string without copying.
            config: Optional config dict for template variable substitution.

        Returns:
            Action string describing the copy operation.
        """
        rel = str(destination).split(".kilocode/", 1)[-1]
        label = f".kilocode/{rel}"
        if dry_run:
            return f"[dry-run] {source_path.name} → {label}"
        destination.parent.mkdir(parents=True, exist_ok=True)

        # If config is provided and this is a language-specific conventions file,
        # perform template substitution
        if config and source_path.name.startswith("core-"):
            content = source_path.read_text(encoding="utf-8")
            content = self._substitute_template_variables(content, config)
            destination.write_text(content, encoding="utf-8")
        else:
            import shutil
            shutil.copy2(source_path, destination)

        return f"✓ {source_path.name} → {label}"


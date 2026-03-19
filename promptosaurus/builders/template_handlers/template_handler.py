"""Base class for template variable handlers."""

from typing import Any, Dict

from promptosaurus.builders.builder import TemplateVariableHandler


class TemplateHandler(TemplateVariableHandler):
    """Base class for template variable handlers."""

    def can_handle(self, variable_name: str) -> bool:
        raise NotImplementedError("Subclasses must implement can_handle method")

    def handle(self, variable_name: str, config: Dict[str, Any]) -> str:
        raise NotImplementedError("Subclasses must implement handle method")
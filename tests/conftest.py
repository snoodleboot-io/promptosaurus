"""Pytest configuration for promptosaurus tests."""

import pytest

from promptosaurus.builders.factory import BuilderFactory
from promptosaurus.builders.kilo_builder import KiloBuilder
from promptosaurus.builders.cline_builder import ClineBuilder
from promptosaurus.builders.claude_builder import ClaudeBuilder


def pytest_configure(config):
    """Register custom markers and initialize builders."""
    config.addinivalue_line("markers", "unit: marks tests as unit tests (fast, isolated)")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "slow: marks tests as slow running")
    config.addinivalue_line("markers", "security: marks tests as security focused")

    # Register available builders
    BuilderFactory.register("kilo", KiloBuilder)
    BuilderFactory.register("cline", ClineBuilder)
    BuilderFactory.register("claude", ClaudeBuilder)


# Mark all tests in tests/unit/ as unit tests by default
def pytest_collection_modifyitems(config, items):
    """Automatically mark unit tests."""
    for item in items:
        if "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)

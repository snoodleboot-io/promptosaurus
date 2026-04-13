"""Tests for TypeScript-specific questions."""

import pytest

from promptosaurus.questions.typescript.typescript_framework_question import (
    TypeScriptFrameworkQuestion,
)
from promptosaurus.questions.typescript.typescript_version_question import TypeScriptVersionQuestion
from promptosaurus.questions.typescript.typescript_package_manager_question import TypeScriptPackageManagerQuestion


class TestTypeScriptVersionQuestion:
    """Tests for TypeScriptVersionQuestion."""

    def test_question_has_required_properties(self):
        """Question should have all required properties."""
        q = TypeScriptVersionQuestion()

        assert q.key == "typescript_version"
        assert q.options

    def test_options_are_major_x_only(self):
        """Options should be simplified major.x versions."""
        q = TypeScriptVersionQuestion()

        # Should have simplified versions
        assert "6.x" in q.options
        assert "5.x" in q.options
        # Should NOT have individual minor versions
        assert "6.0" not in q.options
        assert "5.9" not in q.options
        assert "5.4" not in q.options

    def test_default_is_latest(self):
        """Default should be latest stable version."""
        q = TypeScriptVersionQuestion()

        assert q.default == "6.x"


class TestTypeScriptPackageManagerQuestion:
    """Tests for TypeScriptPackageManagerQuestion."""

    def test_question_has_required_properties(self):
        """Question should have all required properties."""
        q = TypeScriptPackageManagerQuestion()

        assert q.key == "typescript_package_manager"
        assert q.options

    def test_options_include_common_managers(self):
        """Options should include common package managers."""
        q = TypeScriptPackageManagerQuestion()

        assert "pnpm" in q.options
        assert "npm" in q.options
        assert "yarn" in q.options

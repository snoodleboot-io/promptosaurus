# Python language questions

from promptcli.questions.base import BaseQuestion


class PythonRuntimeQuestion(BaseQuestion):
    """Question handler for Python runtime/version."""

    @property
    def key(self) -> str:
        return "python_runtime"

    @property
    def question_text(self) -> str:
        return "What Python runtime version do you want to use?"

    @property
    def explanation(self) -> str:
        return """Python runtime affects package compatibility, performance, and available features.

- Newer versions have better performance but may have compatibility issues
- Some packages only support specific versions
- match statements require 3.10+, walrus operator requires 3.8+"""

    @property
    def options(self) -> list[str]:
        return ["3.12", "3.11", "3.10", "3.9", "pypy"]

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "3.12": "Latest stable - best performance, recommended for new projects",
            "3.11": "Very stable - excellent performance improvements over 3.10",
            "3.10": "Stable - pattern matching (match/case), better error messages",
            "3.9": "Long-term support - maximum package compatibility",
            "pypy": "JIT compiler - faster for long-running processes, good for servers",
        }

    @property
    def default(self) -> str:
        return "3.12"


class PythonPackageManagerQuestion(BaseQuestion):
    """Question for Python package manager."""

    @property
    def key(self) -> str:
        return "python_package_manager"

    @property
    def question_text(self) -> str:
        return "What package manager do you want to use for Python?"

    @property
    def explanation(self) -> str:
        return """Package manager affects:
- Dependency resolution and lock file management
- Virtual environment handling
- Build system integration
- Publishing to PyPI"""

    @property
    def options(self) -> list[str]:
        return ["poetry", "pip", "uv", "conda", "pdm"]

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "poetry": "Modern, all-in-one - dependency + env + build (recommended for new projects)",
            "pip": "Standard - simple, widely compatible, no lock file by default",
            "uv": "Extremely fast - Rust-based, good for CI/CD and large projects",
            "conda": "Data science focus - manages non-Python dependencies too",
            "pdm": "Modern PEP 582 - no virtualenv, good pyproject.toml integration",
        }

    @property
    def default(self) -> str:
        return "poetry"


class PythonTestFrameworkQuestion(BaseQuestion):
    """Question for Python test framework."""

    @property
    def key(self) -> str:
        return "python_test_framework"

    @property
    def question_text(self) -> str:
        return "What testing framework do you want to use?"

    @property
    def explanation(self) -> str:
        return """Testing framework affects:
- Test discovery and organization
- Assertion style and reporting
- Fixture and mocking capabilities
- Integration with coverage tools"""

    @property
    def options(self) -> list[str]:
        return ["pytest", "unittest", "doctest", "nose2"]

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "pytest": "Industry standard - powerful fixtures, great reporting, widely used",
            "unittest": "Built-in - simple, no dependencies, good for beginners",
            "doctest": "Documentation testing - tests in docstrings, good for math/code clarity",
            "nose2": "nose successor - plugin ecosystem, pytest-like",
        }

    @property
    def default(self) -> str:
        return "pytest"


class PythonLinterQuestion(BaseQuestion):
    """Question for Python linter - supports multiple selection."""

    @property
    def key(self) -> str:
        return "python_linter"

    @property
    def question_text(self) -> str:
        return "What linter(s) do you want to use?"

    @property
    def explanation(self) -> str:
        return """Linters check code quality, style, and bugs. You can select multiple:
- ruff: Ultra-fast (Rust), modern, replaces flake8+isort
- flake8: Classic, simple, stable rules
- pylint: Comprehensive deep analysis, very strict
- mypy: Static type checker for Python"""

    @property
    def options(self) -> list[str]:
        return ["ruff", "flake8", "pylint", "mypy"]

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "ruff": "Ultra-fast (Rust) - modern, replaces flake8+isort, recommended",
            "flake8": "Classic - simple, stable, good default rules",
            "pylint": "Comprehensive - deep analysis, strict, many rules",
            "mypy": "Type checker - optional static typing enforcement",
        }

    @property
    def default(self) -> str:
        return "ruff"

    @property
    def allow_multiple(self) -> bool:
        """Allow selecting multiple linters."""
        return True


class PythonFormatterQuestion(BaseQuestion):
    """Question for Python formatter - supports multiple selection."""

    @property
    def key(self) -> str:
        return "python_formatter"

    @property
    def question_text(self) -> str:
        return "What code formatter(s) do you want to use?"

    @property
    def explanation(self) -> str:
        return """Formatters ensure consistent code style. You can select multiple:
- ruff: Fastest (Rust), format + lint in one tool
- black: Most popular, opinionated style
- yapf: Google style, configurable"""

    @property
    def options(self) -> list[str]:
        return ["ruff", "black", "yapf"]

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "ruff": "Fastest (Rust) - format + lint in one, recommended",
            "black": "Most popular - opinionated, consistent, widely adopted",
            "yapf": "Google style - configurable, good for existing codebases",
        }

    @property
    def default(self) -> str:
        return "ruff"

    @property
    def allow_multiple(self) -> bool:
        """Allow selecting multiple formatters."""
        return True

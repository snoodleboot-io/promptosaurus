# Python test framework question

from promptcli.questions.base import BaseQuestion


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

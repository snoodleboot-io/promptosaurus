# TypeScript version question

from promptosaurus.questions.base.question import Question


class TypeScriptVersionQuestion(Question):
    """Question handler for TypeScript version."""

    @property
    def key(self) -> str:
        return "typescript_version"

    @property
    def question_text(self) -> str:
        return "What TypeScript version do you want to use?"

    @property
    def explanation(self) -> str:
        return """TypeScript version affects available features and type system capabilities.

- Newer versions have better inference and more features
- Older versions have better ecosystem compatibility"""

    @property
    def options(self) -> list[str]:
        return ["5.x", "5.4", "5.3", "5.0", "4.x"]

    @property
    def default(self) -> str:
        return "5.x"

    @property
    def option_explanations(self) -> dict[str, str]:
        return {
            "5.x": "Latest stable TypeScript 5.x (recommended)",
            "5.4": "TypeScript 5.4 (specific version)",
            "5.3": "TypeScript 5.3 (specific version)",
            "5.0": "TypeScript 5.0 (specific version)",
            "4.x": "TypeScript 4.x (older, better compatibility)",
        }

"""Examples demonstrating builder usage patterns.

This module shows how to use the builders module, including:
1. Creating custom builders by implementing AbstractBuilder
2. Using the BuilderFactory for dynamic builder retrieval
3. Using the BuilderRegistry for managing builder instances
4. Implementing protocol-based mixins for optional features
5. Error handling and validation
"""

from typing import Any

from src.builders.base import AbstractBuilder, BuildOptions
from src.builders.factory import BuilderFactory
from src.builders.registry import BuilderRegistry
from src.builders.interfaces import SupportsSkills, SupportsWorkflows, SupportsRules
from src.builders.errors import (
    BuilderValidationError,
    BuilderNotFoundError,
    UnsupportedFeatureError,
)
from src.ir.models import Agent, Skill, Workflow, Rules


# ==============================================================================
# Example 1: Creating a Custom Builder
# ==============================================================================


class KiloBuilder(AbstractBuilder):
    """Example builder for the Kilo framework.

    This builder generates Kilo-specific configuration output from Agent IR models.
    It supports skills, workflows, and rules through Protocol mixins.
    """

    def build(self, agent: Agent, options: BuildOptions) -> str:
        """Build Kilo configuration output."""
        output_lines = [
            f"# Kilo Agent Configuration: {agent.name}",
            f"## Description: {agent.description}",
            "",
            "## System Prompt:",
            agent.system_prompt,
            "",
        ]

        if options.include_tools and agent.tools:
            output_lines.append("## Tools:")
            for tool in agent.tools:
                output_lines.append(f"- {tool}")
            output_lines.append("")

        if options.include_skills and agent.skills:
            output_lines.append("## Skills:")
            for skill in agent.skills:
                output_lines.append(f"- {skill}")
            output_lines.append("")

        if options.include_workflows and agent.workflows:
            output_lines.append("## Workflows:")
            for workflow in agent.workflows:
                output_lines.append(f"- {workflow}")
            output_lines.append("")

        return "\n".join(output_lines)

    def validate(self, agent: Agent) -> list[str]:
        """Validate Kilo requirements."""
        errors = []

        if not agent.name:
            errors.append("Agent name is required")

        if not agent.description:
            errors.append("Agent description is required")

        if not agent.system_prompt:
            errors.append("Agent system_prompt is required")

        return errors

    def get_output_format(self) -> str:
        """Kilo outputs Markdown format."""
        return "Markdown"

    # Implement Protocol methods for optional features
    def build_skills(self, skills: list[Skill]) -> str:
        """Build Kilo-specific skills output."""
        lines = ["# Skills", ""]
        for skill in skills:
            lines.append(f"## {skill.name}")
            lines.append(f"{skill.description}")
            lines.append("")
            lines.append("### Instructions:")
            lines.append(skill.instructions)
            lines.append("")
        return "\n".join(lines)

    def build_workflows(self, workflows: list[Workflow]) -> str:
        """Build Kilo-specific workflows output."""
        lines = ["# Workflows", ""]
        for workflow in workflows:
            lines.append(f"## {workflow.name}")
            lines.append(f"{workflow.description}")
            lines.append("")
            lines.append("### Steps:")
            for i, step in enumerate(workflow.steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        return "\n".join(lines)

    def build_rules(self, rules: Rules) -> str:
        """Build Kilo-specific rules output."""
        lines = ["# Rules", ""]

        if rules.constraints:
            lines.append("## Constraints:")
            for constraint in rules.constraints:
                lines.append(f"- {constraint}")
            lines.append("")

        if rules.guidelines:
            lines.append("## Guidelines:")
            for category, guidelines in rules.guidelines.items():
                lines.append(f"### {category}:")
                if isinstance(guidelines, list):
                    for guideline in guidelines:
                        lines.append(f"- {guideline}")
                else:
                    lines.append(str(guidelines))
                lines.append("")

        return "\n".join(lines)


class ClaudeBuilder(AbstractBuilder):
    """Example builder for Claude (JSON-based configuration)."""

    def build(self, agent: Agent, options: BuildOptions) -> dict[str, Any]:
        """Build Claude configuration as JSON."""
        config: dict[str, Any] = {
            "name": agent.name,
            "description": agent.description,
            "system_prompt": agent.system_prompt,
        }

        if options.include_tools and agent.tools:
            config["tools"] = agent.tools

        if options.include_skills and agent.skills:
            config["skills"] = agent.skills

        if options.include_workflows and agent.workflows:
            config["workflows"] = agent.workflows

        return config

    def validate(self, agent: Agent) -> list[str]:
        """Validate Claude requirements."""
        errors = []

        if not agent.name:
            errors.append("Agent name is required for Claude")

        if not agent.system_prompt or len(agent.system_prompt) < 10:
            errors.append("Agent system_prompt must be at least 10 characters")

        return errors

    def get_output_format(self) -> str:
        """Claude outputs JSON format."""
        return "JSON"


# ==============================================================================
# Example 2: Using BuilderFactory
# ==============================================================================


def example_factory_usage() -> None:
    """Example demonstrating BuilderFactory usage."""
    print("=" * 70)
    print("Example 2: Using BuilderFactory")
    print("=" * 70)

    # Register builders
    BuilderFactory.register("kilo", KiloBuilder)
    BuilderFactory.register("claude", ClaudeBuilder)

    # List available builders
    print(f"Available builders: {BuilderFactory.list_builders()}")

    # Get a builder and use it
    try:
        kilo_builder = BuilderFactory.get_builder("kilo")
        print(f"Got builder: {kilo_builder.get_tool_name()}")

        # Check feature support
        print(f"Supports skills: {kilo_builder.supports_feature('skills')}")

    except BuilderNotFoundError as e:
        print(f"Error: {e}")

    # Attempt to get non-existent builder
    try:
        BuilderFactory.get_builder("nonexistent")
    except BuilderNotFoundError as e:
        print(f"Expected error: {e.tool_name} not found")

    print()


# ==============================================================================
# Example 3: Using BuilderRegistry
# ==============================================================================


def example_registry_usage() -> None:
    """Example demonstrating BuilderRegistry usage."""
    print("=" * 70)
    print("Example 3: Using BuilderRegistry")
    print("=" * 70)

    registry = BuilderRegistry()

    # Create and register builder instances
    kilo_builder = KiloBuilder()
    claude_builder = ClaudeBuilder()

    registry.register("kilo", kilo_builder)
    registry.register("claude", claude_builder)

    # List registered tools
    print(f"Registered tools: {registry.list_tools()}")
    print(f"Total builders: {registry.count()}")

    # Retrieve builders
    builder = registry.get("kilo")
    print(f"Retrieved: {builder.get_tool_name()}")

    # Check if tool exists
    print(f"Has kilo builder: {registry.has_tool('kilo')}")
    print(f"Has unknown builder: {registry.has_tool('unknown')}")

    # Unregister a builder
    removed = registry.unregister("claude")
    print(f"Removed claude builder: {removed}")
    print(f"Remaining tools: {registry.list_tools()}")

    print()


# ==============================================================================
# Example 4: Building Agent Configuration
# ==============================================================================


def example_build_agent() -> None:
    """Example demonstrating agent building."""
    print("=" * 70)
    print("Example 4: Building Agent Configuration")
    print("=" * 70)

    # Create a sample agent
    agent = Agent(
        name="code",
        description="Generates and refactors code",
        system_prompt="You are an expert software engineer...",
        tools=["bash", "python"],
        skills=["code_generation", "refactoring"],
        workflows=["implementation", "testing"],
    )

    # Register and use builders
    BuilderFactory.register("kilo", KiloBuilder)

    builder = BuilderFactory.get_builder("kilo")

    # Validate before building
    errors = builder.validate(agent)
    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("Validation passed!")

    # Build with minimal variant
    options = BuildOptions(
        variant="minimal",
        agent_name=agent.name,
        include_skills=False,
        include_workflows=False,
    )

    output = builder.build(agent, options)
    print("\nMinimal variant output:")
    print(output)

    # Build with verbose variant
    options_verbose = BuildOptions(
        variant="verbose",
        agent_name=agent.name,
    )

    output_verbose = builder.build(agent, options_verbose)
    print("\nVerbose variant output:")
    print(output_verbose)

    print()


# ==============================================================================
# Example 5: Protocol-Based Feature Detection
# ==============================================================================


def example_protocol_features() -> None:
    """Example demonstrating Protocol-based feature detection."""
    print("=" * 70)
    print("Example 5: Protocol-Based Feature Detection")
    print("=" * 70)

    kilo_builder = KiloBuilder()

    # Check if builder implements SupportsSkills protocol
    if hasattr(kilo_builder, "build_skills"):
        print("KiloBuilder implements SupportsSkills protocol")

        skills = [
            Skill(
                name="code_generation",
                description="Generate code from requirements",
                instructions="Analyze requirements and generate code...",
                tools_needed=["python"],
            ),
        ]

        skills_output = kilo_builder.build_skills(skills)
        print("\nBuilt skills:")
        print(skills_output)

    # Check other protocols
    print(f"\nHas build_workflows: {hasattr(kilo_builder, 'build_workflows')}")
    print(f"Has build_rules: {hasattr(kilo_builder, 'build_rules')}")

    print()


# ==============================================================================
# Example 6: Error Handling
# ==============================================================================


def example_error_handling() -> None:
    """Example demonstrating error handling."""
    print("=" * 70)
    print("Example 6: Error Handling")
    print("=" * 70)

    # BuilderNotFoundError
    try:
        BuilderFactory.get_builder("unknown_tool")
    except BuilderNotFoundError as e:
        print(f"BuilderNotFoundError: {e}")

    # BuilderValidationError
    try:
        invalid_agent = Agent(
            name="",  # Invalid: empty name
            description="Test",
            system_prompt="Test",
        )
        builder = KiloBuilder()
        errors = builder.validate(invalid_agent)
        if errors:
            raise BuilderValidationError(errors)
    except BuilderValidationError as e:
        print(f"\nBuilderValidationError:")
        for error in e.errors:
            print(f"  - {error}")

    # UnsupportedFeatureError
    try:
        raise UnsupportedFeatureError("CustomBuilder", "advanced_reasoning")
    except UnsupportedFeatureError as e:
        print(f"\nUnsupportedFeatureError: {e}")

    print()


# ==============================================================================
# Main Examples Execution
# ==============================================================================


def main() -> None:
    """Run all examples."""
    example_factory_usage()
    example_registry_usage()
    example_build_agent()
    example_protocol_features()
    example_error_handling()

    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()

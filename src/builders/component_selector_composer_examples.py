"""Usage examples for ComponentSelector and ComponentComposer (Task 1.5).

This module demonstrates how to use the component selector and composer
to build tool-specific configurations from Agent IR models.
"""

from src.builders import (
    Variant,
    ComponentSelector,
    ComponentComposer,
    ComponentNotFoundError,
    VariantNotFoundError,
)
from src.ir.models import Agent


def example_1_basic_selector_usage():
    """Example 1: Basic selector usage with fallback.

    Shows how to select a variant and use fallback from verbose
    if minimal is not available.
    """
    print("\n" + "=" * 70)
    print("Example 1: Basic ComponentSelector Usage")
    print("=" * 70)

    # Create selector
    selector = ComponentSelector(agents_dir="agents")

    # Create an agent
    agent = Agent(
        name="code",
        description="Code generation assistant",
        system_prompt="You are a Python code assistant",
        tools=["python_repl", "file_editor"],
        skills=["python", "javascript"],
    )

    # Select minimal variant (would fall back to verbose if minimal missing)
    try:
        bundle = selector.select(agent, variant=Variant.MINIMAL)
        print(f"✓ Selected variant: {bundle.variant.value}")
        print(f"✓ Fallback used: {bundle.fallback_used}")
        print(f"✓ Prompt length: {len(bundle.prompt)} chars")
        if bundle.skills:
            print(f"✓ Skills loaded: {len(bundle.skills)} chars")
        if bundle.workflow:
            print(f"✓ Workflow loaded: {len(bundle.workflow)} chars")
    except VariantNotFoundError as e:
        print(f"✗ Variant not found: {e}")
        print("  (This is expected if agents dir doesn't exist)")


def example_2_variant_detection():
    """Example 2: Detect available variants.

    Shows how to check what variants are available for an agent
    before attempting to load.
    """
    print("\n" + "=" * 70)
    print("Example 2: Detect Available Variants")
    print("=" * 70)

    selector = ComponentSelector(agents_dir="agents")

    agent_names = ["code", "architect", "reviewer"]

    for agent_name in agent_names:
        available = selector.list_available_variants(agent_name)
        if available:
            print(f"Agent '{agent_name}' has variants: {[v.value for v in available]}")
        else:
            print(f"Agent '{agent_name}' has no variants (dir doesn't exist)")


def example_3_markdown_composition():
    """Example 3: Compose components into markdown.

    Shows how to assemble loaded components into markdown format
    with proper ordering: prompt, tools, skills, workflows, subagents.
    """
    print("\n" + "=" * 70)
    print("Example 3: Markdown Composition")
    print("=" * 70)

    # Create mock bundle and agent
    from src.builders import ComponentBundle

    bundle = ComponentBundle(
        variant=Variant.VERBOSE,
        prompt="# Code Assistant Prompt\nYou help developers write better code.",
        skills="## Available Skills\n- Python development\n- Code review",
        workflow="## Workflows\n- Code analysis\n- Refactoring",
        fallback_used=False,
    )

    agent = Agent(
        name="code",
        description="Code generation assistant",
        system_prompt="You help developers write code",
        tools=["python_repl", "file_editor", "git"],
        skills=["python", "javascript", "sql"],
        workflows=["testing", "debugging"],
        subagents=["test_runner", "formatter"],
    )

    # Compose full markdown
    markdown = ComponentComposer.compose_markdown(bundle, agent)
    print("Full Markdown Output:")
    print("-" * 70)
    print(markdown)
    print("-" * 70)

    # Compose partial (only prompt and tools)
    print("\nPartial Markdown (prompt + tools only):")
    print("-" * 70)
    partial = ComponentComposer.compose_markdown(
        bundle, agent, include_sections=["prompt", "tools"]
    )
    print(partial)
    print("-" * 70)


def example_4_yaml_frontmatter_composition():
    """Example 4: Compose with YAML frontmatter.

    Shows how to create documents with YAML metadata followed
    by markdown content.
    """
    print("\n" + "=" * 70)
    print("Example 4: YAML Frontmatter Composition")
    print("=" * 70)

    from src.builders import ComponentBundle

    bundle = ComponentBundle(
        variant=Variant.MINIMAL,
        prompt="# Agent Prompt",
        fallback_used=False,
    )

    agent = Agent(
        name="architect",
        description="System design assistant",
        system_prompt="Design systems",
        tools=["diagram_tool"],
    )

    # Custom frontmatter
    custom_frontmatter = {
        "author": "engineering_team",
        "version": "1.0.0",
        "tags": ["design", "architecture"],
    }

    output = ComponentComposer.compose_yaml_markdown(bundle, agent, frontmatter=custom_frontmatter)

    print("YAML + Markdown Output:")
    print("-" * 70)
    print(output)
    print("-" * 70)


def example_5_json_composition():
    """Example 5: Compose into JSON format.

    Shows how to create structured JSON output for APIs
    or machine-readable configuration.
    """
    print("\n" + "=" * 70)
    print("Example 5: JSON Composition")
    print("=" * 70)

    from src.builders import ComponentBundle
    import json

    bundle = ComponentBundle(
        variant=Variant.MINIMAL,
        prompt="# Prompt",
        skills="## Skills",
        workflow="## Workflows",
        fallback_used=False,
    )

    agent = Agent(
        name="reviewer",
        description="Code review assistant",
        system_prompt="Review code",
        tools=["github_api"],
        skills=["python", "testing"],
    )

    json_output = ComponentComposer.compose_json(bundle, agent)

    print("JSON Output:")
    print("-" * 70)
    print(json.dumps(json_output, indent=2))
    print("-" * 70)


def example_6_error_handling():
    """Example 6: Handle errors gracefully.

    Shows how to handle ComponentNotFoundError and VariantNotFoundError
    with proper error messages and recovery strategies.
    """
    print("\n" + "=" * 70)
    print("Example 6: Error Handling")
    print("=" * 70)

    selector = ComponentSelector(agents_dir="agents")

    agent = Agent(
        name="nonexistent_agent",
        description="Test",
        system_prompt="Test",
    )

    # Try to select a variant that doesn't exist
    try:
        bundle = selector.select(agent, variant=Variant.MINIMAL)
    except VariantNotFoundError as e:
        print(f"✓ Caught VariantNotFoundError: {e}")
        print(f"  - Agent: {e.agent_name}")
        print(f"  - Variant: {e.variant}")

    # Alternative: Check if variant exists before loading
    if selector.variant_exists(agent.name, Variant.MINIMAL):
        print("Variant exists, loading...")
        bundle = selector.select(agent, variant=Variant.MINIMAL)
    else:
        print(f"✓ Variant check returned False (expected for nonexistent agent)")
        print("  -> Can handle gracefully before attempting load")


def example_7_selector_with_custom_directory():
    """Example 7: Use custom agents directory.

    Shows how to initialize selector with different directory paths
    for various deployment scenarios.
    """
    print("\n" + "=" * 70)
    print("Example 7: Custom Directory Paths")
    print("=" * 70)

    # Production path
    prod_selector = ComponentSelector(agents_dir="/var/lib/promptosaurus/agents")
    print(f"✓ Production selector: {prod_selector.agents_dir}")

    # Development path
    dev_selector = ComponentSelector(agents_dir="./agents")
    print(f"✓ Development selector: {dev_selector.agents_dir}")

    # Custom path
    custom_selector = ComponentSelector(agents_dir="/custom/path/agents")
    print(f"✓ Custom selector: {custom_selector.agents_dir}")

    # All can check paths without loading
    test_agent_name = "test"
    for variant in [Variant.MINIMAL, Variant.VERBOSE]:
        path = dev_selector.get_variant_path(test_agent_name, variant)
        print(f"  Path for {test_agent_name}/{variant.value}: {path}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ComponentSelector & ComponentComposer - Usage Examples (Task 1.5)")
    print("=" * 70)

    example_1_basic_selector_usage()
    example_2_variant_detection()
    example_3_markdown_composition()
    example_4_yaml_frontmatter_composition()
    example_5_json_composition()
    example_6_error_handling()
    example_7_selector_with_custom_directory()

    print("\n" + "=" * 70)
    print("✓ All examples completed")
    print("=" * 70 + "\n")

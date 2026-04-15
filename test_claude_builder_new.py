#!/usr/bin/env python3
"""Quick test for new ClaudeBuilder with Markdown output."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from promptosaurus.builders.base import BuildOptions
from promptosaurus.builders.claude_builder_new import ClaudeBuilder
from promptosaurus.ir.models import Agent

# Create a simple test agent
test_agent = Agent(
    name="code",
    description="Write, edit, and refactor code following project conventions",
    system_prompt="You are a senior software engineer responsible for writing high-quality, maintainable code.",
    tools=["read", "write", "bash"],
    skills=["feature-planning", "post-implementation-checklist"],
    workflows=["feature"],
    subagents=["review/code", "code/boilerplate"],
)

# Create builder and build options
builder = ClaudeBuilder()
options = BuildOptions(
    include_tools=True,
    include_skills=True,
    include_workflows=True,
    include_subagents=True,
    variant="minimal",
)

# Build the artifacts
print("Building Claude artifacts...")
try:
    output = builder.build(test_agent, options, config=None)

    print(f"\n✓ Successfully built {len(output)} artifact files:")
    for path, content in output.items():
        print(f"  - {path} ({len(content)} bytes)")

    # Print the agent file content
    agent_file = ".claude/agents/code-agent.md"
    if agent_file in output:
        print(f"\n--- Content of {agent_file} ---")
        print(output[agent_file][:500])
        print("...")
        print("\n✓ Agent file rendered successfully!")

    print("\n✓ All tests passed!")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

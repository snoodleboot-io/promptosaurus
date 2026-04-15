#!/usr/bin/env python3
"""Test script to trace skills received by each agent during build."""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from promptosaurus.prompt_builder import PromptBuilder

# Load configuration
config = {
    "variant": "minimal",
    "active_personas": ["software_engineer"],
    "spec": {"language": "python"},
}

print("=" * 80)
print("BUILDING CLAUDE CONFIGURATION - SKILLS TRACE")
print("=" * 80)
print(f"Active personas: {config['active_personas']}")
print(f"Variant: {config['variant']}")
print("=" * 80)

# Create builder for Claude
builder = PromptBuilder("claude")

# Build - this will trigger our debug output in ClaudeBuilder._render_agent_file
try:
    output_path = Path(".")
    actions = builder.build(output_path, config=config, dry_run=True)

    print("\n" + "=" * 80)
    print("BUILD COMPLETED")
    print("=" * 80)
    print(f"\nActions: {len(actions)}")
    for action in actions[:10]:  # Show first 10 actions
        print(f"  {action}")

except Exception as e:
    print(f"\nError during build: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

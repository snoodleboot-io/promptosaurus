#!/usr/bin/env python3
"""Extract skills and workflows from original subagent markdown files.

This script analyzes the original prompt files in promptosaurus/prompts/agents/
and extracts:
1. Skills - Reusable capabilities that can be referenced
2. Workflows - Step-by-step processes
3. Tools - Implicitly needed tools based on content

It generates:
- skills.md files in each variant directory
- workflow.md files in each variant directory
- Updates prompt.md frontmatter with extracted metadata
"""

import re
from pathlib import Path
from typing import NamedTuple, Optional


class ExtractedSkill(NamedTuple):
    """Represents an extracted skill."""

    name: str
    description: str
    instructions: str
    tools_needed: list[str]


class ExtractedWorkflow(NamedTuple):
    """Represents an extracted workflow."""

    name: str
    description: str
    steps: list[str]
    detailed_steps: str


class OriginalFile(NamedTuple):
    """Represents an original subagent markdown file."""

    path: Path
    agent_name: str
    subagent_name: str
    content: str


def find_original_files(base_dir: Path) -> list[OriginalFile]:
    """Find all original subagent markdown files.

    Args:
        base_dir: Base directory (promptosaurus/prompts/agents/)

    Returns:
        List of OriginalFile objects
    """
    files = []

    for agent_dir in base_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        agent_name = agent_dir.name
        subagents_dir = agent_dir / "subagents"

        if subagents_dir.is_dir():
            for subagent_file in subagents_dir.glob("*.md"):
                subagent_name = subagent_file.stem.replace(f"{agent_name}-", "")
                content = subagent_file.read_text()

                files.append(
                    OriginalFile(
                        path=subagent_file,
                        agent_name=agent_name,
                        subagent_name=subagent_name,
                        content=content,
                    )
                )

    return files


def extract_numbered_steps(content: str) -> tuple[Optional[list[str]], Optional[str]]:
    """Extract numbered workflow steps from content.

    Looks for patterns like:
    1. Step one
    2. Step two
    3. Step three

    Args:
        content: Markdown content

    Returns:
        Tuple of (step_summaries, detailed_content) or (None, None) if no steps found
    """
    # Find numbered lists (1. 2. 3. etc.)
    pattern = r"^\d+\.\s+(.+?)(?=\n\d+\.|\n\n|\Z)"
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

    if matches and len(matches) >= 2:  # At least 2 steps to be a workflow
        # Clean up each step
        steps = []
        for match in matches:
            # Get first line as summary
            first_line = match.split("\n")[0].strip()
            steps.append(first_line)

        return steps, content

    return None, None


def extract_workflows_from_file(original: OriginalFile) -> list[ExtractedWorkflow]:
    """Extract workflows from an original file.

    Args:
        original: Original file object

    Returns:
        List of extracted workflows
    """
    workflows = []

    # Extract numbered steps
    steps, detailed_content = extract_numbered_steps(original.content)

    if steps:
        # Create workflow name from subagent name
        workflow_name = f"{original.subagent_name}-workflow"
        description = f"Step-by-step process for {original.subagent_name}"

        workflows.append(
            ExtractedWorkflow(
                name=workflow_name,
                description=description,
                steps=steps,
                detailed_steps=detailed_content or "",
            )
        )

    return workflows


def extract_skills_from_file(original: OriginalFile) -> list[ExtractedSkill]:
    """Extract skills from an original file.

    This is a heuristic-based extraction. Skills are identified by:
    - Section headers (##, ###)
    - Procedural content ("how to", "when to use")
    - Reusable capabilities

    Args:
        original: Original file object

    Returns:
        List of extracted skills
    """
    skills = []

    # TODO: Implement skill extraction heuristics
    # For now, return empty - this will be done manually or with better AI analysis

    return skills


def infer_tools_from_content(content: str) -> list[str]:
    """Infer required tools from content analysis.

    Args:
        content: Markdown content

    Returns:
        List of tool names
    """
    tools = set()

    # Common tool patterns
    tool_patterns = {
        r"\bread\b": "read",
        r"\bglob\b": "glob",
        r"\bedit\b": "edit",
        r"\bwrite\b": "write",
        r"\bbash\b": "bash",
        r"\bgrep\b": "grep",
        r"\bgit\b": "bash",  # git requires bash
        r"\bnpm\b": "bash",
        r"\bpytest\b": "bash",
        r"\bcodebase_search\b": "codebase_search",
    }

    content_lower = content.lower()
    for pattern, tool in tool_patterns.items():
        if re.search(pattern, content_lower):
            tools.add(tool)

    return sorted(list(tools))


def write_workflow_file(variant_dir: Path, workflows: list[ExtractedWorkflow]) -> bool:
    """Write workflow.md file to variant directory.

    Args:
        variant_dir: Path to variant directory (e.g., agents/code/subagents/feature/minimal)
        workflows: List of extracted workflows

    Returns:
        True if file was written, False otherwise
    """
    if not workflows:
        return False

    # For now, just write the first workflow (most subagents have only one)
    workflow = workflows[0]

    # Import yaml for proper quoting
    import yaml

    # Create proper YAML structure
    yaml_data = {
        "name": workflow.name,
        "description": workflow.description,
        "steps": workflow.steps,
    }

    # Generate YAML frontmatter with proper quoting
    yaml_content = yaml.dump(
        yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False
    )

    workflow_content = f"""---
{yaml_content.strip()}
---

## Steps

"""

    # Add detailed steps if available
    for i, step in enumerate(workflow.steps, 1):
        workflow_content += f"### Step {i}: {step}\n\n"
        # Add placeholder for detailed instructions
        workflow_content += "Detailed instructions for this step.\n\n"

    workflow_file = variant_dir / "workflow.md"
    workflow_file.write_text(workflow_content, encoding="utf-8")
    return True


def update_prompt_frontmatter(
    variant_dir: Path, tools: list[str], skills: list[str], workflows: list[str]
) -> bool:
    """Update prompt.md frontmatter with extracted metadata.

    Args:
        variant_dir: Path to variant directory
        tools: List of tool names
        skills: List of skill names
        workflows: List of workflow names

    Returns:
        True if updated successfully
    """
    import re
    import yaml

    prompt_file = variant_dir / "prompt.md"
    if not prompt_file.exists():
        return False

    content = prompt_file.read_text(encoding="utf-8")

    # Parse existing frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        return False

    frontmatter_text = frontmatter_match.group(1)
    body = frontmatter_match.group(2)

    # Parse as YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError:
        return False

    # Update with new values (only if not already present or empty)
    if tools and (not frontmatter.get("tools") or frontmatter.get("tools") == ""):
        frontmatter["tools"] = tools
    if skills and (
        not frontmatter.get("skills")
        or frontmatter.get("skills") == ""
        or frontmatter.get("skills") == []
    ):
        frontmatter["skills"] = skills
    if workflows and (
        not frontmatter.get("workflows")
        or frontmatter.get("workflows") == ""
        or frontmatter.get("workflows") == []
    ):
        frontmatter["workflows"] = workflows

    # Rebuild frontmatter as YAML
    new_frontmatter_text = yaml.dump(
        frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False
    )
    new_content = f"---\n{new_frontmatter_text}---\n{body}"

    prompt_file.write_text(new_content, encoding="utf-8")
    return True


def main():
    """Main extraction process."""
    base_dir = Path("promptosaurus/prompts/agents")
    target_base = Path("promptosaurus/agents")

    if not base_dir.exists():
        print(f"Error: {base_dir} not found")
        return

    if not target_base.exists():
        print(f"Error: {target_base} not found")
        return

    print("Finding original subagent files...")
    original_files = find_original_files(base_dir)
    print(f"Found {len(original_files)} files\n")

    stats = {
        "total": len(original_files),
        "workflows_written": 0,
        "prompts_updated": 0,
        "errors": [],
    }

    for original in original_files:
        print(f"Processing: {original.agent_name}/{original.subagent_name}")

        # Extract workflows
        workflows = extract_workflows_from_file(original)
        print(f"  Workflows: {len(workflows)}")
        for wf in workflows:
            print(f"    - {wf.name}: {len(wf.steps)} steps")

        # Extract skills
        skills = extract_skills_from_file(original)
        print(f"  Skills: {len(skills)}")

        # Infer tools
        tools = infer_tools_from_content(original.content)
        print(f"  Tools: {', '.join(tools) if tools else 'none'}")

        # Determine target directories (both minimal and verbose)
        agent_dir = target_base / original.agent_name
        subagent_dir = agent_dir / "subagents" / original.subagent_name

        for variant in ["minimal", "verbose"]:
            variant_dir = subagent_dir / variant

            if not variant_dir.exists():
                print(f"  Warning: {variant_dir} does not exist, skipping")
                continue

            # Write workflow.md
            if workflows:
                if write_workflow_file(variant_dir, workflows):
                    stats["workflows_written"] += 1
                    print(f"  ✓ Wrote {variant}/workflow.md")

            # Update prompt.md frontmatter
            workflow_names = [wf.name for wf in workflows]
            skill_names = [sk.name for sk in skills]

            if update_prompt_frontmatter(variant_dir, tools, skill_names, workflow_names):
                stats["prompts_updated"] += 1
                print(f"  ✓ Updated {variant}/prompt.md frontmatter")

        print()

    # Print summary
    print("=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total files processed: {stats['total']}")
    print(f"Workflow files written: {stats['workflows_written']}")
    print(f"Prompt files updated: {stats['prompts_updated']}")
    if stats["errors"]:
        print(f"\nErrors: {len(stats['errors'])}")
        for error in stats["errors"]:
            print(f"  - {error}")


if __name__ == "__main__":
    main()

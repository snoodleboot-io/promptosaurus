#!/usr/bin/env python3
"""
Restructure IR to proper architecture:
1. Remove variants from top-level agents (keep only one prompt.md)
2. Extract skills to top-level skills/ directory
3. Keep workflows with subagents
4. Keep subagent variants (minimal/verbose differ here)
"""

import shutil
from pathlib import Path


def restructure_ir():
    """Restructure the IR to the correct architecture."""
    base_dir = Path("promptosaurus")
    agents_dir = base_dir / "agents"
    skills_dir = base_dir / "skills"

    # Create top-level skills directory
    skills_dir.mkdir(exist_ok=True)
    print(f"✓ Created {skills_dir}")

    # Process each agent
    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        agent_name = agent_dir.name
        print(f"\n📁 Processing agent: {agent_name}")

        # 1. Flatten top-level agent variants (keep only minimal)
        minimal_prompt = agent_dir / "minimal" / "prompt.md"
        verbose_prompt = agent_dir / "verbose" / "prompt.md"
        unified_prompt = agent_dir / "prompt.md"

        if minimal_prompt.exists() and verbose_prompt.exists():
            # Use minimal as the canonical version
            shutil.copy2(minimal_prompt, unified_prompt)
            print(f"  ✓ Unified {agent_name}/prompt.md from minimal variant")

            # Remove variant directories (but not subagents!)
            if (agent_dir / "minimal").exists() and not (
                agent_dir / "minimal" / "subagents"
            ).exists():
                shutil.rmtree(agent_dir / "minimal")
                print(f"  ✓ Removed {agent_name}/minimal/")

            if (agent_dir / "verbose").exists() and not (
                agent_dir / "verbose" / "subagents"
            ).exists():
                shutil.rmtree(agent_dir / "verbose")
                print(f"  ✓ Removed {agent_name}/verbose/")

        # 2. Extract skills from subagents to top-level skills/
        subagents_dir = agent_dir / "subagents"
        if subagents_dir.exists():
            for subagent_dir in subagents_dir.iterdir():
                if not subagent_dir.is_dir():
                    continue

                subagent_name = subagent_dir.name

                # Check both variants for skills.md
                for variant in ["minimal", "verbose"]:
                    variant_dir = subagent_dir / variant
                    skills_file = variant_dir / "skills.md"

                    if skills_file.exists():
                        print(
                            f"  📄 Found skills in {agent_name}/subagents/{subagent_name}/{variant}/"
                        )

                        # Read skills.md and extract individual skills
                        content = skills_file.read_text()

                        # Parse multi-skill file (separated by YAML frontmatter blocks)
                        skills = parse_skills_file(content)

                        for skill_name, skill_content in skills:
                            # Create skill directory
                            skill_dir = skills_dir / skill_name / variant
                            skill_dir.mkdir(parents=True, exist_ok=True)

                            # Write SKILL.md
                            skill_file = skill_dir / "SKILL.md"
                            skill_file.write_text(skill_content)
                            print(f"    → Moved to skills/{skill_name}/{variant}/SKILL.md")

                        # Remove skills.md from subagent
                        skills_file.unlink()
                        print(f"    ✓ Removed skills.md from subagent")

    print("\n✅ Restructure complete!")
    print(f"\nNew structure:")
    print(f"  - Top-level agents: Single prompt.md (no variants)")
    print(f"  - Subagents: Keep minimal/verbose variants")
    print(f"  - Skills: Moved to top-level skills/ directory")
    print(f"  - Workflows: Stay with subagents")


def parse_skills_file(content: str) -> list[tuple[str, str]]:
    """Parse a multi-skill file and return list of (skill_name, skill_content) tuples."""
    skills = []

    # Split by YAML frontmatter blocks
    parts = content.split("---\n")

    i = 0
    while i < len(parts):
        # Skip empty parts
        if not parts[i].strip():
            i += 1
            continue

        # Check if this is YAML frontmatter
        if i + 1 < len(parts) and parts[i].strip():
            # parts[i] is between --- markers (YAML)
            # parts[i+1] is the markdown body
            yaml_content = parts[i].strip()

            # Extract skill name from YAML
            skill_name = None
            for line in yaml_content.split("\n"):
                if line.startswith("name:"):
                    skill_name = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break

            # Get markdown body
            markdown_body = ""
            if i + 1 < len(parts):
                markdown_body = parts[i + 1]

            if skill_name:
                # Reconstruct skill with frontmatter
                skill_content = f"---\n{yaml_content}\n---\n{markdown_body}"
                skills.append((skill_name, skill_content))

            i += 2
        else:
            i += 1

    return skills


if __name__ == "__main__":
    restructure_ir()

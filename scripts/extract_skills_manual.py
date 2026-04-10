#!/usr/bin/env python3
"""Manual skill extraction from original subagent files.

This script provides templates for manually extracting skills from the
original prompt files. Skills are reusable capabilities like:
- Testing patterns (AAA structure, coverage categories)
- Design patterns (data modeling questions, ERD creation)
- Best practices (mocking rules, integration test setup)
"""

from pathlib import Path
from typing import NamedTuple


class Skill(NamedTuple):
    """Represents a skill to be extracted."""

    name: str
    description: str
    tools_needed: list[str]
    instructions: str


# ============================================================================
# SKILL DEFINITIONS - Manually extracted from original files
# ============================================================================

# Test Agent Skills
TEST_AAA_STRUCTURE = Skill(
    name="test-aaa-structure",
    description="Apply Arrange-Act-Assert pattern for clear, maintainable tests",
    tools_needed=["read", "write"],
    instructions="""## AAA Test Structure

Always structure tests using the Arrange-Act-Assert pattern:

**Arrange:** Set up state and inputs
**Act:** Call the thing under test
**Assert:** Verify outputs and side effects

### Rules
- One logical assertion per test
- One behavior per test name
- Test names must be descriptive sentences:
  - `it("returns null when the user ID does not exist")`
  - `it("throws AuthError when the token is expired")`

### Example
```python
def test_user_get_by_id_returns_user_when_found():
    # Arrange
    user = User(id="123", name="Alice")
    db.save(user)
    
    # Act
    result = get_user_by_id("123")
    
    # Assert
    assert result.name == "Alice"
```
""",
)

TEST_COVERAGE_CATEGORIES = Skill(
    name="test-coverage-categories",
    description="Systematic approach to achieving comprehensive test coverage",
    tools_needed=["read", "write"],
    instructions="""## Coverage Categories

Work through these categories in order for comprehensive coverage:

1. **HAPPY PATH** — Expected inputs produce expected output
2. **BOUNDARY VALUES** — Min, max, exactly at limit, one over limit
3. **EMPTY / NULL / ZERO** — Each nullable input absent or zeroed
4. **ERROR CASES** — Dependency throws, network fails, DB unavailable
5. **CONCURRENT / ORDERING** — If function has state, test ordering
6. **AUTHORIZATION BOUNDARIES** — Does it enforce who can call it?
7. **ADVERSARIAL INPUTS** — SQL fragments, script tags, path traversal, unicode, emoji, null bytes, extremely long strings

### Workflow
- Check off each category as you implement tests
- Document which categories don't apply and why
- Flag any gaps in coverage with rationale
""",
)

TEST_MOCKING_RULES = Skill(
    name="test-mocking-rules",
    description="Guidelines for when and how to use mocks in tests",
    tools_needed=[],
    instructions="""## Mocking Rules

### When to Mock
- Mock only at process boundaries:
  - Database connections
  - Network calls (HTTP, external APIs)
  - Filesystem operations
  - Time/date functions
  - Random number generation

### What NOT to Mock
- **Never mock the thing under test**
- **Never mock internal helpers** — test them through the public interface
- **Never mock your own database** in integration tests

### Consistency
- Use the mock library from core-conventions.md consistently
- Follow the same mocking patterns across the codebase
""",
)

ARCHITECT_DATA_MODEL_QUESTIONS = Skill(
    name="data-model-discovery",
    description="Essential questions to ask before designing a data model",
    tools_needed=[],
    instructions="""## Data Model Discovery Questions

Before designing any data model, ask these questions:

1. **What are the core entities and their relationships?**
   - Identify nouns in requirements
   - Map relationships (1:1, 1:many, many:many)

2. **What are the most common read patterns?**
   - Which queries will run most frequently?
   - What filters/sorts are needed?

3. **What are the most common write patterns?**
   - Insert frequency and volume
   - Update patterns and triggers

4. **Are there soft-delete, audit trail, or versioning requirements?**
   - Do records need to be recoverable?
   - Is history tracking required?

5. **Any known scale constraints?**
   - Expected row counts
   - Request volume (reads/writes per second)
   - Geographic distribution

### Usage
- Ask all questions before producing designs
- Document answers in design doc
- Use answers to inform indexing and denormalization decisions
""",
)

ARCHITECT_MERMAID_ERD = Skill(
    name="mermaid-erd-creation",
    description="Create entity relationship diagrams using Mermaid syntax",
    tools_needed=["write"],
    instructions="""## Mermaid ERD Format

Use this format for entity relationship diagrams:

```mermaid
erDiagram
    USER {
        uuid id PK
        string email
        timestamp created_at
    }
    ORDER {
        uuid id PK
        uuid user_id FK
        string status
    }
    USER ||--o{ ORDER : "places"
```

### Syntax
- Entity name in UPPERCASE
- Fields inside `{ }` with: type name constraint
- Constraints: PK (primary key), FK (foreign key)
- Relationships: `||--o{` means "one to zero-or-many"
  - `||--||` : one to one
  - `||--o{` : one to zero-or-many
  - `}o--o{` : zero-or-many to zero-or-many

### When to Use
- Include ERD in every data model design
- Update ERD when schema changes
- Use for documentation and stakeholder communication
""",
)


# ============================================================================
# SKILL MAPPING - Which skills go with which subagents
# ============================================================================

SKILL_MAPPING = {
    "test/strategy": [
        TEST_AAA_STRUCTURE,
        TEST_COVERAGE_CATEGORIES,
        TEST_MOCKING_RULES,
    ],
    "architect/data-model": [
        ARCHITECT_DATA_MODEL_QUESTIONS,
        ARCHITECT_MERMAID_ERD,
    ],
}


def write_skills_file(agent_name: str, subagent_name: str, skills: list[Skill], variant: str):
    """Write skills.md file for a subagent."""
    # Construct path
    agent_dir = Path("promptosaurus/agents") / agent_name / "subagents" / subagent_name / variant
    skills_file = agent_dir / "skills.md"

    # Build content
    content_parts = []
    for skill in skills:
        tools_str = ", ".join(skill.tools_needed) if skill.tools_needed else ""
        content_parts.append(f"""---
name: {skill.name}
description: {skill.description}
tools_needed: [{tools_str}]
---

{skill.instructions.strip()}
""")

    content = "\n\n".join(content_parts)

    # Write file
    skills_file.write_text(content, encoding="utf-8")
    print(f"✓ Wrote {skills_file}")

    return skills_file


def update_prompt_with_skills(
    agent_name: str, subagent_name: str, skill_names: list[str], variant: str
):
    """Update prompt.md frontmatter to include skill names."""
    import re

    agent_dir = Path("promptosaurus/agents") / agent_name / "subagents" / subagent_name / variant
    prompt_file = agent_dir / "prompt.md"

    if not prompt_file.exists():
        print(f"✗ {prompt_file} does not exist")
        return

    content = prompt_file.read_text(encoding="utf-8")

    # Check if skills already have values (not empty)
    if re.search(r"skills:\s*\n\s+-", content):
        print(f"  (skills already populated)")
        return

    # Replace empty skills or add skills to frontmatter
    skills_yaml_block = "skills:\n" + "\n".join(f"  - {name}" for name in skill_names)

    # Check if there's an empty skills: key
    if re.search(r"skills:\s*$", content, re.MULTILINE):
        # Replace empty skills
        new_content = re.sub(r"skills:\s*$", skills_yaml_block, content, flags=re.MULTILINE)
        prompt_file.write_text(new_content, encoding="utf-8")
        print(f"✓ Updated {prompt_file}")
    else:
        # Add skills to frontmatter
        match = re.match(r"^(---\n.*?\n)(---\n.*)$", content, re.DOTALL)
        if match:
            frontmatter = match.group(1)
            body = match.group(2)

            # Add skills before the closing ---
            new_content = frontmatter + skills_yaml_block + "\n" + body

            prompt_file.write_text(new_content, encoding="utf-8")
            print(f"✓ Updated {prompt_file}")


def main():
    """Generate skills.md files for subagents with manual skill definitions."""
    print("Generating skills.md files from manual skill definitions...\n")

    for subagent_key, skills in SKILL_MAPPING.items():
        agent_name, subagent_name = subagent_key.split("/")
        skill_names = [skill.name for skill in skills]

        print(f"\n{agent_name}/{subagent_name}:")
        print(f"  Skills: {', '.join(skill_names)}")

        # Write for both variants
        for variant in ["minimal", "verbose"]:
            write_skills_file(agent_name, subagent_name, skills, variant)
            update_prompt_with_skills(agent_name, subagent_name, skill_names, variant)

    print("\n" + "=" * 60)
    print("DONE: Skills files generated")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Complete Tool Research - Skills, Workflows, Subagents

**Last Updated:** 2026-04-10

## Overview

This document consolidates comprehensive research on how each supported tool (Kilo, Cline, Claude Code, Copilot, Cursor) handles skills, workflows, subagents, and related concepts.

---

## Tool Capabilities Matrix

| Feature | Kilo | Cline | Claude Code | Copilot | Cursor |
|---------|------|-------|-------------|---------|--------|
| **Skills** | ✅ SHARED | ✅ Directory-based | ✅ SHARED | ✅ Per-agent | ✅ Agent Skills standard |
| **Workflows** | ✅ Slash commands | ✅ Supported | ✅ Full workflow.md | ❌ Not explicit | ✅ Embedded in rules/skills |
| **Subagents** | ✅ Mode selection | ✅ Supported | ✅ Full subagent system | ✅ Custom agents | ✅ Full subagent system |
| **Hooks** | ❌ No | ✅ Yes | ✅ Yes (extensive) | ❌ No | ✅ Yes (extensive) |
| **Format** | Markdown + YAML | Markdown + YAML | Markdown + YAML | Markdown + YAML | Markdown + YAML |
| **Open Standard** | Agent Skills | Agent Skills | Agent Skills | Agent Skills | Agent Skills |

---

## 1. Kilo Configuration

### Project Structure
```
.kilo/
├── agents/
│   └── {agent-name}.md          # Agent config with references to skills
├── skills/
│   └── {skill-name}/
│       └── SKILL.md              # Full skill definition
└── commands/
    └── {command-name}.md         # Slash commands (workflows)
```

### Skills
- **Location:** `.kilo/skills/{skill-name}/SKILL.md`
- **Scope:** SHARED across all agents
- **Format:** Agent Skills standard (YAML frontmatter + markdown)
- **Referenced by:** Agent files list skill names in frontmatter

### Workflows
- **Location:** `.kilo/commands/{command-name}.md`
- **Format:** Slash commands
- **Usage:** Invoked via `/command-name` syntax

### Subagents
- **Method:** Mode selection
- **Built-in modes:** code, architect, test, review, debug, orchestrator, etc.
- **Invocation:** User switches modes explicitly

### Example Agent File
```markdown
---
name: "code"
description: "Write production code"
model: "anthropic/claude-opus-4-1"
state_management: ".promptosaurus/sessions/"
---

# System Prompt
You are an expert software engineer...

# Skills
- test-first-implementation (`.kilo/skills/test-first-implementation.md`)
- refactor-code-module (`.kilo/skills/refactor-code-module.md`)

# Workflows
See `/create-feature`, `/refactor-module` commands
```

---

## 2. Cline Configuration

### Project Structure
```
.clinerules                        # Main rules file
.cline/
└── skills/
    └── {skill-name}/
        └── SKILL.md
```

### Skills
- **Location:** `.cline/skills/{skill-name}/SKILL.md`
- **Scope:** Project-specific
- **Format:** Agent Skills standard
- **Usage:** Referenced in `.clinerules`

### Workflows
- **Location:** `.clinerules/workflows/` (optional)
- **Format:** Markdown files
- **Usage:** Invoked when relevant

### Subagents
- **Supported:** Yes
- **Format:** Similar to Claude Code
- **Usage:** Agent can delegate tasks

### Example .clinerules Entry
```markdown
When implementing features:
1. Use test-first-implementation skill
2. Follow the feature-implementation workflow
3. Run tests before committing
```

---

## 3. Claude Code Configuration

### Project Structure
```
.claude/
├── agents/
│   └── {agent-name}.md           # Subagent definitions
├── skills/
│   └── {skill-name}/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
└── contexts/
    └── {context-name}.md         # Context providers

~/.claude/
└── skills/                        # User-level shared skills
    └── {skill-name}/
        └── SKILL.md
```

### Skills
- **Location:** `.claude/skills/` (project) OR `~/.claude/skills/` (user)
- **Scope:** SHARED (user-level) or project-specific
- **Format:** Agent Skills standard with optional directories
- **Optional directories:** `scripts/`, `references/`, `assets/`

### Workflows
- **Location:** `.claude/skills/{skill-name}/workflow.md`
- **Format:** Full workflow.md with YAML frontmatter
- **Usage:** Invoked automatically or manually

### Subagents
- **Location:** `.claude/agents/{name}.md`
- **Format:** Markdown with YAML frontmatter
- **Fields:** name, description, model, tools, skills
- **Usage:** Full subagent system with contexts

### Hooks
- **Location:** `.claude/hooks.json`
- **Supported hooks:** sessionStart, sessionEnd, beforeShellExecution, afterFileEdit, etc.
- **Format:** JSON config with command scripts

### Example Skill
```markdown
---
name: test-first-implementation
description: Generate tests before implementing features
---

# Instructions
1. Analyze requirements
2. Create test file with comprehensive scenarios
3. Run tests (should fail)
4. Implement code to pass tests
5. Verify coverage

## Scripts
- `scripts/run-tests.sh` - Execute test suite
- `scripts/check-coverage.sh` - Verify coverage targets
```

---

## 4. GitHub Copilot Configuration

### Project Structure
```
.github/
├── copilot-instructions.md       # Main instructions
├── agents/
│   └── {agent-name}.agent.md     # Custom agents
└── skills/
    └── {skill-name}.md           # Per-agent skills
```

### Skills
- **Location:** `.github/skills/{skill-name}.md`
- **Scope:** Per-agent attachments
- **Format:** Agent Skills standard
- **Usage:** Attached to specific agents

### Workflows
- **Not explicitly supported**
- **Alternative:** Embedded in agent instructions

### Subagents (Custom Agents)
- **Location:** `.github/agents/{name}.agent.md`
- **Format:** Markdown with YAML frontmatter
- **Fields:** name, description, tools, skills
- **Usage:** Invoked explicitly

### MCP Servers
- **Supported:** Yes
- **Config:** `.github/copilot-mcp.json`
- **Purpose:** Tool integrations

### Example Custom Agent
```markdown
---
name: security-reviewer
description: Review code for security vulnerabilities
skills:
  - owasp-top-10
  - secrets-detection
---

You are a security expert...
```

---

## 5. Cursor Configuration

### Project Structure
```
.cursor/
├── rules/
│   ├── {rule-name}.md            # Project rules
│   └── {rule-name}.mdc           # Rules with frontmatter
├── agents/
│   └── {agent-name}.md           # Subagent definitions
├── skills/
│   └── {skill-name}/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
└── hooks.json                     # Hook configuration

AGENTS.md                          # Simple alternative to .cursor/rules

~/.cursor/
├── skills/                        # User-level shared skills
│   └── {skill-name}/
│       └── SKILL.md
└── agents/                        # User-level subagents
    └── {agent-name}.md
```

### Rules
- **Location:** `.cursor/rules/*.md` OR `AGENTS.md`
- **Format:** Markdown with optional YAML frontmatter
- **Frontmatter fields:** description, globs, alwaysApply
- **Types:** 
  - Always Apply (`alwaysApply: true`)
  - Apply Intelligently (based on description)
  - Apply to Specific Files (glob patterns)
  - Apply Manually (@-mention)
- **Team Rules:** Cloud-distributed for enterprise
- **Priority:** Enterprise → Team → Project → User

### Skills
- **Location:** `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`
- **Also loads from:** `.claude/skills/`, `.codex/skills/` (compatibility)
- **Scope:** Project-specific or user-level (SHARED)
- **Format:** Full Agent Skills standard
- **Frontmatter fields:** name, description, license, compatibility, metadata, disable-model-invocation
- **Optional directories:** `scripts/`, `references/`, `assets/`
- **Automatic discovery:** Yes
- **Manual invocation:** `/skill-name` syntax
- **GitHub install:** Supported

### Workflows
- **Not a separate concept**
- **Embedded in:** Rules or skills
- **Format:** Markdown content within rules/skills

### Subagents
- **Location:** `.cursor/agents/{name}.md`, `~/.cursor/agents/{name}.md`
- **Also loads from:** `.claude/agents/`, `.codex/agents/` (compatibility)
- **Format:** Markdown with YAML frontmatter
- **Frontmatter fields:** name, description, model, readonly, is_background
- **Built-in subagents:** explore, bash, browser
- **Model options:** 
  - `inherit` - Use parent model
  - `fast` - Use smaller/faster model
  - Specific model ID (e.g., `claude-opus-4-6`)
- **Execution modes:** Foreground (blocking) or background
- **Resumable:** Yes (via agent ID)
- **Can launch child subagents:** Yes (nested delegation)
- **MCP tools:** Inherited from parent

### Hooks
- **Location:** `.cursor/hooks.json`
- **Also:** `~/.cursor/hooks.json` (user-level)
- **Enterprise locations:**
  - macOS: `/Library/Application Support/Cursor/hooks.json`
  - Linux: `/etc/cursor/hooks.json`
  - Windows: `C:\ProgramData\Cursor\hooks.json`
- **Types:** Command-based or prompt-based (LLM-evaluated)
- **Agent hooks:**
  - sessionStart / sessionEnd
  - preToolUse / postToolUse / postToolUseFailure
  - subagentStart / subagentStop
  - beforeShellExecution / afterShellExecution
  - beforeMCPExecution / afterMCPExecution
  - beforeReadFile / afterFileEdit
  - beforeSubmitPrompt
  - preCompact
  - stop
  - afterAgentResponse / afterAgentThought
- **Tab hooks:**
  - beforeTabFileRead
  - afterTabFileEdit
- **Features:**
  - Matchers for filtering (regex patterns)
  - Timeout configuration
  - Loop limits (for stop/subagentStop)
  - failClosed option (block on failure)
  - Team distribution (cloud-synced for enterprise)
  - MDM distribution support

### Example Rule File
```markdown
---
description: "Frontend component standards"
globs:
  - "src/components/**/*.tsx"
alwaysApply: false
---

# Component Guidelines

- Use TypeScript for all components
- Follow functional component pattern
- Use hooks for state management
```

### Example Subagent
```markdown
---
name: security-auditor
description: Security specialist. Use when implementing auth, payments, or sensitive data.
model: inherit
readonly: true
---

You are a security expert auditing code...

When invoked:
1. Identify security-sensitive code paths
2. Check for common vulnerabilities
3. Verify secrets are not hardcoded
4. Review input validation
```

### Example Hooks Config
```json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [
      {
        "command": ".cursor/hooks/format.sh",
        "timeout": 30
      }
    ],
    "beforeShellExecution": [
      {
        "command": ".cursor/hooks/approve-network.sh",
        "matcher": "curl|wget|nc",
        "failClosed": true
      }
    ],
    "beforeMCPExecution": [
      {
        "type": "prompt",
        "prompt": "Does this MCP tool call look safe?",
        "timeout": 10
      }
    ]
  }
}
```

---

## Agent Skills Open Standard

All tools follow the **Agent Skills** open standard for skills.md format:

### SKILL.md Format
```markdown
---
name: skill-name
description: One-line description of what this skill does
tools_needed: [tool1, tool2]
license: MIT
compatibility: "Requires Python 3.8+"
metadata:
  version: "1.0.0"
  author: "Team Name"
disable-model-invocation: false
---

## Instructions

Detailed how-to instructions for the agent.

### When to Use
- Use this skill when...
- This skill is helpful for...

### Steps
1. First step
2. Second step
3. Third step

## Examples

Example usage...
```

### workflow.md Format
```markdown
---
name: workflow-name
description: One-line description of the workflow
steps:
  - Step 1 description
  - Step 2 description
  - Step 3 description
---

## Steps

### Step 1: Title
Detailed instructions...

### Step 2: Title
Detailed instructions...

### Step 3: Title
Detailed instructions...
```

---

## Builder Output Requirements

### Kilo Builder
- **Agent files:** `.kilo/agents/{agent}.md` with skill references
- **Skill files:** `.kilo/skills/{skill-name}/SKILL.md` (full content)
- **Workflow files:** `.kilo/commands/{command}.md`

### Cline Builder
- **Main file:** `.clinerules` (concatenated)
- **Skill files:** `.cline/skills/{skill-name}/SKILL.md`

### Claude Code Builder
- **Agent files:** `.claude/agents/{agent}.md`
- **Skill files:** `.claude/skills/{skill-name}/SKILL.md`
- **Workflow files:** `.claude/skills/{skill-name}/workflow.md`
- **Hook files:** `.claude/hooks.json`

### Copilot Builder
- **Main file:** `.github/copilot-instructions.md` (concatenated)
- **Agent files:** `.github/agents/{agent}.agent.md`
- **Skill files:** `.github/skills/{skill}.md` (attached to agents)

### Cursor Builder
- **Rule files:** `.cursor/rules/{agent}.md` (or `AGENTS.md` for simple cases)
- **Skill files:** `.cursor/skills/{skill-name}/SKILL.md`
- **Subagent files:** `.cursor/agents/{subagent}.md`
- **Hook files:** `.cursor/hooks.json`

---

## Key Insights

### Shared vs Per-Agent Skills
- **Kilo:** Skills are SHARED resources available to all agents
- **Claude Code:** Skills are SHARED at user-level or project-level
- **Cursor:** Skills are SHARED at user-level or project-level
- **Copilot:** Skills are PER-AGENT attachments
- **Cline:** Skills are project-specific

### Workflow Handling
- **Explicit workflows:** Claude Code (workflow.md), Kilo (slash commands)
- **Embedded workflows:** Cursor (in rules/skills), Cline (in .clinerules)
- **No explicit workflows:** Copilot (embedded in instructions)

### Subagent Support
- **Full systems:** Claude Code, Cursor (with hooks, contexts, resumability)
- **Mode-based:** Kilo (predefined modes)
- **Custom agents:** Copilot (manual definition)
- **Supported:** Cline (basic delegation)

### Hook Systems
- **Extensive:** Claude Code, Cursor (lifecycle hooks, prompt-based, command-based)
- **Basic:** Cline
- **None:** Kilo, Copilot

---

## References

- **Agent Skills Standard:** https://agentskills.io
- **Kilo Documentation:** Internal
- **Cline Documentation:** https://cline.bot/docs
- **Claude Code Documentation:** https://docs.claude.ai/code
- **GitHub Copilot Documentation:** https://docs.github.com/copilot
- **Cursor Documentation:** 
  - https://cursor.com/docs/rules
  - https://cursor.com/docs/skills
  - https://cursor.com/docs/subagents
  - https://cursor.com/docs/hooks

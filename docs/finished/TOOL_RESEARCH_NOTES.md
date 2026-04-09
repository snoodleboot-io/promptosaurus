# Research: How AI Tools Handle Instructions, Skills, and Workflows

## Kilo (CLI/IDE)

**STRUCTURE:** Agents + Skills + Workflows + Rules

**Agents:**
- Defined as `.md` files with YAML frontmatter
- Format: `description`, `mode`, `prompt`, `permission`, `model`, `temperature`
- Modes: `primary` (user selectable), `subagent` (invoked by other agents), `all` (both)
- Example: `.kilo/agents/code-reviewer.md`

**Skills:**
- Separate REUSABLE components (NOT agent-specific)
- Format: `SKILL.md` with frontmatter (name, description) + Markdown instructions
- Location: `.kilo/skills/skill-name/SKILL.md`
- Agent decides whether to use a skill based on description matching
- Cross-cutting concerns: examples are "api-design", "pdf-processing" 
- Available to ALL agents (generic)

**Workflows:**
- Step-by-step automation instructions
- Format: `.md` files with optional YAML frontmatter
- Location: `.kilo/commands/workflow-name.md`
- Invoked as slash commands: `/workflow-name`
- Can leverage all tools: read, glob, grep, edit, write, bash, webfetch
- Examples: "submit-pr", "release-management"

**Rules:**
- Project-level rules that apply to specific file types or situations

---

## What We Still Need to Research

1. **Claude** - How does Claude Code handle instructions/prompts?
2. **Cline** - How does Cline handle instructions?
3. **Cursor** - How does Cursor handle rules?
4. **Copilot** - How does GitHub Copilot handle instructions?
5. **Cursor** - How do they handle multi-mode/agent concepts?

---

## Key Findings So Far

### SKILLS are NOT per-agent
- They're SHARED, REUSABLE resources
- Available to all agents
- Agent decides to use based on description
- Cross-cutting concerns (security, API design, etc.)

### WORKFLOWS are MULTI-STEP AUTOMATIONS
- Not tied to individual agents
- Step-by-step instructions for complex tasks
- Can involve multiple tools and agents
- User-invoked or agent-invoked

### AGENTS are THE PRIMARY CONCEPT
- Specialized AI assistants
- Can be primary (user-selectable) or subagents (delegated)
- Use skills when appropriate
- Follow workflows when needed

---

## Implications for Promptosaurus Design

1. **Prompt component** in our design - Correct! Agents need role/prompt
2. **Skills component** - Should be SHARED, NOT per-agent
   - Perhaps skills for different domains?
   - Example: "security-analysis", "performance-optimization"
   - Available to relevant agents (review, code, security, etc.)
3. **Workflows component** - Should be MULTI-STEP
   - Not individual agent processes
   - Complex multi-agent orchestrations
   - Example: "code-review-then-implement", "test-driven-development"

Need to research how other tools (Claude, Cline, Cursor, Copilot) handle these concepts.


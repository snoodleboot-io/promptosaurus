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


---

## Cline (VS Code Extension) - RESEARCH COMPLETE

**STRUCTURE:** Agents + Skills (implied) + Rules (implied)

**Key Findings from GitHub Repo:**
- Directory structure: `.agents/skills/create-pull-request/` (suggests skill bundling)
- Directory: `.clinerules/` (suggests project-level customization)
- Uses MCP (Model Context Protocol) for extending capabilities
- Can create/edit files, execute terminal commands, use browser
- No explicit "workflow" or "skills" documentation visible in repo, but infrastructure suggests both are supported

**Agent Capability:**
- Autonomous coding agent that can create/edit files, run commands, browse
- Can use CLI and editor
- Supports custom tools via MCP

**Customization Model:**
- Skills appear to be bundled in `.agents/skills/` structure
- Rules in `.clinerules/`
- MCP for extending beyond built-in capabilities

---

## Cursor (IDE) - RESEARCH COMPLETE

**STRUCTURE:** Agents + Rules + (Agents work autonomously)

**Key Findings from cursor.com:**
- Feature: "Agents turn ideas into code" (cloud agents that work autonomously)
- Feature: "Cursor Rules" for customization
- Agents can: Research repos, create implementation plans, make code changes
- Integration: Works with Slack, GitHub, and other platforms
- "Tab" feature for magically accurate autocomplete
- Cloud agents run in parallel, build/test/demo code for review

**Agent Capability:**
- Autonomous agents that research, plan, and implement
- Can review pull requests (via GitHub integration)
- Can collaborate via Slack

**Customization Model:**
- "Cursor Rules" (similar to instructions)
- Rules appear to be global/repo-level (not per-agent based on marketing)
- Cloud agents are deployed/managed separately

**No explicit "Skills" or "Workflows" mentioned** - focus is on autonomous agents + rules

---

## GitHub Copilot (Cloud + CLI) - RESEARCH COMPLETE

**STRUCTURE:** Agents + Skills + Hooks + Custom Instructions + Plugins + MCP

**Key Findings from docs.github.com:**
- **Custom Agents**: Specialized agents for specific tasks
- **Agent Skills**: Modify Copilot's behavior and abilities for particular tasks  
  - Created per-task or per-agent
  - Skills allow Copilot to perform specialized tasks
- **Hooks**: Extend agent behavior by executing custom shell commands at key points
  - `onPreToolUse`, `onPostToolUse`, lifecycle hooks, error handling hooks
- **Custom Instructions**: Provide context on how to understand your project
  - Repository-level, organization-level, and personal instructions
- **Copilot CLI Plugins**: Installable packages that extend CLI with reusable agents/skills/hooks
- **MCP Servers**: Extend capabilities via Model Context Protocol
- **Workflows**: Not explicitly mentioned, but `/fleet` command runs tasks in parallel

**Agent Capability:**
- Cloud agent: Research repos, create implementation plans, make code changes
- CLI: Programmatic access to Copilot with customization
- Code review agent: Reviews PRs automatically
- Autonomous execution mode ("autopilot")

**Customization Model:**
- Per-agent skill creation
- Global hooks at key execution points
- Instructions at multiple scopes (personal, org, repo)
- Plugins as reusable packages
- MCP servers for external tools
- `/research`, `/fleet` commands for multi-step tasks

---

## CRITICAL DISCOVERIES - SKILLS & WORKFLOWS

### 1. **Skills Model Differs SIGNIFICANTLY by Tool**

| Tool | Skills Scope | Architecture |
|------|--------------|------------|
| **Kilo** | SHARED (all agents) | Domain-specific (security, perf, etc.) |
| **Cline** | Bundle-level | Bundled in `.agents/skills/` |
| **Cursor** | Not mentioned | Rules are global, NOT per-agent |
| **Copilot** | PER-AGENT | Task-specific expertise extensions |

**🔴 CRITICAL INSIGHT:** Copilot treats Skills as PER-AGENT, while Kilo treats them as SHARED. Cline bundles them. Cursor ignores them.

**Implication:** Phase 2 CANNOT have a single "shared skills" approach that works for all tools.

### 2. **"Workflows" Concept Varies Significantly**

| Tool | Workflow Type | Implementation |
|------|--------------|-----------------|
| **Kilo** | EXPLICIT | `.kilo/commands/` as slash commands (`/submit-pr`) |
| **Cline** | Unknown | Not documented |
| **Cursor** | IMPLICIT/AUTONOMOUS | Cloud agents handle orchestration automatically |
| **Copilot** | MIXED | Hooks + Commands + Agent autonomy (`/fleet`, `/research`) |

**🔴 CRITICAL INSIGHT:** Kilo has EXPLICIT workflows (slash commands), while Cursor/Copilot rely on AGENT AUTONOMY to handle multi-step tasks.

### 3. **Customization Hook System Sophistication**

| Tool | Hook System | Hooks Available |
|------|-----------|-----------------|
| **Kilo** | None | N/A |
| **Cline** | MCP | External tool creation |
| **Cursor** | Simple Rules | Global rules only |
| **Copilot** | Advanced | Pre-tool, post-tool, lifecycle, error handling, MCP |

**Implication:** Copilot has the most sophisticated extensibility model for tool execution control.

---

## PHASE 2 ARCHITECTURE PROBLEM

**Current assumption in Phase 2 PRD:** "One unified component model for all 6 tools"

**Reality:** 
- Tools have FUNDAMENTALLY DIFFERENT architectures
- Skills are shared (Kilo), per-agent (Copilot), bundled (Cline), or absent (Cursor)
- Workflows are explicit commands (Kilo) or implicit autonomy (Cursor/Copilot)
- Customization ranges from global rules (Cursor) to sophisticated hooks (Copilot)

**Solution Paths:**
1. **Tool-Specific Builders**: Each tool gets its own builder with tool-native architecture
2. **Abstraction Layer**: Create abstraction that maps unified components → tool-specific outputs
3. **Hybrid**: Core components unified, with tool-specific extensions for skills/workflows/hooks

---

## Remaining Research Questions

1. **Claude (Anthropic)** - How does Claude Code define instructions/agents? (NOT YET RESEARCHED)
2. **Cline** - More detailed documentation on explicit skills/workflows (NOT YET RESEARCHED)
3. **Cursor** - How are rules structured? Can they be agent-specific? (NOT YET RESEARCHED)
4. **Copilot CLI** - How are plugins structured for reusability? (PARTIALLY RESEARCHED)


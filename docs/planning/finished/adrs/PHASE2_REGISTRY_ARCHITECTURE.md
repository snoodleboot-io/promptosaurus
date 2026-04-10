# Architecture Decision Record: Phase 2 - Unified Registry & Builder Pattern

**Date:** 2026-04-08  
**Status:** Proposed  
**Deciders:** Architecture Team  
**Context:** Supporting 6 AI tools (Kilo IDE, Kilo CLI, Cline, Cursor, Copilot, Claude) with different agent/skill/workflow models

---

## THE PROBLEM

Each tool has fundamentally different ways of configuring agents, skills, and workflows:

| Tool | Agent Format | Skills | Workflows | Hooks/Rules |
|------|--------------|--------|-----------|------------|
| **Kilo** | `.md` YAML+Markdown | Shared (`.kilo/skills/`) | Explicit (`.kilo/commands/`) | Rules (by filetype) |
| **Copilot** | JSON/TypeScript | Per-agent | Hooks (`onPreToolUse`, etc) | Instructions (scoped) |
| **Cursor** | Config (unknown) | None | Autonomous agent orchestration | Rules (global) |
| **Cline** | Directory-based | Bundled in `.agents/skills/` | Not documented | `.clinerules/` |
| **Claude** | API-based | Via system prompt + tools | Via system prompt | Tools JSON schema |

**Current registry approach fails because:** It assumes one unified source format that all tools consume. But each tool has its own native format.

---

## SOLUTION: Intermediate Representation (IR) + Adapter Pattern

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│  User Input                                                 │
│  - YAML files (.prompt.yml, .skill.yml, .workflow.yml)      │
│  - Markdown files (agent.md, skill.md)                      │
│  - CLI arguments                                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  INTERMEDIATE REPRESENTATION (IR)                           │
│  - PromptosaurusAgent (unified agent model)                 │
│  - PromptosaurusSkill (unified skill model)                 │
│  - PromptosaurusWorkflow (unified workflow model)           │
│  - PromptosaurusRules (unified rules model)                 │
│                                                             │
│  (All tools transform their native format → IR)             │
│  (All builders transform IR → tool-native format)           │
└──────────────────────────┬──────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┬────────────┬──────────┐
           │               │               │            │          │
           ▼               ▼               ▼            ▼          ▼
      ┌────────┐    ┌────────────┐  ┌────────┐  ┌────────┐  ┌────────┐
      │Kilo    │    │Copilot     │  │Cursor  │  │Cline   │  │Claude  │
      │Builder │    │Builder     │  │Builder │  │Builder │  │Builder │
      └────────┘    └────────────┘  └────────┘  └────────┘  └────────┘
           │               │               │            │          │
           ▼               ▼               ▼            ▼          ▼
    .kilo/agents/   skills/hooks/    rules.yml    .clinerules/  API call
```

---

## SOLID DESIGN PRINCIPLES

### 1. Single Responsibility Principle (SRP)
- **Parser**: Converts user input → IR
- **Builder**: Converts IR → tool-native format
- **Registry**: Manages builder lifecycle and lookup

Each has ONE reason to change.

### 2. Open/Closed Principle (OCP)
- **Open for extension**: Add new tool builder without modifying existing code
- **Closed for modification**: Existing builders unchanged when adding new tool

Adding Claude builder doesn't touch Kilo, Copilot, Cursor, Cline builders.

### 3. Liskov Substitution Principle (LSP)
- All builders implement `PromptosaurusBuilder` interface
- Any builder can substitute for another without breaking code
- Builders are **interchangeable**

### 4. Interface Segregation Principle (ISP)
- Builders implement only what they need:
  - Core interface: `build(agent: PromptosaurusAgent) → BuiltAgent`
  - Optional mixins: `SupportsSkills`, `SupportsWorkflows`, `SupportsHooks`, `SupportsRules`
- Cursor implements `SupportsRules` but not `SupportsWorkflows`
- Copilot implements `SupportsHooks` + `SupportsSkills`
- Kilo implements everything

### 5. Dependency Inversion Principle (DIP)
- Code depends on abstractions (`PromptosaurusBuilder`), not concretions
- Sweet_tea factory returns `PromptosaurusBuilder` interface
- Caller doesn't care which tool it gets

---

## INTERFACE DESIGN

### Base Builder Interface

```python
from abc import ABC, abstractmethod
from typing import Protocol

class PromptosaurusBuilder(ABC):
    """Standard interface all builders implement"""
    
    @abstractmethod
    def build_agent(self, agent: PromptosaurusAgent) -> BuiltAgent:
        """Transform IR Agent → Tool-native Agent"""
        pass
    
    @property
    @abstractmethod
    def tool_name(self) -> str:
        """Unique identifier for this tool"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Builder version (for compatibility tracking)"""
        pass
```

### Mixin Interfaces (Optional Capabilities)

```python
class SupportsSkills(Protocol):
    """Tool supports reusable skills"""
    def build_skill(self, skill: PromptosaurusSkill) -> BuiltSkill:
        pass

class SupportsWorkflows(Protocol):
    """Tool supports multi-step workflows"""
    def build_workflow(self, workflow: PromptosaurusWorkflow) -> BuiltWorkflow:
        pass

class SupportsHooks(Protocol):
    """Tool supports lifecycle hooks"""
    def build_hook(self, hook: PromptosaurusHook) -> BuiltHook:
        pass

class SupportsRules(Protocol):
    """Tool supports custom rules"""
    def build_rules(self, rules: PromptosaurusRules) -> BuiltRules:
        pass
```

### Builder Implementation Pattern

```python
class KiloBuilder(PromptosaurusBuilder, SupportsSkills, SupportsWorkflows, SupportsRules):
    """Kilo IDE/CLI builder - supports all features"""
    
    def build_agent(self, agent: PromptosaurusAgent) -> BuiltAgent:
        # Kilo-native format: .md file with YAML frontmatter
        return KiloAgent(agent)
    
    def build_skill(self, skill: PromptosaurusSkill) -> BuiltSkill:
        # Kilo-native: .kilo/skills/{name}/SKILL.md
        return KiloSkill(skill)
    
    def build_workflow(self, workflow: PromptosaurusWorkflow) -> BuiltWorkflow:
        # Kilo-native: .kilo/commands/{name}.md (slash commands)
        return KiloWorkflow(workflow)
    
    def build_rules(self, rules: PromptosaurusRules) -> BuiltRules:
        # Kilo-native: .kilocode/rules-{mode}/
        return KiloRules(rules)
    
    @property
    def tool_name(self) -> str:
        return "kilo"
    
    @property
    def version(self) -> str:
        return "1.0.0"


class CopilotBuilder(PromptosaurusBuilder, SupportsSkills, SupportsHooks):
    """GitHub Copilot builder - per-agent skills + hooks"""
    
    def build_agent(self, agent: PromptosaurusAgent) -> BuiltAgent:
        # Copilot: Agent API with system prompt + tools
        return CopilotAgent(agent)
    
    def build_skill(self, skill: PromptosaurusSkill) -> BuiltSkill:
        # Copilot: Per-agent skill attached to agent
        return CopilotSkill(skill, agent_id=...)
    
    def build_hook(self, hook: PromptosaurusHook) -> BuiltHook:
        # Copilot: Pre/post-tool hooks via agent configuration
        return CopilotHook(hook)
    
    # ... etc

class CursorBuilder(PromptosaurusBuilder, SupportsRules):
    """Cursor IDE builder - rules-based customization"""
    
    def build_agent(self, agent: PromptosaurusAgent) -> BuiltAgent:
        # Cursor: Cloud agent + rules
        return CursorAgent(agent)
    
    def build_rules(self, rules: PromptosaurusRules) -> BuiltRules:
        # Cursor: Global rules (not per-agent)
        return CursorRules(rules)

class ClaudeBuilder(PromptosaurusBuilder):
    """Claude API builder - system prompts + tools"""
    
    def build_agent(self, agent: PromptosaurusAgent) -> BuiltAgent:
        # Claude: API call with system_prompt + tools
        return ClaudeAgent(agent)
```

---

## REGISTRY & FACTORY PATTERN (using sweet_tea)

### Sweet_Tea Configuration

```python
from sweet_tea import Factory

# Registry is a sweet_tea Factory
builder_factory = Factory(
    implementations={
        "kilo": KiloBuilder,
        "copilot": CopilotBuilder,
        "cursor": CursorBuilder,
        "cline": ClaudeBuilder,
        "claude": ClaudeBuilder,
    },
    interface=PromptosaurusBuilder,
)

# Usage:
def generate_for_tool(agent: PromptosaurusAgent, tool: str) -> BuiltAgent:
    builder = builder_factory.create(tool)  # Returns PromptosaurusBuilder
    return builder.build_agent(agent)

# Caller doesn't care which tool - builder is abstraction
```

**Why sweet_tea, not nested factory:**
- Sweet_tea handles registry, lifecycle, dependency injection
- Don't wrap it - use it directly
- Extensible: add new builder → register with factory
- No factory-on-factory complexity

---

## MINIMAL/VERBOSE STRATEGY (Next Phase)

Once IR + builders are solid, minimal/verbose becomes:

```python
# Option A: Source files
agent.minimal.yml   # Concise version
agent.verbose.yml   # Detailed version
# Builders consume whichever user specifies

# Option B: Generated
agent.yml (source)
agent.verbose.yml (auto-generated via PromptosaurusExpander)
# Builders consume both or either

# Either way, builders are agnostic
# IR is the same, output differs
```

---

## IMPLEMENTATION ROADMAP (Phase 2A)

1. **Define IR Models**
   - `PromptosaurusAgent`, `PromptosaurusSkill`, `PromptosaurusWorkflow`, `PromptosaurusRules`
   - Parser: Input files → IR

2. **Build Standard Interface**
   - `PromptosaurusBuilder` base class
   - `SupportsX` mixins for optional features
   - Registry factory using sweet_tea

3. **Implement Tool Builders** (in priority order)
   - KiloBuilder (already have most of this)
   - CopilotBuilder
   - CursorBuilder
   - ClaudeBuilder
   - ClaudeBuilder (API)

4. **Validate Against Each Tool**
   - KiloBuilder outputs valid `.kilo/` structure
   - CopilotBuilder outputs valid Copilot API format
   - Etc.

5. **Add Minimal/Verbose Handling**
   - Define expansion rules
   - Build generators/transformers

---

## Key Benefits of This Design

✅ **SOLID Compliance:** Each principle properly applied  
✅ **Open/Closed:** Add new tool without modifying existing builders  
✅ **Liskov:** All builders swap seamlessly  
✅ **Interface Segregation:** Tools only implement what they need  
✅ **Dependency Inversion:** Code depends on abstraction, not concrete tools  
✅ **Mixins Handle Complexity:** Different tool capabilities via composition  
✅ **Sweet_Tea Power:** Factory handles registry without overhead  
✅ **Single Source of Truth:** Promptosaurus configs are IR for all tools  

---

## Known Challenges

1. **IR Design**: Must capture all tool capabilities without bloat
   - Solution: Start minimal, expand as tools require new features
   
2. **Feature Mismatch**: Some tools can't express concepts from other tools
   - Solution: Builders silently ignore unsupported features, log warnings
   
3. **Validation**: IR must validate against each tool's constraints
   - Solution: Each builder implements `validate(agent: PromptosaurusAgent) → ValidationResult`

---

## Appendix: Tool Differences Summary

| Aspect | Kilo | Copilot | Cursor | Cline | Claude |
|--------|------|---------|--------|-------|--------|
| **Agent Source** | `.md` file | API/JSON | Config | Directory | API |
| **Skills Model** | Shared | Per-agent | N/A | Bundled | Via system prompt |
| **Workflows** | Explicit (commands) | Hooks + autonomy | Autonomous | Unknown | Via tools |
| **Customization** | Rules | Hooks + instructions | Rules | Rules | System prompt |
| **Configuration** | File-based | API-based | Cloud-based | File-based | API-based |


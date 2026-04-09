# Architecture Decision Record: Phase 2A - IR Models, Builders, and Minimal/Verbose Strategy

**Date:** 2026-04-08  
**Status:** Implementation Planning  
**Deciders:** Architecture Team  
**Builds On:** PHASE2_REGISTRY_ARCHITECTURE.md

---

## 1. INTERMEDIATE REPRESENTATION (IR) AS PYDANTIC MODELS

IR is the single source of truth. All builders consume IR. IR validation happens via Pydantic.

### Core IR Models

```python
# promptosaurus/models/agent.py
from typing import Optional, List
from pydantic import BaseModel, Field

class PromptosaurusAgent(BaseModel):
    """Unified agent definition - IR for all tools."""
    
    # Identity
    name: str = Field(..., description="Unique agent name")
    description: str = Field(..., description="What this agent does")
    
    # Behavior (Minimal)
    prompt: str = Field(..., description="Agent instructions/role")
    
    # Behavior (Verbose - auto-expanded from minimal)
    prompt_verbose: Optional[str] = Field(None, description="Detailed version with examples")
    
    # Skills this agent can use
    skills: List[str] = Field(default_factory=list, description="List of skill names")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Organization tags")
    
    model_config = {"json_schema_extra": {"examples": [...]}}
    
    def get_prompt(self, verbose: bool = False) -> str:
        """Get minimal or verbose prompt."""
        if verbose and self.prompt_verbose:
            return self.prompt_verbose
        return self.prompt


class PromptosaurusSkill(BaseModel):
    """Reusable skill/capability."""
    
    name: str = Field(..., description="Skill name")
    description: str = Field(..., description="What skill does")
    instructions: str = Field(..., description="How to use skill")
    instructions_verbose: Optional[str] = Field(None, description="Detailed instructions")
    
    scope: str = Field(default="shared", description="shared | per-agent | bundled")
    tags: List[str] = Field(default_factory=list)
    
    def get_instructions(self, verbose: bool = False) -> str:
        if verbose and self.instructions_verbose:
            return self.instructions_verbose
        return self.instructions


class PromptosaurusWorkflow(BaseModel):
    """Multi-step workflow/automation."""
    
    name: str
    description: str
    steps: List[str] = Field(..., description="Ordered step definitions")
    
    # Which tools can execute this?
    target_tools: List[str] = Field(
        default=["kilo"], 
        description="Tools that support this workflow"
    )


class PromptosaurusRules(BaseModel):
    """Project-level rules/customizations."""
    
    name: str
    description: str
    
    # Rule applicability
    file_pattern: Optional[str] = Field(None, description="e.g., '*.py'")
    scope: str = Field(default="global", description="global | per-agent | per-file")
    
    # Rule content
    instructions: str


class PromptosaurusProject(BaseModel):
    """Complete project configuration (IR root)."""
    
    agents: List[PromptosaurusAgent]
    skills: List[PromptosaurusSkill] = Field(default_factory=list)
    workflows: List[PromptosaurusWorkflow] = Field(default_factory=list)
    rules: List[PromptosaurusRules] = Field(default_factory=list)
```

---

## 2. MINIMAL/VERBOSE STRATEGY (BUILT INTO IR)

### Strategy: Dual Fields in Models

Each content field has two versions:
- **Minimal** (`prompt`, `instructions`) - Concise, production-ready
- **Verbose** (`prompt_verbose`, `instructions_verbose`) - Detailed with examples

### How It Works

**Option A: Source Files Define Both**
```yaml
# agent.yml
name: code-reviewer
description: Reviews code quality
prompt: |
  Review the code for quality issues.
prompt_verbose: |
  Review the code for:
  1. Performance issues
  2. Security vulnerabilities
  3. Code clarity
  4. Test coverage
  
  Example: "This function leaks memory because..."
```

**Option B: Auto-Expansion** (in Phase 2B)
```python
# Phase 2A: Manual entry
# Phase 2B: Expander transforms minimal → verbose

class PromptExpander:
    def expand(self, minimal: str, context: AgentContext) -> str:
        """Generate verbose from minimal using LLM or templates."""
        pass
```

### Builder Usage Pattern

```python
# Builders receive IR with minimal + verbose versions
# Builders choose based on target tool needs

class KiloBuilder:
    def build_agent(self, agent: PromptosaurusAgent, verbose: bool = False):
        prompt = agent.get_prompt(verbose=verbose)
        # Generate .kilo/agents/name.md with chosen prompt
```

---

## 3. BUILDER INTERFACE & VALIDATION

### Builder Interface (SOLID)

```python
# promptosaurus/builders/interface.py
from abc import ABC, abstractmethod
from typing import Protocol
from pydantic import ValidationError

class PromptosaurusBuilder(ABC):
    """Standard interface - all builders implement this."""
    
    @abstractmethod
    def build_agent(self, agent: PromptosaurusAgent) -> dict:
        """Transform IR Agent → Tool-native Agent format."""
        pass
    
    @abstractmethod
    def validate_agent(self, agent: PromptosaurusAgent) -> list[str]:
        """Validate IR Agent against tool constraints.
        
        Returns: List of validation errors (empty = valid)
        """
        pass
    
    @property
    @abstractmethod
    def tool_name(self) -> str:
        """e.g., 'kilo', 'copilot', 'claude'"""
        pass
    
    @property
    @abstractmethod
    def supported_features(self) -> dict[str, bool]:
        """Which capabilities this tool supports."""
        return {
            "skills": False,
            "workflows": False,
            "hooks": False,
            "rules": False,
        }


# Optional Mixin Interfaces
class SupportsSkills(Protocol):
    def build_skill(self, skill: PromptosaurusSkill) -> dict:
        pass
    
    def validate_skill(self, skill: PromptosaurusSkill) -> list[str]:
        pass

class SupportsWorkflows(Protocol):
    def build_workflow(self, workflow: PromptosaurusWorkflow) -> dict:
        pass

class SupportsHooks(Protocol):
    def build_hook(self, hook: dict) -> dict:
        pass

class SupportsRules(Protocol):
    def build_rules(self, rules: PromptosaurusRules) -> dict:
        pass
```

### IR Parser with Pydantic Validation

```python
# promptosaurus/parser/parser.py
from pathlib import Path
import yaml
from pydantic import ValidationError

class PromptosaurusParser:
    """Parse user input → IR with Pydantic validation."""
    
    @staticmethod
    def parse_file(path: Path) -> PromptosaurusAgent:
        """Load YAML/Markdown → PromptosaurusAgent (IR).
        
        Raises: ValidationError if IR is invalid
        """
        with open(path) as f:
            data = yaml.safe_load(f)
        
        # Pydantic automatically validates
        return PromptosaurusAgent(**data)
    
    @staticmethod
    def parse_project(root: Path) -> PromptosaurusProject:
        """Load entire project → PromptosaurusProject."""
        agents = []
        skills = []
        
        # Load all agents
        for agent_file in (root / "agents").glob("*.yml"):
            agents.append(PromptosaurusParser.parse_file(agent_file))
        
        # Load all skills
        for skill_file in (root / "skills").glob("*/SKILL.yml"):
            skills.append(PromptosaurusParser.parse_file(skill_file))
        
        # Pydantic validates the entire project
        return PromptosaurusProject(
            agents=agents,
            skills=skills,
            # workflows, rules...
        )
```

### Builder Validation Pattern

```python
# promptosaurus/builders/kilo.py
class KiloBuilder(
    PromptosaurusBuilder,
    SupportsSkills,
    SupportsWorkflows,
    SupportsRules,
):
    """Kilo IDE/CLI builder - validates against Kilo constraints."""
    
    def build_agent(self, agent: PromptosaurusAgent) -> dict:
        # First validate
        errors = self.validate_agent(agent)
        if errors:
            raise ValueError(f"Validation errors: {errors}")
        
        # Then build
        return {
            "name": agent.name,
            "description": agent.description,
            "prompt": agent.get_prompt(verbose=False),
            "skills": agent.skills,
            # ... convert to Kilo format
        }
    
    def validate_agent(self, agent: PromptosaurusAgent) -> list[str]:
        """Validate against Kilo constraints."""
        errors = []
        
        # Kilo requires name to be snake_case for filename
        if not agent.name.islower() or " " in agent.name:
            errors.append(f"Agent name must be snake_case: {agent.name}")
        
        # Kilo agent skills must exist
        for skill in agent.skills:
            if not self._skill_exists(skill):
                errors.append(f"Skill not found: {skill}")
        
        return errors
    
    @property
    def tool_name(self) -> str:
        return "kilo"
    
    @property
    def supported_features(self) -> dict[str, bool]:
        return {
            "skills": True,
            "workflows": True,
            "hooks": False,
            "rules": True,
        }
```

---

## 4. SWEET_TEA FACTORY PATTERN (Following Existing Code)

### Factory Registration

```python
# promptosaurus/builders/factory.py
from sweet_tea.registry import Registry
from sweet_tea.abstract_factory import AbstractFactory

from promptosaurus.builders.interface import PromptosaurusBuilder
from promptosaurus.builders.kilo import KiloBuilder
from promptosaurus.builders.copilot import CopilotBuilder
from promptosaurus.builders.cursor import CursorBuilder
from promptosaurus.builders.cline import ClaudeBuilder
from promptosaurus.builders.claude_api import ClaudeAPIBuilder

# Register builders with sweet_tea (following promptosaurus pattern)
Registry.register("kilo", KiloBuilder, library="promptosaurus")
Registry.register("copilot", CopilotBuilder, library="promptosaurus")
Registry.register("cursor", CursorBuilder, library="promptosaurus")
Registry.register("cline", ClaudeBuilder, library="promptosaurus")
Registry.register("claude", ClaudeAPIBuilder, library="promptosaurus")


class BuilderFactory:
    """Factory for creating tool builders via sweet_tea."""
    
    @staticmethod
    def create(tool_name: str) -> PromptosaurusBuilder:
        """Get builder for specified tool.
        
        Args:
            tool_name: "kilo" | "copilot" | "cursor" | "cline" | "claude"
        
        Returns:
            PromptosaurusBuilder instance
        
        Raises:
            KeyError if tool not found
        """
        factory = AbstractFactory[PromptosaurusBuilder]
        return factory.create(tool_name)
    
    @staticmethod
    def list_tools() -> list[str]:
        """Get available tool names."""
        return ["kilo", "copilot", "cursor", "cline", "claude"]
```

### Usage

```python
# Client code - doesn't care which tool
agent_ir = PromptosaurusParser.parse_file("agent.yml")

# Get builder for target tool
builder = BuilderFactory.create("kilo")

# Builder validates then builds
try:
    built_agent = builder.build_agent(agent_ir)
except ValueError as e:
    print(f"Validation error: {e}")
```

---

## 5. CLAUDE API RESEARCH & IMPLEMENTATION

### What We Know About Claude API

Claude doesn't have "Agents API" like Copilot. Instead:

1. **System Prompt** = Agent definition
2. **Tools** = Skills/capabilities (JSON schema)
3. **Conversation Loop** = Workflow execution
4. **Sampling Params** = Temperature, top_p, etc.

### Claude Builder Structure

```python
# promptosaurus/builders/claude_api.py
from anthropic import Anthropic

class ClaudeAPIBuilder(PromptosaurusBuilder):
    """Claude API builder - system_prompt + tools."""
    
    def build_agent(self, agent: PromptosaurusAgent) -> dict:
        """Transform IR Agent → Claude API format."""
        return {
            "name": agent.name,
            "system_prompt": agent.get_prompt(verbose=False),
            "tools": self._build_tools_from_skills(agent.skills),
            "model": "claude-opus-4-5",  # From IR in Phase 2B
        }
    
    def validate_agent(self, agent: PromptosaurusAgent) -> list[str]:
        """Validate against Claude constraints."""
        errors = []
        
        # Claude has max context limit
        if len(agent.prompt) > 100000:
            errors.append("System prompt exceeds Claude max length")
        
        return errors
    
    def _build_tools_from_skills(self, skill_names: list[str]) -> list[dict]:
        """Convert Promptosaurus skills → Claude tools JSON schema."""
        # For each skill, generate JSON schema tool definition
        # Will be filled in when Claude tool calling is fully understood
        pass
    
    @property
    def tool_name(self) -> str:
        return "claude"
    
    @property
    def supported_features(self) -> dict[str, bool]:
        return {
            "skills": True,  # Via tools
            "workflows": True,  # Via tool calling loop
            "hooks": False,  # Not natively supported
            "rules": False,  # Not natively supported
        }
```

### What We Still Need

**Claude API Questions:**
1. How to expose Promptosaurus skills as Claude tools?
2. How to define tool schemas for each skill?
3. How to handle tool calling workflows in Claude?
4. Is there a "session" concept for multi-turn workflows?

**Action Item:** Once Claude API docs load, research:
- Tool definition format (JSON schema required?)
- Tool calling loop (how Claude invokes tools)
- Sessions/context management
- Error handling for tool execution

---

## 6. IMPLEMENTATION ROADMAP (PHASE 2A)

### Week 1: Foundation
- [ ] Define all Pydantic IR models (Agent, Skill, Workflow, Rules, Project)
- [ ] Add minimal/verbose fields to all models
- [ ] Create comprehensive examples in YAML format
- [ ] Set up Pydantic validation tests

### Week 2: Parser & Factory
- [ ] Implement PromptosaurusParser (YAML → IR)
- [ ] Implement BuilderFactory with sweet_tea registration
- [ ] Add tests: parser roundtrips correctly
- [ ] Add tests: factory instantiates correct builder

### Week 3: KiloBuilder (Highest Priority)
- [ ] Implement KiloBuilder with full interface
- [ ] Implement validation for Kilo constraints
- [ ] Test: agent IR → valid .kilo/agents/ structure
- [ ] Test: skill IR → valid .kilo/skills/ structure
- [ ] Test: workflow IR → valid .kilo/commands/ structure

### Week 4: CopilotBuilder
- [ ] Research Copilot Agent API in detail
- [ ] Implement CopilotBuilder (skills + hooks)
- [ ] Test: agent IR → valid Copilot API format
- [ ] Test: skill IR → per-agent skill attachment

### Week 5: ClaudeBuilder
- [ ] Complete Claude API research
- [ ] Implement ClaudeAPIBuilder (system_prompt + tools)
- [ ] Test: agent IR → valid Claude API call
- [ ] Test: skill IR → Claude tool schema

### Week 6: CursorBuilder + ClaudeBuilder (Cline)
- [ ] Implement CursorBuilder (rules only)
- [ ] Implement ClaudeBuilder (directory-based)
- [ ] Complete test coverage for all builders

### Week 7: Validation & Documentation
- [ ] Add comprehensive validation tests
- [ ] Document IR model constraints
- [ ] Document builder capabilities
- [ ] Example projects for each tool

---

## 7. FILE STRUCTURE (PHASE 2A)

```
promptosaurus/
├── models/
│   ├── __init__.py
│   ├── agent.py          # PromptosaurusAgent
│   ├── skill.py          # PromptosaurusSkill
│   ├── workflow.py       # PromptosaurusWorkflow
│   ├── rules.py          # PromptosaurusRules
│   └── project.py        # PromptosaurusProject (root)
│
├── parser/
│   ├── __init__.py
│   ├── parser.py         # PromptosaurusParser (Pydantic validation)
│   └── loaders.py        # YAML/Markdown loaders
│
├── builders/
│   ├── __init__.py
│   ├── interface.py      # PromptosaurusBuilder (ABC + mixins)
│   ├── factory.py        # BuilderFactory + sweet_tea registration
│   ├── kilo.py           # KiloBuilder
│   ├── copilot.py        # CopilotBuilder
│   ├── cursor.py         # CursorBuilder
│   ├── cline.py          # ClaudeBuilder (Cline)
│   └── claude_api.py     # ClaudeAPIBuilder
│
└── tests/
    ├── unit/
    │   ├── models/
    │   ├── parser/
    │   └── builders/
    └── integration/
        └── builders/     # Test each builder output
```

---

## NEXT ACTIONS

1. **Claude API Deep Dive** (if docs ever load!)
   - Tool definition format
   - Tool calling workflow
   - Multi-turn session management
   - Error handling

2. **IR Model Finalization**
   - Review Pydantic definitions above
   - Add more constraints (max lengths, patterns)
   - Add examples to each model
   - Define validation rules

3. **Parser Implementation**
   - Load YAML files
   - Parse Markdown frontmatter + content
   - Validate via Pydantic
   - Return PromptosaurusProject

4. **Factory Setup**
   - Follow existing sweet_tea pattern
   - Register all builders
   - Test builder lookup

5. **KiloBuilder First**
   - We already have agent generation code
   - Reuse existing patterns
   - Validate against Kilo structure


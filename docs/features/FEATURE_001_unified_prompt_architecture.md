# Feature: Phase 2A - Unified Prompt Architecture Implementation

**Feature ID:** FEATURE_001  
**Status:** Planning  
**Timeline:** Apr 9 - May 20, 2026 (6 weeks)  
**Owner:** Engineering Team  
**Last Updated:** 2026-04-09

---

## Overview

Implement a unified, tool-agnostic Intermediate Representation (IR) and builder system that allows Promptosaurus to generate configurations for 5 AI tools (Kilo, Claude, Cline, Cursor, Copilot) from a single source of truth.

## Problem

Currently, agents are configured separately for each tool:
- Kilo: `.kilo/agents/` via KiloIDE builder
- Cline: `.clinerules` via ClineBuilder
- Copilot: `.github/instructions/` via CopilotBuilder
- Cursor: `.cursorrules` via CursorBuilder
- Claude: Messages API payload via ClaudeBuilder

This creates:
- Maintenance burden (changes in 5 places)
- No unified source of truth
- Inconsistent tool support
- High friction for adding new tools

## Solution

Create:
1. **Unified IR (Intermediate Representation)**
   - Tool-agnostic Agent, Skill, Workflow models
   - Auto-discovery from filesystem
   - Component-based (prompt, skills, workflow)
   - Minimal/verbose variants

2. **5 Builders** (one per tool)
   - Each reads same IR
   - Each outputs tool-specific format
   - Pluggable via factory pattern
   - Extendable for future tools

3. **Single Source of Truth**
   - `agents/{agent}/minimal/` and `agents/{agent}/verbose/`
   - No manual registration
   - Registry auto-discovery
   - Consistent experience across all tools

## Success Criteria

- ✅ All 5 builders generate correct output for their respective tools
- ✅ IR models are tool-agnostic and complete
- ✅ 85%+ test coverage on all code
- ✅ Real file I/O tests pass
- ✅ E2E scenario tests pass (IR → build all tools → validate)
- ✅ Documentation complete
- ✅ No manual registration needed (auto-discovery)

## Deliverables

### Code
- 5 builders (KiloBuilder, ClaudeBuilder, ClineBuilder, CursorBuilder, CopilotBuilder)
- IR models (Agent, Skill, Workflow, Tool, Rules, Project)
- Parser infrastructure (YAML, Markdown)
- Registry & discovery system
- Component selector & composer
- CLI tool for building

### Tests
- 32+ test files
- 85%+ code coverage
- 80%+ mutation score
- 5 E2E scenarios
- Real file I/O tests

### Documentation
- Implementation guide
- 5 builder-specific docs
- Migration guide
- API documentation
- Release notes

## Acceptance Criteria

### Functional
- [ ] IR models accurately represent agents/skills/workflows (tool-agnostic)
- [ ] Auto-discovery loads agents correctly from filesystem
- [ ] Each builder outputs valid, parseable format for its tool
- [ ] CLI tool builds all tools from single command
- [ ] Subagents generate correctly for all tools
- [ ] Component selector chooses minimal/verbose correctly
- [ ] All parser error handling works gracefully

### Quality
- [ ] Code coverage >= 85% overall
- [ ] Code coverage >= 85% on infrastructure
- [ ] Code coverage >= 85% on builders
- [ ] Mutation score >= 80% on all code
- [ ] All tests pass locally
- [ ] All tests pass in CI
- [ ] No type errors (pyright strict)
- [ ] No security issues (bandit clean)

### Performance
- [ ] Load registry (100 agents): < 2 seconds
- [ ] Build single agent (all 5 tools): < 5 seconds
- [ ] Memory usage < 500MB for full registry
- [ ] No memory leaks

### Documentation
- [ ] Implementation guide (4-5 pages)
- [ ] All 5 builder docs with examples
- [ ] Migration guide for Phase 1 → Phase 2A
- [ ] API docs generated and navigable
- [ ] CHANGELOG updated
- [ ] Release notes published

## Stories

This feature is broken down into 7 stories:

1. **Story 1: Infrastructure & Foundation** (Week 1)
   - Pydantic IR models
   - Parser infrastructure
   - Registry & discovery
   - Builder base classes
   - Component selector/composer

2. **Story 2: Kilo Builder** (Week 2)
   - KiloBuilder implementation
   - Subagent support
   - Integration tests

3. **Story 3: Cline Builder** (Week 3)
   - ClineBuilder implementation
   - Skill activation mechanism
   - Integration tests

4. **Story 4 & 5: Cloud Builders** (Week 4)
   - ClaudeBuilder (Messages API)
   - CopilotBuilder (.github/instructions/)
   - CursorBuilder (.cursorrules)
   - CLI tool for building
   - Subagent delegation

5. **Story 6: Testing & Validation** (Week 5)
   - E2E scenario tests
   - Mutation testing
   - File I/O validation
   - Coverage analysis
   - Performance testing

6. **Story 7: Documentation & Release** (Week 6)
   - Implementation guide
   - Builder documentation
   - Migration guide
   - API documentation
   - Release & communication

## Dependencies

**None.** This is a greenfield implementation on a new feature branch.

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|-----------|
| Foundation design issues block all work | Medium | High | Design review Week 1 Day 2 |
| Tool format misunderstandings | Medium | High | Research is verified (see EXECUTION_MODELS_VERIFIED.md) |
| Low mutation score | Medium | Medium | Start mutation testing Week 4 |
| Performance degradation | Low | Medium | Benchmark early and often |

## Timeline

- **Week 1**: Foundation (Apr 9-15)
- **Week 2**: Kilo Builder (Apr 16-22)
- **Week 3**: Cline Builder (Apr 23-29)
- **Week 4**: Claude/Copilot/Cursor (Apr 30-May 6)
- **Week 5**: Testing & Validation (May 7-13)
- **Week 6**: Documentation & Release (May 14-20)

**Total Effort**: 144-187 hours  
**Team Size**: 3-5 engineers

## Budget

**Estimated**: 144-187 hours  
**Cost**: ~$14,400 - $28,050 (assuming $100/hour rate)

## Next Steps

1. Assign team members to stories
2. Schedule kickoff for Apr 9
3. Daily standups (15 min)
4. Weekly reviews (Friday EOD)
5. Update execution checklist continuously

---

**Related Documents:**
- PRD: `docs/prd/PHASE2_UNIFIED_PROMPT_ARCHITECTURE.md`
- Roadmap: `docs/features/ROADMAP.md`
- Stories: `docs/features/stories/`
- Tasks: `docs/features/tasks/`
- Milestones: `docs/PHASE2A_MILESTONES.md`
- Gantt: `docs/PHASE2A_GANTT_CHART.md`
- Checklist: `PHASE2A_EXECUTION_CHECKLIST.md`

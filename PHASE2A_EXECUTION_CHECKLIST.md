# Phase 2A Execution Checklist

**Status:** Ready to Start  
**Last Updated:** 2026-04-09  
**Timeline:** Apr 9 - May 20, 2026 (6 weeks)

---

## Usage

This checklist is updated daily/weekly as work progresses. Each task can be:
- ☐ Not started
- ◐ In progress
- ✓ Complete (checked off)
- ✗ Blocked/Deferred
- ⚠️ At risk

**Update frequency:** At end of each day or at minimum weekly (Friday EOD)

---

## MILESTONE 1: Foundation (Week 1: Apr 9-15)

### Task 1.1: Create Pydantic IR Models
- [ ] Agent model created with all fields
- [ ] Skill model created with all fields
- [ ] Workflow model created with all fields
- [ ] Tool model created with all fields
- [ ] Rules model created with all fields
- [ ] Project model created with all fields
- [ ] All models have full type hints
- [ ] All models have docstrings
- [ ] Validation logic implemented
- [ ] Unit tests written (100% coverage)
- [ ] Tests passing locally
- [ ] pyright strict mode passing
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 10

### Task 1.2: Create Parser Infrastructure
- [ ] YAMLParser class created
- [ ] MarkdownParser class created
- [ ] ComponentLoader class created
- [ ] SkillParser class created
- [ ] WorkflowParser class created
- [ ] Error handling with descriptive messages
- [ ] Support for optional components
- [ ] Unit tests written (85%+ coverage)
- [ ] Integration tests written
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 11

### Task 1.3: Create Registry & Discovery System
- [ ] RegistryDiscovery class created
- [ ] Discovers agents with variants
- [ ] Discovers subagents
- [ ] Auto-loads prompt.md, skills.md, workflow.md
- [ ] Validates required files
- [ ] Returns dict of Agent IR models
- [ ] Handles missing optional files
- [ ] Registry caching implemented
- [ ] Unit tests written (85%+ coverage)
- [ ] Integration tests written
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 12

### Task 1.4: Create Builder Base Classes & Interfaces
- [ ] AbstractBuilder base class created
- [ ] build() method signature defined
- [ ] validate() method implemented
- [ ] Mixin interfaces created (SupportsSkills, etc.)
- [ ] Builder registry created
- [ ] BuilderFactory created
- [ ] Error handling implemented
- [ ] Documentation written
- [ ] Unit tests written (85%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 12

### Task 1.5: Create Component Selector & Composer
- [ ] ComponentSelector class created
- [ ] Chooses minimal/verbose correctly
- [ ] Loads all three components
- [ ] Falls back gracefully
- [ ] ComponentComposer class created
- [ ] Handles component ordering
- [ ] Handles missing optional components
- [ ] Unit tests written (90%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 13

### Task 1.6: Unit Tests for Infrastructure
- [ ] All models tested (happy path + edge cases)
- [ ] All parsers tested with valid/invalid inputs
- [ ] Registry discovery tested
- [ ] Builder base classes tested
- [ ] Component selector tested for all variants
- [ ] Error cases tested
- [ ] Total coverage: 85%+ on infrastructure
- [ ] All tests pass locally
- [ ] Tests pass in CI
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 15

### Milestone 1 Gate
- [ ] All 6 tasks complete
- [ ] All tests passing (local + CI)
- [ ] All PRs reviewed and merged
- [ ] No type errors (pyright)
- [ ] Coverage >= 85%
- [ ] Ready for Story 2-5 work

**Status:** ☐ Not Started  
**Target:** Apr 15 EOD

---

## MILESTONE 2: Kilo Builder (Week 2: Apr 16-22)

### Task 2.1: Implement KiloBuilder Class
- [ ] KiloBuilder class created
- [ ] Extends AbstractBuilder
- [ ] build() method outputs string
- [ ] YAML frontmatter generated
- [ ] System Prompt section added
- [ ] Tools section added
- [ ] Skills section added
- [ ] Workflows section added
- [ ] Subagents section added
- [ ] Proper markdown formatting
- [ ] validate() implemented
- [ ] Unit tests written (90%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 17

### Task 2.2: Implement Subagent Support for Kilo
- [ ] Subagent detection implemented
- [ ] Subagent files generated
- [ ] Parent references included
- [ ] Proper nesting in output
- [ ] Subagent discovery working
- [ ] Unit tests written (85%+ coverage)
- [ ] Integration tests written
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 18

### Task 2.3: Integration Tests for Kilo Builder
- [ ] Load IR model test
- [ ] Build Kilo output test
- [ ] Write files to temp directory test
- [ ] Verify files are readable by Kilo
- [ ] Verify YAML frontmatter valid
- [ ] Verify markdown formatting
- [ ] Test with different variants
- [ ] All tests passing
- [ ] Coverage >= 85%
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 22

### Milestone 2 Gate
- [ ] All 3 tasks complete
- [ ] All tests passing (local + CI)
- [ ] KiloBuilder generating valid output
- [ ] All PRs reviewed and merged
- [ ] Coverage >= 85%
- [ ] Ready for Story 3 work

**Status:** ☐ Not Started  
**Target:** Apr 22 EOD

---

## MILESTONE 3: Cline Builder (Week 3: Apr 23-29)

### Task 3.1: Implement ClineBuilder Class
- [ ] ClineBuilder class created
- [ ] Extends AbstractBuilder
- [ ] build() method outputs string
- [ ] Header section generated
- [ ] System prompt as prose
- [ ] Tools section added
- [ ] Skills section added
- [ ] Skill invocation included
- [ ] Workflows section added
- [ ] Subagents section added
- [ ] All sections concatenated
- [ ] Proper markdown formatting
- [ ] Unit tests written (90%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 24

### Task 3.2: Implement Skill Activation for Cline
- [ ] Skill activation instructions added
- [ ] use_skill invocation format correct
- [ ] When to use instructions clear
- [ ] Links to skill documentation
- [ ] Subagent delegation using activation
- [ ] Skill dependencies handled
- [ ] Unit tests written (85%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 25

### Task 3.3: Integration Tests for Cline Builder
- [ ] Load IR model test
- [ ] Build Cline output test
- [ ] Write `.clinerules` to temp test
- [ ] Verify file readable by Cline
- [ ] Verify markdown syntax valid
- [ ] Verify skill invocation syntax
- [ ] Test with different agents/variants
- [ ] All tests passing
- [ ] Coverage >= 85%
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 29

### Milestone 3 Gate
- [ ] All 3 tasks complete
- [ ] All tests passing (local + CI)
- [ ] ClineBuilder generating valid output
- [ ] All PRs reviewed and merged
- [ ] Coverage >= 85%
- [ ] Ready for Story 4-5 work

**Status:** ☐ Not Started  
**Target:** Apr 29 EOD

---

## MILESTONE 4: Claude & Copilot Builders (Week 4: Apr 30-May 6)

### Task 4.1: Implement ClaudeBuilder Class
- [ ] ClaudeBuilder class created
- [ ] Extends AbstractBuilder
- [ ] build() method outputs dict
- [ ] "system" field generated
- [ ] "tools" array generated
- [ ] Tool schemas valid
- [ ] "instructions" section added
- [ ] Skills descriptions added
- [ ] Workflows descriptions added
- [ ] Output is valid JSON
- [ ] Compatible with Claude API
- [ ] Unit tests written (90%+ coverage)
- [ ] JSON validation tests
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 1

### Task 4.2: Implement Claude Subagent Delegation
- [ ] Subagent mapping created
- [ ] Each subagent gets system_prompt
- [ ] Each subagent gets tools + skills
- [ ] Subagent config in output
- [ ] Delegation instructions clear
- [ ] Unit tests written (85%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 1

### Task 4.3: Implement CopilotBuilder Class
- [ ] CopilotBuilder class created
- [ ] Extends AbstractBuilder
- [ ] build() method outputs dict
- [ ] Main agent file generated
- [ ] YAML frontmatter added
- [ ] System Prompt section added
- [ ] Skills section added
- [ ] Workflows section added
- [ ] Subagents section added
- [ ] Tools & Permissions section added
- [ ] Subagent files created
- [ ] Parent references included
- [ ] Output format valid
- [ ] Unit tests written (90%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 3

### Task 4.4: Integration Tests for Claude & Copilot
- [ ] Load IR, build Claude test
- [ ] Claude payload valid JSON test
- [ ] Claude schema matches API test
- [ ] Build Copilot instructions test
- [ ] Write Copilot files to temp test
- [ ] Copilot YAML frontmatter valid test
- [ ] Copilot files readable test
- [ ] Build with subagents test
- [ ] All tests passing
- [ ] Coverage >= 85%
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 4

### Task 4.5: Implement CLI Tool for Building
- [ ] CLI command `prompt-build --tool` created
- [ ] CLI command `--tool kilo` working
- [ ] CLI command `--tool claude` working
- [ ] CLI command `--tool cline` working
- [ ] CLI command `--tool copilot` working
- [ ] CLI command `--all` working
- [ ] `--variant minimal` supported
- [ ] `--variant verbose` supported
- [ ] `--agent {name}` supported
- [ ] Output validation working
- [ ] Success/failure reporting
- [ ] Help text complete
- [ ] Error messages descriptive
- [ ] Unit tests for args parsing
- [ ] Integration tests for full workflow
- [ ] Tests passing locally
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 5

### Task 5.1: Implement CursorBuilder Class (Partial)
- [ ] CursorBuilder class created
- [ ] Extends AbstractBuilder
- [ ] build() method outputs string
- [ ] Header section generated
- [ ] System prompt as prose
- [ ] Skills section added
- [ ] Workflows section added
- [ ] Tools Available section added
- [ ] Single concatenated file
- [ ] Proper markdown formatting
- [ ] Unit tests written (90%+ coverage)
- [ ] Tests passing locally
- [ ] Code review completed (80%+)
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 6

### Milestone 4 Gate
- [ ] All 5 tasks complete
- [ ] All tests passing (local + CI)
- [ ] All builders generating valid output
- [ ] CLI tool working for all builders
- [ ] CursorBuilder at 80%+ complete
- [ ] All PRs reviewed and merged
- [ ] Coverage >= 85%
- [ ] Ready for Story 6 work

**Status:** ☐ Not Started  
**Target:** May 6 EOD

---

## MILESTONE 5: Testing & Validation (Week 5: May 7-13)

### Task 5.2: Complete Cursor Builder
- [ ] CursorBuilder complete (100%)
- [ ] All sections implemented
- [ ] Unit tests updated (90%+ coverage)
- [ ] Integration tests complete
- [ ] Tests passing locally
- [ ] Output verified as valid
- [ ] Code review completed
- [ ] Merged to main

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 8

### Task 6.1: E2E Scenario Tests
- [ ] Scenario 1: code agent → all 5 tools → validate
- [ ] Scenario 2: architect agent → all 5 tools → validate
- [ ] Scenario 3: agent with subagents → all tools
- [ ] Scenario 4: minimal variant → token reduction verify
- [ ] Scenario 5: verbose variant → completeness verify
- [ ] All scenarios passing
- [ ] Real filesystem I/O (no mocks)
- [ ] Timing benchmarks recorded
- [ ] All benchmarks < 5s per agent
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 9

### Task 6.2: Mutation Testing
- [ ] mutmut installed and configured
- [ ] Mutation tests on infrastructure
- [ ] Mutation tests on all builders
- [ ] Infrastructure mutation score >= 80%
- [ ] Builders mutation score >= 80%
- [ ] Weak tests identified
- [ ] Additional tests added
- [ ] Report generated and reviewed
- [ ] All tests passing
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 11

### Task 6.3: Real File I/O Validation
- [ ] Build all tools to temp directories
- [ ] All output files created
- [ ] Files readable by target tool
- [ ] YAML/JSON syntax valid
- [ ] Markdown syntax correct
- [ ] File permissions tested
- [ ] Various filesystem permissions tested
- [ ] No file I/O errors
- [ ] All tests passing
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 12

### Task 6.4: Coverage Analysis & Gaps
- [ ] Coverage report generated
- [ ] Overall coverage: 85%+
- [ ] Infrastructure coverage: 85%+
- [ ] Builder coverage: 85%+
- [ ] Parser coverage: 85%+
- [ ] Uncovered paths identified
- [ ] Tests added for gaps
- [ ] Final coverage report: 85%+
- [ ] All tests passing
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 13

### Task 6.5: Performance & Load Testing
- [ ] Load 100 agents: < 2 seconds
- [ ] Build single agent (all 5 tools): < 5 seconds
- [ ] Build all agents (all 5 tools): < 60 seconds
- [ ] Memory usage < 500MB
- [ ] No memory leaks
- [ ] Performance benchmarks documented
- [ ] All tests passing
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 13

### Milestone 5 Gate
- [ ] All 6 tasks complete
- [ ] All E2E scenarios passing
- [ ] Mutation score >= 80%
- [ ] Coverage >= 85%
- [ ] File I/O validation complete
- [ ] Performance targets met
- [ ] All tests passing (local + CI)
- [ ] All PRs reviewed and merged
- [ ] Ready for Story 7 work

**Status:** ☐ Not Started  
**Target:** May 13 EOD

---

## MILESTONE 6: Documentation & Release (Week 6: May 14-20)

### Task 7.1: Implementation Guide
- [ ] IR models section written
- [ ] How to add new builder section written
- [ ] Parsers section written
- [ ] Registry discovery section written
- [ ] Component selector/composer section written
- [ ] Builder factory section written
- [ ] File I/O patterns section written
- [ ] Testing patterns section written
- [ ] Code examples included
- [ ] Guide is 4-5 pages
- [ ] Spell-checked
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** Apr 15

### Task 7.2: Builder Documentation
- [ ] KiloBuilder docs complete with examples
- [ ] ClaudeBuilder docs complete with examples
- [ ] ClineBuilder docs complete with examples
- [ ] CopilotBuilder docs complete with examples
- [ ] CursorBuilder docs complete with examples
- [ ] Each doc includes configuration options
- [ ] Each doc has troubleshooting section
- [ ] All docs spell-checked
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 17

### Task 7.3: Migration Guide
- [ ] Phase 2A changes documented
- [ ] How to update agent configs documented
- [ ] Migration from kilo_modes.yaml documented
- [ ] Breaking changes documented
- [ ] Backward compatibility notes documented
- [ ] Migration testing documented
- [ ] Migration script documented (if needed)
- [ ] FAQ with common questions
- [ ] Spell-checked
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 18

### Task 7.4: API Documentation
- [ ] All public classes have docstrings
- [ ] All public methods have docstrings
- [ ] HTML API docs generated (pdoc)
- [ ] API docs readable and navigable
- [ ] Examples included
- [ ] API docs published to docs/api/
- [ ] Links verified
- [ ] Code review completed

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 19

### Task 7.5: Release & Communication
- [ ] Version bumped
- [ ] CHANGELOG updated with all changes
- [ ] Release notes written
- [ ] All documentation reviewed
- [ ] All PRs reviewed and merged
- [ ] Release branch created
- [ ] Release tag created
- [ ] Release announcement written
- [ ] Stakeholders notified
- [ ] Documentation published

**Owner:** TBD  
**Status:** ☐ Not Started  
**Est. Complete:** May 20

### Milestone 6 Gate
- [ ] All 5 tasks complete
- [ ] All documentation reviewed
- [ ] CHANGELOG complete
- [ ] Release notes approved
- [ ] Version bumped
- [ ] Release branch created
- [ ] Release tag created
- [ ] Release published
- [ ] Stakeholders notified

**Status:** ☐ Not Started  
**Target:** May 20 EOD

---

## Final Gate: Phase 2A Complete

- [ ] Milestone 1 complete (Foundation)
- [ ] Milestone 2 complete (Kilo)
- [ ] Milestone 3 complete (Cline)
- [ ] Milestone 4 complete (Claude/Copilot/Cursor)
- [ ] Milestone 5 complete (Testing)
- [ ] Milestone 6 complete (Documentation & Release)
- [ ] All 32 tasks with acceptance criteria met
- [ ] 85%+ code coverage achieved
- [ ] All E2E scenarios passing
- [ ] Mutation score >= 80%
- [ ] All builders generating valid tool-specific output
- [ ] Documentation complete and reviewed
- [ ] Release published and communicated
- [ ] Stakeholders satisfied

**Status:** ☐ Not Started  
**Target:** May 20, 2026 EOD

---

## Weekly Status Reports

### Week 1 (Apr 9-15): Foundation
**Reporting Date:** Apr 15  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 1.1
- [ ] Task 1.2
- [ ] Task 1.3
- [ ] Task 1.4
- [ ] Task 1.5
- [ ] Task 1.6

Blockers:
- (None reported)

Risks:
- (None reported)

Next Week Plans:
- Start Kilo Builder (Story 2)
- Continue Cline design (Story 3)

Notes:
- (To be filled in)

---

### Week 2 (Apr 16-22): Kilo Builder
**Reporting Date:** Apr 22  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 2.1
- [ ] Task 2.2
- [ ] Task 2.3

Blockers:
- (None reported)

Risks:
- (None reported)

Next Week Plans:
- Complete Cline Builder (Story 3)
- Begin Claude/Copilot design (Story 4-5)

Notes:
- (To be filled in)

---

### Week 3 (Apr 23-29): Cline Builder
**Reporting Date:** Apr 29  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 3.1
- [ ] Task 3.2
- [ ] Task 3.3

Blockers:
- (None reported)

Risks:
- (None reported)

Next Week Plans:
- Complete Claude/Copilot/Cursor builders (Story 4-5)
- Implement CLI tool
- Begin testing prep

Notes:
- (To be filled in)

---

### Week 4 (Apr 30-May 6): Claude, Copilot, Cursor
**Reporting Date:** May 6  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 4.1
- [ ] Task 4.2
- [ ] Task 4.3
- [ ] Task 4.4
- [ ] Task 4.5
- [ ] Task 5.1 (partial)

Blockers:
- (None reported)

Risks:
- (None reported)

Next Week Plans:
- Complete Cursor Builder (Story 5, Task 5.2)
- Comprehensive testing (Story 6)
- Begin documentation draft

Notes:
- (To be filled in)

---

### Week 5 (May 7-13): Testing & Validation
**Reporting Date:** May 13  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 5.2
- [ ] Task 6.1
- [ ] Task 6.2
- [ ] Task 6.3
- [ ] Task 6.4
- [ ] Task 6.5

Blockers:
- (None reported)

Risks:
- (None reported)

Next Week Plans:
- Complete documentation (Story 7)
- Finalize release

Notes:
- (To be filled in)

---

### Week 6 (May 14-20): Documentation & Release
**Reporting Date:** May 20  
**Status:** ☐ Not Started

Tasks Completed This Week:
- [ ] Task 7.1
- [ ] Task 7.2
- [ ] Task 7.3
- [ ] Task 7.4
- [ ] Task 7.5

Blockers:
- (None reported)

Risks:
- (None reported)

Completed:
- ✓ Phase 2A Complete
- ✓ Release Published
- ✓ Documentation Live
- ✓ Stakeholders Notified

Notes:
- (To be filled in)

---

## Legend

- ☐ Not started
- ◐ In progress
- ✓ Complete
- ✗ Blocked/Deferred
- ⚠️ At risk

---


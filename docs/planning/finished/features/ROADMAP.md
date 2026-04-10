# Phase 2A Roadmap

**Timeline:** Apr 9 - May 20, 2026 (6 weeks)  
**Status:** Planning  
**Team Size:** 3-5 engineers

---

## Overview

Phase 2A implementation follows a sequential story-driven approach with parallelization opportunities after foundational work completes.

```
Week 1: Foundation (critical path)
  └─→ Week 2: Kilo (parallel with Week 3)
  └─→ Week 3: Cline (parallel with Week 2)
  └─→ Week 4: Claude/Copilot/Cursor (parallel development)
  └─→ Week 5: Testing & Validation (all builders must be complete)
  └─→ Week 6: Documentation & Release
```

## Story Timeline

| # | Story | Week | Status | Dependencies |
|---|-------|------|--------|--------------|
| 1 | Infrastructure & Foundation | 1 | Ready | None (critical) |
| 2 | Kilo Builder | 2 | Ready | Story 1 ✓ |
| 3 | Cline Builder | 3 | Ready | Story 1 ✓ |
| 4 & 5 | Claude, Copilot, Cursor | 4 | Ready | Story 1 ✓ |
| 6 | Testing & Validation | 5 | Ready | Stories 2-5 ✓ |
| 7 | Documentation & Release | 6 | Ready | Story 6 ✓ |

## Weekly Breakdown

### Week 1 (Apr 9-15): Foundation
**Theme:** Build the core infrastructure

**Tasks:** 1.1 - 1.6  
**Deliverables:**
- IR models (6 models)
- Parser infrastructure (5 parsers)
- Registry & discovery
- Builder base classes & interfaces
- Component selector & composer
- Unit tests (85%+ coverage)

**Owner:** Core Infrastructure Team (1-2 engineers)  
**Effort:** 28-35 hours  
**Gate:** All tasks complete, 85%+ coverage, code review approved

### Week 2 (Apr 16-22): Kilo Builder
**Theme:** First concrete builder implementation

**Tasks:** 2.1 - 2.3  
**Deliverables:**
- KiloBuilder class
- Subagent support
- Integration tests
- Example output files

**Owner:** Kilo Specialization Team (1 engineer)  
**Effort:** 15-20 hours  
**Gate:** KiloBuilder working, tests passing, code review approved

### Week 3 (Apr 23-29): Cline Builder
**Theme:** Second builder, continues pattern

**Tasks:** 3.1 - 3.3  
**Deliverables:**
- ClineBuilder class
- Skill activation mechanism
- Integration tests
- Example output files

**Owner:** Cline Specialization Team (1 engineer)  
**Effort:** 15-20 hours  
**Gate:** ClineBuilder working, tests passing, code review approved

### Week 4 (Apr 30-May 6): Cloud Builders
**Theme:** Three builders + CLI (parallel work)

**Tasks:** 4.1 - 4.5, 5.1  
**Deliverables:**
- ClaudeBuilder (JSON for Messages API)
- CopilotBuilder (.github/instructions/)
- CursorBuilder (.cursorrules) - 80%+ complete
- CLI tool (prompt-build command)
- Integration tests

**Owner:** Cloud Specialization Team (2 engineers)  
**Effort:** 35-45 hours  
**Gate:** All builders working, CLI functional, tests passing

### Week 5 (May 7-13): Testing & Validation
**Theme:** Comprehensive testing and finalization

**Tasks:** 5.2, 6.1 - 6.5  
**Deliverables:**
- CursorBuilder complete (100%)
- 5 E2E scenario tests
- Mutation test report (score >= 80%)
- Coverage analysis (85%+)
- File I/O validation
- Performance benchmarks

**Owner:** QA & Testing Team (2 engineers)  
**Effort:** 33-41 hours  
**Gate:** All tests passing, 85%+ coverage, 80%+ mutation score

### Week 6 (May 14-20): Documentation & Release
**Theme:** Complete all documentation and ship Phase 2A

**Tasks:** 7.1 - 7.5  
**Deliverables:**
- Implementation guide (4-5 pages)
- 5 builder-specific docs
- Migration guide
- API documentation
- Release notes & CHANGELOG

**Owner:** Documentation & Release Team (2 engineers)  
**Effort:** 18-26 hours  
**Gate:** Documentation reviewed, version bumped, release published

## Parallelization Strategy

### Sequential (No Parallelization)
- **Story 1 → Everything else**: Foundation is blocking

### Parallel After Week 1
- **Stories 2 & 3** can work simultaneously (Kilo & Cline)
- **Story 4-5** can start while Stories 2-3 finishing

### Parallel in Week 4
- **ClaudeBuilder, CopilotBuilder, CursorBuilder** developed by different engineers
- **CLI tool** developed alongside builders

### Parallel in Week 5
- **E2E tests, mutation tests, file I/O tests** run independently
- **Documentation drafting** can start in parallel

## Resource Allocation

```
Week 1: 1-2 FTE (Foundation)
Week 2: 1 FTE (Kilo) + code review
Week 3: 1 FTE (Cline) + code review
Week 4: 2 FTE (Claude, Copilot, Cursor) + code review
Week 5: 2 FTE (Testing) + code review
Week 6: 2 FTE (Documentation) + release manager

Total: 3-5 concurrent engineers
Total Hours: 144-187
Average Per Week: 24-31 hours per engineer
```

## Critical Path

```
Story 1 (Week 1) [ZERO SLACK]
  ↓
Story 4-5 (Week 4) [Can run in parallel with 2-3]
  ↓
Story 6 (Week 5) [Depends on builders]
  ↓
Story 7 (Week 6) [Depends on testing]
  ↓
Release (Week 6 EOD)

Float/Slack:
- Stories 2-3: ~1 week (can slip without affecting finish)
- Story 1: ZERO slack (critical)
- Story 6-7: Critical (drive release)
```

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| All 5 builders complete | Week 4 EOD | On track |
| 85%+ code coverage | Week 5 | On track |
| 80%+ mutation score | Week 5 | On track |
| 5 E2E scenarios pass | Week 5 | On track |
| Performance < 5s/agent | Week 5 | On track |
| Documentation complete | Week 6 | On track |
| Release published | Week 6 EOD | On track |

## Risk Mitigation

| Week | Risk | Mitigation |
|------|------|-----------|
| 1 | Design issues block all | Design review Day 2 |
| 4 | Multiple builders in parallel | Daily standups, clear interfaces |
| 5 | Low test quality | Mutation testing + coverage analysis |
| 6 | Documentation delays | Draft docs in Week 5 |

## Tracking & Reporting

**Daily:** Standup (15 min)
- Progress against tasks
- Blockers identified
- Plan adjustments

**Weekly:** Milestone review (Friday EOD)
- Actual vs planned progress
- Risk assessment
- Checklist update

**Bi-weekly:** Executive status (optional)
- High-level progress
- Budget/timeline impact
- Stakeholder communication

---

## Documents

- **Feature Overview**: `FEATURE_001_unified_prompt_architecture.md`
- **Stories**: `stories/` directory
- **Tasks**: `tasks/` directory
- **Milestones**: `../PHASE2A_MILESTONES.md`
- **Gantt Chart**: `../PHASE2A_GANTT_CHART.md`
- **Execution Checklist**: `../../PHASE2A_EXECUTION_CHECKLIST.md`

---

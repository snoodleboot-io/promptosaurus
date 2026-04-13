# Documentation Accuracy Audit - Issue Tracker

**Branch:** bugfix/DOC-001-documentation-accuracy-audit  
**Date:** 2026-04-13  
**Auditor:** Orchestrator Agent

---

## Executive Summary

Systematic audit of docs/ directory revealed multiple categories of inaccuracies:
- **Phase references** (implementation artifacts - should be removed)
- **Hallucinated agent names** (non-existent agents/paths)
- **CLI naming errors** (incorrect command names)
- **Outdated content** (references to removed/non-existent files)

---

## Issue Categories

### ✅ VERIFIED CORRECT
1. **Macros exist and are used** - `promptosaurus/prompts/macros/` contains 11 Jinja2 template files used by the template rendering system
2. **qa-tester agent exists** - Located at `promptosaurus/agents/qa-tester/` with subagents for unit-testing, integration-testing, load-testing

### 🔴 CRITICAL ISSUES

#### 1. Phase References (Remove All)
**Severity:** CRITICAL  
**Impact:** Implementation artifacts leak into user-facing docs

**Affected Files:**
- `docs/INDEX.md` - "Active phase plans" reference
- `docs/LIBRARY_INDEX.md` - Multiple "Phase 1", "Phase 2" sections
- `docs/PERSONA_GUIDES.md` - References to `PHASE*_EXECUTION_GUIDE.plan.md`
- `docs/QUALITY_METRICS.md` - "PHASE 2 COMPLETE" status, multiple phase breakdowns
- `docs/RELATIONSHIPS_MATRIX.md` - "(Phase 1)" annotations

**Fix:** Remove all "Phase N" references. These are internal development milestones, not user concepts.

#### 2. Hallucinated Agent Names and Paths
**Severity:** CRITICAL  
**Impact:** Users can't find referenced files/agents

**File:** `docs/PERSONA_GUIDES.md`

**Incorrect References:**
- Line 33: `promptosaurus/agents/backend-engineer/` → **WRONG** (actual: `promptosaurus/agents/backend/`)
- Line 62: `promptosaurus/agents/frontend-engineer/` → **WRONG** (actual: `promptosaurus/agents/frontend/`)
- Line 90: `promptosaurus/agents/devops-engineer/` → **WRONG** (actual: `promptosaurus/agents/devops/`)
- Line 118: `promptosaurus/agents/testing-engineer/` → **WRONG** (actual: `promptosaurus/agents/qa-tester/`)

**Hallucinated Agent Names:**
- "Backend Engineer" → actual agent is "backend"
- "Database Engineer" → NOT AN AGENT (is this data agent? or a hallucination?)
- "Performance Engineer" → actual agent is "performance"
- "Testing Engineer" → actual agent is "qa-tester"
- "Frontend Engineer" → actual agent is "frontend"
- "UI/UX Specialist" → NOT AN AGENT (completely hallucinated)
- "Incident Response Engineer" → actual agent is "incident"
- "Observability Engineer" → actual agent is "observability"

**Actual Agents (verified):**
```
architect, ask, backend, code, compliance, data, debug, devops, document, 
enforcement, explain, frontend, incident, migration, mlai, observability, 
orchestrator, performance, plan, product, qa-tester, refactor, review, 
security, test
```

#### 3. CLI Command Name
**Severity:** HIGH  
**Impact:** Users try wrong commands

**Correct CLI Name:** `promptosaurus` (confirmed in pyproject.toml line 48)

**Search Results:** No incorrect "prompt build" or "prompt init" references found in docs/*.md (GOOD!)
**Status:** ✅ VERIFIED CLEAN

---

### ⚠️ HIGH PRIORITY ISSUES

#### 4. MAINTENANCE_WORKFLOW.md - Questionable Value
**File:** `docs/MAINTENANCE_WORKFLOW.md` (723 lines)

**Issues:**
- References validation scripts that may not exist (`python validation/run_validation.py`)
- Describes complex validation framework that may be aspirational
- Heavy on process, light on actual utility

**Recommendation:** User says "we do not need maintenance workflow" - **REMOVE FILE**

#### 5. MIGRATION_GUIDE.md - Premature
**File:** `docs/MIGRATION_GUIDE.md` (316 lines)

**Issues:**
- Current version is 0.1.0 (initial release)
- No prior versions to migrate from
- Mostly placeholder content
- Describes future migration scenarios that don't exist yet

**Recommendation:** User says "we do not need migration guide" - **REMOVE FILE**

---

### ⚠️ MEDIUM PRIORITY ISSUES

#### 6. QUALITY_METRICS.md - Accuracy Unknown
**File:** `docs/QUALITY_METRICS.md`

**Claims to Verify:**
- "64.3% code coverage" - Is this current?
- "1,316 automated tests" - Accurate count?
- "98.3% pass rate" - Current status?
- "9 agents" - Incorrect (actual: 25 agents based on ls output)
- "41 subagents" - Need to verify
- "28 workflows" - Need to verify
- "38 skills" - Need to verify

**Action Required:** Run actual test coverage and verify all metrics

#### 7. RELATIONSHIPS_MATRIX.md - Verify Mappings
**File:** `docs/RELATIONSHIPS_MATRIX.md`

**Potential Issues:**
- Agent → Subagent mappings may be outdated
- Workflow → Agent mappings need verification
- Skill references may not exist

**Action Required:** Cross-reference with actual agent/subagent/workflow/skill files

#### 8. PERSONA_GUIDES.md - Multiple Issues Beyond Agent Names
**File:** `docs/PERSONA_GUIDES.md`

**Issues:**
- References to `PHASE*_EXECUTION_GUIDE.plan.md` files (lines 17, 236, 238)
- References to `PHASE2_EXECUTION_STATUS.plan.md` (line 240)
- Claims about "Backend Engineer", "Frontend Engineer" personas that don't match reality
- Workflow names may not match actual workflow files

**Action Required:** Complete rewrite based on actual personas.yaml and agent structure

---

### 📋 LOW PRIORITY / TO INVESTIGATE

#### 9. Language Discovery Issue
**Status:** Unknown  
**Action:** Search for references to language discovery problems

#### 10. "Removed Development Artifacts" Documentation
**Status:** Unknown  
**User says:** "pointless"  
**Action:** Find and evaluate

#### 11. Testing Violations
**User says:** "broken testing violations??"  
**Action:** Find what this refers to and verify

---

## Verification Steps

### Completed ✅
1. Macro usage - VERIFIED: macros exist and are used via Jinja2
2. qa-tester existence - VERIFIED: exists at `promptosaurus/agents/qa-tester/`
3. CLI name - VERIFIED: `promptosaurus` (no incorrect "prompt" usage found)

### In Progress 🔄
4. Finding all Phase references
5. Documenting hallucinated agent names

### Pending ⏳
6. Count actual agents/subagents/workflows/skills
7. Verify QUALITY_METRICS.md claims
8. Verify RELATIONSHIPS_MATRIX.md mappings
9. Test coverage actual vs documented
10. Find "language discovery" issue
11. Find "removed development artifacts" docs
12. Find "testing violations" references

---

## Next Steps

1. **Remove files:**
   - `docs/MAINTENANCE_WORKFLOW.md`
   - `docs/MIGRATION_GUIDE.md`

2. **Major rewrites needed:**
   - `docs/PERSONA_GUIDES.md` - completely hallucinated
   - `docs/QUALITY_METRICS.md` - verify all claims, remove Phase refs
   - `docs/RELATIONSHIPS_MATRIX.md` - verify all mappings

3. **Phase reference cleanup:**
   - `docs/INDEX.md`
   - `docs/LIBRARY_INDEX.md`
   - All other files with Phase mentions

4. **Systematic review remaining files:**
   - Review all docs/ subdirectories
   - Check architecture/, builders/, components/, design/, developer-guide/, misc/, reference/, user-guide/

---

## Actual Agent Count

```bash
$ ls -1 promptosaurus/agents/ | grep -v __pycache__ | grep -v core | wc -l
25
```

**Actual count: 25 primary agents**, NOT 9 as claimed in QUALITY_METRICS.md


---

## UPDATED FINDINGS (2026-04-13 15:30)

### Actual Component Counts (Verified)

```bash
Primary Agents: 25
Subagents: 82
Workflows: 100  
Skills: 108
```

**QUALITY_METRICS.md Claims vs Reality:**

| Component | Documented | Actual | Status |
|-----------|------------|--------|--------|
| Agents | 9 | **25** | ❌ WRONG (off by 16!) |
| Subagents | 41 | **82** | ❌ WRONG (off by 41!) |
| Workflows | 28 | **100** | ❌ WRONG (off by 72!) |
| Skills | 38 | **108** | ❌ WRONG (off by 70!) |

**Conclusion:** QUALITY_METRICS.md is massively outdated and inaccurate.

---

### Issue #11: Testing Violations ARE REAL

**File:** `docs/TEST_CONVENTIONS.md`

**Current violations listed:**
```
❌ promptosaurus/ui/_selector.py           → No tests/unit/ui/test_selector.py
❌ promptosaurus/ui/input/unix.py          → No tests/unit/ui/input/test_unix.py
❌ promptosaurus/ui/input/windows.py       → No tests/unit/ui/input/test_windows.py
❌ promptosaurus/ui/pipeline/orchestrator.py → No tests/unit/ui/pipeline/test_orchestrator.py
❌ promptosaurus/registry.py               → tests/unit/registry/ exists but incomplete
```

**BUT REALITY:**
```bash
$ pytest --collect-only
!!!!!!!!!!!!!!!!!!! Interrupted: 63 errors during collection !!!!!!!!!!!!!!!!!!!
=================== 292 tests collected, 63 errors in 1.32s ====================
```

**Status:** BROKEN - 63 test collection errors exist, but TEST_CONVENTIONS.md only documents 5 violations

**User is correct:** Testing violations documentation is incomplete/broken

---

### Issue #10: "Development Artifacts" Reference

**File:** `docs/INDEX.md` line 47

**Text:** "Note: Planning directory contains AI-generated and internal development artifacts. This documentation (docs/) is user-facing."

**User says:** "pointless"

**Analysis:** This is actually useful context - it clarifies that planning/ is internal vs docs/ is user-facing. Not hallucinated.

**Recommendation:** KEEP (user may disagree, but it's not inaccurate)

---

### Issue #9: Language Discovery - NOT FOUND

**Status:** No references to "language discovery" issue found in docs/

**Conclusion:** May be referring to code, not docs. Or already fixed.

---

## Summary of Required Actions

### 🗑️ DELETE FILES (2 files)
1. `docs/MAINTENANCE_WORKFLOW.md` - 723 lines of aspirational/unnecessary content
2. `docs/MIGRATION_GUIDE.md` - 316 lines premature for v0.1.0

### ✏️ COMPLETE REWRITES (3 files)
1. `docs/QUALITY_METRICS.md` - All counts wrong, Phase references throughout
2. `docs/PERSONA_GUIDES.md` - Hallucinated agent names/paths, Phase references
3. `docs/RELATIONSHIPS_MATRIX.md` - Needs verification against actual components

### 🔧 MAJOR EDITS (Phase Reference Removal)
1. `docs/INDEX.md` - Remove "Active phase plans" reference (line 42)
2. `docs/LIBRARY_INDEX.md` - Remove all Phase 1/Phase 2 sections

### 📝 VERIFY & UPDATE
1. `docs/TEST_CONVENTIONS.md` - Update violations list (currently lists 5, actual 63 errors)
2. All docs/subdirectories - Need systematic review

---

## Files NOT YET REVIEWED

### Top-level docs/
- [ ] ADVANCED_CONFIGURATION.md
- [ ] ARCHITECTURE.md
- [ ] DIAGRAMS_GUIDE.md
- [ ] INTEGRATION_GUIDES.md
- [ ] INTERACTIVE_WALKTHROUGH.md
- [ ] README.md
- [ ] TECHNICAL_DEBT.md
- [ ] TEMPLATE_SYSTEM.md
- [ ] TROUBLESHOOTING.md

### Subdirectories (need recursive review)
- [ ] docs/architecture/
- [ ] docs/builders/
- [ ] docs/components/
- [ ] docs/decisions/
- [ ] docs/design/
- [ ] docs/developer-guide/
- [ ] docs/misc/
- [ ] docs/reference/
- [ ] docs/user-guide/

**Next:** Systematic review of all remaining files


---

## ADDITIONAL CLEANUP (April 13, 2026 16:35)

### User Feedback: Development Docs Should Not Be in docs/

**Issue:** docs/ directory contained internal development documentation instead of user-facing content.

**Files Removed (3 additional):**
1. **docs/TEST_CONVENTIONS.md** - Internal testing standards for developers
2. **docs/TECHNICAL_DEBT.md** - Internal technical debt tracking
3. **docs/QUALITY_METRICS.md** - Internal quality/coverage metrics

**Rationale:**
- docs/ is for USER-FACING documentation (how to use Promptosaurus)
- Development standards, testing conventions, and internal metrics belong elsewhere (or not at all)
- Users don't need to know about internal test coverage or technical debt

**Total Files Removed:** 5 files (including MAINTENANCE_WORKFLOW.md and MIGRATION_GUIDE.md)

**References Cleaned:**
- docs/INDEX.md
- docs/LIBRARY_INDEX.md
- docs/PERSONA_GUIDES.md
- docs/RELATIONSHIPS_MATRIX.md
- docs/README.md
- docs/QUICKSTART.md


---

## SUBDIRECTORY AUDIT FINDINGS (April 13, 2026 16:40)

### Issues Found in Subdirectories

#### 1. Empty Directories (DELETE)
- **docs/developer-guide/** - Empty, development-focused (should not be in user docs)
- **docs/decisions/** - Empty

#### 2. "Phase 2A" References (REMOVE - Implementation Detail)
**Files with "Phase 2A" references:**
- docs/builders/INTEGRATION_GUIDE.builder.md - Title: "Phase 2A Integration Guide"
- docs/design/ADVANCED_PATTERNS.design.md - Title: "Phase 2A Advanced Patterns Guide"
- docs/reference/GETTING_STARTED.reference.md - "Getting Started with Phase 2A"

**Issue:** "Phase 2A" is an internal development milestone, not a user-facing version.
**Fix:** Remove "Phase 2A" - just call it current version/functionality.

#### 3. Phase 1/2/3 Implementation References
**Files with implementation phase references:**
- docs/design/VARIANT_DIFFERENTIATION_STRATEGY.design.md - "Phase 1: Core", "Phase 2: Specialized", "Phase 3: Advanced"
- docs/design/WORKFLOW_HANDLING_ANALYSIS.design.md - "Phase 1/2/3" implementation steps
- docs/design/LANGUAGE_INTEGRATION_DESIGN.design.md - "Phase 1" through "Phase 5" implementation plan

**Issue:** These are design docs describing IMPLEMENTATION phases - possibly acceptable if they're historical design decisions, but should be reviewed.

#### 4. References to Deleted Development Docs
**File:** docs/reference/DIRECTORY_STRUCTURE.reference.md

**References to deleted files:**
- TECHNICAL_DEBT.md
- TEST_CONVENTIONS.md
- QUALITY_METRICS.md
- Multiple PHASE*_EXECUTION_GUIDE.plan.md references

**Fix:** Update to reflect actual current structure.

#### 5. Misc Directory Content
**Files:** 3 PNG image files (promptosaurus logos)
**Status:** ✅ OK - these are assets, not documentation

---

### Subdirectory File Count

| Directory | File Count | Status |
|-----------|------------|--------|
| architecture/ | 1 | ⚠️ Review needed |
| builders/ | 10 | ⚠️ Phase refs |
| components/ | 6 | ⚠️ Review needed |
| decisions/ | 0 | 🗑️ DELETE (empty) |
| design/ | 5 | ⚠️ Phase refs |
| developer-guide/ | 0 | 🗑️ DELETE (empty, dev-focused) |
| misc/ | 3 images | ✅ OK |
| reference/ | 5 | ⚠️ Broken refs |
| user-guide/ | 3 | ⚠️ Review needed |

---

### Recommended Actions

**DELETE (2 directories):**
1. docs/developer-guide/ - Empty, development-focused
2. docs/decisions/ - Empty

**CLEAN PHASE REFERENCES (15+ files):**
1. Remove "Phase 2A" from titles/content
2. Review design docs - keep if historical ADR, remove if implementation detail

**UPDATE REFERENCES (1 file):**
1. docs/reference/DIRECTORY_STRUCTURE.reference.md - Remove deleted file references

**REVIEW FOR HALLUCINATIONS (remaining subdirectory files)**


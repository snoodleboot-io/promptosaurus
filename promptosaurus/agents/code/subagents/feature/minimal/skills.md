---
name: feature-planning
description: Plan before implementing - understand scope and approach
tools_needed: [read, glob]
---

## Instructions

Before implementing any feature:

1. **Restate the goal** in your own words to confirm understanding
2. **Read relevant source files** - do not assume their contents
3. **Identify all files** that will need to change
4. **Propose implementation approach** with tradeoffs noted
5. **Flag assumptions** you are making
6. **Wait for confirmation** before proceeding

This ensures alignment and prevents rework.

---
name: incremental-implementation
description: Implement code one file at a time following conventions
tools_needed: [edit, write, read]
---

## Instructions

When implementing:

1. **Follow Core Conventions exactly** - match language/framework standards
2. **Match existing patterns** in the same code layer
3. **Add inline comments** for non-obvious logic
4. **Add TODO comments** for judgment calls requiring user review
5. **Implement one file at a time** - don't jump between files

This maintains code quality and consistency.

---
name: post-implementation-checklist
description: Document follow-up work and testing needs after implementation
tools_needed: []
---

## Instructions

After completing implementation:

1. **List follow-up work created:**
   - Technical debt introduced
   - Missing features or edge cases
   - Related changes needed elsewhere

2. **List tests needed:**
   - Unit tests to write or update
   - Integration tests required
   - Edge cases to cover

This ensures nothing is forgotten and work is documented.

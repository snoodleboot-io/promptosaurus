---
name: test-aaa-structure
description: Apply Arrange-Act-Assert pattern for clear, maintainable tests
tools_needed: [read, write]
---

## AAA Test Structure

Always structure tests using the Arrange-Act-Assert pattern:

**Arrange:** Set up state and inputs
**Act:** Call the thing under test
**Assert:** Verify outputs and side effects

### Rules
- One logical assertion per test
- One behavior per test name
- Test names must be descriptive sentences:
  - `it("returns null when the user ID does not exist")`
  - `it("throws AuthError when the token is expired")`

### Example
```python
def test_user_get_by_id_returns_user_when_found():
    # Arrange
    user = User(id="123", name="Alice")
    db.save(user)
    
    # Act
    result = get_user_by_id("123")
    
    # Assert
    assert result.name == "Alice"
```


---
name: test-coverage-categories
description: Systematic approach to achieving comprehensive test coverage
tools_needed: [read, write]
---

## Coverage Categories

Work through these categories in order for comprehensive coverage:

1. **HAPPY PATH** — Expected inputs produce expected output
2. **BOUNDARY VALUES** — Min, max, exactly at limit, one over limit
3. **EMPTY / NULL / ZERO** — Each nullable input absent or zeroed
4. **ERROR CASES** — Dependency throws, network fails, DB unavailable
5. **CONCURRENT / ORDERING** — If function has state, test ordering
6. **AUTHORIZATION BOUNDARIES** — Does it enforce who can call it?
7. **ADVERSARIAL INPUTS** — SQL fragments, script tags, path traversal, unicode, emoji, null bytes, extremely long strings

### Workflow
- Check off each category as you implement tests
- Document which categories don't apply and why
- Flag any gaps in coverage with rationale


---
name: test-mocking-rules
description: Guidelines for when and how to use mocks in tests
tools_needed: []
---

## Mocking Rules

### When to Mock
- Mock only at process boundaries:
  - Database connections
  - Network calls (HTTP, external APIs)
  - Filesystem operations
  - Time/date functions
  - Random number generation

### What NOT to Mock
- **Never mock the thing under test**
- **Never mock internal helpers** — test them through the public interface
- **Never mock your own database** in integration tests

### Consistency
- Use the mock library from core-conventions.md consistently
- Follow the same mocking patterns across the codebase

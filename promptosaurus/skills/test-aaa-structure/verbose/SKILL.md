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



<!-- path: promptosaurus/prompts/agents/core/core-conventions-ruby.md -->
# Core Conventions Ruby

Language:             {{config.language}}           e.g., Ruby 3.3
Runtime:              {{config.runtime}}            e.g., MRI, JRuby
Package Manager:      {{config.package_manager}}        e.g., Bundler
Linter:               {{config.linter}}             e.g., RuboCop
Formatter:           {{config.formatter}}          e.g., Rufo, RuboCop

### Naming Conventions

Files:              snake_case
Variables:          snake_case
Constants:          UPPER_SNAKE
Classes/Types:      PascalCase
Functions:          snake_case (methods)
Database tables:    snake_case
Environment vars:   UPPER_SNAKE_CASE always

## Ruby-Specific Rules

### Type System
- Use RBS for type signatures (Ruby 3.0+)
- Use strict typing in critical code paths

### Error Handling
- Use exceptions for error handling
- Never rescue Exception (rescue StandardError instead)
- Use begin/rescue/ensure blocks

### Code Style
- Follow Ruby style guide (RuboCop)
- Use RuboCop for linting
- Use meaningful method names

### Testing

#### Coverage Targets
Line:           {{config.coverage.line}}          e.g., 80%
Branch:         {{config.coverage.branch}}        e.g., 70%
Method:         {{config.coverage.method}}         e.g., 90%

#### Test Types

##### Unit Tests
- Use RSpec or Minitest
- Test one class/method in isolation
- Use doubles/mocks for external dependencies

##### Integration Tests
- Test at service boundary
- Use factory_bot for test data

##### System Tests
- Use Capybara for browser testing

#### Framework & Tools
Framework:       {{config.testing_framework}}        e.g., RSpec, Minitest
Mocking:        {{config.mocking_library}}              e.g., RSpec mocks, RR
Coverage tool:  {{config.coverage_tool}}              e.g., SimpleCov

#### Scaffolding

```bash
# Install
gem install rspec simplecov

# Run tests
rspec                          # Run tests
rspec --format documentation  # Detailed output
rspec --coverage             # With coverage

# Configuration (.rspec)
--require spec_helper
--format documentation
--color
```

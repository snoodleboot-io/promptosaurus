<!-- path: promptosaurus/prompts/agents/core/core-conventions-kotlin.md -->
# Core Conventions Kotlin

Language:             {{config.language}}           e.g., Kotlin 1.9
Runtime:              {{config.runtime}}            e.g., JVM 21, Kotlin/JS, Kotlin/Native
Package Manager:      {{config.package_manager}}        e.g., Gradle, Maven
Linter:               {{config.linter}}             e.g., ktlint, detekt
Formatter:           {{config.formatter}}          e.g., ktlint

### Naming Conventions

Files:               PascalCase
Variables:          camelCase
Constants:          UPPER_SNAKE
Classes/Types:      PascalCase
Functions:          camelCase
Database tables:    snake_case
Environment vars:   UPPER_SNAKE_CASE always

## Kotlin-Specific Rules

### Null Safety
- Use nullable types (?) for values that can be null
- Use safe call operator (?.) and elvis operator (?:)
- Prefer val over var
- Avoid null checks, use built-in operators

### Error Handling
- Use Result for fallible operations
- Use exceptions for truly exceptional cases
- Use sealed classes for error types

### Coroutines
- Use suspend functions for async operations
- Use structured concurrency
- Use Flow for streams of data

### Testing

#### Coverage Targets
Line:           {{config.coverage.line}}          e.g., 80%
Branch:         {{config.coverage.branch}}        e.g., 70%
Function:       {{config.coverage.function}}       e.g., 90%
Statement:      {{config.coverage.statement}}      e.g., 85%
Path:           {{config.coverage.path}}           e.g., 60%

#### Test Types

##### Unit Tests
- Use JUnit 5 or Kotest
- Use MockK for mocking
- Test one function/class in isolation

##### Integration Tests
- Use Spring Boot Test for integration
- Use Testcontainers for databases

##### Property Tests
- Use Kotest property-based testing

#### Framework & Tools
Framework:       {{config.testing_framework}}        e.g., JUnit 5, Kotest
Mocking:        {{config.mocking_library}}              e.g., MockK
Property tool:   {{config.property_tool}}        e.g., Kotest
Coverage tool:  {{config.coverage_tool}}              e.g., JaCoCo

#### Scaffolding

```kotlin
// build.gradle.kts
dependencies {
    testImplementation("io.kotest:kotest-runner-junit5:5.8.0")
    testImplementation("io.kotest:kotest-property:5.8.0")
    testImplementation("io.mockk:mockk:1.13.8")
}

// Run tests
././gradlew testgradlew test
 -Pcoverage=true
```

##### CI Integration
```yaml
# GitHub Actions
- name: Run tests
  run: ./gradlew test
```

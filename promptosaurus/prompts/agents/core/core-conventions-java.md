<!-- path: promptosaurus/prompts/agents/core/core-conventions-java.md -->
# Core Conventions Java

Language:             {{config.language}}           e.g., Java 21
Runtime:              {{config.runtime}}            e.g., JDK 21, OpenJDK
Package Manager:      {{config.package_manager}}        e.g., Maven, Gradle
Linter:               {{config.linter}}             e.g., Checkstyle, SpotBugs
Formatter:           {{config.formatter}}          e.g., Google Java Format, Spotless

### Naming Conventions

Files:               PascalCase
Variables:          camelCase
Constants:          UPPER_SNAKE
Classes/Types:      PascalCase
Functions:          camelCase
Database tables:    snake_case
Environment vars:   UPPER_SNAKE_CASE always

## Java-Specific Rules

### Type System
- Use strong typing - avoid raw types
- Prefer immutable objects where possible
- Use Optional for nullable return types
- Enable checker framework for null annotations

### Error Handling
- Use specific exception types, not generic Exception
- Never catch Exception or Throwable unless rethrowing
- Use try-with-resources for all Closeable resources
- Log at the boundary where the error is handled

### Imports & Packages
- Use standard package structure (com.company.module)
- Group imports: java → javax → third-party → internal
- Never use wildcard imports (*)

### Testing

#### Coverage Targets
Line:           {{config.coverage.line}}          e.g., 80%
Branch:         {{config.coverage.branch}}        e.g., 70%
Function:       {{config.coverage.function}}       e.g., 90%
Statement:      {{config.coverage.statement}}      e.g., 85%
Mutation:       {{config.coverage.mutation}}       e.g., 80%
Path:           {{config.coverage.path}}           e.g., 60%

#### Test Types

##### Unit Tests
- One class or method in isolation
- Use JUnit 5 (Jupiter) for testing
- Mock external dependencies with Mockito
- Test behavior, not implementation

##### Integration Tests
- Test at service or component boundary
- Use Testcontainers for database testing
- Use Spring Boot Test for integration tests

##### E2E Tests
- Use Selenium or Playwright for browser testing
- Test critical user flows end-to-end

##### Mutation Tests
- Use Pitest for mutation testing

#### Framework & Tools
Framework:       {{config.testing_framework}}        e.g., JUnit 5, TestNG
Mocking library: {{config.mocking_library}}              e.g., Mockito, EasyMock
Coverage tool:  {{config.coverage_tool}}              e.g., JaCoCo, Cobertura
Mutation tool:  {{config.mutation_tool}}          e.g., Pitest

#### Scaffolding

```bash
# Maven
mvn test                          # Run tests
mvn test -Dcoverage=true         # With coverage
mvn org.pitest:pitest-maven:mutationCoverage  # Mutation testing

# Gradle
gradle test                      # Run tests
gradle test --coverage           # With coverage
gradle pitest                   # Mutation testing

# Dependencies (Maven)
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.8.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

##### CI Integration
```yaml
# GitHub Actions
- name: Run tests
  run: mvn verify -DskipITs

- name: Mutation tests
  run: mvn org.pitest:pitest-maven:mutationCoverage
```

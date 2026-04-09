# Promptosaurus Documentation

**Version:** v2.0.0 (Phase 2A Unified Prompt Architecture)  
**Status:** Production Ready  
**Last Updated:** April 9, 2026

---

## 🎯 Documentation Overview

Welcome to Promptosaurus documentation! This directory contains comprehensive guides for all audiences.

### What is Promptosaurus?

**Promptosaurus** is a unified prompt architecture system that:
- 📝 Defines agent configurations **once**
- 🔨 Builds for **5 AI tools automatically**
- ✅ Keeps all tools **always in sync**
- ⚡ Reduces configuration time by **40x** (3-4 hours → 5 minutes)

---

## 🚀 Quick Navigation

### For First-Time Users: Start Here

| Document | Duration | Purpose |
|----------|----------|---------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | 5 min | Installation + quick example |
| **[GITHUB_RELEASE_NOTES.md](../GITHUB_RELEASE_NOTES.md)** | 10 min | What's new in v2.0.0 |
| **[PHASE2A_RELEASE_NOTES.md](PHASE2A_RELEASE_NOTES.md)** | 15 min | Detailed feature descriptions |

### For Teams Upgrading from Phase 1

| Document | Duration | Purpose |
|----------|----------|---------|
| **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** | 20 min | Step-by-step upgrade instructions |
| **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** | 30 min | Team workflows & integration patterns |

### For Developers & API Users

| Document | Duration | Purpose |
|----------|----------|---------|
| **[BUILDER_API_REFERENCE.md](BUILDER_API_REFERENCE.md)** | 30 min | Complete API documentation |
| **[BUILDER_IMPLEMENTATION_GUIDE.md](BUILDER_IMPLEMENTATION_GUIDE.md)** | 1 hour | System architecture & extending |
| **[PHASE2A_IMPLEMENTATION_GUIDE.md](PHASE2A_IMPLEMENTATION_GUIDE.md)** | 1.5 hours | Deep dive into design & implementation |

### For Architects & Systems Designers

| Document | Duration | Purpose |
|----------|----------|---------|
| **[ard/PHASE2A_IR_MODELS_AND_BUILDERS.md](ard/PHASE2A_IR_MODELS_AND_BUILDERS.md)** | 45 min | Architecture decision record |
| **[ard/PHASE2_UNIFIED_ARCHITECTURE.md](ard/PHASE2_UNIFIED_ARCHITECTURE.md)** | 30 min | System design overview |
| **[ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md)** | 45 min | Extension patterns & customization |

### For Operations & DevOps

| Document | Duration | Purpose |
|----------|----------|---------|
| **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** | 30 min | CI/CD integration patterns |
| **[PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)** | 15 min | Benchmarks & performance |
| **[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** | 20 min | Deployment procedures |

---

## 📚 Documentation by Audience

### 👥 End Users / Product Users

Get started quickly with Promptosaurus:

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Installation & quick start (5 min)
2. **[GITHUB_RELEASE_NOTES.md](../GITHUB_RELEASE_NOTES.md)** - What's new (10 min)
3. **[PHASE2A_RELEASE_NOTES.md](PHASE2A_RELEASE_NOTES.md)** - Feature details (15 min)
4. **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Upgrade instructions (20 min)

**Quick Links:**
- Installation: `pip install promptosaurus`
- CLI Help: `prompt-build --help`
- Example: See GETTING_STARTED.md

### 👨‍💻 Developers & Integration Teams

Integrate Promptosaurus into your applications:

1. **[BUILDER_API_REFERENCE.md](BUILDER_API_REFERENCE.md)** - API documentation (30 min)
2. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Integration patterns (30 min)
3. **[TOOL_CONFIGURATION_EXAMPLES.md](TOOL_CONFIGURATION_EXAMPLES.md)** - Real-world examples (20 min)
4. **[ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md)** - Advanced usage (45 min)

**Quick Example:**
```python
from src.ir.models import Agent, Skill
from src.builders import BuilderFactory

agent = Agent(name="code", description="Expert engineer", skills=[...])
factory = BuilderFactory()
builder = factory.create("kilo")
output = builder.build(agent)
```

**Common Tasks:**
- Build for one tool: See GETTING_STARTED.md
- Build for all tools: See BUILDER_API_REFERENCE.md
- Custom configuration: See INTEGRATION_GUIDE.md

### 🏗️ Software Architects & System Designers

Understand the system architecture and design decisions:

1. **[ard/PHASE2A_IR_MODELS_AND_BUILDERS.md](ard/PHASE2A_IR_MODELS_AND_BUILDERS.md)** - Architecture decision (45 min)
2. **[PHASE2A_IMPLEMENTATION_GUIDE.md](PHASE2A_IMPLEMENTATION_GUIDE.md)** - Deep dive (1.5 hours)
3. **[ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md)** - Extension patterns (45 min)
4. **[BUILDER_IMPLEMENTATION_GUIDE.md](BUILDER_IMPLEMENTATION_GUIDE.md)** - Custom builders (1 hour)

**Key Concepts:**
- Intermediate Representation (IR) models
- Builder pattern for tool-specific output
- Registry with auto-discovery
- Component selector & composer

### 🔧 DevOps, SRE, Operations

Deploy and operate Promptosaurus:

1. **[RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)** - Deployment procedures (20 min)
2. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - CI/CD integration (30 min)
3. **[PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)** - Performance baselines (15 min)
4. **[COVERAGE_REPORT.md](COVERAGE_REPORT.md)** - Quality metrics (10 min)

**Common Tasks:**
- Deploy to PyPI: See RELEASE_CHECKLIST.md
- Set up CI/CD: See INTEGRATION_GUIDE.md
- Monitor performance: See PERFORMANCE_REPORT.md

### 🎓 Educators & Documentation Writers

Learn how Promptosaurus works for teaching or documentation purposes:

1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Introduction (5 min)
2. **[BUILDER_API_REFERENCE.md](BUILDER_API_REFERENCE.md)** - API overview (30 min)
3. **[PHASE2A_IMPLEMENTATION_GUIDE.md](PHASE2A_IMPLEMENTATION_GUIDE.md)** - Complete system (1.5 hours)
4. **[ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md)** - Advanced concepts (45 min)

**Teaching Resources:**
- Code examples in all guides
- Step-by-step walkthrough in GETTING_STARTED.md
- Architecture diagrams in PHASE2A_IMPLEMENTATION_GUIDE.md
- Real-world patterns in INTEGRATION_GUIDE.md

### 💼 Product Managers & Business Stakeholders

Understand value and business impact:

1. **[GITHUB_RELEASE_NOTES.md](../GITHUB_RELEASE_NOTES.md)** - Key achievements (10 min)
2. **[PHASE2A_RELEASE_NOTES.md](PHASE2A_RELEASE_NOTES.md)** - Feature summary (15 min)
3. **[PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)** - Performance metrics (15 min)
4. **[COVERAGE_REPORT.md](COVERAGE_REPORT.md)** - Quality assurance (10 min)

**Key Metrics:**
- 40x faster iterations (3-4 hours → 5 minutes)
- 1,200 tests passing (100%)
- 93.7% code coverage
- 0 backwards incompatibilities

---

## 📖 Complete Documentation Index

### Getting Started & Basics
- [GETTING_STARTED.md](GETTING_STARTED.md) - 5-minute quick start
- [GITHUB_RELEASE_NOTES.md](../GITHUB_RELEASE_NOTES.md) - v2.0.0 release highlights
- [PHASE2A_RELEASE_NOTES.md](PHASE2A_RELEASE_NOTES.md) - Detailed release information

### Migration & Upgrade
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Upgrade from Phase 1 (step-by-step)

### API & Implementation
- [BUILDER_API_REFERENCE.md](BUILDER_API_REFERENCE.md) - Complete API documentation
- [BUILDER_IMPLEMENTATION_GUIDE.md](BUILDER_IMPLEMENTATION_GUIDE.md) - System architecture
- [PHASE2A_IMPLEMENTATION_GUIDE.md](PHASE2A_IMPLEMENTATION_GUIDE.md) - Deep dive (47 pages)

### Integration & Deployment
- [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Team workflows & CI/CD
- [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md) - Deployment procedures
- [TOOL_CONFIGURATION_EXAMPLES.md](TOOL_CONFIGURATION_EXAMPLES.md) - Real-world examples

### Quality & Performance
- [COVERAGE_REPORT.md](COVERAGE_REPORT.md) - Test coverage metrics
- [MUTATION_TESTING_RESULTS.md](MUTATION_TESTING_RESULTS.md) - Mutation analysis
- [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md) - Performance benchmarks

### Architecture & Design
- [ard/PHASE2A_IR_MODELS_AND_BUILDERS.md](ard/PHASE2A_IR_MODELS_AND_BUILDERS.md) - ADR
- [ard/PHASE2_UNIFIED_ARCHITECTURE.md](ard/PHASE2_UNIFIED_ARCHITECTURE.md) - System design
- [ADVANCED_PATTERNS.md](ADVANCED_PATTERNS.md) - Extension patterns

### Tool-Specific Guides
- [builders/README.md](builders/README.md) - Builder overview
- [builders/KILO_BUILDER_GUIDE.md](builders/KILO_BUILDER_GUIDE.md) - Kilo IDE integration
- [builders/CLINE_BUILDER_GUIDE.md](builders/CLINE_BUILDER_GUIDE.md) - Cline integration
- [builders/CLAUDE_BUILDER_GUIDE.md](builders/CLAUDE_BUILDER_GUIDE.md) - Claude API integration
- [builders/COPILOT_BUILDER_GUIDE.md](builders/COPILOT_BUILDER_GUIDE.md) - GitHub Copilot
- [builders/CURSOR_BUILDER_GUIDE.md](builders/CURSOR_BUILDER_GUIDE.md) - Cursor IDE integration

### Features & Roadmap
- [features/FEATURE_001_unified_prompt_architecture.md](features/FEATURE_001_unified_prompt_architecture.md) - Feature overview
- [features/ROADMAP.md](features/ROADMAP.md) - Product roadmap
- [features/tasks/STORY7_TASK_BREAKDOWN.md](features/tasks/STORY7_TASK_BREAKDOWN.md) - Upcoming work

### AI Tool Capability Matrix
- [AI_TOOL_CAPABILITY_MATRIX.md](AI_TOOL_CAPABILITY_MATRIX.md) - Feature support by tool

---

## 🎥 Video & Tutorial Recommendations

### Getting Started (5-10 minutes)
- **Installation & Quick Start** - See GETTING_STARTED.md for step-by-step with code
- **Building for All 5 Tools** - Quick example in GITHUB_RELEASE_NOTES.md

### Deep Dives (30-60 minutes)
- **System Architecture** - Read PHASE2A_IMPLEMENTATION_GUIDE.md
- **Custom Builder Creation** - Follow guide in BUILDER_IMPLEMENTATION_GUIDE.md
- **Team Integration Patterns** - See INTEGRATION_GUIDE.md

### Advanced Topics (1-2 hours)
- **Extension Patterns** - Study ADVANCED_PATTERNS.md
- **Architecture Decisions** - Review all ADRs in `ard/` directory
- **Performance Tuning** - Analyze PERFORMANCE_REPORT.md

---

## 📋 Common Tasks & How to Find Them

### "I want to get started in 5 minutes"
→ Read [GETTING_STARTED.md](GETTING_STARTED.md)

### "I'm upgrading from Phase 1"
→ Follow [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

### "I need API documentation"
→ See [BUILDER_API_REFERENCE.md](BUILDER_API_REFERENCE.md)

### "I want to integrate into my team workflow"
→ Check [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

### "I need to deploy to production"
→ Use [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md)

### "I want to understand the architecture"
→ Read [PHASE2A_IMPLEMENTATION_GUIDE.md](PHASE2A_IMPLEMENTATION_GUIDE.md)

### "I want to create a custom builder"
→ Follow [BUILDER_IMPLEMENTATION_GUIDE.md](BUILDER_IMPLEMENTATION_GUIDE.md)

### "I need to optimize performance"
→ Review [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)

### "I need tool-specific guidance (Kilo/Cline/Claude/etc)"
→ Check [builders/](builders/) directory

### "I found a bug or have questions"
→ See troubleshooting sections in relevant guides or [GETTING_STARTED.md](GETTING_STARTED.md)

---

## 🔍 Search Tips

- **Search by tool:** Use Ctrl+F to search for "Kilo", "Cline", "Claude", "Copilot", or "Cursor"
- **Search by topic:** Try "API", "integration", "deployment", "performance", "migration"
- **Search by problem:** Try "error", "troubleshoot", "issue", "debug"

---

## 📞 Getting Help

### Documentation Not Enough?

1. **Troubleshooting Sections** - Most guides have troubleshooting
2. **Code Examples** - Check GETTING_STARTED.md and INTEGRATION_GUIDE.md
3. **API Reference** - See BUILDER_API_REFERENCE.md for method signatures
4. **GitHub Issues** - Report bugs with minimal reproduction

### Reporting Issues

Please include:
- Python version: `python --version`
- Package version: `pip show promptosaurus`
- Error message/traceback
- Minimal code reproduction
- Operating system

---

## 🚀 What's New in v2.0.0

**Phase 2A Unified Prompt Architecture** includes:

✅ **5 Production Builders**
- KiloBuilder (YAML + Markdown)
- ClaudeBuilder (JSON)
- ClineBuilder (Markdown + Skills)
- CopilotBuilder (GitHub instructions)
- CursorBuilder (Plain markdown)

✅ **Core Infrastructure**
- Unified IR models (Agent, Skill, Workflow, Tool, Rules, Project)
- Registry with auto-discovery
- Component selector (minimal/verbose)
- Component composer (reusable output)

✅ **Testing & Quality**
- 1,200 automated tests (100% passing)
- 93.7% code coverage
- 0 type errors (pyright strict)
- 83.9% mutation score

✅ **Documentation**
- 17+ comprehensive guides
- Getting started (5 min)
- Migration guide (step-by-step)
- API reference (complete)
- Implementation guide (30+ pages)

---

## 📝 License

All documentation is provided under the MIT License. See LICENSE file for details.

---

## 🙋 Contributing & Feedback

We'd love your feedback! To report issues or suggest improvements:

1. **Documentation Issues:** GitHub Issues (with "docs" label)
2. **Feature Requests:** GitHub Discussions
3. **Bug Reports:** GitHub Issues (with "bug" label and minimal reproduction)

---

## 📚 Additional Resources

- **GitHub Repository:** https://github.com/snoodleboot-io/promptosaurus
- **Package on PyPI:** https://pypi.org/project/promptosaurus/
- **Issue Tracker:** https://github.com/snoodleboot-io/promptosaurus/issues
- **Discussions:** https://github.com/snoodleboot-io/promptosaurus/discussions

---

**Last Updated:** April 9, 2026  
**Version:** v2.0.0  
**Status:** Production Ready  

**Happy building! 🚀**

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-01-23

### Added
- **Initial release** of Claude Code Project Template
- **Interactive setup wizard** (`setup.py`) with 3-tier system (minimal, standard, complete)
- **15 specialized AI agents** with strict role boundaries
  - Orchestrators: Atharva 2.0, Bug-Fix Orchestrator
  - Executors: Anand 2.0, Hitesh 2.0, SAMA 2.0
  - Validators: Ankur 2.0, Harshit 2.0
  - Domain Experts: Shawar 2.0, Vidya 2.0, Varsha 2.0, Debugger
  - Support: Memory Expert, Reflection Expert, Documentation Manager
- **Structure enforcement system** with git hooks and auto-fix
- **Tri-tier memory system** (hot/warm/cold) for agent learning
- **Jinja2 templates** for project configuration
- **Comprehensive documentation**
  - TIER_COMPARISON.md - Decision guide
  - QUICK_START_STANDARD.md - 2-hour setup guide
  - HOW_TO_USE_AGENTS.md - Agent system guide
  - TROUBLESHOOTING.md - Common issues and fixes
- **Validation test suite** (`tests/validate_setup.py`)
- **Portable automation scripts**
  - `structure_validator.py` - File placement validation
  - `auto_fix.py` - Automatic violation repair
  - `cleanup-manager.py` - Automated archival
  - `install-hooks.sh` - Git hook installer
  - `validate-agent-skills.sh` - Agent frontmatter validator

### Features
- **Zero-maintenance file organization** via lifecycle rules
- **Agent memory persistence** across sessions
- **Skills auto-loading** (requires Claude Code v2.0.43+)
- **Permission modes** (ask, auto-accept, auto-deny)
- **DPPM orchestration framework** (Discover → Plan → Prototype → Monitor)
- **Delegation protocol** with explicit handoffs
- **Quality gates** (Tier 1: self-reflection, Tier 2: validator review)

### Documentation
- README.md with feature overview and quick start
- TIER_COMPARISON.md with decision tree
- QUICK_START_STANDARD.md for production setup
- HOW_TO_USE_AGENTS.md for agent system
- TROUBLESHOOTING.md for common issues
- CONTRIBUTING.md for contributors
- LICENSE (MIT)

### Infrastructure
- Git hooks: pre-commit, commit-msg, post-merge
- Structure validation with canonical YAML schema
- Memory consolidation (hot → warm → cold)
- Lifecycle rules for automatic archival

---

## [Unreleased]

### Planned
- **Tier upgrades:** `setup.py --upgrade-to=complete`
- **Additional agents:**
  - Mobile testing specialist
  - Security scanning expert
  - Performance optimization expert
- **GitHub Actions integration** (CI/CD templates)
- **Docker support** (containerized agents)
- **VSCode extension** (visual setup wizard)
- **Community marketplace** for custom agents

### Under Consideration
- **Windows native support** (currently works via WSL)
- **Remote configuration** (fetch best practices from URL)
- **AI-powered setup wizard** (infer tier from project size)
- **Cross-project memory sharing** (agents learn from multiple projects)

---

## Version History

- **v1.0.0** (2025-01-23) - Initial release
  - Extracted from LCT Medical Claims Q&A Widget project
  - Production-tested infrastructure
  - 15 specialized agents
  - 3-tier system (minimal, standard, complete)

---

**How to Update:**

When changes are made:
1. Update this CHANGELOG.md
2. Bump version in `setup.py` (if applicable)
3. Tag release: `git tag v1.0.1 && git push --tags`

# Claude Code Project Template

> **Production-ready agent orchestration infrastructure for any project**

Bootstrap your next project with a sophisticated multi-agent system, automated quality gates, structure enforcement, and battle-tested workflows — all in one command.

---

## 🚀 Quick Start

```bash
# Clone this template
git clone https://github.com/your-org/claude-code-project-template.git my-awesome-project
cd my-awesome-project

# Run interactive setup wizard
python setup.py

# That's it! Start working with agents immediately
```

---

## 🎯 What You Get

This template extracts the complete infrastructure from a production project and gives you:

### ✅ **15 Specialized AI Agents**
- **Orchestrators:** Feature planning (DPPM framework), bug coordination
- **Executors:** Full-stack code, frontend specialists, AI/ML engineering
- **Validators:** Quality gates, test execution, code review
- **Experts:** Deployment, architecture, design, debugging, memory management

### ✅ **Automated Structure Enforcement**
- Git hooks validate file placement on every commit
- Auto-fix repairs violations automatically
- Lifecycle rules archive old files (completion reports, test results)
- Zero-maintenance file organization

### ✅ **Tri-Tier Memory System**
- Agents remember past work across sessions
- Hot/Warm/Cold memory tiers (performance-optimized)
- Weekly consolidation, monthly archival
- Memory Expert ensures safety

### ✅ **Quality Gates & Reflection**
- Silent self-reflection (agents self-assess before submission)
- Tier 1 (agent) + Tier 2 (validator) quality gates
- 50% reduction in rework
- Continuous improvement

### ✅ **Production-Grade Automation**
- Pre-commit structure validation
- Commit message enforcement
- Post-merge reminders
- Automated cleanup (nightly cron jobs)

---

## 🎚️ Choose Your Tier

Not all projects need the same infrastructure. Pick your tier:

| Feature | Minimal | Standard | Complete |
|---------|---------|----------|----------|
| **Setup Time** | 30 minutes | 2 hours | 1 day |
| **Core Agents** | 5 | 15 | 15 |
| **Structure Enforcement** | Basic | Full | Full |
| **Auto-Fix** | ❌ | ✅ | ✅ |
| **Memory System** | ❌ | ✅ | ✅ |
| **Git Hooks** | Pre-commit only | All 3 | All 3 |
| **Reflection System** | ❌ | ❌ | ✅ |
| **Automated Cleanup** | ❌ | ❌ | ✅ (cron) |
| **Best For** | Prototypes, learning | Production projects | Mission-critical |

**Unsure?** See [docs/TIER_COMPARISON.md](docs/TIER_COMPARISON.md) for a decision tree.

**Can I upgrade later?** Yes! `python setup.py --upgrade-to=standard`

---

## 📚 Documentation

### Getting Started
- [**Tier Comparison**](docs/TIER_COMPARISON.md) - Which tier should I choose?
- [**Quick Start (Minimal)**](docs/QUICK_START_MINIMAL.md) - 30-minute setup
- [**Quick Start (Standard)**](docs/QUICK_START_STANDARD.md) - 2-hour setup
- [**Quick Start (Complete)**](docs/QUICK_START_COMPLETE.md) - 1-day setup

### How-To Guides
- [**How to Use Agents**](docs/HOW_TO_USE_AGENTS.md) - Invoking agents, delegation protocol
- [**How to Use Structure Enforcement**](docs/HOW_TO_USE_STRUCTURE.md) - Lifecycle rules, auto-fix
- [**How to Use Memory System**](docs/HOW_TO_USE_MEMORY.md) - Tri-tier memory, consolidation
- [**How to Use Reflection**](docs/HOW_TO_USE_REFLECTION.md) - Quality gates, self-scoring
- [**How to Use Git Hooks**](docs/HOW_TO_USE_HOOKS.md) - Customizing hooks

### Troubleshooting
- [**Troubleshooting Guide**](docs/TROUBLESHOOTING.md) - Common issues and fixes

---

## 🏗️ What's Inside

```
claude-code-project-template/
├── setup.py                    # Interactive wizard (all the magic)
├── .claude/
│   ├── agents/                 # 15 specialized agents
│   ├── scripts/                # Portable automation
│   ├── hooks/                  # Git hook templates
│   ├── structure/              # Canonical structure schema
│   ├── memory/                 # Memory system templates
│   └── docs/                   # Protocols & methodologies
├── docs/                       # Comprehensive guides
└── tests/                      # Validation suite
```

---

## 🧬 Agent System Overview

**Orchestrators (Planning, No Execution):**
- `@atharva-2.0` - Feature orchestrator (DPPM framework)
- `@bug-fix-orchestrator` - Bug fix coordination

**Executors (Implementation, No Planning):**
- `@anand-2.0` - Full-stack code executor
- `@hitesh-2.0` - Frontend specialist (React, Vue, etc.)
- `@sama-2.0` - AI/ML engineering

**Validators (Review, No Implementation):**
- `@ankur-2.0` - Quality gatekeeper (APPROVE/REVISE/FAIL verdicts)
- `@harshit-2.0` - Test executor (runs tests, reports results)

**Domain Experts:**
- `@shawar-2.0` - Deployment expert (Vercel, Railway, AWS, etc.)
- `@vidya-2.0` - Solution architect
- `@varsha-2.0` - UI/UX designer
- `@debugger` - Bug investigation

**Support:**
- `@memory-expert` - Memory management & curation
- `@reflection-expert` - Meta-reflection on agent quality
- `@documentation-manager` - Documentation lifecycle

**Every agent has:**
- Strict role boundaries (MUST/MUST NOT guardrails)
- Skills auto-loading (frontend-design, document-skills, etc.)
- Permission modes (ask, auto-accept, auto-deny)
- Persistent memory (learns from past work)

---

## 🛡️ What Makes This Special

### ✨ **Zero-Maintenance File Organization**
- Git hooks validate structure on every commit
- Auto-fix repairs violations automatically
- Lifecycle rules archive old files (7-45 day retention)
- Result: Developers never think about file placement

### ✨ **Agent Specialization at Scale**
- 15 agents, each with ONE job
- Strict boundaries prevent role confusion
- Explicit handoffs ensure accountability
- Result: Predictable, high-quality output

### ✨ **Tri-Tier Memory System**
- Hot memory (last 20 events): Always fast
- Warm memory (events 21-100): Pattern recognition
- Cold memory (events 101+): Long-term learnings
- Result: Agents learn without performance degradation

### ✨ **Silent Self-Reflection**
- Agents self-assess before submission (Tier 1)
- Validator provides calibration feedback (Tier 2)
- Agents improve over time
- Result: 50% fewer rejections

### ✨ **Production-Tested**
- Extracted from real production project
- Battle-tested workflows
- Conservative defaults
- Result: Works out-of-the-box

---

## 🧪 Validation

After setup, run:

```bash
python tests/validate_setup.py
```

Expected output:
```
Running setup validation...

✅ Git hooks installed (pre-commit, commit-msg, post-merge)
✅ Structure validator operational
✅ All 15 agents have valid frontmatter
✅ Memory system initialized (15 memory files)
✅ CLAUDE.md configured for "my-awesome-project"
✅ Scripts executable
✅ Configurations valid

🎉 All checks passed! Setup complete.
```

---

## 📦 Requirements

- **Python 3.8+** (for setup wizard and automation scripts)
- **Git** (for hooks and version control)
- **Claude Code v2.0.43+** (for skills auto-loading)

Python packages (auto-installed):
- `PyYAML` - Configuration parsing
- `jinja2` - Template rendering
- `questionary` - Interactive wizard

---

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new agents
- How to improve scripts
- How to enhance documentation

---

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

This template extracts infrastructure from the **LCT Medical Claims Q&A Widget** project, which pioneered:
- Multi-agent orchestration (15 specialized agents)
- Tri-tier memory system
- Silent reflection quality gates
- Automated structure enforcement
- DPPM orchestration framework

---

## 🚀 Next Steps

1. **Run setup:** `python setup.py`
2. **Read quick start:** [docs/QUICK_START_STANDARD.md](docs/QUICK_START_STANDARD.md)
3. **Invoke your first agent:** `@anand-2.0 help me get started`
4. **Make a test commit** to verify git hooks work

**Welcome to production-grade agent orchestration!** 🎉

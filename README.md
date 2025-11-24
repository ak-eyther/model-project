# Claude Code Project Template

> **🎯 Your universal starting point for any new project**

Transform this template into your custom project in 5 minutes. Includes Next.js 14 + FastAPI, 15 AI agents, auto-setup scripts, and intelligent project customization that configures everything for your specific use case.

---

## 🚀 Quick Start - Start Your New Project

### Step 1: Clone This Template

```bash
# Use as template on GitHub (recommended)
# → Click "Use this template" button on GitHub
# → Clone your new repository

# OR clone directly
git clone https://github.com/your-org/claude-code-project-template.git my-new-project
cd my-new-project
```

### Step 2: One-Command Setup

```bash
./setup.sh
```

**What happens:**
1. ✅ Checks Node.js 18+ and Python 3.8+ installed
2. ✅ Installs all dependencies (Next.js + FastAPI packages)
3. ✅ Launches interactive wizard (customizes for YOUR project)

**The wizard asks:**
- Project name (e.g., "Task Manager Pro")
- Tech stack (Next.js + FastAPI by default)
- Deployment platforms (Vercel + Railway)
- Domain/industry (Healthcare, SaaS, E-commerce, etc.)
- Author info

**What gets customized:**
- ✅ `package.json` → Your project name/description
- ✅ `app/layout.tsx` → Page titles and metadata
- ✅ `main.py` → API title and description
- ✅ `.claude/context/project-context.yaml` → All 15 agents know your project
- ✅ `README.md` → Updated with your project details

### Step 3: Start Developing

```bash
# Terminal 1 - Frontend
npm run dev
# → http://localhost:3000

# Terminal 2 - Backend
uvicorn main:app --reload
# → http://localhost:8000
# → API docs: http://localhost:8000/docs
```

**That's it!** In 5 minutes you have:
- ✅ Fully configured Next.js + FastAPI project
- ✅ 15 AI agents that know your project context
- ✅ Beautiful landing page with your project name
- ✅ Working health check endpoints
- ✅ Auto-generated API documentation

**See [QUICK_START_NEW_PROJECT.md](QUICK_START_NEW_PROJECT.md) for detailed guide.**

---

## 🔐 Security Notice - API Keys

**⚠️ IMPORTANT:** This template contains **placeholder API keys only**. Before deploying:

1. **Get your own API keys:**
   - Anthropic Claude: https://console.anthropic.com/settings/keys
   - OpenRouter (optional): https://openrouter.ai/keys

2. **Where to add them:**
   - **Railway:** Dashboard → Environment Variables
   - **Vercel:** Dashboard → Environment Variables
   - **Local development:** Copy `.env.example` to `.env.local`

3. **Files with placeholders:**
   - `.claude/scripts/restore-railway-env-vars.sh` - Railway restoration script
   - `.env.example` - Local development template

**Never commit real API keys to git.** Use environment variables in your deployment platform.

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
- **Auto-context loading** (inherits project context automatically)

---

## 🔄 Auto-Context System

**Problem:** When creating new projects from this template, agents need to know project-specific context (name, URLs, tech stack). Manual updates across 15 agent files are error-prone.

**Solution:** Single source of truth with automatic context propagation.

### How It Works

1. **Run initialization script once:**
   ```bash
   ./.claude/scripts/init-project.sh
   ```

2. **Answer prompts:**
   - Project name, slug, description
   - Tech stack (React/Vue, FastAPI/Express, etc.)
   - Deployment (Vercel, Railway, AWS, etc.)
   - URLs, domain context

3. **Script generates:** `.claude/context/project-context.yaml`

4. **All agents auto-load this file** via frontmatter:
   ```yaml
   context:
     inherit: ".claude/context/project-context.yaml"
   ```

5. **Variables interpolated automatically:**
   - `{{ project.name }}` → "Task Manager Pro"
   - `{{ tech_stack.frontend.framework }}` → "Next.js"
   - `{{ deployment.backend.platform }}` → "Railway"

**Result:** Every agent knows your project without manual updates!

### Available Commands

```bash
# Initialize new project context (Quick wizard)
python3 init-project.py

# Initialize new project context (Full wizard)
./.claude/scripts/init-project.sh

# Validate context completeness
./.claude/scripts/validate-context.sh

# Add context to agent files (auto-run during init)
./.claude/scripts/add-context-to-agents.sh
```

### Documentation

- **Complete Guide:** [`.claude/docs/guides/AUTO_CONTEXT_SYSTEM.md`](.claude/docs/guides/AUTO_CONTEXT_SYSTEM.md)
- **Context Schema:** [`.claude/context/project-context.yaml`](.claude/context/project-context.yaml)
- **Wizard Comparison:** [`INITIALIZATION_WIZARDS.md`](INITIALIZATION_WIZARDS.md)

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

### System Requirements
- **Node.js 18+** (for Next.js frontend)
- **Python 3.8+** (for FastAPI backend and automation scripts)
- **Git** (for hooks and version control)
- **Claude Code v2.0.43+** (for skills auto-loading)

### Dependencies (Auto-Installed via `./setup.sh`)

**Node.js packages (via npm):**
- `next` - Next.js framework
- `react`, `react-dom` - React library
- `typescript` - TypeScript compiler
- `tailwindcss` - CSS framework
- `playwright` - E2E testing
- `eslint` - Code linting

**Python packages (via pip):**
- `PyYAML` - Configuration parsing
- `jinja2` - Template rendering
- `questionary` - Interactive wizard
- `anthropic` - Claude API (optional)
- `requests` - HTTP requests (optional)

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

This template is built on production-tested patterns from real-world projects, which pioneered:
- Multi-agent orchestration (15 specialized agents)
- Tri-tier memory system
- Silent reflection quality gates
- Automated structure enforcement
- DPPM orchestration framework

---

## 🚀 Next Steps

1. **Run setup:** `./setup.sh` (installs all dependencies)
2. **Initialize project:** `./.claude/scripts/init-project.sh`
3. **Start development:**
   - Frontend: `npm run dev` (Next.js on http://localhost:3000)
   - Backend: `uvicorn main:app --reload` (FastAPI on http://localhost:8000)
4. **Read quick start:** [docs/QUICK_START_STANDARD.md](docs/QUICK_START_STANDARD.md)
5. **Invoke your first agent:** `@anand-2.0 help me get started`
6. **Make a test commit** to verify git hooks work

**Welcome to production-grade agent orchestration!** 🎉

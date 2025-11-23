# Quick Start: Standard Tier (2-Hour Setup)

**You chose: STANDARD tier** - Production-ready with all 15 agents, full structure enforcement, and memory system.

---

## ✅ What You Just Got

- **15 specialized agents** (orchestrators, executors, validators, domain experts)
- **Full structure enforcement** (git hooks + auto-fix)
- **Tri-tier memory system** (agents learn from past work)
- **Documentation architecture** (active vs archive)
- **Quality gates** (Tier 2 validation by Ankur)

---

## 🚀 Getting Started (5 Minutes)

### 1. Verify Setup

```bash
python tests/validate_setup.py
```

Expected output:
```
✅ Git hooks installed
✅ Structure validator operational  
✅ Agent frontmatter valid
✅ Memory system initialized
✅ CLAUDE.md configured
✅ Scripts executable
✅ Configuration files valid

🎉 All checks passed!
```

### 2. Make Your First Commit

```bash
echo "# My Project" > README.md
git add README.md
git commit -m "[SETUP-001] Initial project setup"
```

The pre-commit hook will validate structure. If it passes, you're good!

### 3. Invoke Your First Agent

Open Claude Code and type:
```
@anand-2.0 help me understand this project structure
```

---

## 📚 Key Files to Know

- **`CLAUDE.md`** - Instructions for Claude Code (already configured for your project)
- **`AGENT_COMMUNICATION_BOARD.md`** - Track what agents are working on
- **`.claude/structure/canonical-structure.yaml`** - File placement rules
- **`.claude/config/project-config.yaml`** - Your project configuration
- **`.claude/memory/*.json`** - Agent memories (will populate over time)

---

## 🤖 Your 15 Agents

**Orchestrators (Planning):**
- `@atharva-2.0` - Feature orchestrator (DPPM framework)
- `@bug-fix-orchestrator` - Bug coordination

**Executors (Implementation):**
- `@anand-2.0` - Full-stack code executor
- `@hitesh-2.0` - Frontend specialist
- `@sama-2.0` - AI/ML engineer

**Validators (Review):**
- `@ankur-2.0` - Quality gatekeeper (gives APPROVE/REVISE/FAIL verdicts)
- `@harshit-2.0` - Test executor (runs tests, reports results)

**Domain Experts:**
- `@shawar-2.0` - Deployment expert
- `@vidya-2.0` - Solution architect
- `@varsha-2.0` - UI/UX designer
- `@debugger` - Bug investigation

**Support:**
- `@memory-expert` - Memory management
- `@reflection-expert` - Meta-reflection
- `@documentation-manager` - Doc lifecycle

---

## 🔧 Common Commands

**Structure Validation:**
```bash
# Check for violations
python .claude/scripts/structure_validator.py

# Auto-fix violations (dry-run first)
python .claude/scripts/auto_fix.py --dry-run
python .claude/scripts/auto_fix.py --apply
```

**Agent Skills:**
```bash
# Validate all agents have correct skills
.claude/scripts/validate-agent-skills.sh
```

**Memory System:**
Agents automatically update their memory files (`.claude/memory/*-memory.json`). No manual intervention needed!

---

## 🎯 Your First Task

Try implementing a small feature to see the system in action:

```
@atharva-2.0 I want to add a simple "Hello World" homepage. Can you plan this feature using DPPM?
```

Atharva will:
1. Create a feature plan (Discover → Plan → Prototype → Monitor)
2. Hand off to @anand-2.0 or @hitesh-2.0 for implementation
3. @ankur-2.0 will review the code
4. @shawar-2.0 can deploy it

Watch how agents hand off work to each other!

---

## 📖 Next Steps

- **Read:** `.claude/docs/protocols/DELEGATION_PROTOCOL.md` - How agents work together
- **Read:** `.claude/docs/methodologies/DPPM_FRAMEWORK.md` - Feature development workflow
- **Explore:** `AGENT_COMMUNICATION_BOARD.md` - See task tracking in action

---

## 🚨 Troubleshooting

**Git hook blocking commit?**
```bash
# See what's wrong
python .claude/scripts/structure_validator.py

# Fix automatically
python .claude/scripts/auto_fix.py --apply
```

**Agent not responding?**
- Check frontmatter in `.claude/agents/{agent-name}.md`
- Validate: `.claude/scripts/validate-agent-skills.sh`

**Need help?**
- Check `docs/TROUBLESHOOTING.md`
- Ask `@memory-expert` to search past similar issues

---

**You're all set! Start building.** 🚀

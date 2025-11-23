# How to Use Agents

Your project has 15 specialized AI agents. Here's how to work with them effectively.

---

## 🎯 Core Principle: Delegation, Not Execution

**You coordinate agents. Agents execute.**

Think of yourself as a project manager directing specialized contractors:
- Don't do the work yourself
- Delegate to the right specialist
- Let agents hand off to each other
- Trust their expertise

---

## 📞 Invoking Agents

**Syntax:** `@agent-name [your request]`

**Examples:**
```
@atharva-2.0 plan a new user authentication feature

@anand-2.0 implement the login form from Atharva's plan

@ankur-2.0 review the authentication code

@shawar-2.0 deploy to staging
```

---

## 🔄 Agent Workflows

### Feature Development
```
User Request
  ↓
@atharva-2.0 (plans using DPPM framework)
  ↓
@anand-2.0 or @hitesh-2.0 (implements)
  ↓
@harshit-2.0 (runs tests)
  ↓
@ankur-2.0 (reviews → APPROVE/REVISE/FAIL)
  ↓
@shawar-2.0 (deploys)
```

### Bug Fix
```
User Reports Bug
  ↓
@debugger (investigates root cause)
  ↓
@anand-2.0 (fixes code)
  ↓
@harshit-2.0 (verifies fix)
  ↓
@ankur-2.0 (reviews)
  ↓
@shawar-2.0 (deploys hotfix)
```

---

## 🛡️ Agent Guardrails

Every agent has strict boundaries (MUST/MUST NOT):

**Orchestrators (Atharva, Bug-Fix Orchestrator):**
- ✅ MUST: Plan features, coordinate work
- ❌ MUST NOT: Write code, run tests, deploy

**Executors (Anand, Hitesh, SAMA):**
- ✅ MUST: Write code, implement features
- ❌ MUST NOT: Plan features, make architecture decisions

**Validators (Ankur, Harshit):**
- ✅ Ankur MUST: Review code quality, give verdicts
- ✅ Harshit MUST: Run tests, report results
- ❌ MUST NOT: Write code, make architecture decisions

**Domain Experts:**
- ✅ MUST: Stay in their domain (deployment, architecture, design)
- ❌ MUST NOT: Cross into other domains

---

## 💾 Memory System

Agents remember past work via `.claude/memory/{agent-name}-memory.json`.

**How to query memory:**
```
@memory-expert query experiences similar to: [your task]
```

**Example:**
```
@memory-expert query experiences similar to: React component with localStorage
```

Returns past similar work with learnings.

**Submitting experiences:**
Agents automatically submit experiences after completing tasks. No manual action needed.

---

## 🧠 Skills Auto-Loading

Agents have skills that auto-load when invoked:

- `@anand-2.0` → frontend-design, document-skills
- `@hitesh-2.0` → frontend-design
- `@harshit-2.0` → webapp-testing
- `@sama-2.0` → document-skills:xlsx, document-skills:pdf

You don't need to manually load skills - they're automatic!

---

## ⚠️ Common Mistakes

**❌ Don't:**
- Ask orchestrators to write code
- Ask executors to plan features
- Ask validators to fix bugs (they identify, executors fix)

**✅ Do:**
- Use explicit handoffs (`@agent-name do X`)
- Check `AGENT_COMMUNICATION_BOARD.md` for status
- Let agents delegate to each other

---

## 📋 Tracking Work

All agents MUST update `AGENT_COMMUNICATION_BOARD.md`:

**When starting work:**
```markdown
## 📋 In Progress
- **[FEAT-001]** User auth – @atharva-2.0 🔄 (2025-01-15 10:00 - Planning discovery phase)
```

**When completing:**
```markdown
## ✅ Completed Today
- **[FEAT-001]** User auth – @atharva-2.0 ✅ (2025-01-15 14:00 - Plan complete, handed to Anand)
```

---

## 🎓 Learn More

- `.claude/docs/protocols/DELEGATION_PROTOCOL.md` - Handoff rules
- `.claude/docs/protocols/MEMORY_PROTOCOL.md` - How memory works
- `.claude/docs/methodologies/DPPM_FRAMEWORK.md` - Feature planning process

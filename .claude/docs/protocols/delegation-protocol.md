# Delegation Protocol (Standard for All Agents)

## Overview
This protocol defines how agents delegate work to other specialized agents. All agents MUST follow this protocol.

## Core Principle
**Each agent has ONE job. If a task is outside your domain, delegate to the specialist.**

## Delegation Pattern

### 1. Identify the Right Agent
Before delegating, identify which agent owns the task:

| Task Type | Agent | Invocation |
|-----------|-------|------------|
| Feature Planning | @atharva-2.0 | `/atharva [feature]` |
| Code Execution | @anand-2.0 | Direct mention |
| AI/ML Engineering | @sama-2.0 | `/sama` |
| Deployment | @shawar-2.0 | `/shawar` |
| Test Execution | @harshit-2.0 | `/harshit-test` |
| Quality Validation | @ankur-2.0 | `/ankur` |
| Architecture | @vidya-2.0 | Direct mention |
| Frontend Code | @hitesh-2.0 | Direct mention |
| UI/UX Design | @varsha-2.0 | Direct mention |
| Bug Investigation | @debugger | `/debug-fix` |

### 2. Delegation Request Format

Use this format when delegating:

```markdown
## Task Delegation

**Delegating to:** @[agent-name]
**Task:** [One-line description]
**Context:** [Brief background]
**Expected outcome:** [What success looks like]
**Priority:** [High/Medium/Low]
**Dependencies:** [What must be done first]

**Handoff details:**
- [Key detail 1]
- [Key detail 2]
- [Key detail 3]
```

### 3. Explicit Handoff

Always use explicit agent mentions:

✅ **CORRECT:**
```
@harshit-2.0 run the full test suite and report results
```

❌ **INCORRECT:**
```
I'll just quickly test this... (No! You're not the test agent!)
```

### 4. Wait for Completion

After delegating:
1. **DO NOT** take over the agent's work
2. **DO** wait for their response
3. **DO** help diagnose if they get stuck (but don't do their work)
4. **DO** let the same agent retry after fixing blockers

## Delegation Chains

### Feature Development Chain
```
User Request
    ↓
@atharva-2.0 (orchestrator - plans feature)
    ↓
@vidya-2.0 (architecture - if needed)
    ↓
@sama-2.0 (AI impact analysis - if AI/ML involved)
    ↓
@anand-2.0 OR @hitesh-2.0 (execution - writes code)
    ↓
@harshit-2.0 (testing - runs tests)
    ↓
@ankur-2.0 (validation - code review + risk scoring)
    ↓
@shawar-2.0 (deployment - deploys to environments)
```

### Bug Fix Chain
```
User Bug Report
    ↓
@debugger (investigate - root cause analysis)
    ↓
@harshit-2.0 (reproduce - create failing test)
    ↓
@anand-2.0 OR @hitesh-2.0 (fix - implement solution)
    ↓
@harshit-2.0 (verify - run tests)
    ↓
@ankur-2.0 (validate - code review)
    ↓
@shawar-2.0 (deploy - push to environments)
```

## Escalation Rules

### When to Escalate UP (to orchestrator)
- Task is blocked and you can't unblock
- Task requires decisions beyond your scope
- Multiple agents need coordination
- User approval required

**Example:**
```
@atharva-2.0 I'm blocked on this feature because the architecture isn't defined yet.
Need @vidya-2.0 to specify the system design before I can proceed.
```

### When to Escalate SIDEWAYS (to specialist)
- Task requires expertise you don't have
- Task is outside your domain guardrails

**Example:**
```
@harshit-2.0 I found a bug during testing.
Delegating to @debugger for root cause analysis.
```

### When to Escalate DOWN (to executor)
- Planning is complete, need execution
- Architecture is defined, need implementation

**Example:**
```
@anand-2.0 Feature plan complete.
Implement the medical summary redesign per the plan in ATHARVA-PLAN-001.md
```

## Anti-Patterns (DON'T DO THIS)

### ❌ Silent Takeover
```
# Harshit thinking: "Tests are failing. Let me just fix the code..."
# NO! Harshit runs tests, @anand-2.0 fixes code
```

### ❌ Vague Delegation
```
# Bad: "Someone should test this"
# Good: "@harshit-2.0 run test suite TC-001 through TC-010"
```

### ❌ Skipping Delegation
```
# Bad: "This is a simple fix, I'll just deploy it myself"
# Good: "@shawar-2.0 deploy fix BUGFIX-123 to staging"
```

### ❌ Delegating to Wrong Agent
```
# Bad: "@harshit-2.0 review this code for security issues"
# Good: "@ankur-2.0 review this code for security issues"
# (Harshit runs tests, Ankur does code review)
```

## Delegation Checklist

Before delegating, verify:

- [ ] Is this task in my domain? (If yes, don't delegate)
- [ ] Who is the specialist for this task?
- [ ] Have I provided enough context?
- [ ] Have I defined success criteria?
- [ ] Have I checked for dependencies?
- [ ] Have I used explicit @mention?

## Collaboration vs Delegation

### Collaboration (Multiple Agents Work Together)
```
@sama-2.0 work with @vidya-2.0 to evaluate RAG architecture options
```
Both agents contribute their expertise simultaneously.

### Delegation (Sequential Handoff)
```
@atharva-2.0 complete feature plan → @anand-2.0 implement it
```
One agent finishes, then hands off to next.

## Delegation Tracking

All delegations should be tracked in:
1. **Agent Communication Board:** `AGENT_COMMUNICATION_BOARD.md`
2. **Agent Memory:** `.claude/memory/[agent-name]-memory.json`
3. **Task Status:** TodoWrite tool (if applicable)

## References
- **Memory Protocol:** `.claude/docs/protocols/memory-protocol.md`
- **Completion Protocol:** `.claude/docs/protocols/completion-protocol.md`
- **Agent Guardrails:** See individual agent files

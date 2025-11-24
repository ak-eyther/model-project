---
name: agent-communication
description: Update Agent Communication Board with task status, completion messages, and blocker tracking. Use after completing tasks or when blocked.
allowed-tools:
  - Read
  - Edit
---

# Agent Communication Protocol

## Task Status Updates

### When Starting Task
```markdown
## 📋 In Progress
- **[TASK-001]** Description – @agent-name 🔄 (timestamp - status)
```

### When Completing Task
```markdown
## ✅ Completed Today
- **[TASK-001]** Description – @agent-name ✅ (timestamp - result summary)
```

### When Blocked
```markdown
## 🚨 Blockers
- **[TASK-001]** Description – @agent-name ⚠️ (Needs: [what's needed])
```

## Completion Message Format

```
✅ [Agent Name] completed [task]!

Key results:
- [Result 1]
- [Result 2]

Next step: [What happens next]
```

## Blocker Message Format

```
⚠️ BLOCKER: [Agent Name] stuck on [issue]

Issue: [One sentence]
Needs: [Who/what is needed]
Impact: [Why this matters]

Action taken: [What you did]
```

## Rules
1. Lead with status emoji (✅ ⚠️ ❌)
2. Keep under 10 lines
3. State blocker FIRST
4. Say what you did to unblock

---
name: dppm-orchestration
description: Feature development using DPPM framework (Discover, Plan, Prototype, Monitor). Use for feature planning and multi-agent orchestration.
allowed-tools:
  - Read
  - Grep
  - TodoWrite
---

# DPPM Orchestration Framework

## 4 Phases

### 1. DISCOVER
- Analyze requirements
- Read project context
- Identify constraints
- Risk assessment

```
Tasks:
- Review feature request
- Search codebase for existing patterns
- Check architecture docs
- Identify affected components
```

### 2. PLAN
- Break down into tasks
- Assign to specialists
- Define dependencies
- Risk mitigation

```
Create:
- Task breakdown
- Agent assignments (@varsha, @vidya, @anand, @hitesh, @harshit, @shawar)
- Dependency graph
- Timeline estimate
```

### 3. PROTOTYPE
- Delegate to execution agents
- Monitor progress
- Handle blockers

```
Delegate:
- Design → @varsha-2.0
- Architecture → @vidya-2.0
- Backend → @anand-2.0
- Frontend → @hitesh-2.0
- Testing → @harshit-2.0
- Deployment → @shawar-2.0
```

### 4. MONITOR
- Track progress on Agent Communication Board
- Validate scope
- Ensure quality gates pass

```
Track:
- Update AGENT_COMMUNICATION_BOARD.md
- Monitor blockers
- Coordinate handoffs
```

## Workflow

```
User: "Build medical claims feature"
↓
DISCOVER: Read context, analyze requirements
↓
PLAN: Break into tasks, assign agents
↓
PROTOTYPE: Delegates execute in parallel
↓
MONITOR: Track on communication board
↓
COMPLETE: Feature delivered
```

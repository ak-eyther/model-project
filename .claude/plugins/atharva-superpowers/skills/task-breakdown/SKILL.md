---
name: task-breakdown
description: Break complex features into delegatable tasks with clear ownership and dependencies. Use for feature planning phase.
allowed-tools:
  - TodoWrite
  - Read
---

# Task Breakdown

## Process

### 1. Decompose Feature

```
Feature: User Authentication
↓
Tasks:
1. Design: Login UI (@varsha-2.0)
2. Architecture: Auth flow (@vidya-2.0)
3. Backend: Auth API (@anand-2.0)
4. Frontend: Login form (@hitesh-2.0)
5. Testing: E2E auth tests (@harshit-2.0)
6. Deployment: Deploy to staging (@shawar-2.0)
```

### 2. Define Dependencies

```
Task 1 (Design) → Must complete before Task 4 (Frontend)
Task 2 (Architecture) → Must complete before Task 3 (Backend)
Task 3, 4 → Must complete before Task 5 (Testing)
Task 5 → Must complete before Task 6 (Deployment)
```

### 3. Assign Ownership

```
Each task has clear owner:
- @varsha-2.0: Design (1 task)
- @vidya-2.0: Architecture (1 task)
- @anand-2.0: Backend (1 task)
- @hitesh-2.0: Frontend (1 task)
- @harshit-2.0: Testing (1 task)
- @shawar-2.0: Deployment (1 task)
```

### 4. Update Communication Board

```markdown
## 📋 In Progress
- **[AUTH-001]** Login UI design – @varsha-2.0 🔄
- **[AUTH-002]** Auth flow architecture – @vidya-2.0 🔄

## 📝 Backlog
- **[AUTH-003]** Auth API backend – @anand-2.0 (blocked by AUTH-002)
- **[AUTH-004]** Login form frontend – @hitesh-2.0 (blocked by AUTH-001)
```

## Output Template

```markdown
## Task Breakdown: [Feature Name]

### Tasks
1. **[TASK-ID]** Description
   - Owner: @agent-name
   - Dependencies: [TASK-IDs]
   - Estimate: S/M/L

### Parallel Execution
- Tasks 1, 2 can run in parallel
- Task 3, 4 blocked by Task 2
```

---
name: task-breakdown
description: Break complex features into delegatable tasks with clear ownership and dependencies. Use for feature planning phase.
metadata:
  short-description: Feature task breakdown
---

# Task Breakdown

## Process

### 1. Decompose Feature

```
Feature: User Authentication
↓
Tasks:
1. Design: Login UI (@design-owner)
2. Architecture: Auth flow (@architecture-owner)
3. Backend: Auth API (@backend-owner)
4. Frontend: Login form (@frontend-owner)
5. Testing: E2E auth tests (@test-owner)
6. Deployment: Deploy to staging (@deploy-owner)
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
- @design-owner: Design (1 task)
- @architecture-owner: Architecture (1 task)
- @backend-owner: Backend (1 task)
- @frontend-owner: Frontend (1 task)
- @test-owner: Testing (1 task)
- @deploy-owner: Deployment (1 task)
```

### 4. Update Communication Board

```markdown
## 📋 In Progress
- **[AUTH-001]** Login UI design – @design-owner 🔄
- **[AUTH-002]** Auth flow architecture – @architecture-owner 🔄

## 📝 Backlog
- **[AUTH-003]** Auth API backend – @backend-owner (blocked by AUTH-002)
- **[AUTH-004]** Login form frontend – @frontend-owner (blocked by AUTH-001)
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

## Scripts
- `scripts/skill_info.py`: Print skill name and description.

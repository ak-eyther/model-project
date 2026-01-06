# Plan template

Use this template when creating `plans/<feature-name>.md`.

# <Feature Name> Plan

## Type
- feature | fix | refactor

## Summary
- What this is
- Why we are doing it

## Scope
- In scope:
- Out of scope:

## Impact analysis
- Files/modules to touch:
  - UI:
  - API:
  - DB:
  - Infra:
  - Tests:
- Dependencies:
- Risks:

## ASCII impact diagram
```
[Client/UI] --> [API] --> [DB]
      |             |
      v             v
  [components/]  [routes/]
```

## Plan
### 1) <Major action item>
- [ ] <task>
- [ ] <task>

### 2) <Major action item>
- [ ] <task>
- [ ] <task>

### 3) <Major action item>
- [ ] <task>
- [ ] <task>

## Evidence log
- Item 1: <evidence>
- Item 2: <evidence>

## Compaction checkpoint
- Before compaction: update this plan with completed tasks and evidence.
- After compaction: reopen this plan and resume from the last evidenced item.

## User test plan
- Test goal:
- Steps:
  1)
  2)
  3)
- Expected results:
- Pass criteria:

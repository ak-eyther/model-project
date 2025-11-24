---
name: memory-management
description: Manage tri-tier agent memory (hot/warm/cold) with event consolidation and weekly cleanup. Use for memory updates after completing tasks.
allowed-tools:
  - Read
  - Edit
---

# Memory Management - Tri-Tier System

## Memory Structure

```json
{
  "hot_memory": {
    "_description": "Last 20 events - always loaded",
    "recent_events": [],
    "active_tasks": [],
    "recent_learnings": []
  },
  "warm_memory": {
    "_description": "Events 21-100 - patterns",
    "patterns": [],
    "known_issues": [],
    "successful_strategies": []
  },
  "cold_memory": {
    "_description": "Events 101+ - archived",
    "historical_patterns": []
  }
}
```

## When to Update

### After Task Completion
```
Update hot_memory.recent_events:
- What was done
- Outcome
- Lessons learned
```

### Weekly Consolidation
```
hot → warm (after 20 events)
warm → cold (after 100 events)
```

## Update Pattern

```json
{
  "recent_events": [
    {
      "date": "2025-11-24",
      "task": "Built FastAPI endpoint",
      "outcome": "Success",
      "lessons": ["Async patterns work well", "Remember CORS"]
    }
  ]
}
```

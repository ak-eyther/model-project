# Memory Protocol (Standard for All Agents)

## Overview
All agents MUST maintain memory of their work in structured JSON files located in `.claude/memory/[agent-name]-memory.json`.

## Memory File Structure

```json
{
  "agent_name": "agent-name",
  "version": "2.0",
  "last_updated": "2025-11-18T12:00:00Z",
  "hot_memory": {
    "recent_events": [],
    "active_tasks": [],
    "recent_learnings": []
  },
  "warm_memory": {
    "patterns": [],
    "known_issues": [],
    "successful_strategies": []
  },
  "cold_memory": {
    "historical_patterns": [],
    "archived_events": []
  },
  "statistics": {
    "total_tasks_completed": 0,
    "total_deployments": 0,
    "success_rate": 0.0
  }
}
```

## Tri-Tier Memory System

### Hot Memory (Last 20 Events)
**Purpose:** Immediate context, always loaded

**What to store:**
- Last 20 completed tasks
- Current active tasks
- Recent learnings (last 7 days)

**Update frequency:** After every task

### Warm Memory (Events 21-100)
**Purpose:** Medium-term patterns, loaded on demand

**What to store:**
- Patterns identified from recent work
- Known issues encountered
- Successful strategies that worked

**Update frequency:** Weekly consolidation

### Cold Memory (Events 101+)
**Purpose:** Long-term patterns, archived

**What to store:**
- Historical patterns only (no raw details)
- Major milestones
- Significant learnings

**Update frequency:** Monthly archival

## When to Update Memory

### 1. After Completing ANY Task
```json
{
  "hot_memory": {
    "recent_events": [
      {
        "id": "de-015",
        "timestamp": "2025-11-18T12:00:00Z",
        "task": "Deploy to production",
        "outcome": "success",
        "duration_minutes": 5,
        "details": "Deployed commit 3d9840b to production via Vercel + Railway",
        "learnings": "Railway cold start took 8s, within expected range"
      }
    ]
  }
}
```

### 2. When Learning Something New
```json
{
  "hot_memory": {
    "recent_learnings": [
      {
        "date": "2025-11-18",
        "learning": "Railway auto-deploy fails if .railwayignore contains Dockerfile",
        "solution": "Remove .railwayignore before deploying",
        "confidence": "high"
      }
    ]
  }
}
```

### 3. When Identifying a Pattern
```json
{
  "warm_memory": {
    "patterns": [
      {
        "pattern": "Railway health checks fail 30% of the time on first attempt due to cold start",
        "frequency": "30% of deployments",
        "mitigation": "GitHub Actions retry loop handles this automatically",
        "confidence": "high"
      }
    ]
  }
}
```

### 4. When Task is Blocked
```json
{
  "hot_memory": {
    "active_tasks": [
      {
        "id": "TASK-123",
        "status": "blocked",
        "blocker": "Waiting for @ankur-2.0 APPROVE verdict",
        "blocked_since": "2025-11-18T11:00:00Z",
        "next_action": "Deploy to staging once approved"
      }
    ]
  }
}
```

## Memory Update Checklist

After EVERY task completion, update:

- [ ] `hot_memory.recent_events` - Add new event (max 20, archive older)
- [ ] `hot_memory.active_tasks` - Mark task as completed or remove
- [ ] `hot_memory.recent_learnings` - Add any new learnings
- [ ] `statistics` - Increment counters (tasks completed, success rate)
- [ ] `last_updated` - Update timestamp

## Memory Consolidation

### Weekly Consolidation (Move Hot → Warm)
```bash
# Every 7 days:
# 1. Review hot_memory.recent_events (last 20)
# 2. Identify patterns
# 3. Move patterns to warm_memory.patterns
# 4. Keep only raw events in hot_memory
```

### Monthly Archival (Move Warm → Cold)
```bash
# Every 30 days:
# 1. Review warm_memory.patterns
# 2. Identify long-term patterns
# 3. Move to cold_memory.historical_patterns
# 4. Remove raw details, keep only patterns
```

## Memory Size Management

### Target Sizes
- **Hot Memory:** <50KB (20 events)
- **Warm Memory:** <100KB (patterns)
- **Cold Memory:** <50KB (patterns only, no details)
- **Total Memory File:** <200KB

### If Memory File Exceeds 200KB
```bash
# 1. Archive oldest hot events to warm
# 2. Archive oldest warm patterns to cold
# 3. Remove raw details from cold (keep patterns only)
# 4. Verify total size <200KB
```

## Memory Access Patterns

### Reading Memory (at task start)
```
1. Load hot_memory (always)
2. Scan for relevant recent_events
3. Check active_tasks
4. Check recent_learnings
5. Load warm_memory if needed (pattern lookup)
```

### Writing Memory (at task end)
```
1. Add event to hot_memory.recent_events
2. Update active_tasks status
3. Add learnings if applicable
4. Increment statistics
5. Update last_updated timestamp
6. Save memory file
```

## Memory File Location
All agent memory files stored in:
```
.claude/memory/[agent-name]-memory.json
```

**Examples:**
- `.claude/memory/shawar-2.0-memory.json`
- `.claude/memory/atharva-2.0-memory.json`
- `.claude/memory/anand-2.0-memory.json`

## Cross-Agent Memory Sharing

### Agents CAN Read Other Agents' Memory
```bash
# Shawar 2.0 can read Ankur's memory to see if approval was given
cat .claude/memory/ankur-2.0-memory.json | grep "APPROVE"
```

### Agents CANNOT Write to Other Agents' Memory
```bash
# Only update your own memory file
# ❌ Don't modify .claude/memory/atharva-2.0-memory.json if you're Shawar
# ✅ Only modify .claude/memory/shawar-2.0-memory.json
```

## Memory Audit Trail

### Track All Memory Updates
Each memory update should include:
- Timestamp (ISO 8601 format)
- Event ID (unique identifier)
- Task description
- Outcome (success/failure/blocked)
- Learnings (if any)

### Example Memory Event
```json
{
  "id": "de-015",
  "timestamp": "2025-11-18T12:00:00Z",
  "task": "Deploy commit 3d9840b to production",
  "outcome": "success",
  "duration_minutes": 5,
  "verification": {
    "frontend_health": true,
    "backend_health": true,
    "cors_check": true
  },
  "learnings": [
    "Railway cold start: 8s (within expected 5-10s range)",
    "Vercel deployment: 2m 15s (faster than average 3m)"
  ],
  "next_action": "Monitor production for 24h"
}
```

## Memory Consistency Rules

### 1. Always Use ISO 8601 Timestamps
```json
✅ "timestamp": "2025-11-18T12:00:00Z"
❌ "timestamp": "Nov 18, 2025 12:00 PM"
```

### 2. Use Consistent Event IDs
```json
# Format: [agent-prefix]-[sequential-number]
✅ "id": "de-015"  # Shawar (deployment) event 15
✅ "id": "qa-042"  # Ankur (quality) event 42
❌ "id": "random-uuid-123"
```

### 3. Store Outcomes as Enums
```json
✅ "outcome": "success" | "failure" | "blocked" | "partial"
❌ "outcome": "It worked but had some issues"
```

### 4. Limit String Lengths
```json
✅ "task": "Deploy to production"  # <50 chars
❌ "task": "Deploy the latest commit 3d9840b which includes the new medical summary redesign feature and CSS fixes to production environment via Vercel and Railway"
```

## Memory Recovery

### If Memory File is Corrupted
```bash
# 1. Check for backup
ls -la .claude/memory/shawar-2.0-memory.json.bak

# 2. Restore from backup
cp .claude/memory/shawar-2.0-memory.json.bak .claude/memory/shawar-2.0-memory.json

# 3. If no backup, recreate from template
# Use structure defined at top of this document
```

### Backup Strategy
```bash
# Create backup before major updates
cp .claude/memory/shawar-2.0-memory.json .claude/memory/shawar-2.0-memory.json.bak

# Keep last 3 backups
.claude/memory/shawar-2.0-memory.json
.claude/memory/shawar-2.0-memory.json.bak
.claude/memory/shawar-2.0-memory.json.bak2
.claude/memory/shawar-2.0-memory.json.bak3
```

## References
- **Delegation Protocol:** `.claude/docs/protocols/delegation-protocol.md`
- **Completion Protocol:** `.claude/docs/protocols/completion-protocol.md`
- **Agent Memory Files:** `.claude/memory/[agent-name]-memory.json`

# Architecture Gate Rule

## Purpose
Automatically invoke `Skill(senior-architect)` before any major architecture changes. Turns the skill from "nice doc" into "mandatory seatbelt".

---

## Trigger Patterns

When a user request contains ANY of these phrases, **STOP and invoke the architecture skill BEFORE implementation**:

### System Topology Changes
- "refactor architecture"
- "add service" / "add worker" / "add new service"
- "split into microservices"
- "move to" (hosting changes)
- "migrate from X to Y" (infrastructure)

### Queue / Async Changes
- "introduce queue" / "add queue" / "message queue"
- "background worker" / "job queue"
- "async processing" (when adding new async infrastructure)

### Database / Data Layer Changes
- "change database" / "new database" / "add database"
- "replace PostgreSQL" / "replace ChromaDB"
- "new data store" / "add Redis as primary"
- "breaking migration" / "schema overhaul"

### API Contract Changes
- "change API contract"
- "breaking change to /api/"
- "version the API"
- "new authentication model"

### Security Boundary Changes
- "expose backend directly"
- "bypass server proxy"
- "change auth boundaries"

---

## Action Required

When triggered:

1. **STOP** - Do not proceed with implementation
2. **Invoke** - Run `Skill(senior-architect)` with the user's request
3. **Wait** - The skill will produce options, trade-offs, and an ADR stub
4. **Approval** - Only proceed after explicit user approval of the recommended approach

---

## Example

**User:** "Let's add a Redis queue for background email processing"

**Correct response:**
```
This request involves adding new infrastructure (queue/worker).
Per the architecture gate, I'll invoke the senior-architect skill first.

[Skill(senior-architect)]
```

**Wrong response:**
```
Sure! I'll add Redis and create a worker service...
[Starts coding]
```

---

## Exceptions (Skip the Gate)

- Pure UI changes in Next.js components
- Adding new FastAPI endpoints that follow existing patterns
- Bug fixes that don't change architecture
- Performance tuning within existing modules
- Documentation updates

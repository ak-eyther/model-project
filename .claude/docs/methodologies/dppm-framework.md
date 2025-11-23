# DPPM Framework (Discover, Plan, Prototype, Monitor)

## Overview
DPPM is Atharva 2.0's core orchestration methodology for feature development. It ensures thorough discovery before execution.

## The Four Phases

### Phase 1: DISCOVER
**Objective:** Understand problem space completely before planning

**Activities:**
1. **Stakeholder interviews** (simulated from user requirements)
2. **Codebase discovery** (grep patterns, read relevant files)
3. **Architecture review** (consult @vidya-2.0's Architecture Digest)
4. **Constraint identification** (technical, business, timeline)
5. **Risk assessment** (what could go wrong?)

**Outputs:**
- Discovery notes (what we know, what we don't know)
- Problem statement (one sentence: what are we solving?)
- Success criteria (how will we know we're done?)

**Example:**
```markdown
## DISCOVERY: Medical Summary Redesign

**Problem:** Current medical summary is hard to scan, users miss critical info
**Stakeholders:** Medical claims reviewers, @varsha-2.0 (design)
**Constraints:** Must fit in existing widget, no backend changes
**Risks:** CSS specificity conflicts, responsive design
**Success Criteria:** Reviewers can scan summary in <5 seconds
```

---

### Phase 2: PLAN
**Objective:** Create detailed execution plan before writing code

**Activities:**
1. **Break down into tasks** (granular, actionable steps)
2. **Assign to specialists** (@anand-2.0, @hitesh-2.0, @sama-2.0, etc.)
3. **Define dependencies** (what must happen first?)
4. **Estimate effort** (complexity: Simple/Medium/Complex)
5. **Identify risks** (what could block us?)

**Outputs:**
- **BRD** (Business Requirements Document) - See `.claude/docs/orchestration/brd-template.md`
- **PRD** (Product Requirements Document) - See `.claude/docs/orchestration/prd-template.md`
- **Task list** (sequenced, with owners)
- **Risk mitigation plan**

**Planning Template:**
```markdown
## PLAN: [Feature Name]

### Task Breakdown
1. **TASK-001:** Design UI mockup (@varsha-2.0)
   - Duration: 2 hours
   - Dependencies: None
   - Risk: Low

2. **TASK-002:** Implement React component (@hitesh-2.0)
   - Duration: 4 hours
   - Dependencies: TASK-001 complete
   - Risk: Medium (CSS conflicts)

3. **TASK-003:** Test responsive layouts (@harshit-2.0)
   - Duration: 2 hours
   - Dependencies: TASK-002 complete
   - Risk: Low

### Critical Path
TASK-001 → TASK-002 → TASK-003 → Deploy

### Risk Mitigation
- **Risk:** CSS conflicts with existing styles
  **Mitigation:** Use CSS modules, scoped styles, test in isolation
```

---

### Phase 3: PROTOTYPE
**Objective:** Validate approach before full implementation

**Activities:**
1. **Create minimal working version** (proof of concept)
2. **Test assumptions** (does this solve the problem?)
3. **Get feedback** (show to user, get approval)
4. **Iterate if needed** (refine before full build)

**When to prototype:**
- ✅ Complex new features (uncertain approach)
- ✅ UI/UX changes (need visual validation)
- ✅ Architecture changes (prove it works)
- ❌ Simple bug fixes (just fix it)
- ❌ Well-defined features (plan is clear)

**Prototype Checklist:**
- [ ] Implements core functionality only (no polish)
- [ ] Demonstrates feasibility
- [ ] Can be shown to user for feedback
- [ ] Throwaway or evolve into full implementation?

**Example:**
```markdown
## PROTOTYPE: Medical Summary Redesign

**Goal:** Validate new card layout improves scannability

**Scope:**
- ✅ Create card component with sample data
- ✅ Test 3 layout options (side-by-side comparison)
- ✅ Show to user for feedback
- ❌ Don't implement full logic yet
- ❌ Don't deploy to production

**Outcome:**
- User selects Option B (3-column layout)
- Proceed to full implementation
```

---

### Phase 4: MONITOR
**Objective:** Track execution, unblock issues, ensure quality

**Activities:**
1. **Track task status** (use TodoWrite tool or AGENT_COMMUNICATION_BOARD.md)
2. **Unblock agents** (if @anand-2.0 stuck, diagnose why)
3. **Review progress** (are we on track?)
4. **Adjust plan** (if risks materialize, adapt)
5. **Coordinate handoffs** (@anand-2.0 done → @harshit-2.0 test → @ankur-2.0 validate)

**Monitoring Cadence:**
- **Daily:** Check task status, unblock agents
- **Per task:** Review when agent completes work
- **Per phase:** Reflect after Discovery, Plan, Prototype, Deploy

**Monitoring Template:**
```markdown
## MONITOR: [Feature Name]

### Current Status
- **Phase:** Implementation (TASK-002 in progress)
- **Owner:** @hitesh-2.0
- **Blocked:** No
- **On track:** Yes

### Completed Tasks
- ✅ TASK-001: Design mockup (@varsha-2.0) - 2h
- ✅ TASK-002: React component (@hitesh-2.0) - 4h

### In Progress
- 🔄 TASK-003: Test responsive (@harshit-2.0) - 1h remaining

### Blockers
- None

### Risks Materialized
- CSS specificity conflict detected → Resolved by using CSS modules

### Next Steps
- @harshit-2.0 complete testing
- @ankur-2.0 code review
- @shawar-2.0 deploy to staging
```

---

## DPPM Decision Tree

```
User Feature Request
    ↓
Is feature well-understood? → NO → DISCOVER first
    ↓ YES
Is there an existing plan? → NO → PLAN before execution
    ↓ YES
Is approach uncertain? → YES → PROTOTYPE first
    ↓ NO
Delegate to executor (@anand-2.0/@hitesh-2.0)
    ↓
MONITOR execution
    ↓
Blocked? → YES → Unblock or adjust plan
    ↓ NO
Task complete? → NO → Continue monitoring
    ↓ YES
Hand off to next phase (test → validate → deploy)
```

---

## DPPM for Different Feature Types

### New Feature (Complex)
**Use:** Full DPPM cycle
```
DISCOVER (2-4 hours) → PLAN (2-3 hours) → PROTOTYPE (optional, 2-4 hours) → EXECUTE → MONITOR
```

### Enhancement (Moderate)
**Use:** PLAN + MONITOR
```
PLAN (1-2 hours) → EXECUTE → MONITOR
```

### Bug Fix (Simple)
**Use:** MONITOR only
```
EXECUTE (delegate to @debugger + @anand-2.0) → MONITOR
```

### Urgent Hotfix (Critical)
**Use:** Fast-track PLAN
```
Quick PLAN (30 minutes) → EXECUTE → MONITOR → Deploy immediately
```

---

## DPPM Metrics

Track these metrics in Atharva's memory:

```json
{
  "dppm_metrics": {
    "total_features": 15,
    "discovery_phase_avg_hours": 2.5,
    "plan_phase_avg_hours": 1.8,
    "prototype_phase_used": 5,
    "plan_changes_mid_execution": 3,
    "success_rate": 0.93
  }
}
```

---

## References
- **BRD Template:** `.claude/docs/orchestration/brd-template.md`
- **PRD Template:** `.claude/docs/orchestration/prd-template.md`
- **Feature Development Workflow:** `.claude/docs/orchestration/feature-development-workflow.md`
- **Atharva 2.0 Agent:** `.claude/agents/atharva-2.0.md`

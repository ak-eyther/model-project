# Completion Protocol (Standard for All Agents)

## Overview
When ANY agent completes a task, they MUST follow this protocol to ensure visibility and proper handoff.

## Completion Checklist

After completing ANY task:

### 1. Update Agent Communication Board
**File:** `AGENT_COMMUNICATION_BOARD.md`

**Action:** Move task from "In Progress" to "✅ Completed Today"

**Format:**
```markdown
## ✅ Completed Today
- **[TASK-ID]** Task Description – @agent-name ✅ (timestamp - result summary)
```

**Example:**
```markdown
## ✅ Completed Today
- **[DEPLOY-PROD-015]** Production deployment – @shawar-2.0 ✅ (2025-11-18 12:00 - All environments healthy, commit 3d9840b deployed)
```

### 2. Update Agent Memory
**File:** `.claude/memory/[agent-name]-memory.json`

**Action:** Add event to `hot_memory.recent_events`

**Example:**
```json
{
  "hot_memory": {
    "recent_events": [
      {
        "id": "de-015",
        "timestamp": "2025-11-18T12:00:00Z",
        "task": "Deploy commit 3d9840b to production",
        "outcome": "success",
        "duration_minutes": 5,
        "learnings": "Railway cold start 8s, within expected range"
      }
    ]
  }
}
```

### 3. Communicate Status to User
Use the **Mandatory Status Communication Format** (see below)

### 4. Delegate Next Step (if applicable)
If task completion requires next step, delegate explicitly:

**Example:**
```
✅ @shawar-2.0 completed production deployment!

Deployment successful:
- Frontend: https://edit-widget-new.vercel.app
- Backend: https://lct-edit-widget-production.up.railway.app
- Health checks: All passing

Next step: @ankur-2.0 perform post-deployment validation
```

## Status Communication Format (MANDATORY)

### Format for SUCCESS ✅
```
✅ [Agent Name] completed [task]!

Key results:
- [Bullet 1]
- [Bullet 2]

Next step: [What happens next]
```

**Example:**
```
✅ Shawar 2.0 completed production deployment!

Key results:
- Frontend deployed to Vercel (2m 15s)
- Backend deployed to Railway (3m 40s)
- All health checks passing

Next step: Monitor for 24h, no further action needed
```

### Format for BLOCKED ⚠️
```
⚠️ BLOCKER: [Agent Name] is stuck

Issue: [One sentence: what's blocking]
Needs: [Who/what is needed to unblock]
Impact: [Why this matters]

I've [created urgent request / assigned to X / notified Y]
```

**Example:**
```
⚠️ BLOCKER: Shawar 2.0 is stuck on production deployment

Issue: Railway production won't auto-deploy (webhook failure)
Needs: Manual trigger via Railway CLI
Impact: Final step to complete BLOCKER-001 fix

I've created manual deployment command in SHAWAR-DEPLOY-MANUAL.md
```

### Format for PARTIAL SUCCESS ⚠️
```
⚠️ [Agent Name] completed with issues

✅ What worked: [Brief]
❌ What failed: [Brief]
Needs: [What's required to complete]
```

**Example:**
```
⚠️ Shawar 2.0 completed with issues

✅ What worked: Frontend deployed successfully to Vercel
❌ What failed: Backend Railway health check timeout (cold start)
Needs: Wait 5 minutes for Railway spin-up, then verify

I'm monitoring Railway logs and will report when healthy
```

## Communication Rules

### 1. Lead with Status Emoji
✅ Success
⚠️ Blocked / Partial
❌ Failed

**Why:** Makes it scannable - user sees status instantly

### 2. State the Blocker FIRST (if blocked)
❌ **BAD:**
```
I tried deploying to production. The build succeeded and tests passed.
Then I ran the deployment script. But then Railway had an issue...
[3 more paragraphs]
The issue is that Railway webhook failed.
```

✅ **GOOD:**
```
⚠️ BLOCKER: Railway webhook failed

Issue: Railway not triggering auto-deploy
Needs: Manual deployment via CLI
Impact: Blocks production release

I've created SHAWAR-DEPLOY-MANUAL.md with commands
```

### 3. Keep it Under 10 Lines
User doesn't have time to read essays. Be concise.

### 4. Say What You Did to Unblock
Don't just report the blocker - show proactive action:

❌ **BAD:**
```
Railway is down. I can't deploy.
```

✅ **GOOD:**
```
⚠️ Railway webhook failed.

I've prepared manual deployment commands in SHAWAR-DEPLOY-MANUAL.md
Ready to execute when you approve.
```

### 5. Never Assume User Will Read Full Details
Highlight critical info in the summary. Details go in files.

## Task Completion States

### SUCCESS ✅
- Task completed fully
- All acceptance criteria met
- No errors or blockers
- Ready for next step

**Action:** Update board, update memory, communicate success, delegate if needed

### BLOCKED ⚠️
- Task cannot proceed without external action
- Waiting for another agent
- Waiting for user approval
- Waiting for external service

**Action:** Update board (mark blocked), update memory, communicate blocker clearly, create unblock plan

### PARTIAL ⚠️
- Some parts completed successfully
- Other parts failed or incomplete
- Needs additional work

**Action:** Update board (specify what's done/not done), update memory, communicate partial status, plan completion

### FAILED ❌
- Task could not be completed
- Errors encountered
- Need to roll back or abandon

**Action:** Update board (mark failed), update memory, communicate failure with root cause, delegate to debugger if needed

## Direction Change Protocol

### If User Asks to STOP Current Task
When user says "stop that and do this instead":

1. **Update Agent Communication Board:**
   - Move task from "In Progress" to "⏸️ Paused/Cancelled"
   - Add reason for stopping

   **Format:**
   ```markdown
   ## ⏸️ Paused/Cancelled
   - **[TASK-ID]** Task Description – @agent-name ⏸️ (timestamp - Stopped by user: [reason], switched to [new task])
   ```

2. **Update Agent Memory:**
   ```json
   {
     "hot_memory": {
       "recent_events": [
         {
           "id": "de-015",
           "timestamp": "2025-11-18T12:00:00Z",
           "task": "Deploy feature X to production",
           "outcome": "cancelled",
           "reason": "User reprioritized to urgent bug fix",
           "switched_to": "Deploy bug fix BUGFIX-123",
           "learnings": "User prioritizes production issues over features"
         }
       ]
     }
   }
   ```

3. **Communicate Direction Change:**
   ```
   ⏸️ Paused: Feature X deployment

   Reason: User requested urgent bug fix BUGFIX-123 instead
   Status: Feature X deployment ready to resume anytime

   Now working on: Bug fix BUGFIX-123 deployment
   ```

## Handoff Template

When handing off to next agent:

```markdown
## Handoff to @[next-agent]

**Task:** [What they need to do]

**Context:**
- [Key context 1]
- [Key context 2]

**What I completed:**
- [Your deliverable 1]
- [Your deliverable 2]

**What you need to do:**
- [Their task 1]
- [Their task 2]

**Files/Docs:**
- [Reference file 1]
- [Reference file 2]

**Success criteria:**
- [How to know when done]

Ready for you to take over!
```

**Example:**
```markdown
## Handoff to @ankur-2.0

**Task:** Validate production deployment

**Context:**
- Deployed commit 3d9840b to production
- Frontend: Vercel deployment successful
- Backend: Railway deployment successful

**What I completed:**
- ✅ Frontend deployed to Vercel
- ✅ Backend deployed to Railway
- ✅ Health checks passing
- ✅ CORS configuration verified

**What you need to do:**
- [ ] Code review of deployed changes
- [ ] Security scan (npm audit)
- [ ] Risk scoring
- [ ] Final APPROVE/REVISE/FAIL verdict

**Files/Docs:**
- Deployment verification: DEPLOYMENT_VERIFICATION_COMPLETE.md
- Commit: 3d9840b
- PR: #123

**Success criteria:**
- APPROVE verdict → deployment complete
- REVISE verdict → create fix plan
- FAIL verdict → rollback required

Ready for you to take over!
```

## Completion Metrics

Track these metrics in agent memory:

```json
{
  "statistics": {
    "total_tasks_completed": 42,
    "success_rate": 0.95,
    "avg_duration_minutes": 8.5,
    "blockers_encountered": 3,
    "blockers_resolved": 3
  }
}
```

## Anti-Patterns (DON'T DO THIS)

### ❌ Verbose Technical Reports
```
Shawar 2.0 has completed staging deployment verification.

[5 paragraphs of technical details...]

Production deployment status: Railway not triggering auto-deploy...

[3 more paragraphs about git commits and verification...]

Would you like me to proceed?
```

**Why bad:** User can't quickly see if work is complete or blocked

### ❌ Burying the Blocker
```
I've deployed to Vercel successfully. Tests passed. Build succeeded.
The Railway service is configured correctly. Environment variables are set.
Oh by the way, Railway webhook failed so I can't deploy to production.
```

**Why bad:** Critical blocker should be stated FIRST

### ❌ No Next Action
```
✅ Deployment complete!
```

**Why bad:** User doesn't know what happens next

**Fix:**
```
✅ Deployment complete!

Next step: Monitor production for 24h
```

## References
- **Delegation Protocol:** `.claude/docs/protocols/delegation-protocol.md`
- **Memory Protocol:** `.claude/docs/protocols/memory-protocol.md`
- **Agent Communication Board:** `AGENT_COMMUNICATION_BOARD.md`
- **Agent Memory:** `.claude/memory/[agent-name]-memory.json`

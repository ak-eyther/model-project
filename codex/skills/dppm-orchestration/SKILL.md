---
name: dppm-orchestration
description: DPPM (Discover, Plan, Prototype, Monitor) planning and orchestration with mandatory plan documents, impact analysis, ASCII diagrams, task breakdowns, evidence gating, context-compaction check-ins, and user test plans. Use for feature planning, fixes, refactors, task creation, or multi-agent orchestration when a structured plan document is required.
---

# DPPM Orchestration Framework

## Mandatory artifacts
- Create a plan document for every request.
- Name the plan file with the feature name (slug-case) and store it in `plans/`.
  - Example: `plans/<feature-name>.md`
- In the plan document, state whether the work is a feature, fix, or refactor.
- Include impact analysis with a list of files/modules to touch and an ASCII diagram.
- Include a user test plan for the feature/fix/refactor.

## Plan document structure (required)
- Title: `<Feature Name> Plan`
- Type: `feature` | `fix` | `refactor`
- Summary: what it is and why
- Scope: in-scope / out-of-scope
- Impact analysis:
  - Files and modules to touch
  - Dependencies and risks
  - ASCII impact diagram
- Plan:
  - Major action items (3-6)
  - Each major item broken into smaller tasks with checkboxes
- Evidence log:
  - Record evidence before moving to the next major item
- Compaction checkpoint:
  - On context compaction, reopen this plan and resume from the last evidenced item
- User test plan:
  - Steps, expected results, and pass criteria

## Execution rules
- Do not start the next major action item until the previous one is completed and recorded with evidence in the plan.
- Keep the plan document as the source of truth and update it after each completed task.

## Impact analysis rules
- List impacted files grouped by area (UI, API, DB, infra, tests).
- Include an ASCII diagram showing components and file impact.
- Keep diagrams ASCII only.

## DPPM phases

### 1. DISCOVER
- Analyze requirements.
- Read project context.
- Identify constraints.
- Assess risks.

### 2. PLAN
- Break down into major action items and smaller tasks.
- Assign specialists when helpful.
- Define dependencies and mitigation steps.
- Create the plan document in `plans/`.

### 3. PROTOTYPE
- Execute tasks in the plan order.
- Update the plan document with evidence after each major item.
- Stop and request clarification when blockers appear.

### 4. MONITOR
- Track progress and blockers.
- Validate scope and quality gates.
- Keep the plan document current.

## Delegation defaults
- Design: @design-owner
- Architecture: @architecture-owner
- Backend: @backend-owner
- Frontend: @frontend-owner
- Testing: @test-owner
- Bug Fix Orchestration: @bugfix-owner
- Deployment: @deploy-owner

## References
- Use `references/plan-template.md` for the standard plan layout.
- Use `references/impact-analysis.md` for file impact analysis and ASCII diagram guidance.
- Use `references/user-test-template.md` to write the user test section.

## Scripts
- From repo root, run `python3 codex/skills/dppm-orchestration/scripts/print_plan_template.py --feature "<Feature Name>" --type feature` to print a plan template.
- From repo root, run `python3 codex/skills/dppm-orchestration/scripts/print_impact_diagram_template.py` to print an ASCII diagram template.
- From repo root, run `python3 codex/skills/dppm-orchestration/scripts/skill_info.py` to show skill metadata.

---
paths: "**/*"
---



# Agent Delegation Rules

## Core Principle

Claude Code acts as a **coordinator**, not an executor. All implementation tasks must be delegated to specialist agents.

## Task Routing Matrix

| Task Type | Primary Agent | Command | What They Do |
|-----------|---------------|---------|--------------|
| Feature Planning | @atharva-2.0 | `/atharva` | Plans features, creates impact analysis, coordinates workflow |
| Code Implementation | @anand-2.0 | `/anand` | Writes backend/full-stack code |
| AI/ML Design | @sama-2.0 | `/sama` | Designs RAG, prompts, model selection |
| Architecture | @vidya-2.0 | `/vidya` | Makes architecture decisions |
| Deployment | @shawar-2.0 | `/shawar` | Deploys to Railway/Vercel |
| Testing | @mokshi-2.0 | `/mokshi` | Runs E2E tests, performance profiling |
| Bug Investigation | @sumit-2.0 | `/sumit` | Investigates bugs, root cause analysis |
| Bug Fix Orchestration | @harshit-2.0 | `/harshit` | Coordinates bug fixes, test verification |
| Quality Review | @ankur-2.0 | `/ankur` | Code review, quality verdicts |
| Design | @varsha-2.0 | `/varsha` | UI/UX design specs |
| Documentation | @talib-2.0 | `/talib` | Documentation updates |
| Memory Management | Memory Expert | `/memory` | Agent memory and experience |
| Quality Validation | Reflection Expert | `/reflection` | Quality validation |

## Delegation Chains

### New Feature Flow
```
User Request → @atharva-2.0 (plan)
            → @vidya-2.0 (architecture, if complex)
            → @sama-2.0 (AI impact, if applicable)
            → @anand-2.0/@hitesh-2.0 (implement)
            → @mokshi-2.0 (test)
            → @ankur-2.0 (review)
            → @shawar-2.0 (deploy)
```

### Bug Fix Flow
```
Bug Report → @sumit-2.0 (investigate)
          → @harshit-2.0 (reproduce)
          → @anand-2.0 (fix)
          → @mokshi-2.0 (verify)
          → @ankur-2.0 (review)
          → @shawar-2.0 (deploy)
```

### Deployment Flow
```
Merge to main → @shawar-2.0 (deploy)
             → @mokshi-2.0 (E2E tests)
             → @ankur-2.0 (validation)
```

## Strict Boundaries

### Never Cross These Lines

- **Atharva** plans, never writes code
- **Anand/Hitesh** implement, never deploy
- **Mokshi** runs tests, never gives quality verdicts
- **Ankur** reviews, never runs tests himself
- **Shawar** deploys, never writes features
- **Sumit** investigates, never fixes bugs
- **Varsha** designs, never implements

### Immediate Delegation Triggers

When you see these requests, delegate immediately:

- "Write code for..." → @anand-2.0
- "Deploy to..." → @shawar-2.0
- "Run tests..." → @mokshi-2.0
- "Fix this bug..." → @sumit-2.0 (investigate) → @anand-2.0 (fix)
- "Review this code..." → @ankur-2.0
- "Design a UI for..." → @varsha-2.0
- "Plan this feature..." → @atharva-2.0

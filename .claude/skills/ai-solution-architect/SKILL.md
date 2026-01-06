---
name: ai-solution-architect
description: Advanced AI Solution Architect wisdom for designing production-grade AI systems. Use when (1) architecting new agents, workflows, or AI features, (2) debugging agent behavior or performance issues, (3) making technology choices (models, frameworks, observability), (4) reviewing AI system designs for production-readiness, (5) planning agent orchestration with LangGraph, (6) designing memory/context systems, (7) optimizing LLM costs and latency, or (8) building email marketing AI optimization systems. This skill thinks like a senior architect at OpenAI/Anthropic - questioning assumptions, anticipating failures, and designing for the AI-native future.
---

# AI Solution Architect (Vidya)

## Core Philosophy

**You are not a software architect who uses AI. You are an AI-native architect.**

The paradigm shift:
- OLD: "I have an application. Where can I add AI?"
- NEW: "I have an AI system. What minimal scaffolding makes it useful?"

## Architectural Wisdom Patterns

Wisdom is encoded as patterns. Each pattern includes:
- **SIGNAL**: What triggers recognition of this pattern
- **WISDOM**: What experienced architects know
- **QUESTIONS**: Not answers - questions to ask
- **ANTI-PATTERN**: What beginners do wrong
- **WHEN TO BREAK**: Rules have exceptions

---

## 1. AGENT DESIGN PATTERNS

### Pattern: Agent Amnesia
**SIGNAL**: "The agent keeps forgetting what we discussed" or "It starts fresh every time"
**WISDOM**: LLMs have no memory between calls. Every "memory" is actually context engineering - putting the right information INTO the prompt.
**QUESTIONS**:
- What state needs to persist across turns?
- Where will this state live? (DB, vector store, session?)
- What's the retrieval strategy? (recency? relevance? both?)
- How do you prevent context bloat over long conversations?
**ANTI-PATTERN**: Assuming the LLM "remembers" previous calls
**WHEN TO BREAK**: Single-turn tools don't need memory infrastructure

### Pattern: God Agent
**SIGNAL**: One agent doing everything, prompt is 2000+ words
**WISDOM**: Multi-agent swarms with clear separation of concerns outperform monolithic agents. Each agent should have ONE job.
**QUESTIONS**:
- What are the distinct responsibilities? (understand, analyze, validate, execute)
- Which agent makes which decisions?
- How do agents communicate state?
- Where are the handoff points?
**ANTI-PATTERN**: Adding more instructions to one mega-prompt
**WHEN TO BREAK**: Simple single-purpose tools (translation, formatting)

### Pattern: Infinite Loop Risk
**SIGNAL**: Agents calling each other, feedback loops, "let the agent figure it out"
**WISDOM**: Always implement circuit breakers. MAX_ITERATIONS, timeouts, and forced exits.
**QUESTIONS**:
- What's the maximum number of iterations?
- What happens when timeout is hit?
- How do you return partial results gracefully?
- Can you explain WHY the loop stopped?
**ANTI-PATTERN**: Trusting the LLM to know when to stop
**WHEN TO BREAK**: Never. Always have circuit breakers.

### Pattern: Tool Explosion
**SIGNAL**: Agent has 20+ tools, takes forever to choose the right one
**WISDOM**: LLMs struggle with large tool sets. Group tools, use meta-tools, or route to specialized sub-agents.
**QUESTIONS**:
- Can tools be grouped by domain?
- Should a router agent select the tool category first?
- Are any tools redundant or overlapping?
- Can tool descriptions be more distinctive?
**ANTI-PATTERN**: Adding every possible tool to one agent
**WHEN TO BREAK**: When tools are truly orthogonal and well-named

---

## 2. LangGraph PATTERNS

> **Deep dive**: See [references/langgraph-patterns.md](references/langgraph-patterns.md)

### Pattern: State Explosion
**SIGNAL**: WorkflowState has 30+ fields, hard to debug
**WISDOM**: State should be minimal. Derive what you can, don't store everything.
**QUESTIONS**:
- Can this field be computed from other fields?
- Is this field used by multiple nodes or just one?
- Would this be better as a tool result than state?
**ANTI-PATTERN**: Treating state as a dumping ground
**WHEN TO BREAK**: When derivation is expensive and caching helps

### Pattern: Edge Spaghetti
**SIGNAL**: Complex conditional routing, hard to visualize the graph
**WISDOM**: Graph should be drawable on a whiteboard. If you can't explain it, simplify it.
**QUESTIONS**:
- Can you draw this graph in 30 seconds?
- Are there more than 3 conditions on any edge?
- Could a sub-graph encapsulate complexity?
**ANTI-PATTERN**: Over-engineering routing logic
**WHEN TO BREAK**: Genuinely complex workflows with many valid paths

### Pattern: Synchronous Trap
**SIGNAL**: Sequential agent calls, each waiting for the previous
**WISDOM**: LangGraph supports parallel execution. Independent evidence gathering should parallelize.
**QUESTIONS**:
- Which nodes are truly dependent on each other?
- Can evidence gathering happen in parallel?
- Where are the natural synchronization points?
**ANTI-PATTERN**: Linear chains when parallelism is possible
**WHEN TO BREAK**: When order genuinely matters (validation after generation)

---

## 3. OBSERVABILITY PATTERNS

> **Deep dive**: See [references/observability-stack.md](references/observability-stack.md)

### Pattern: Silent Failure
**SIGNAL**: Agent returns "plausible but wrong" answers
**WISDOM**: You need to trace INTERMEDIATE reasoning, not just inputs/outputs. LangSmith traces are essential.
**QUESTIONS**:
- Can you replay the exact context that caused bad output?
- Are you logging agent reasoning steps?
- Do you have evals that catch "plausible but wrong"?
- Can you compare traces between good and bad runs?
**ANTI-PATTERN**: Only logging final answers
**WHEN TO BREAK**: Never skip observability for production agents

### Pattern: Metric Mismatch
**SIGNAL**: Tracking latency/cost but not answer quality
**WISDOM**: The stack should be: LangSmith (traces + evals) + Sentry (errors) + PostHog (usage patterns). Each has a distinct purpose.
**QUESTIONS**:
- Are you tracking what users ACTUALLY do after getting an answer?
- Can you correlate errors with specific trace patterns?
- Do you have human evaluation loops?
**ANTI-PATTERN**: Only tracking what's easy to measure
**WHEN TO BREAK**: MVP stage - add quality metrics before scaling

### Pattern: Debugging in Production
**SIGNAL**: "It worked in testing but fails in prod"
**WISDOM**: LangSmith Hub lets you capture production inputs and replay them locally. Build this workflow early.
**QUESTIONS**:
- Can you reproduce any production failure locally?
- Are you sampling production traces?
- Do you have a "replay this conversation" capability?
**ANTI-PATTERN**: Guessing what went wrong from logs
**WHEN TO BREAK**: Never. Reproducibility is non-negotiable.

---

## 4. MODEL INTELLIGENCE PATTERNS

> **Deep dive**: See [references/model-intelligence.md](references/model-intelligence.md)

### Pattern: Wrong Model for the Job
**SIGNAL**: Using GPT-4 for simple classification, slow and expensive
**WISDOM**: Model routing is an architecture decision. Fast models for routing, powerful models for reasoning.
**QUESTIONS**:
- What's the cognitive complexity of this task?
- Is this classification, generation, or reasoning?
- What's the latency budget?
- Can a smaller model handle 80% of cases?
**ANTI-PATTERN**: Using the biggest model for everything
**WHEN TO BREAK**: When consistency matters more than cost

### Pattern: Prompt vs Fine-tune Confusion
**SIGNAL**: "Should we fine-tune a model for this?"
**WISDOM**: Fine-tuning is for FORMAT and STYLE, not knowledge. Prompting + RAG handles most knowledge needs.
**QUESTIONS**:
- Is the issue format/style or knowledge?
- Do you have 1000+ high-quality examples?
- Will the knowledge change frequently?
- Can few-shot examples solve this?
**ANTI-PATTERN**: Fine-tuning to inject knowledge
**WHEN TO BREAK**: When you need consistent format at scale (JSON output)

### Pattern: Context Window Abuse
**SIGNAL**: Stuffing everything into the prompt, hitting token limits
**WISDOM**: Context engineering > context stuffing. What you EXCLUDE matters as much as what you include.
**QUESTIONS**:
- What's the minimum context needed for this query?
- Can you retrieve relevant context dynamically?
- Is there redundant information?
- What's your chunking strategy?
**ANTI-PATTERN**: "More context is always better"
**WHEN TO BREAK**: When reasoning requires seeing the full picture

---

## 5. EMAIL MARKETING AI PATTERNS

> **Deep dive**: See [references/email-marketing-ai.md](references/email-marketing-ai.md)

### Pattern: Metric Confusion
**SIGNAL**: Optimizing for opens when revenue is the goal
**WISDOM**: Conv (conversions) is THE money metric. Revenue = Conv × Payout. Everything else is a proxy.
**QUESTIONS**:
- What metric actually drives revenue?
- Are you optimizing for vanity metrics?
- How does this metric correlate with business outcomes?
**ANTI-PATTERN**: Celebrating high open rates with low conversions
**WHEN TO BREAK**: Never. Follow the money.

### Pattern: Deliverability Blindspot
**SIGNAL**: Great campaign performance, then sudden drop
**WISDOM**: Complaint rate > 0.3% kills deliverability. Google/Yahoo 2024 rules are strict. Prevention > cure.
**QUESTIONS**:
- What's the current complaint rate trend?
- Are you monitoring IP reputation?
- Do you have early warning thresholds?
- Is there a "red flag" that blocks sends?
**ANTI-PATTERN**: Optimizing performance without deliverability guardrails
**WHEN TO BREAK**: Never. Deliverability is existential.

### Pattern: Cold Start Problem
**SIGNAL**: "What should I do with this new offer/list?"
**WISDOM**: New items need explicit handling. Fall back to similar items, flag low confidence, use overall baselines.
**QUESTIONS**:
- How many data points before confident predictions?
- What's the fallback for new items?
- How do you find "similar" items?
- Are you flagging low-confidence recommendations?
**ANTI-PATTERN**: Treating new items like established ones
**WHEN TO BREAK**: When you have strong transfer learning from similar items

---

## 6. MISSION INBOX PATTERNS

> **Deep dive**: See [references/{{PROJECT_PREFIX}}-playbook.md](references/{{PROJECT_PREFIX}}-playbook.md)

### Pattern: Orchestrator Overreach
**SIGNAL**: Orchestrator doing analysis, not just routing
**WISDOM**: Orchestrator is a traffic cop, not a detective. Parse intent → identify gaps → hand off.
**QUESTIONS**:
- Is the Orchestrator making decisions it shouldn't?
- Is intent understanding separate from analysis?
- Are knowledge gaps clearly defined for Analyst?
**ANTI-PATTERN**: Putting analysis logic in Orchestrator
**WHEN TO BREAK**: Never in multi-agent architecture

### Pattern: Evidence Starvation
**SIGNAL**: Judge rejects options, Analyst keeps failing to provide enough
**WISDOM**: Minimum 3 data points for confidence. Evidence loops need exit conditions.
**QUESTIONS**:
- What's the minimum evidence threshold?
- After how many loops do you force a decision?
- Can you give a low-confidence answer vs no answer?
**ANTI-PATTERN**: Infinite evidence loops
**WHEN TO BREAK**: When user explicitly accepts low-confidence answers

### Pattern: Pattern Store vs Raw Data
**SIGNAL**: Querying raw campaigns for every question
**WISDOM**: ChromaDB stores PROCESSED insights. PostgreSQL has raw data. Query patterns first, raw data for fresh questions.
**QUESTIONS**:
- Is this question answerable from stored patterns?
- When was the pattern last updated?
- Does this need fresh calculation?
**ANTI-PATTERN**: Always querying raw data (slow, expensive)
**WHEN TO BREAK**: When patterns are stale or question is novel

---

## Decision Frameworks

### When to Add a New Agent
✅ ADD if:
- Clear separation of concern
- Different LLM needs (speed vs reasoning)
- Independent failure modes
- Parallelizable work

❌ DON'T ADD if:
- Just to "organize" the prompt
- One agent can handle it with tools
- Adds coordination overhead without benefit

### When to Use RAG vs Long Context
| Factor | RAG | Long Context |
|--------|-----|--------------|
| Data changes frequently | ✅ | ❌ |
| Need precise retrieval | ✅ | ❌ |
| Need full document reasoning | ❌ | ✅ |
| Cost-sensitive | ✅ | ❌ |
| Latency-sensitive | ❌ | ✅ |

### When to Break the Rules
Every rule has exceptions. Ask:
1. What's the COST of following this rule here?
2. What's the RISK of breaking it?
3. Is this a temporary exception or permanent?
4. How will I know if breaking it was wrong?

---

## Quick Reference: The Stack

```
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND: Next.js + Vercel                                 │
│  └─ Chat UI, Admin Dashboard                                │
├─────────────────────────────────────────────────────────────┤
│  ORCHESTRATION: LangGraph                                   │
│  └─ Orchestrator → Analyst → Judge                          │
├─────────────────────────────────────────────────────────────┤
│  LLM LAYER                                                  │
│  ├─ Claude Sonnet 4.5: Complex reasoning                    │
│  ├─ GPT-4o-mini: Fast routing/classification                │
│  └─ OpenRouter: Fallbacks, cost optimization                │
├─────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                 │
│  ├─ PostgreSQL: Raw campaigns, rollups                      │
│  ├─ ChromaDB: Patterns, insights, embeddings                │
│  └─ CatBoost: Predictions (EPC, OR, CTR)                    │
├─────────────────────────────────────────────────────────────┤
│  OBSERVABILITY                                              │
│  ├─ LangSmith: Traces, evals, debugging                     │
│  ├─ Sentry: Errors, performance                             │
│  └─ PostHog: Usage analytics, user behavior                 │
├─────────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE: Railway                                    │
│  └─ Backend API, databases                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## How to Use This Skill

**Before designing anything, ask:**
1. What pattern does this situation match?
2. What questions should I be asking?
3. What's the anti-pattern to avoid?
4. When might I break this rule?

**For deep dives, consult:**
- [LangGraph Patterns](references/langgraph-patterns.md) - Advanced graph design
- [Observability Stack](references/observability-stack.md) - LangSmith + Sentry + PostHog
- [Model Intelligence](references/model-intelligence.md) - Selection, routing, fine-tuning
- [Context Engineering](references/context-engineering.md) - What goes INTO prompts
- [Email Marketing AI](references/email-marketing-ai.md) - Domain patterns
- [{{PROJECT_NAME}} Playbook](references/{{PROJECT_PREFIX}}-playbook.md) - System-specific wisdom

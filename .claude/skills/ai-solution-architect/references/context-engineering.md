# Context Engineering: The Art of Prompt Design

## The Fundamental Insight

**Context engineering is MORE important than prompt engineering.**

Prompt engineering: How you ASK for something
Context engineering: What INFORMATION the model sees

A perfect prompt with wrong context = bad output
A simple prompt with right context = great output

---

## Context Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  SYSTEM PROMPT (persistent context)                         │
│  - Agent identity and role                                  │
│  - Core capabilities and constraints                        │
│  - Output format requirements                               │
├─────────────────────────────────────────────────────────────┤
│  RETRIEVED CONTEXT (dynamic)                                │
│  - Relevant data from databases                             │
│  - Pattern matches from vector store                        │
│  - Previous conversation turns                              │
├─────────────────────────────────────────────────────────────┤
│  USER QUERY (current input)                                 │
│  - What the user is asking                                  │
│  - Extracted entities                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## What to Include

### Always Include

✅ **Role clarity**: "You are the Analyst agent..."
✅ **Task scope**: "Your job is to gather evidence, NOT make recommendations"
✅ **Output format**: "Respond with JSON: {evidence: [...], draft_options: [...]}"
✅ **Constraints**: "Maximum 4 options. Each must have rationale."
✅ **Examples**: 1-2 high-quality examples of expected output

### Include When Relevant

✅ **User context**: "User is optimizing for GM_30D_Opener list"
✅ **Retrieved data**: Performance metrics, patterns, health status
✅ **Conversation history**: Previous turns (summarized if long)
✅ **Business rules**: Compliance thresholds, safety limits

### Never Include

❌ **Redundant instructions**: Don't repeat what's obvious
❌ **All possible scenarios**: Only what's relevant now
❌ **Raw data dumps**: Summarize, don't dump
❌ **Implementation details**: Model doesn't need to know how tools work

---

## Context Window Management

### Token Budget

```
Claude Sonnet: 200K tokens
Recommended usage:
  System prompt:     ~2K (1%)
  Retrieved context: ~10K (5%)
  Conversation:      ~5K (2.5%)
  Response space:    ~4K (2%)
  Buffer:            ~179K (89.5%)
```

### Chunking Strategies

**For campaign data:**
```python
# BAD: Include all 3,963 campaigns
context = all_campaigns  # 500K tokens!

# GOOD: Include relevant summary
context = f"""
Top 5 performers for {list_name}:
{top_5_summary}

Recent trends (7d):
{trend_summary}

Relevant patterns:
{pattern_summary}
"""
```

**For conversation history:**
```python
# BAD: Include all messages
history = all_messages  # Grows unbounded

# GOOD: Sliding window + summary
if len(messages) > 10:
    history = summarize(messages[:-5]) + messages[-5:]
```

---

## Retrieval Strategies

### When to Query PostgreSQL

- Specific date range metrics
- Compliance calculations
- Fresh aggregations
- Exact record lookups

### When to Query ChromaDB

- Semantic pattern search
- Similar campaign finding
- Historical insight retrieval
- Recommendation context

### Hybrid Approach

```python
# 1. Get fresh metrics from PostgreSQL
metrics = await get_list_health(list_name, days=30)

# 2. Get relevant patterns from ChromaDB
patterns = await search_patterns(
    f"patterns for {list_name}",
    filter={"tier": "entity"}
)

# 3. Combine into context
context = f"""
Current Health (last 30 days):
{format_metrics(metrics)}

Relevant Patterns:
{format_patterns(patterns)}
"""
```

---

## Prompt Templates

### Orchestrator Prompt

```
You are the Orchestrator agent for {{PROJECT_NAME}} email optimization.

YOUR JOB:
1. Understand the user's intent (what do they want?)
2. Extract entities (list name, offer, timeframe)
3. Identify knowledge gaps (what does Analyst need to find?)

OUTPUT FORMAT:
{
  "user_intent": "...",
  "key_entities": {"list_name": "...", "offer_id": "...", "timeframe": "..."},
  "knowledge_gaps": ["...", "..."],
  "orchestrator_message": "..."
}

RULES:
- Do NOT analyze data yourself
- Do NOT make recommendations
- Just understand and route

USER QUERY: {query}
```

### Analyst Prompt

```
You are the Analyst agent for {{PROJECT_NAME}}.

YOUR JOB:
1. Investigate the knowledge gaps identified by Orchestrator
2. Call tools to gather evidence
3. Generate 2-4 draft campaign options

CONTEXT FROM ORCHESTRATOR:
{orchestrator_output}

AVAILABLE TOOLS:
- get_list_health: Check deliverability status
- get_top_performers: Find best performing combinations
- get_patterns: Search for relevant patterns
- compare_entities: Compare two offers/lists

EVIDENCE GATHERED:
{evidence}

NOW: Generate draft options based on evidence.
Each option needs: label, title, setup, metrics, risk, rationale
```

---

## Anti-Patterns

### Context Poisoning

❌ **Too much irrelevant data**
```python
# BAD: Include everything
context = all_campaigns + all_patterns + all_history
# Model gets confused, focuses on wrong things
```

✅ **Curated, relevant context**
```python
# GOOD: Only what's needed
context = relevant_metrics + matching_patterns
```

### Context Contradiction

❌ **Conflicting instructions**
```
You must always recommend the highest performing option.
...
Consider risk and deliverability equally important.
```

✅ **Clear hierarchy**
```
PRIORITY ORDER:
1. Deliverability safety (hard constraint)
2. Performance potential (optimize)
3. Risk tolerance (consider)
```

### Context Staleness

❌ **Outdated information**
```
# Pattern cached 90 days ago
patterns = get_cached_patterns()  # Stale!
```

✅ **Fresh when it matters**
```
# Check cache freshness
if pattern.cached_at < 7_days_ago:
    pattern = await refresh_pattern()
```

---

## {{PROJECT_NAME}} Context Design

### Orchestrator Context
```
System: 500 tokens
├── Role definition
├── Output format
└── Routing rules

User query: 50 tokens
Total: ~550 tokens
```

### Analyst Context
```
System: 1000 tokens
├── Role definition
├── Tool descriptions
├── Output format
└── Quality requirements

Orchestrator output: 200 tokens
Retrieved evidence: 2000 tokens (varies)
Total: ~3200 tokens
```

### Judge Context
```
System: 800 tokens
├── Role definition
├── Compliance thresholds
├── Validation rules
└── Output format

Analyst output: 1500 tokens
Total: ~2300 tokens
```

---

## Key Principles

1. **Less is more**: Curate, don't dump
2. **Relevance over recency**: Old relevant > new irrelevant
3. **Structure matters**: Format context for LLM scanning
4. **Examples teach**: One good example > many rules
5. **Test with traces**: See what the model actually receives

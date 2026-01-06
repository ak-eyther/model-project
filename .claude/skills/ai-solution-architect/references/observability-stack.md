# Observability Stack: LangSmith + Sentry + PostHog

## The Three Pillars

| Tool | Purpose | What It Answers |
|------|---------|-----------------|
| **LangSmith** | Agent tracing & evals | "Why did the agent give this answer?" |
| **Sentry** | Errors & performance | "What broke and why?" |
| **PostHog** | User analytics | "How are users actually using this?" |

These are NOT interchangeable. Each serves a distinct purpose.

---

## LangSmith Deep Dive

### What to Trace

```python
from langsmith import traceable

@traceable(name="orchestrator_node")
async def orchestrator_node(state: dict) -> dict:
    # All LLM calls inside are automatically traced
    ...
```

### Trace Hierarchy

```
Conversation
└── LangGraph Run
    ├── Orchestrator Node
    │   ├── LLM Call (intent extraction)
    │   └── Entity Extraction
    ├── Analyst Node
    │   ├── Tool: get_list_health
    │   ├── Tool: get_top_performers
    │   └── LLM Call (generate options)
    └── Judge Node
        ├── Compliance Check
        └── LLM Call (finalize)
```

### Key Metrics to Track

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Orchestrator latency | <2s | 2-5s | >5s |
| Analyst latency | <10s | 10-20s | >20s |
| Total workflow | <30s | 30-60s | >60s |
| LLM token cost | <$0.05 | $0.05-0.20 | >$0.20 |

### Evaluation Patterns

```python
from langsmith.evaluation import evaluate

# Define evaluator
def answer_quality(run, example):
    # Check if answer addresses the question
    return {"score": 0.8, "reasoning": "..."}

# Run evaluation
evaluate(
    target=my_agent,
    data="email-optimization-evals",
    evaluators=[answer_quality],
)
```

**Critical Evals for Email Marketing AI:**
1. **Metric Accuracy**: Do predicted numbers match reality?
2. **Recommendation Safety**: No deliverability red flags ignored?
3. **Completeness**: Are all requested components addressed?
4. **Confidence Calibration**: Is HIGH confidence actually better?

### Debugging Workflow

1. Find bad output in production
2. Get trace ID from response
3. Open trace in LangSmith
4. Walk through each node:
   - What was the input state?
   - What did the LLM see?
   - What did it output?
   - Where did reasoning go wrong?
5. Add to evaluation dataset
6. Fix and verify with eval

---

## Sentry Deep Dive

### What to Track

```python
import sentry_sdk

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=0.1,  # 10% of requests
    profiles_sample_rate=0.1,
    environment="production",
)

# Tag agent errors
with sentry_sdk.push_scope() as scope:
    scope.set_tag("agent", "analyst")
    scope.set_tag("tool", "get_list_health")
    scope.set_context("state", {"list_name": list_name})
    # ... operation that might fail
```

### Error Categories

| Category | Example | Action |
|----------|---------|--------|
| **LLM Timeout** | OpenAI 30s timeout | Retry with backoff |
| **LLM Rate Limit** | 429 error | Queue, backoff |
| **DB Connection** | PostgreSQL pool exhausted | Connection pooling |
| **Tool Failure** | Invalid parameters | Validate before call |
| **State Corruption** | Missing required field | Schema validation |

### Alerts to Configure

```
CRITICAL (page):
- Error rate > 10% for 5 minutes
- LLM API completely down
- Database unreachable

WARNING (Slack):
- Error rate > 5% for 10 minutes
- Latency P95 > 60 seconds
- Cost spike > 2x average
```

### Sentry + LangSmith Integration

```python
try:
    result = await agent.ainvoke(state)
except Exception as e:
    sentry_sdk.capture_exception(e)
    sentry_sdk.set_context("langsmith", {
        "trace_url": f"https://smith.langchain.com/runs/{run_id}"
    })
    raise
```

---

## PostHog Deep Dive

### Events to Track

```javascript
// Frontend events
posthog.capture('query_submitted', {
    query_length: query.length,
    has_list_name: Boolean(extractedList),
});

posthog.capture('recommendation_viewed', {
    option_count: options.length,
    recommended: recommendedOption,
});

posthog.capture('recommendation_accepted', {
    option_chosen: chosenOption,
    was_recommended: chosenOption === recommendedOption,
});
```

### Key Funnels

```
Query Submitted
    → Options Generated (conversion: 95%)
    → Option Viewed (conversion: 80%)
    → Option Accepted (conversion: 60%)
    → Campaign Created (conversion: 40%)
```

### User Segments

| Segment | Definition | Insight |
|---------|------------|---------|
| Power Users | >10 queries/day | Feature requests |
| Skeptics | Never accept recommendations | Trust issues |
| Speed Users | <5s per decision | Optimize latency |
| Explorers | Use compare features | Add more comparisons |

### Session Recordings

Enable for:
- Users who gave thumbs down
- Sessions with errors
- New feature usage

Disable for:
- High-volume routine users
- Privacy-sensitive operations

---

## Integration Pattern

```
User Query
    │
    ├──▶ PostHog: query_submitted
    │
    ▼
┌─────────────────┐
│   LangGraph     │ ◀── LangSmith traces all nodes
│   Workflow      │
└────────┬────────┘
         │
         ├──▶ Sentry: errors, performance
         │
         ▼
Response to User
    │
    ├──▶ PostHog: response_delivered
    │
    ▼
User Feedback
    │
    ├──▶ PostHog: thumbs_up/thumbs_down
    │
    └──▶ LangSmith: feedback attached to trace
```

---

## Dashboard Recommendations

### LangSmith Dashboard
- Trace latency distribution
- Error rate by agent
- Token usage trends
- Eval scores over time

### Sentry Dashboard
- Error rate (last 24h)
- Most common errors
- Performance bottlenecks
- Release comparison

### PostHog Dashboard
- Daily active users
- Query → Acceptance funnel
- Feature usage breakdown
- User satisfaction (thumbs up rate)

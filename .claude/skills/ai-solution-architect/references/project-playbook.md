# {{PROJECT_NAME}} Playbook: System-Specific Wisdom

## System Overview

{{PROJECT_NAME}} is a 3-agent LangGraph system for domain-specific optimization:

```
User Query → Orchestrator → Analyst → Judge → Response
                              ↑         │
                              └─────────┘ (evidence loop)
```

**Goal**: Replace manual analysis with AI-assisted planning.

---

## Agent Responsibilities

### Orchestrator: The Traffic Cop

**DOES:**
- Parse user intent
- Extract entities (list, offer, timeframe)
- Identify what Analyst needs to investigate

**DOES NOT:**
- Analyze data
- Make recommendations
- Call database tools

**Output template:**
```json
{
  "user_intent": "Find best campaign setup for tomorrow",
  "key_entities": {
    "list_name": "{{EXAMPLE_LIST_NAME}}",
    "offer_id": null,
    "timeframe": "7d"
  },
  "knowledge_gaps": [
    "Current health status of {{EXAMPLE_LIST_NAME}}",
    "Top performing items for this segment",
    "Any quality or fatigue signals"
  ],
  "orchestrator_message": "Please investigate list health and top performers"
}
```

### Analyst: The Detective

**DOES:**
- Call tools to gather evidence
- Synthesize findings
- Generate 2-4 draft options

**DOES NOT:**
- Make final recommendations
- Override compliance rules
- Skip evidence gathering

**Tool priority (replace with your tool names):**
1. `{{TOOL_HEALTH_CHECK}}` - Always first for safety-sensitive questions
2. `{{TOOL_TOP_PERFORMERS}}` - For recommendation questions
3. `{{TOOL_PATTERNS}}` - For pattern-based insights
4. `{{TOOL_COMPARE}}` - For comparison questions

### Judge: The Quality Gate

**DOES:**
- Validate evidence sufficiency (min 3 data points)
- Check compliance thresholds
- Finalize options with risk levels
- Pick recommended option

**DOES NOT:**
- Gather new evidence (requests from Analyst)
- Override safety limits
- Approve RED deliverability status

---

## Data Architecture

### PostgreSQL: Source of Truth

**Tables used:**
| Table | Purpose |
|-------|---------|
| `{{TABLE_ROLLUP_COMBO}}` | Pre-aggregated performance metrics |
| `{{TABLE_ROLLUP_LIST}}` | Segment-level aggregates |
| `{{TABLE_RAW_EVENTS}}` | Raw event records (fallback) |

**Query patterns:**
```sql
-- List health
SELECT SUM(sends), SUM(complaints), SUM(bounces)
FROM {{TABLE_ROLLUP_LIST}}
WHERE segment_name = :segment_name
AND event_date >= CURRENT_DATE - INTERVAL '{{LOOKBACK_DAYS}} days'

-- Top performers
SELECT item_id, AVG(primary_metric) as avg_metric
FROM {{TABLE_ROLLUP_COMBO}}
WHERE segment_name = :segment_name
GROUP BY item_id
ORDER BY avg_metric DESC
LIMIT 5
```

### ChromaDB: Pattern Memory

**Collections:**
| Collection | Content |
|------------|---------|
| `{{COLLECTION_PATTERNS}}` | Discovered synergies, anti-patterns |
| `{{COLLECTION_INSIGHTS}}` | Generated insights (reusable) |
| `{{COLLECTION_PERFORMANCE}}` | Cached performance data with TTL |

**Pattern types:**
- `{{PATTERN_FATIGUE}}` - Fatigue signals for segments
- `{{PATTERN_HIDDEN_GEM}}` - Underutilized high performers
- `{{PATTERN_SYNERGY}}` - Pairs that work well together
- `{{PATTERN_ANTI}}` - Pairs to avoid

---

## Compliance Thresholds

### Traffic Light System (replace thresholds)

| Status | Complaint Rate | Bounce Rate | Action |
|--------|----------------|-------------|--------|
| 🟢 GREEN | <0.1% | <2% | Safe to send |
| 🟡 YELLOW | 0.1-0.3% | 2-5% | Proceed with caution |
| 🔴 RED | >0.3% | >5% | DO NOT SEND |

**Hard rule**: Judge MUST block RED status recommendations.

### Validation Checks

```python
def validate_option(option, list_health):
    issues = []
    
    if list_health["complaint_rate"] > 0.003:
        issues.append("CRITICAL: Complaint rate exceeds safe threshold")
        option["blocked"] = True
    
    if list_health["bounce_rate"] > 0.05:
        issues.append("CRITICAL: Bounce rate too high")
        option["blocked"] = True
    
    if list_health["sends_7d"] < 1000:
        issues.append("WARNING: Limited recent data")
        option["confidence"] = "LOW"
    
    return issues
```

---

## Common Query Patterns

### Planning Query
**User**: "What should I send to {{EXAMPLE_LIST_NAME}} tomorrow?"

**Flow**:
1. Orchestrator extracts: segment={{EXAMPLE_LIST_NAME}}, timeframe=recent
2. Analyst: {{TOOL_HEALTH_CHECK}} → {{TOOL_TOP_PERFORMERS}} → {{TOOL_PATTERNS}}
3. Judge: Validate 3 options, recommend safest high performer

### Comparison Query
**User**: "Compare {{EXAMPLE_ITEM_A}} vs {{EXAMPLE_ITEM_B}} for {{EXAMPLE_LIST_NAME}}"

**Flow**:
1. Orchestrator extracts: list, offer1, offer2
2. Analyst: {{TOOL_COMPARE}}(item_a, item_b, segment)
3. Judge: Format comparison, flag winner with caveats

### Diagnostic Query
**User**: "Why did yesterday's campaign underperform?"

**Flow**:
1. Orchestrator: diagnostic intent, yesterday's date
2. Analyst: {{TOOL_TRENDS}} → {{TOOL_PATTERNS}} (look for fatigue, anti-patterns)
3. Judge: Synthesize diagnosis, suggest fixes

### Health Query
**User**: "Is {{EXAMPLE_LIST_NAME}} safe to send today?"

**Flow**:
1. Orchestrator: health check intent
2. Analyst: {{TOOL_HEALTH_CHECK}}, {{TOOL_DELIVERABILITY}}
3. Judge: Return traffic light status with explanation

---

## Circuit Breakers

### Constants (MUST NOT CHANGE)

```python
MAX_ITERATIONS = 5          # Total workflow cycles
MAX_EVIDENCE_LOOPS = 3      # Judge → Analyst loops
MAX_CLARIFICATIONS = 2      # User clarification requests
EARLY_CUTOFF_SECONDS = 70   # Timeout for partial results
```

### Timeout Handling

When timeout approaches (>60s):
1. Return partial results if any
2. Flag incomplete analysis
3. Suggest user retry with simpler query

### Evidence Loop Exit

After 3 evidence loops:
1. Force decision with available evidence
2. Flag low confidence
3. Explain what's missing

---

## Debugging Checklist

### When Agent Returns Wrong Answer

1. **Check LangSmith trace**
   - What did Orchestrator extract?
   - What tools did Analyst call?
   - What evidence did Judge see?

2. **Check data quality**
   - Is the data in PostgreSQL correct?
   - Are patterns in ChromaDB stale?
   - Is there enough data for this query?

3. **Check prompt**
   - Did the agent get the right context?
   - Was output format clear?
   - Were examples helpful?

### When Agent Is Slow

1. **Check tool latency**
   - Which tool is slowest?
   - Is PostgreSQL query optimized?
   - Is ChromaDB search efficient?

2. **Check LLM calls**
   - How many LLM calls per node?
   - Is prompt too long?
   - Wrong model for task?

3. **Check loops**
   - How many evidence loops?
   - Why is Judge requesting more?

---

## Learned Patterns (To Be Updated)

### What Works
- Memory-first architecture (patterns > raw queries)
- Clear separation of agent concerns
- Compliance as hard gate, not suggestion

### What Failed
- (Add failures as they're discovered)

### User Feedback Patterns
- (Track what users thumbs up/down)

### Prediction Accuracy
- (Track predicted vs actual performance)

---

## Future Enhancements

### Phase 2: Guardian Agent
- Monitor system health 24/7
- Auto-fix common issues
- Alert on anomalies

### Phase 3: Planning Advisor
- Daily 6AM recommendations
- Learn from human overrides
- Capture team's "gut feel" in patterns

### Phase 4: Fine-tuned Models
- Train on Zappian's specific data
- Faster, cheaper inference
- Consistent output format

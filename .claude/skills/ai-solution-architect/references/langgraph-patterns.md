# LangGraph Architecture Patterns

## Core Concepts

### StateGraph vs MessageGraph
**StateGraph**: Full control over state schema. Use for complex workflows.
**MessageGraph**: Simplified, message-based. Use for simple chatbots.

**Decision**: {{PROJECT_NAME}} uses StateGraph because:
- Multiple agents need shared context
- Complex routing logic
- Evidence accumulation across nodes

### State Design Principles

```python
# GOOD: Minimal, purposeful state
class WorkflowState(TypedDict):
    query: str                    # Input
    user_intent: str              # Orchestrator output
    knowledge_gaps: List[str]     # What to investigate
    evidence: List[Dict]          # Analyst findings
    final_options: List[Dict]     # Judge output
    status: str                   # Workflow status

# BAD: Kitchen sink state
class BadState(TypedDict):
    query: str
    query_lowercase: str          # Derivable
    query_length: int             # Derivable
    timestamp: datetime           # Put in metadata
    all_campaigns: List           # Too large, query on demand
    intermediate_thoughts: List   # Debugging only, use traces
```

### Routing Patterns

**Pattern 1: Simple Sequential**
```
START → A → B → C → END
```
Use when: Order is fixed, no conditionals.

**Pattern 2: Conditional Exit**
```
START → A → B (if needs_clarification → END, else → C) → END
```
Use when: Early exit conditions exist.

**Pattern 3: Feedback Loop**
```
START → A → B → C (if needs_more → B, else → END)
```
Use when: Iteration improves quality. ALWAYS add circuit breaker.

**Pattern 4: Parallel Fan-out**
```
START → A → [B, C, D parallel] → E (aggregator) → END
```
Use when: Independent work can parallelize.

---

## Advanced Patterns

### Checkpointing & Persistence

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(DATABASE_URL)
graph = workflow.compile(checkpointer=checkpointer)

# Resume from checkpoint
config = {"configurable": {"thread_id": session_id}}
result = await graph.ainvoke(state, config)
```

**When to use**: 
- Long-running workflows
- Human-in-the-loop approvals
- Resumable conversations

### Subgraphs

```python
# Define subgraph for evidence gathering
evidence_subgraph = StateGraph(EvidenceState)
evidence_subgraph.add_node("search_db", search_db_node)
evidence_subgraph.add_node("search_patterns", search_patterns_node)
# ...compile

# Use in main graph
main_graph.add_node("gather_evidence", evidence_subgraph.compile())
```

**When to use**:
- Reusable workflow components
- Complex logic that deserves encapsulation
- Testing subsystems independently

### Human-in-the-Loop

```python
graph.add_node("human_approval", human_approval_node)
graph.add_conditional_edges(
    "generate_recommendation",
    lambda s: "human_approval" if s["requires_approval"] else "execute"
)
```

**Pattern**: 
1. Generate recommendation
2. Pause for human approval
3. Resume on approval signal

---

## Debugging LangGraph

### Using LangSmith Traces

Every node execution creates a trace. Look for:
- Which node failed?
- What was the state at failure?
- How long did each node take?
- What was the LLM prompt/response?

### Common Issues

**Issue: Node not executing**
Check: Edge conditions, previous node output

**Issue: Infinite loop**
Check: Circuit breaker constants, loop counters

**Issue: State not updating**
Check: Return statement in node, state key names

**Issue: Timeout**
Check: LLM latency, database queries, external APIs

---

## {{PROJECT_NAME}} Specific

### The Three-Agent Pattern

```
┌─────────────────┐
│   Orchestrator  │  Understand intent, identify gaps
└────────┬────────┘
         │ Always
         ▼
┌─────────────────┐
│     Analyst     │  Gather evidence, draft options
└────────┬────────┘
         │ Conditional
         ▼
┌─────────────────┐
│      Judge      │  Validate, finalize, recommend
└────────┬────────┘
         │ May loop back to Analyst
         ▼
       [END]
```

### Circuit Breaker Constants

```python
MAX_ITERATIONS = 5          # Total workflow runs
MAX_EVIDENCE_LOOPS = 3      # Judge → Analyst loops
MAX_CLARIFICATIONS = 2      # User clarification requests
EARLY_CUTOFF_SECONDS = 70   # Timeout for partial results
```

### State Flow

| Field | Set By | Used By |
|-------|--------|---------|
| `query` | User | Orchestrator |
| `user_intent` | Orchestrator | Analyst |
| `knowledge_gaps` | Orchestrator | Analyst |
| `evidence` | Analyst | Judge |
| `draft_options` | Analyst | Judge |
| `final_options` | Judge | Response |
| `recommended_option` | Judge | Response |
| `needs_more_evidence` | Judge | Router |
| `needs_clarification` | Analyst | Router |

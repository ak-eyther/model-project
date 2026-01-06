# Model Intelligence: Selection, Routing & Optimization

## Model Landscape (2025)

### Tier 1: Frontier Reasoning
| Model | Strengths | Weaknesses | Cost |
|-------|-----------|------------|------|
| Claude Opus 4.5 | Deep reasoning, nuance | Slow, expensive | $$$$$ |
| GPT-4o | Fast, reliable | Less creative | $$$$ |
| Claude Sonnet 4.5 | Balanced | - | $$$ |

### Tier 2: Fast & Capable
| Model | Strengths | Weaknesses | Cost |
|-------|-----------|------------|------|
| GPT-4o-mini | Fast, cheap, good enough | Less reasoning | $ |
| Claude Haiku 4.5 | Very fast | Simpler tasks only | $ |
| Gemini Flash | Multimodal, fast | Less consistent | $ |

### Tier 3: Specialized
| Model | Use Case |
|-------|----------|
| Fine-tuned GPT-4o-mini | Consistent JSON output |
| Embedding models | Vector search |
| Whisper | Audio transcription |

---

## Model Routing Strategy

### By Task Complexity

```
┌─────────────────────────────────────────────────────────────┐
│  USER QUERY                                                 │
└─────────────────────────────┬───────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │  Simple  │   │  Medium  │   │ Complex  │
        │ Routing  │   │ Analysis │   │ Reasoning│
        └────┬─────┘   └────┬─────┘   └────┬─────┘
             │              │              │
             ▼              ▼              ▼
        GPT-4o-mini    Claude Sonnet   Claude Opus
        (fast, cheap)   (balanced)     (when needed)
```

### Task Classification

| Task Type | Model Choice | Why |
|-----------|--------------|-----|
| Intent classification | GPT-4o-mini | Fast, structured |
| Entity extraction | GPT-4o-mini | Pattern matching |
| Evidence synthesis | Claude Sonnet | Nuance needed |
| Option generation | Claude Sonnet | Creative + logical |
| Compliance validation | GPT-4o-mini | Rule-based |
| Final recommendation | Claude Sonnet | Requires judgment |
| Complex comparisons | Claude Opus | Deep reasoning |

---

## Prompt vs Fine-tuning Decision

### When to Prompt Engineer

✅ Use prompting when:
- Requirements change frequently
- You need flexibility
- Dataset is small (<1000 examples)
- Knowledge is the issue (use RAG)
- Iteration speed matters

### When to Fine-tune

✅ Use fine-tuning when:
- Consistent output FORMAT needed
- High volume (cost optimization)
- Specific STYLE required
- 1000+ high-quality examples
- Performance is bottleneck

### Common Mistakes

❌ **Don't fine-tune for knowledge**
Knowledge changes. Fine-tuning bakes in stale data.
Use RAG or prompting for knowledge.

❌ **Don't fine-tune too early**
Get prompting working first. Fine-tune to optimize.

❌ **Don't expect fine-tuning to fix bad prompts**
If prompt doesn't work, fine-tuning won't magically fix it.

---

## Cost Optimization

### Token Economics

```
Claude Sonnet 4.5:
  Input:  $3.00 / 1M tokens
  Output: $15.00 / 1M tokens

GPT-4o-mini:
  Input:  $0.15 / 1M tokens
  Output: $0.60 / 1M tokens
```

**Cost ratio: Sonnet is ~20x more expensive than mini**

### Optimization Strategies

**1. Prompt Caching**
```python
# Cache system prompt (Claude feature)
# Reuse across conversations
cached_prompt = cache_prompt(system_prompt)
```

**2. Model Cascade**
```python
# Try cheap model first
response = await gpt4_mini(query)
if response.confidence < 0.8:
    response = await claude_sonnet(query)
```

**3. Response Caching**
```python
# Cache identical queries
cache_key = hash(query + context)
if cache_key in redis:
    return redis.get(cache_key)
```

**4. Shorter Prompts**
- Remove redundant instructions
- Use examples efficiently
- Compress context

### Cost Monitoring

```python
# Track per-conversation cost
total_cost = (
    input_tokens * input_price +
    output_tokens * output_price
)

if total_cost > BUDGET_WARNING:
    alert("High cost conversation", conversation_id)
```

---

## Latency Optimization

### Latency Breakdown

```
User Query → Response

Network (fixed)           ~100ms
LLM Orchestrator call     ~1-2s
LLM Analyst call          ~3-5s
Database queries          ~100-500ms
LLM Judge call            ~2-3s
Network (fixed)           ~100ms
─────────────────────────────────
Total                     ~7-12s
```

### Optimization Strategies

**1. Streaming Responses**
```python
# Start showing response while generating
async for chunk in llm.astream(prompt):
    yield chunk
```

**2. Parallel Tool Calls**
```python
# Instead of sequential
result1 = await tool1()
result2 = await tool2()

# Use parallel
result1, result2 = await asyncio.gather(tool1(), tool2())
```

**3. Smaller Models for Classification**
```python
# Use mini for routing (100ms)
# Use Sonnet only for generation (3s)
intent = await gpt4_mini.classify(query)  # Fast
response = await sonnet.generate(intent)  # Only when needed
```

**4. Precomputation**
- Daily rollup tables
- Pattern pre-extraction
- Cached embeddings

---

## OpenRouter Integration

### Why OpenRouter?

- Single API for multiple models
- Automatic fallbacks
- Cost optimization
- Rate limit handling

### Configuration

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # Or any model
    messages=[...],
)
```

### Fallback Strategy

```python
FALLBACK_CHAIN = [
    "anthropic/claude-3.5-sonnet",
    "openai/gpt-4o",
    "anthropic/claude-3-haiku",
]

for model in FALLBACK_CHAIN:
    try:
        return await call_model(model, prompt)
    except RateLimitError:
        continue
raise AllModelsFailed()
```

---

## {{PROJECT_NAME}} Model Usage

### Current Configuration

| Agent | Model | Why |
|-------|-------|-----|
| Orchestrator | GPT-4o-mini | Fast routing, structured output |
| Analyst | Claude Sonnet | Evidence synthesis needs nuance |
| Judge | Claude Sonnet | Compliance + judgment |

### Cost Projection

```
Per conversation (average):
  Orchestrator: ~500 tokens → $0.001
  Analyst:      ~2000 tokens → $0.04
  Judge:        ~1000 tokens → $0.02
  ─────────────────────────────────
  Total:                       $0.06

Monthly (500 conversations):   $30
```

### Future Optimization

1. **Cache common queries** (50% hit rate → 50% cost reduction)
2. **Batch similar queries** (reduce overhead)
3. **Fine-tune for JSON** (faster, cheaper for structured output)

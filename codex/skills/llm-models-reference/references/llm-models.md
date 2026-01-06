# OpenAI Models Reference

**Last Updated:** 2026-01-07
**Update Protocol:** If >30 days old, verify with WebSearch before critical decisions.

---

## OPENAI MODELS

### Model Lineup

| Model | ID | Context | Pricing (M tokens) | API |
|-------|----|---------|--------------------|-----|
| **GPT-5** | gpt-5 | Large | $1.25 / $10 | Responses |
| **GPT-5-mini** | gpt-5-mini-2025-08-07 | Large | $0.25 / $2 | Responses |
| GPT-5-nano | gpt-5-nano | Large | Lowest | Responses |
| **GPT-5.2** | gpt-5.2 | 1M+ | Premium | Responses |
| **o3** | o3 | Varies | Higher | Responses |
| **o4-mini** | o4-mini | Varies | Lower | Responses |

### Capabilities Matrix

| Capability | GPT-5/mini/nano | GPT-5.2 | o3/o4-mini |
|------------|-----------------|---------|------------|
| Function Calling | ✅ | ✅ | ✅ |
| Web Search | ✅ | ✅ | ✅ |
| File Search | ✅ | ✅ | ✅ |
| Code Interpreter | ✅ | ✅ | ✅ |
| Image Generation | ❌ | ✅ | ✅ |
| MCP Support | ✅ | ✅ | ✅ |
| Computer Use | ❌ | ❌ | ❌ |
| Local Shell | ❌ | ✅ | ❌ |
| Verbosity Param | ✅ (low/medium/high) | ✅ | ❌ |
| Reasoning Effort | ✅ (minimal to high) | ✅ | ✅ |

### Best For

- **GPT-5**: Complex coding, front-end generation, debugging
- **GPT-5-mini**: Clear tasks, budget-friendly ($0.25/M input)
- **GPT-5.2**: Latest frontier, long-running agents, local shell access
- **o3/o4-mini**: Math, science, deep reasoning

---

## OPENAI TOOL USE - HOW TO

**API:** Responses API (Chat Completions deprecated for new features)

**Tool Definition Schema:**
```json
{
  "type": "function",
  "name": "get_weather",
  "description": "Get temperature for location",
  "parameters": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "City name"}
    },
    "required": ["location"],
    "additionalProperties": false
  },
  "strict": true
}
```

**Python SDK Example (Responses API):**
```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="gpt-5-mini-2025-08-07",
    input="Weather in NYC?",
    tools=[{
        "type": "function",
        "name": "get_weather",
        "description": "Get temperature for location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
            "additionalProperties": false
        },
        "strict": true
    }]
)
```

**Built-in Tools (no definition needed):**
- `web_search` - Search the web
- `file_search` - Search uploaded files
- `code_interpreter` - Execute Python code
- MCP servers - Connect external services

**Custom Tools:**
Set `type: "custom"` to send raw text (SQL, shell commands, prose) instead of JSON.

**Verbosity & Reasoning Control:**
```python
response = client.responses.create(
    model="gpt-5-mini-2025-08-07",
    input="Explain quantum computing",
    verbosity="low",  # low, medium, high
    reasoning_effort="minimal"  # minimal, low, medium, high
)
```

---

## OPENAI RESPONSES API (RECOMMENDED)

### Why Responses API over Chat Completions

| Benefit | Details |
|---------|---------|
| Better performance | 3% improvement in SWE-bench with same prompt |
| Lower costs | 40-80% cache utilization improvement |
| Stateful context | `store: true` for turn-to-turn preservation |
| Agentic by default | Built-in tool loop, multiple tools per request |
| Future-proof | New features only in Responses API |

### Basic Usage

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    instructions="You are a helpful assistant.",
    input="Hello!"
)
print(response.output_text)
```

### Multi-turn with previous_response_id

```python
# First turn - enable storage
res1 = client.responses.create(
    model="gpt-5",
    input="What is the capital of France?",
    store=True
)

# Subsequent turns - pass previous_response_id
res2 = client.responses.create(
    model="gpt-5",
    input="And its population?",
    previous_response_id=res1.id,
    store=True
)
```

### Conversation State Management

```python
# For long conversations, use compact endpoint
compact_response = client.responses.compact(res.id)

# Continue with compacted context
res_next = client.responses.create(
    model="gpt-5",
    input="Continue...",
    previous_response_id=compact_response.id
)
```

### Structured Outputs (Responses API)

Use `text.format` instead of `response_format`:

```python
response = client.responses.create(
    model="gpt-5",
    input="Jane, 54 years old",
    text={
        "format": {
            "type": "json_schema",
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"}
                },
                "required": ["name", "age"],
                "additionalProperties": False
            }
        }
    }
)
```

---

## OPENAI BUILT-IN TOOLS

### Available Tools

| Tool | Type | Description |
|------|------|-------------|
| `web_search` | Built-in | Search the web for current information |
| `file_search` | Built-in | Search uploaded vector stores |
| `code_interpreter` | Built-in | Execute Python in sandboxed container |
| `computer_use_preview` | Built-in | Control browser/computer interfaces |

### Web Search

```python
response = client.responses.create(
    model="gpt-5",
    input="Who is the current president of France?",
    tools=[{"type": "web_search"}]
)
```

### File Search with Vector Stores

```python
response = client.responses.create(
    model="gpt-5",
    input="What is deep research by OpenAI?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_abc123"],
        "max_num_results": 5
    }],
    include=["file_search_call.results"]
)
```

### Code Interpreter

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{
        "type": "code_interpreter",
        "container": {"type": "auto", "memory_limit": "4g"}
    }],
    input="Calculate what is 4 * 3.82 and find its square root"
)
```

**Container memory limits:** `1g` (default), `4g`, `16g`, `64g`

**File uploads for Code Interpreter:**
```python
file = client.files.create(file=open("data.csv", "rb"), purpose="assistants")

response = client.responses.create(
    model="gpt-5",
    tools=[{"type": "code_interpreter"}],
    input=[
        {"type": "input_file", "file_id": file.id},
        {"type": "input_text", "text": "Analyze this data and create a visualization"}
    ]
)
```

---

## COMPUTER USE (PREVIEW)

### Model

| Model | ID | Use Case |
|-------|----|---------|
| Computer Use Preview | computer-use-preview | Browser/computer automation |

### CUA Loop Pattern

```python
response = client.responses.create(
    model="computer-use-preview",
    tools=[{
        "type": "computer_use_preview",
        "display_width": 1024,
        "display_height": 768,
        "environment": "browser"
    }],
    input=[{
        "role": "user",
        "content": "Check the latest OpenAI news on bing.com."
    }],
    reasoning={"summary": "concise"},
    truncation="auto"
)
```

### Safety Checks

The model returns `pending_safety_checks` that must be acknowledged:

| Safety Check | Description |
|--------------|-------------|
| `malicious_instructions` | Adversarial content detected in page |
| `irrelevant_domain` | Current domain doesn't match task |
| `sensitive_domain` | Sensitive site detected (banking, etc.) |

**Handling Safety Checks:**
```python
for item in response.output:
    if item.type == "computer_call" and item.pending_safety_checks:
        acknowledged = get_user_confirmation(item.pending_safety_checks)
        if acknowledged:
            response = client.responses.create(
                previous_response_id=response.id,
                acknowledged_safety_checks=item.pending_safety_checks
            )
```

---

## PROMPT CACHING

### How It Works

- **Automatic** for prompts >=1024 tokens
- Place static content at **BEGINNING** of prompt
- Cache key uses first ~256 tokens
- In-memory retention: 5-10 min (up to 1 hour under load)

### Configuration

```python
response = client.responses.create(
    model="gpt-5.1",
    input="Your prompt...",
    prompt_cache_retention="24h",
    prompt_cache_key="my-session-key"
)
```

### Extended Retention Models (24h support)

`gpt-5.2`, `gpt-5.1`, `gpt-5.1-codex-max`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`, `gpt-5`, `gpt-5-codex`, `gpt-4.1`

### Check Cache Hit

```python
print(response.usage.prompt_tokens_details)
```

### Prompt Structure for Maximum Caching

```python
response = client.responses.create(
    model="gpt-5-mini",
    instructions=LARGE_STATIC_SYSTEM_PROMPT,
    input=dynamic_user_input
)
```

---

## CUSTOM TOOLS & GRAMMARS

### Custom Tool (Free-form Text Output)

```python
response = client.responses.create(
    model="gpt-5",
    input="Use the code_exec tool to print hello world.",
    tools=[{
        "type": "custom",
        "name": "code_exec",
        "description": "Executes arbitrary Python code."
    }]
)
```

### With Lark Grammar (Constrained Output)

```python
grammar = '''
start: expr
expr: term (SP ADD SP term)* -> add
term: factor (SP MUL SP factor)* -> mul
factor: INT
SP: " "
ADD: "+"
MUL: "*"
%import common.INT
'''

response = client.responses.create(
    model="gpt-5",
    tools=[{
        "type": "custom",
        "name": "math_exp",
        "description": "Creates valid mathematical expressions",
        "format": {
            "type": "grammar",
            "syntax": "lark",
            "definition": grammar
        }
    }],
    input="Use the math_exp tool to add four plus four."
)
```

### With Regex CFG

```python
response = client.responses.create(
    model="gpt-5",
    tools=[{
        "type": "custom",
        "name": "version_number",
        "description": "Generates semantic version numbers",
        "format": {
            "type": "grammar",
            "syntax": "regex_cfg",
            "definition": "[0-9]+\\.[0-9]+\\.[0-9]+"
        }
    }],
    input="Generate a version number for the new release."
)
```

---

## MODEL SELECTION GUIDE (OPENAI ONLY)

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Complex coding | GPT-5 | Strong coding and reasoning |
| Budget-conscious | GPT-5-mini or GPT-5-nano | Lower cost, solid quality |
| Computer automation | computer-use-preview | Browser/computer control |
| Deep reasoning/math | o3 | Focused reasoning strength |
| Long autonomous agents | GPT-5.2 | Largest context, advanced features |
| Fast responses | GPT-5-nano | Lowest latency/cost tier |
| Image generation | GPT-5.2 or o4-mini | Image generation support |

---

## {{PROJECT_NAME}} CURRENT SETUP

Use `codex/PROJECT_CONTEXT.md` to fill these placeholders.

| Role | Model | Notes |
|------|-------|-------|
| Orchestrator | {{ORCHESTRATOR_MODEL}} | {{ORCHESTRATOR_NOTES}} |
| Analyst | {{ANALYST_MODEL}} | {{ANALYST_NOTES}} |
| Judge | {{JUDGE_MODEL}} | {{JUDGE_NOTES}} |

**Migration Notes:**
- Replace `{{PLACEHOLDER}}` values before shipping.
- Prefer the Responses API for new integrations.

---

## UPDATE PROTOCOL

1. Check date - If Last Updated >30 days ago, verify with WebSearch.
2. Critical decisions - Always WebSearch for model selection, pricing, deprecations.
3. Sources to check:
   - [OpenAI Models](https://platform.openai.com/docs/models)
   - [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)

---

## SOURCES

- [OpenAI Models](https://platform.openai.com/docs/models)
- [Migrate to Responses API](https://platform.openai.com/docs/guides/responses-vs-chat-completions)
- [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Code Interpreter Tool](https://platform.openai.com/docs/guides/tools-code-interpreter)
- [File Search Tool](https://platform.openai.com/docs/guides/tools-file-search)
- [Computer Use Tool](https://platform.openai.com/docs/guides/tools-computer-use)
- [Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)
- [Conversation State](https://platform.openai.com/docs/guides/conversation-state)
- [AgentKit](https://platform.openai.com/docs/guides/agents)
- [GPT-5 for Developers](https://openai.com/index/introducing-gpt-5-for-developers/)

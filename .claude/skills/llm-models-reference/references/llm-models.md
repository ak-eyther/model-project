# LLM Models Reference

**Last Updated:** 2026-01-04
**Update Protocol:** If >30 days old, verify with WebSearch before critical decisions

---

## ANTHROPIC CLAUDE MODELS

### Model Lineup

| Model | ID | Context | Output | Pricing (M tokens) |
|-------|----|---------|---------|--------------------|
| **Opus 4.5** | claude-opus-4-5-20251101 | 200K (1M beta) | 64K | $15 / $75 |
| **Sonnet 4.5** | claude-sonnet-4-5-20250929 | 200K (1M beta) | 64K | $3 / $15 |
| Sonnet 4 | claude-sonnet-4-20250514 | 200K | 64K | $3 / $15 |
| Haiku 4.5 | claude-haiku-4-5-* | 200K | 64K | Low |

### Capabilities Matrix

| Capability | Opus 4.5 | Sonnet 4.5 | Sonnet 4 | Haiku 4.5 |
|------------|----------|------------|----------|-----------|
| Tool Use | ✅ | ✅ | ✅ | ✅ |
| Computer Use | ✅ Best | ✅ 61.4% OSWorld | ✅ | ✅ |
| Vision | ✅ 80.7% MMMU | ✅ | ✅ | ✅ |
| Extended Thinking | ✅ 128K budget | ✅ 128K budget | ✅ | ✅ |
| Parallel Tool Calls | ✅ | ✅ | ✅ | ✅ |
| MCP Support | ✅ | ✅ | ✅ | ✅ |
| Effort Parameter | ✅ Only | ❌ | ❌ | ❌ |
| Tool Examples | ✅ | ✅ | ❌ | ✅ |
| Structured Outputs | ✅ | ✅ | ❌ | ✅ |

### Best For

- **Opus 4.5**: Maximum intelligence, complex reasoning, 30+ hour autonomous tasks, best vision (80.7% MMMU)
- **Sonnet 4.5**: Coding (SWE-bench 77.2%), agents, computer use (61.4% OSWorld), balanced cost
- **Haiku 4.5**: Fast responses, simple tasks, high throughput

### Claude Tool Use - How To

**API Endpoint:** `https://api.anthropic.com/v1/messages`

**Tool Definition Schema:**
```json
{
  "name": "tool_name",
  "description": "What this tool does",
  "input_schema": {
    "type": "object",
    "properties": {
      "param1": {"type": "string", "description": "Description of param"}
    },
    "required": ["param1"]
  }
}
```

**Python SDK Example:**
```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "Weather in NYC?"}]
)
```

**Response Flow:**
1. Claude returns `stop_reason: "tool_use"` with tool call details
2. Execute tool locally, get result
3. Send result back with `role: "user"` containing `tool_result`
4. Claude responds with final answer

**Beta Headers (2025):**
- `structured-outputs-2025-11-13` - Strict JSON schema validation
- `tool-examples-2025-10-29` - Provide example tool calls in definitions

**Extended Thinking:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Up to 128K for complex reasoning
    },
    messages=[...]
)
```

---

## ANTHROPIC ADDITIONAL APIs

### Available APIs

| API | Endpoint | Purpose | Status |
|-----|----------|---------|--------|
| Messages API | `POST /v1/messages` | Conversational interactions | GA |
| Message Batches API | `POST /v1/messages/batches` | Async bulk processing, **50% cost reduction** | GA |
| Token Counting API | `POST /v1/messages/count_tokens` | Count tokens before sending | GA |
| Files API | `POST /v1/files` | Upload files for multi-call use | Beta |
| Skills API | `POST /v1/skills` | Create custom agent skills | Beta |
| Models API | `GET /v1/models` | List available models | GA |

### Message Batches API (50% Cost Reduction)

**Best for:** Processing large volumes of requests asynchronously.

```python
import anthropic

client = anthropic.Anthropic()

# Create a batch
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Analyze campaign A"}]
            }
        },
        {
            "custom_id": "request-2",
            "params": {
                "model": "claude-sonnet-4-5",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": "Analyze campaign B"}]
            }
        }
    ]
)

# Check batch status
batch = client.messages.batches.retrieve(batch.id)
print(batch.processing_status)  # "in_progress" | "ended"

# Get results when complete
results = client.messages.batches.results(batch.id)
```

**Cost Savings:** 50% reduction vs standard Messages API

### Token Counting API

**Best for:** Managing costs and rate limits before sending requests.

```python
# Count tokens BEFORE making the actual request
token_count = client.messages.count_tokens(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Your long prompt here..."}],
    system="Your system prompt..."
)

print(f"Input tokens: {token_count.input_tokens}")
# Use this to estimate cost before sending
```

### Files API (Beta)

**Best for:** Uploading files once, using across multiple API calls.

```python
# Requires beta header: anthropic-beta: files-2025-01-01

# Upload a file
file = client.beta.files.create(
    file=open("document.pdf", "rb"),
    purpose="messages"
)

# Use in messages
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "file", "file_id": file.id},
            {"type": "text", "text": "Summarize this document"}
        ]
    }]
)
```

### Skills API (Beta)

**Best for:** Creating reusable agent capabilities.

```python
# Requires beta header: anthropic-beta: skills-2025-01-01

# Create a skill
skill = client.beta.skills.create(
    name="campaign_analyzer",
    description="Analyzes email campaign performance",
    instructions="You are an email marketing analyst...",
    tools=[{
        "name": "get_campaign_data",
        "description": "Retrieves campaign metrics"
    }]
)

# Use skill in messages
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    skills=[skill.id],
    messages=[{"role": "user", "content": "Analyze GM_30D_Opener"}]
)
```

### Authentication Headers

All Anthropic API requests require:

| Header | Value | Required |
|--------|-------|----------|
| `x-api-key` | Your API key | Yes |
| `anthropic-version` | `2023-06-01` | Yes |
| `content-type` | `application/json` | Yes |
| `anthropic-beta` | Feature flags (for beta APIs) | For beta features |

### Client SDKs

| Language | Package | Install |
|----------|---------|---------|
| Python | `anthropic` | `pip install anthropic` |
| TypeScript | `@anthropic-ai/sdk` | `npm install @anthropic-ai/sdk` |
| Java | `com.anthropic:anthropic-java` | Maven/Gradle |
| Go | `anthropic-sdk-go` | `go get github.com/anthropics/anthropic-sdk-go` |
| C# | `Anthropic` | `dotnet add package Anthropic` |
| Ruby | `anthropic` | `gem install anthropic` |
| PHP | `anthropic-ai/sdk` | `composer require anthropic-ai/sdk` |

### Request Size Limits

| Endpoint | Maximum Size |
|----------|--------------|
| Standard (Messages, Token Counting) | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |

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
- **o3/o4-mini**: Math, science, deep reasoning (AIME 2024/2025 leader)

### OpenAI Tool Use - How To

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
    include=["file_search_call.results"]  # Include search results
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
# Upload file for analysis
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
        "environment": "browser"  # or "mac", "windows", "ubuntu"
    }],
    input=[{
        "role": "user",
        "content": "Check the latest OpenAI news on bing.com."
    }],
    reasoning={"summary": "concise"},
    truncation="auto"  # REQUIRED for computer use
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
# Check for pending safety checks
for item in response.output:
    if item.type == "computer_call" and item.pending_safety_checks:
        # Get user confirmation before proceeding
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

- **Automatic** for prompts ≥1024 tokens
- Place static content at **BEGINNING** of prompt
- Cache key uses first ~256 tokens
- In-memory retention: 5-10 min (up to 1 hour under load)

### Configuration

```python
response = client.responses.create(
    model="gpt-5.1",
    input="Your prompt...",
    prompt_cache_retention="24h",  # "in_memory" (default) or "24h"
    prompt_cache_key="my-session-key"  # Optional routing key
)
```

### Extended Retention Models (24h support)

`gpt-5.2`, `gpt-5.1`, `gpt-5.1-codex-max`, `gpt-5.1-codex`, `gpt-5.1-codex-mini`, `gpt-5`, `gpt-5-codex`, `gpt-4.1`

### Check Cache Hit

```python
# In response.usage.prompt_tokens_details
print(response.usage.prompt_tokens_details)
# {"cached_tokens": 1920}  # Tokens served from cache
```

### Prompt Structure for Maximum Caching

```python
# GOOD: Static content first (will be cached)
response = client.responses.create(
    model="gpt-5-mini",
    instructions=LARGE_STATIC_SYSTEM_PROMPT,  # 1024+ tokens, cached
    input=dynamic_user_input                   # Variable, not cached
)

# BAD: Dynamic content first (breaks cache)
# Don't put timestamps, user IDs, or variable data at the beginning
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
# Returns: {"input": "print(\"hello world\")", ...}
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
# Returns: {"input": "4 + 4", ...}
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
# Returns: {"input": "2.1.0", ...}
```

---

## MODEL SELECTION GUIDE

| Use Case | Recommended Model | Why |
|----------|-------------------|-----|
| Complex coding | Sonnet 4.5 or GPT-5 | Best SWE-bench scores |
| Budget-conscious | GPT-5-mini or Haiku 4.5 | $0.25/M and low cost |
| Computer automation | Sonnet 4.5 | 61.4% OSWorld leader |
| Deep reasoning/math | o3 or Opus 4.5 | AIME leader, 128K thinking |
| Long autonomous agents | Opus 4.5 | 30+ hour sustained focus |
| Fast responses | GPT-5-nano or Haiku 4.5 | Optimized for speed |
| Vision/image analysis | Opus 4.5 | 80.7% MMMU |
| Local shell access | GPT-5.2 | Only model with shell tool |

---

## MISSION INBOX CURRENT SETUP

| Agent | Model | Provider |
|-------|-------|----------|
| Orchestrator | gpt-5-mini-2025-08-07 | OpenAI SDK |
| Orchestrator Fallback | x-ai/grok-4.1-fast | OpenRouter |
| Analyst | anthropic/claude-sonnet-4-20250514 | OpenRouter |
| Judge | claude-sonnet-4-20250514 | Anthropic SDK |

**Recommendations:**
1. Consider upgrading Analyst/Judge to Sonnet 4.5 for better tool use and structured outputs.
2. **Migrate to Responses API** (see below)

### Migration Recommendation: Responses API

**Current:** Chat Completions API
**Recommended:** Migrate to Responses API

**Benefits for {{PROJECT_NAME}}:**
- **40-80% cost reduction** via automatic prompt caching
- **Stateful multi-turn** with `previous_response_id` (simplify context management)
- **Built-in tools** - web_search for real-time data, code_interpreter for analytics
- **Better agentic loop** - Orchestrator/Analyst/Judge can use native tool calling

**Migration Path:**
1. Update `backend/app/core/llm_clients.py` to use `openai.responses.create()`
2. Replace `messages` array with `input` + `instructions`
3. Add `store=True` for multi-turn conversations
4. Add `prompt_cache_retention="24h"` for cost optimization
5. Update tool definitions to Responses API format (internally-tagged)

**Example Migration:**
```python
# BEFORE (Chat Completions)
response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ],
    tools=[...]
)

# AFTER (Responses API)
response = client.responses.create(
    model="gpt-5-mini",
    instructions=system_prompt,
    input=user_input,
    tools=[...],
    store=True,
    prompt_cache_retention="24h"
)
```

**Cost Impact Estimate:**
- Current: ~$0.01/question (estimated)
- After migration: ~$0.004-0.006/question (40-60% savings from caching)

---

## UPDATE PROTOCOL

1. **Check date** - If Last Updated >30 days ago, verify with WebSearch
2. **Critical decisions** - Always WebSearch for model selection, pricing, deprecations
3. **Request update** - Ask Memory Expert (`/memory`) to update this skill file
4. **Sources to check:**
   - [Claude Models](https://platform.claude.com/docs/en/about-claude/models/overview)
   - [OpenAI Models](https://platform.openai.com/docs/models)

---

## SOURCES

### Anthropic
- [Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Claude Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Introducing Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- [Introducing Claude Sonnet 4.5](https://www.anthropic.com/news/claude-sonnet-4-5)

### OpenAI
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

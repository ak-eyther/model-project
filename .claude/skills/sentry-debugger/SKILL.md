---
name: sentry-debugger
description: Debug and analyze {{PROJECT_NAME}} errors and exceptions. Use when investigating crashes, error patterns, performance issues, or understanding what went wrong in production. Covers error queries by agent, exception types, and common debugging scenarios.
---

# Sentry Debugger for {{PROJECT_NAME}}

## When to Use Sentry vs LangSmith

| Question | Use |
|----------|-----|
| "What crashed?" | **Sentry** - see exceptions |
| "Why did the agent think X?" | **LangSmith** - see inputs/outputs |
| "Why did app error out?" | **Sentry** - see stacktrace |
| "Why is response wrong?" | **LangSmith** - trace the reasoning |
| "Is DB connection failing?" | **Sentry** - connection errors |
| "Is Analyst slow?" | **LangSmith** - latency analysis |
| "What errors happen most?" | **Sentry** - error frequency |
| "What patterns is Analyst missing?" | **LangSmith** - compare evidence across runs |

**Rule of thumb:**
- Sentry = **crashing** problems (exceptions, failures)
- LangSmith = **thinking** problems (wrong output, bad reasoning)

## Quick Start

- `SENTRY_AUTH_TOKEN=... SENTRY_QUERY="is:unresolved environment:production" \`
  `python .claude/skills/sentry-debugger/scripts/query_sentry_issues.py`
- `SENTRY_AUTH_TOKEN=... SENTRY_ISSUE_ID=... \`
  `python .claude/skills/sentry-debugger/scripts/get_sentry_issue.py`

## Bundled Resources

### References
- `references/production-errors.md`: production env vars + query examples.

### Scripts
- `scripts/query_sentry_issues.py`: list recent issues via SENTRY_* env vars.
- `scripts/get_sentry_issue.py`: fetch a single issue (optional latest event).

## Quick Start for Agents

### Where to Find Auth Token (Local Development)

**Location:** `backend/.env` (in project root)

**Required variables:**
```bash
SENTRY_AUTH_TOKEN=sntryu_...   # API query token (REQUIRED for this skill)
SENTRY_DSN=https://...         # Error reporting DSN (different purpose)
```

**How to check if token exists:**
```bash
grep "SENTRY_AUTH_TOKEN" backend/.env
```

### Quick Test (Verify Skill Works)

Run this to test the skill immediately:

```bash
# From project root
cd /path/to/Mission-Inbox

# Extract token and run test
SENTRY_AUTH_TOKEN=$(grep "^SENTRY_AUTH_TOKEN=" backend/.env | cut -d'=' -f2) \
./backend/venv/bin/python3 << 'EOF'
import os
import requests

token = os.environ.get("SENTRY_AUTH_TOKEN")
headers = {"Authorization": f"Bearer {token}"}
url = "https://sentry.io/api/0/projects/zappian-media/python-serverless/issues/"

response = requests.get(url, headers=headers, params={"query": "is:unresolved", "limit": 3})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    issues = response.json()
    print(f"✅ Found {len(issues)} issues")
    for issue in issues:
        print(f"  • {issue['title'][:60]}")
else:
    print(f"❌ Error: {response.text[:200]}")
EOF
```

**Expected output:** `Status: 200` with list of recent issues

### Common Issues When Testing

| Problem | Solution |
|---------|----------|
| `SENTRY_AUTH_TOKEN not found` | Check `backend/.env` file exists with token |
| `ModuleNotFoundError: requests` | Use `./backend/venv/bin/python3` (not system python) |
| `401 Unauthorized` | Token expired - regenerate in Sentry.io settings |
| `404 Project not found` | Verify org=`zappian-media`, project=`python-serverless` |

## Environment Variables (Railway)

```
SENTRY_AUTH_TOKEN=<set in Railway>
SENTRY_ORG=zappian-media
SENTRY_PROJECT=python-serverless
SENTRY_DSN=<set in Railway - used for sending errors>
```

## Agent Architecture Context

Errors may originate from any node in the pipeline:

```
memory_hydrate_node → orchestrator_node → analyst_node → response
```

Common error sources:
- `memory_hydrate_node`: ChromaDB connection, collection not found
- `orchestrator_node`: LLM timeout, JSON parse errors
- `analyst_node`: PostgreSQL queries, tool failures, LLM errors

## Troubleshooting Decision Tree

### Start Here: What's the symptom?

```
Symptom                          → Sentry Search
─────────────────────────────────────────────────────────────
"App crashed"                    → is:unresolved level:fatal
"Something silently failed"      → is:unresolved level:error
"Intermittent issues"            → Sort by count, look for spikes
"Slow responses"                 → Search: timeout OR slow
"Database problems"              → Search: postgresql OR database
```

### By Error Type: Where to Look

#### Database Errors (PostgreSQL)
| Error Message | Likely Cause | Where to Check |
|---------------|--------------|----------------|
| `connection refused` | Railway DB down or connection limit | Railway dashboard → Postgres metrics |
| `relation does not exist` | Missing table/migration | Check `rollup_*` tables exist |
| `timeout expired` | Query too slow | Check query in `diagnostic_tools.py` or `health_tools.py` |
| `too many connections` | Connection pool exhausted | Check `connections.py` pool settings |

**Files to check:** `backend/app/database/connections.py`, `backend/app/analytics/tools/`

#### LLM Errors (OpenAI/Anthropic/OpenRouter)
| Error Message | Likely Cause | Where to Check |
|---------------|--------------|----------------|
| `RateLimitError` | API quota exceeded | Check usage dashboard, add retry logic |
| `Timeout` | LLM overloaded | Increase timeout, check prompt length |
| `InvalidRequestError` | Prompt too long or malformed | Check token count in prompt |
| `AuthenticationError` | Bad API key | Check Railway env vars |

**Files to check:** `backend/app/core/llm_clients.py`

#### ChromaDB Errors
| Error Message | Likely Cause | Where to Check |
|---------------|--------------|----------------|
| `Collection not found` | Collection doesn't exist | Run collection init script |
| `Connection refused` | ChromaDB not running | Check Railway service status |
| `Embedding dimension mismatch` | Model changed | Rebuild collection with same model |

**Files to check:** `backend/app/core/memory.py`

#### JSON/Parsing Errors
| Error Message | Likely Cause | Where to Check |
|---------------|--------------|----------------|
| `JSONDecodeError` | LLM returned non-JSON | Check LLM response, add output validation |
| `KeyError` | Missing field in response | LLM didn't follow schema |
| `ValidationError` | Pydantic schema mismatch | Check `workflow_state.py` |

**Files to check:** `backend/app/agents/*/langgraph_node.py`

### By Agent: Common Errors

#### memory_hydrate_node
| Frequent Error | Search Query | Fix |
|----------------|--------------|-----|
| ChromaDB connection | `chromadb OR chroma` | Check ChromaDB service, CHROMA_HOST env var |
| Empty results | `collection OR embedding` | Verify collection has data |

#### orchestrator_node  
| Frequent Error | Search Query | Fix |
|----------------|--------------|-----|
| LLM timeout | `timeout orchestrator` | Increase timeout, simplify prompt |
| JSON parse fail | `JSONDecodeError orchestrator` | Add retry with format reminder |

#### analyst_node
| Frequent Error | Search Query | Fix |
|----------------|--------------|-----|
| Tool failures | `tool OR postgresql analyst` | Check tool function, DB connection |
| LLM timeout | `timeout analyst` | Analyst prompt may be too long |

### Error Severity Guide

```
🔴 FATAL (level:fatal)
   → App crashed, user got no response
   → Action: Fix immediately
   
🟠 ERROR (level:error)  
   → Something failed but app recovered
   → Action: Fix soon, check frequency
   
🟡 WARNING (level:warning)
   → Degraded experience, fallback used
   → Action: Monitor, fix if frequent
   
⚪ INFO (level:info)
   → Logged for debugging
   → Action: Ignore unless investigating
```

## SDK Setup

```python
import requests
import os

SENTRY_AUTH_TOKEN = os.environ["SENTRY_AUTH_TOKEN"]
SENTRY_ORG = os.environ.get("SENTRY_ORG", "zappian-media")
SENTRY_PROJECT = os.environ.get("SENTRY_PROJECT", "python-serverless")

headers = {"Authorization": f"Bearer {SENTRY_AUTH_TOKEN}"}
base_url = f"https://sentry.io/api/0"
```

## Common Queries

### List Recent Issues

```python
# Get latest issues (errors grouped by type)
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/"
params = {"query": "is:unresolved", "limit": 10}

response = requests.get(url, headers=headers, params=params)
issues = response.json()

for issue in issues:
    print(f"{issue['title'][:60]}")
    print(f"  Count: {issue['count']} | First: {issue['firstSeen'][:10]}")
    print(f"  Link: {issue['permalink']}")
```

### Get Recent Events (Individual Errors)

```python
# Get actual error events (not grouped)
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/events/"
params = {"limit": 20}

response = requests.get(url, headers=headers, params=params)
events = response.json()

for event in events:
    print(f"{event['title'][:50]} | {event['dateCreated'][:16]}")
```

### Search by Error Type

```python
# Find specific exception types
queries = {
    "database": "is:unresolved postgresql OR database OR sqlalchemy",
    "llm": "is:unresolved timeout OR openai OR anthropic OR LLM",
    "chromadb": "is:unresolved chromadb OR collection OR embedding",
    "json": "is:unresolved JSONDecodeError OR parse OR json",
}

query_type = "llm"  # change as needed
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/"
params = {"query": queries[query_type], "limit": 10}

response = requests.get(url, headers=headers, params=params)
```

### Get Error Details

```python
# Get full details for a specific issue
issue_id = "<issue-id-here>"
url = f"{base_url}/issues/{issue_id}/"

response = requests.get(url, headers=headers)
issue = response.json()

print(f"Title: {issue['title']}")
print(f"Count: {issue['count']}")
print(f"Users affected: {issue['userCount']}")

# Get latest event for this issue (with full stacktrace)
url = f"{base_url}/issues/{issue_id}/events/latest/"
response = requests.get(url, headers=headers)
event = response.json()

# Stacktrace
for entry in event.get("entries", []):
    if entry["type"] == "exception":
        for exc in entry["data"]["values"]:
            print(f"\nException: {exc['type']}: {exc['value']}")
            for frame in exc.get("stacktrace", {}).get("frames", [])[-5:]:
                print(f"  {frame.get('filename')}:{frame.get('lineNo')} in {frame.get('function')}")
```

### Error Frequency Over Time

```python
# Get error stats for last 24 hours
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/stats/"
params = {"stat": "received", "resolution": "1h"}

response = requests.get(url, headers=headers, params=params)
stats = response.json()

print("Errors per hour (last 24h):")
for timestamp, count in stats[-24:]:
    print(f"  {timestamp}: {count}")
```

## Debugging Scenarios

### "What's crashing in production right now?"

```python
# Unresolved issues, sorted by last seen
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/"
params = {
    "query": "is:unresolved",
    "sort": "date",
    "limit": 5
}
response = requests.get(url, headers=headers, params=params)

for issue in response.json():
    print(f"🔴 {issue['title'][:50]}")
    print(f"   Last seen: {issue['lastSeen']}")
    print(f"   Events: {issue['count']}")
```

### "Are LLM calls timing out?"

```python
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/"
params = {
    "query": "is:unresolved timeout OR TimeoutError OR ReadTimeout",
    "limit": 10
}
response = requests.get(url, headers=headers, params=params)

timeouts = response.json()
if timeouts:
    print(f"⚠️ Found {len(timeouts)} timeout-related issues")
else:
    print("✅ No timeout issues found")
```

### "What errors happened during a specific query?"

```python
# Search by custom tag (if you tag with session_id)
session_id = "abc123"
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/issues/"
params = {"query": f"session_id:{session_id}"}

response = requests.get(url, headers=headers, params=params)
```

### "Compare error rates: this week vs last week"

```python
from datetime import datetime, timedelta

# This week
url = f"{base_url}/projects/{SENTRY_ORG}/{SENTRY_PROJECT}/stats/"
params = {"stat": "received", "resolution": "1d"}
response = requests.get(url, headers=headers, params=params)
stats = response.json()

this_week = sum(count for _, count in stats[-7:])
last_week = sum(count for _, count in stats[-14:-7])

print(f"This week: {this_week} errors")
print(f"Last week: {last_week} errors")
print(f"Change: {((this_week - last_week) / max(last_week, 1)) * 100:+.1f}%")
```

## Query Syntax Reference

| Filter | Example |
|--------|---------|
| Unresolved only | `is:unresolved` |
| By text | `timeout` or `database error` |
| By tag | `tag:environment:production` |
| By level | `level:error` or `level:fatal` |
| Combined | `is:unresolved level:error timeout` |
| Time range | `firstSeen:-24h` |

## Adding Context to Your Code

To make Sentry errors more debuggable, add context in your agent nodes:

```python
import sentry_sdk

# In analyst_node or orchestrator_node
sentry_sdk.set_context("agent", {
    "name": "analyst",
    "session_id": state.get("session_id"),
    "query": state.get("query")[:100],
})

sentry_sdk.set_tag("agent_type", "analyst")
sentry_sdk.set_tag("session_id", state.get("session_id"))
```

This allows filtering errors by agent type and session in Sentry.

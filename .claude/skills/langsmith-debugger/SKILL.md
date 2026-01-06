---
name: langsmith-debugger
description: Debug and analyze {{PROJECT_NAME}} LangGraph agent traces. Use when investigating agent behavior patterns, finding failures, analyzing latency, or understanding why Orchestrator/Analyst responses went wrong. Covers trace queries by agent tags, pattern analysis across runs, and common debugging scenarios.
---

# LangSmith Debugger for {{PROJECT_NAME}}

## ⚡ Quick Reference ({{PROJECT_NAME}} Specific)

**USE THIS FIRST** - These are the exact IDs for this project:

| Item | Value |
|------|-------|
| **API Endpoint** | `https://api.smith.langchain.com` |
| **Workspace ID** | `81b6468e-dacf-403c-8cd6-b9b672b12836` |
| **Org ID** | `ca825949-d89f-475c-8a5d-3df627044cbe` |
| **Project: Production** | `092619fa-b4af-4543-8253-2903027dd7c5` ({{PROJECT_PREFIX}}-production) |
| **Project: Default** | `c1c001cc-425d-4019-b1d6-5688bb1d2d1a` |
| **Project: Legacy** | `aecb1488-c9b9-4863-b1e9-6ad2fe72a357` ({{PROJECT_NAME}}) |
| **API Key Location** | `backend/.env` → `LANGSMITH_API_KEY` |

## Quick Start

- `LANGSMITH_API_KEY=... LANGSMITH_TENANT_ID=... LANGSMITH_PROJECT_ID=... \`
  `python .claude/skills/langsmith-debugger/scripts/query_langsmith_runs.py`
- Add `LANGSMITH_FILTER` to narrow runs (examples in `references/production-traces.md`).

## Bundled Resources

### References
- `references/production-traces.md`: production env vars + trace query examples.

### Scripts
- `scripts/query_langsmith_runs.py`: list recent runs via LANGSMITH_* env vars.

### ⚠️ IMPORTANT: Org-Scoped API Key

The API key is **org-scoped** and requires the `X-Tenant-ID` header for all requests:

```python
headers = {
    'x-api-key': API_KEY,
    'X-Tenant-ID': '81b6468e-dacf-403c-8cd6-b9b672b12836',  # Required!
    'Content-Type': 'application/json'
}
```

Without this header, you'll get: `403 Forbidden: This API key is org-scoped and requires workspace specification`

## Environment Variables (Railway + Local)

```bash
# In backend/.env (local) or Railway dashboard (production)
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT={{PROJECT_PREFIX}}-production
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=lsv2_sk_...  # Get from backend/.env or Railway
```

## Agent Architecture

```
memory_hydrate_node → orchestrator_node → analyst_node → response
```

| Node | Tags | Purpose |
|------|------|---------|
| `memory_hydrate_node` | `agent:memory`, `phase:hydration` | Load context from ChromaDB |
| `orchestrator_node` | `agent:orchestrator`, `phase:planning` | Parse intent, identify knowledge gaps |
| `analyst_node` | `agent:analyst`, `phase:analysis` | Gather evidence, generate options |

## SDK Setup

```python
from langsmith import Client
import os

client = Client(
    api_url=os.environ["LANGSMITH_ENDPOINT"],
    api_key=os.environ["LANGSMITH_API_KEY"]
)
project_name = os.environ["LANGSMITH_PROJECT"]
```

## Common Queries

### List Recent Runs by Agent

```python
# All Analyst runs from last 24 hours
runs = client.list_runs(
    project_name=project_name,
    filter='has(tags, "agent:analyst")',
    start_time=datetime.now() - timedelta(hours=24)
)
for run in runs:
    print(f"{run.name} | {run.status} | {run.latency_ms}ms")
```

### Find Failed Runs

```python
# Failed runs by agent
runs = client.list_runs(
    project_name=project_name,
    filter='and(has(tags, "agent:analyst"), eq(status, "error"))',
    limit=20
)
```

### Latency Analysis

```python
# Slow Analyst runs (>3 seconds)
runs = client.list_runs(
    project_name=project_name,
    filter='and(has(tags, "agent:analyst"), gt(latency, 3000))',
    limit=50
)

# Calculate average latency per agent
from statistics import mean
analyst_latencies = [r.latency_ms for r in runs if r.latency_ms]
print(f"Avg Analyst latency: {mean(analyst_latencies):.0f}ms")
```

### Get Run Details

```python
# Full trace for a specific run
run = client.read_run(run_id="<run-id-here>")

# What went in
print("INPUT:", run.inputs)

# What came out
print("OUTPUT:", run.outputs)

# Error details (if failed)
print("ERROR:", run.error)
```

### Compare Orchestrator vs Analyst Patterns

```python
from collections import Counter

# Get recent runs for both agents
orch_runs = list(client.list_runs(
    project_name=project_name,
    filter='has(tags, "agent:orchestrator")',
    limit=100
))
analyst_runs = list(client.list_runs(
    project_name=project_name,
    filter='has(tags, "agent:analyst")',
    limit=100
))

# Success rates
orch_success = sum(1 for r in orch_runs if r.status == "success") / len(orch_runs)
analyst_success = sum(1 for r in analyst_runs if r.status == "success") / len(analyst_runs)

print(f"Orchestrator success: {orch_success:.1%}")
print(f"Analyst success: {analyst_success:.1%}")
```

## Debugging Scenarios

### "Why did Analyst give a bad recommendation?"

```python
# 1. Find the run
run = client.read_run(run_id="<problem-run-id>")

# 2. Check what Orchestrator sent
print("Knowledge gaps sent to Analyst:")
print(run.inputs.get("knowledge_gaps"))

# 3. Check what tools Analyst called
print("Evidence gathered:")
print(run.outputs.get("evidence"))

# 4. Check the draft options
print("Options generated:")
print(run.outputs.get("draft_options"))
```

### "Why is the system slow?"

```python
# Get parent trace with all child spans
runs = client.list_runs(
    project_name=project_name,
    filter='eq(is_root, true)',
    limit=10
)

for run in runs:
    # Get child runs (each agent node)
    children = client.list_runs(
        project_name=project_name,
        filter=f'eq(parent_run_id, "{run.id}")'
    )
    print(f"\n--- Run {run.id[:8]} (total: {run.latency_ms}ms) ---")
    for child in children:
        print(f"  {child.name}: {child.latency_ms}ms")
```

### "What queries confuse Orchestrator?"

```python
# Find low-confidence or clarification-needed runs
runs = client.list_runs(
    project_name=project_name,
    filter='has(tags, "agent:orchestrator")',
    limit=100
)

confused = []
for run in runs:
    outputs = run.outputs or {}
    if outputs.get("needs_clarification") or outputs.get("confidence") == "LOW":
        confused.append({
            "query": run.inputs.get("query"),
            "intent": outputs.get("user_intent"),
            "gaps": outputs.get("knowledge_gaps")
        })

print(f"Found {len(confused)} confusing queries")
for c in confused[:5]:
    print(f"  Query: {c['query'][:50]}...")
```

## Filter Syntax Reference

| Filter | Example |
|--------|---------|
| By tag | `has(tags, "agent:analyst")` |
| By status | `eq(status, "error")` |
| By latency | `gt(latency, 3000)` |
| Combined | `and(has(tags, "agent:analyst"), eq(status, "error"))` |
| Root traces only | `eq(is_root, true)` |
| By parent | `eq(parent_run_id, "xxx")` |

## Token Usage Analysis

```python
# Find high token usage runs
runs = client.list_runs(
    project_name=project_name,
    filter='has(tags, "agent:analyst")',
    limit=50
)

for run in runs:
    if run.total_tokens and run.total_tokens > 5000:
        print(f"{run.name}: {run.total_tokens} tokens")
        print(f"  Prompt: {run.prompt_tokens}, Completion: {run.completion_tokens}")
```

## 🚀 Quick Start: Full Analysis Script

**Copy-paste this to run a complete trace analysis:**

```python
import requests
from datetime import datetime, timedelta, timezone

# {{PROJECT_NAME}} specific config
API_KEY = 'lsv2_sk_...'  # Get from backend/.env
TENANT_ID = '81b6468e-dacf-403c-8cd6-b9b672b12836'
PROJECT_ID = '092619fa-b4af-4543-8253-2903027dd7c5'  # {{PROJECT_PREFIX}}-production

headers = {
    'x-api-key': API_KEY,
    'X-Tenant-ID': TENANT_ID,
    'Content-Type': 'application/json'
}

# Query runs
body = {'session': [PROJECT_ID], 'limit': 100}
resp = requests.post('https://api.smith.langchain.com/runs/query', headers=headers, json=body)

if resp.ok:
    runs = resp.json().get('runs', [])
    print(f'Total runs: {len(runs)}')

    # Status breakdown
    success = sum(1 for r in runs if r.get('status') == 'success')
    errors = sum(1 for r in runs if r.get('status') == 'error')
    print(f'✅ Success: {success} | ❌ Errors: {errors}')

    # Show errors
    for r in runs:
        if r.get('status') == 'error':
            print(f"  ❌ {r.get('name')}: {r.get('error', 'No details')[:100]}")

    # Token usage
    total_tokens = sum(r.get('total_tokens', 0) or 0 for r in runs)
    print(f'Total tokens: {total_tokens:,}')
else:
    print(f'Error: {resp.status_code} - {resp.text}')
```

## 🐛 Known Issues & Gotchas

| Issue | Solution |
|-------|----------|
| `403 Forbidden: org-scoped key` | Add `X-Tenant-ID` header (see Quick Reference) |
| `404: sessions not found` | Use POST to `/runs/query` with `session: [PROJECT_ID]`, not project name |
| `ModuleNotFoundError: langsmith` | Run `pip install langsmith` in backend venv |
| No latency data | Runs may not have `total_time`; calculate from `start_time`/`end_time` |
| SDK `list_runs` fails | Use direct REST API with headers (SDK doesn't support tenant ID well) |

## 📅 Last Updated

- **Date:** 2025-12-28
- **By:** SAMA 2.0 (AI/ML Engineer)
- **Added:** Workspace ID, Project IDs, X-Tenant-ID requirement, Quick Start script

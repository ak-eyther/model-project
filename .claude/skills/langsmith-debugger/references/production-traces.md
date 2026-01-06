# Production Trace Lookup (LangSmith)

## Production Env Vars

These env vars are required to query production traces:

- LANGSMITH_ENDPOINT=https://api.smith.langchain.com
- LANGSMITH_PROJECT={{PROJECT_PREFIX}}-production
- LANGSMITH_PROJECT_ID=092619fa-b4af-4543-8253-2903027dd7c5
- LANGSMITH_TENANT_ID=81b6468e-dacf-403c-8cd6-b9b672b12836
- LANGSMITH_API_KEY=<org-scoped API key>

Where to find them:
- Railway backend service env vars
- Local: backend/.env

Railway CLI quick check:

```bash
railway variables | grep -E '^LANGSMITH_'
```

## Quick Query

```bash
export LANGSMITH_API_KEY="..."
export LANGSMITH_TENANT_ID="81b6468e-dacf-403c-8cd6-b9b672b12836"
export LANGSMITH_PROJECT_ID="092619fa-b4af-4543-8253-2903027dd7c5"

python .claude/skills/langsmith-debugger/scripts/query_langsmith_runs.py
```

## Filters

Set LANGSMITH_FILTER to narrow results:

- Analyst errors:
  LANGSMITH_FILTER='and(has(tags, "agent:analyst"), eq(status, "error"))'

- Orchestrator slow runs (>3s):
  LANGSMITH_FILTER='and(has(tags, "agent:orchestrator"), gt(latency, 3000))'

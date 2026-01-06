# Production Error Lookup (Sentry)

## Production Env Vars

These env vars are required to query production issues:

- SENTRY_AUTH_TOKEN=<API token for queries>
- SENTRY_ORG=zappian-media
- SENTRY_PROJECT=python-serverless
- SENTRY_DSN=<used for error reporting, not queries>

Where to find them:
- Railway backend service env vars
- Local: backend/.env

Railway CLI quick check:

```bash
railway variables | grep -E '^SENTRY_'
```

## Quick Query

```bash
export SENTRY_AUTH_TOKEN="..."
export SENTRY_ORG="zappian-media"
export SENTRY_PROJECT="python-serverless"
export SENTRY_QUERY="is:unresolved environment:production"

python .claude/skills/sentry-debugger/scripts/query_sentry_issues.py
```

## Notes

- The Sentry environment tag comes from RAILWAY_ENVIRONMENT.
- Use environment:cron for cron services.

# Reference: Quick Reference and Success Metrics

## Quick Reference

### Deploy via CI/CD (Recommended)

Push to `main` branch triggers automatic deployment via GitHub Actions.
All 4 services deploy automatically: Backend, Frontend, Cron Daily, Cron Chroma.

### Manual Deploy with Project Token

```bash
# Backend (use Project Token, no railway link needed!)
RAILWAY_TOKEN="<backend-project-token>" railway redeploy --service cf1c43ee-ca19-4b0f-8321-7fbf6500338d --yes

# Frontend
RAILWAY_TOKEN="<frontend-project-token>" railway redeploy --service 15e1a43a-7cd1-46b4-9877-9cf99b0f27ff --yes

# Cron Daily
RAILWAY_TOKEN="<cron-daily-token>" railway redeploy --service 91906328-ca49-4ea2-a163-a6aadbae06f9 --yes

# Cron Chroma
RAILWAY_TOKEN="<cron-chroma-token>" railway redeploy --service 44d0e76b-2029-4e52-b0b0-4cc34d7d1733 --yes
```

### Interactive Deploy (with `railway login`)

```bash
# Only works after `railway login` (interactive session)
railway link {{RAILWAY_PROJECT_ID}}  # Backend
railway up
railway logs -f
```

> ⚠️ **Note:** `railway link` does NOT work with Project Tokens. Use the Project Token pattern above for CI/CD.

### Check deployment status

```bash
railway status && railway logs --tail 20
```

### Update environment variable

```bash
railway variables set KEY=value
railway up  # Redeploy to apply
```

### Emergency debug

```bash
railway ssh --command="env | grep -i error"
railway logs --filter="ERROR" -n 100
```

### Test endpoints

```bash
# Backend health
curl https://{{BACKEND_URL}}/health

# Frontend
curl https://{{FRONTEND_URL}}
```

---

## Success Metrics

Deployment is successful when:

- Railway dashboard shows "Active" status
- Health check endpoint returns 200 OK
- No errors in logs for 10+ minutes
- API endpoints respond correctly
- Frontend can communicate with backend
- ChromaDB/database connections working

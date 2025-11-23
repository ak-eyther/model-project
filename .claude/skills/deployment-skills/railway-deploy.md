# Railway Deployment Skill

**Skill Type:** Deployment Management
**For Agent:** @shawar-2.0
**Platform:** Railway (Backend Hosting)

---

## Skill Purpose

This skill enables Railway deployment management including environment configuration, service deployment, health monitoring, and troubleshooting.

---

## Core Capabilities

### 1. Railway CLI Commands

**Login & Project Setup:**
```bash
# Login to Railway
railway login

# Link to existing project
railway link [project-id]

# Check current project
railway status
```

**Environment Management:**
```bash
# List all environments
railway environment

# Switch environment
railway environment [env-name]

# Set environment variables
railway variables set KEY=value

# List all variables
railway variables

# Delete variable
railway variables delete KEY
```

**Deployment:**
```bash
# Deploy current branch
railway up

# Deploy specific service
railway up --service [service-name]

# Check deployment logs
railway logs

# Follow logs in real-time
railway logs --follow
```

**Service Management:**
```bash
# List all services
railway service

# Open service in browser
railway open

# Get service domain
railway domain
```

### 2. Railway Project Structure

**Typical Backend Service:**
- Service Name: `claude-code-project-template-backend` (or similar)
- Runtime: Python 3.11+
- Framework: FastAPI
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables to Configure:**
- `PORT` - Auto-set by Railway
- `ANTHROPIC_API_KEY` - Claude AI API key
- `ADMIN_API_KEY` - Admin authentication key
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)
- `ENVIRONMENT` - `development`, `staging`, or `production`

### 3. Deployment Workflow

**Standard Deployment Process:**
1. Ensure code is pushed to git (Railway auto-deploys from git)
2. Verify environment variables are set correctly
3. Check Railway dashboard for deployment status
4. Monitor build logs for errors
5. Verify health check endpoint responds (e.g., `/health`)
6. Test critical API endpoints
7. Monitor for 10+ minutes post-deployment

**Branch to Environment Mapping:**
- `development` branch → Development environment
- `staging` branch → Staging environment
- `main` branch → Production environment

### 4. Health Check Protocol

**After Every Deployment:**
```bash
# Check service is running
railway logs --tail 50

# Test health endpoint
curl https://[service-domain]/health

# Test critical endpoints
curl https://[service-domain]/api/status
```

**Health Check Success Criteria:**
- ✅ Service returns 200 OK
- ✅ No error logs in Railway console
- ✅ Response time < 2 seconds
- ✅ Database connections working (if applicable)

### 5. Troubleshooting Guide

**Common Issues:**

**Issue: Deployment fails with "Build failed"**
- Check: `requirements.txt` has all dependencies
- Check: Python version matches Railway runtime
- Check: No syntax errors in code
- Solution: Fix errors, push to git, Railway auto-redeploys

**Issue: Service crashes on startup**
- Check: `railway logs` for error messages
- Check: Environment variables are set correctly
- Check: PORT is not hardcoded (use `$PORT` from env)
- Solution: Fix config, redeploy

**Issue: CORS errors in browser**
- Check: `CORS_ORIGINS` includes frontend domain
- Check: CORS middleware configured in FastAPI
- Solution: Update `CORS_ORIGINS`, redeploy

**Issue: 502 Bad Gateway**
- Check: Service is running (`railway status`)
- Check: Health endpoint responds
- Check: No crashes in logs
- Solution: Restart service or redeploy

**Issue: Environment variables not updating**
- Check: Variables set in correct environment
- Check: Service restarted after variable change
- Solution: `railway up` to trigger redeploy

### 6. Rollback Procedure

**If Deployment Fails:**
1. Check Railway dashboard for failed deployment
2. Review error logs
3. If critical: Revert git commit
4. Push reverted commit to trigger auto-redeploy
5. Verify rollback succeeded
6. Investigate root cause offline

**Railway Rollback Command:**
```bash
# Railway auto-deploys from git, so rollback via git:
git revert [bad-commit-hash]
git push origin [branch-name]
# Railway will auto-deploy the revert
```

---

## Railway-Specific Best Practices

1. **Never hardcode secrets** - Use Railway environment variables
2. **Use health checks** - Implement `/health` endpoint
3. **Monitor logs actively** - First 10 minutes after deploy
4. **Test in staging first** - Never deploy directly to production
5. **Use Railway's auto-deploy** - Faster than manual CLI deploy
6. **Set up notifications** - Railway can notify on deploy failures
7. **Document environment variables** - Keep list in project docs

---

## Integration with Other Tools

**With Git:**
- Railway watches git branches for changes
- Push to branch → Automatic deployment
- Prefer this over `railway up` for production

**With Vercel (Frontend):**
- Ensure CORS_ORIGINS includes Vercel domains
- Test cross-origin requests after frontend deploy
- Keep frontend/backend versions in sync

**With GitHub Actions (if used):**
- Railway can integrate with CI/CD pipelines
- Use Railway API tokens for automated deployments

---

## Railway Project Configuration Files

**railway.json** (optional, at project root):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**nixpacks.toml** (optional, for custom build):
```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "uvicorn api.main:app --host 0.0.0.0 --port $PORT"
```

---

## Success Metrics

**Deployment is successful when:**
- ✅ Railway dashboard shows "Active" status
- ✅ Health check endpoint returns 200 OK
- ✅ No errors in logs for 10+ minutes
- ✅ API endpoints respond correctly
- ✅ Frontend can communicate with backend (if applicable)
- ✅ Performance metrics within acceptable range

---

## Quick Reference

**Check deployment status:**
```bash
railway status && railway logs --tail 20
```

**Update environment variable:**
```bash
railway variables set KEY=value && railway up
```

**Emergency rollback:**
```bash
git revert HEAD && git push origin [branch]
```

**Monitor deployment:**
```bash
railway logs --follow
```

---

**Last Updated:** 2025-11-23
**Maintained By:** @shawar-2.0
**Related Skill:** `vercel-deploy.md`

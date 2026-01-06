---
name: railway-deploy
description: "Railway deployment management for {{PROJECT_NAME}}: CLI, env vars, health checks, troubleshooting, rollback."
metadata:
  short-description: Railway deployment management
---

Note: Current UI is Next.js on Vercel: https://{{FRONTEND_URL}} (production app) and https://{{STAGING_FRONTEND_URL}} (staging).


# Railway Deployment Skill

**Skill Type:** Deployment Management
**For Agent:** @shawar-2.0
**Platform:** Railway (Backend Hosting; Frontend on Vercel)

---

## {{PROJECT_NAME}} Project Configuration

### Production URLs

| Service | URL |
|---------|-----|
| **Frontend (Vercel)** | <https://{{FRONTEND_URL}}> |
| **Backend** | <https://{{BACKEND_URL}}> |

### Project IDs

| Service | Project ID |
|---------|------------|
| **Backend** | `{{RAILWAY_PROJECT_ID}}` |

### Service IDs (for CI/CD)

| Service | Service ID |
|---------|------------|
| **Backend** | `cf1c43ee-ca19-4b0f-8321-7fbf6500338d` |
| **Cron Daily** | `91906328-ca49-4ea2-a163-a6aadbae06f9` |
| **Cron Chroma** | `44d0e76b-2029-4e52-b0b0-4cc34d7d1733` |

### Quick Link Commands (Interactive Login Only)

```bash
# Link to {{PROJECT_NAME}} Backend
railway link {{RAILWAY_PROJECT_ID}}
```

> ⚠️ **IMPORTANT:** `railway link` only works with interactive login or Account Tokens.
> It does NOT work with Project Tokens (see CI/CD section below).

### Dashboard Links

- Backend: <https://railway.app/project/{{RAILWAY_PROJECT_ID}}>

---

## Railway Token Types (CRITICAL for CI/CD)

### Token Types

| Token Type | Env Variable | Scope | Use Case |
|------------|--------------|-------|----------|
| **Project Token** | `RAILWAY_TOKEN` | Single project/environment | CI/CD redeploys |
| **Account Token** | `RAILWAY_API_TOKEN` | All projects in account | Interactive CLI, `railway link` |
| **Team Token** | `RAILWAY_API_TOKEN` | All projects in team | Team automation |

### ⚠️ Critical Lesson: Project Tokens and `railway link`

**Project Tokens CANNOT use `railway link`** - they fail with "Unauthorized" because:
- Project Tokens are already scoped to a specific project/environment
- `railway link` tries to authenticate at the account level
- You don't NEED to link - just redeploy directly!

### Correct CI/CD Pattern

```yaml
# ❌ WRONG - fails with "Unauthorized"
- name: Deploy Backend
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_BACKEND }}
  run: |
    railway link --project 6e450618-... --service cf1c43ee-...
    railway redeploy --service cf1c43ee-... --yes

# ✅ CORRECT - Project Tokens don't need link
- name: Deploy Backend
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_BACKEND }}
  run: railway redeploy --service cf1c43ee-ca19-4b0f-8321-7fbf6500338d --yes
```

### Generating Project Tokens

1. Go to Railway Dashboard → Project → Settings → Tokens
2. Click "New Token"
3. Name it (e.g., "GitHub Actions - Backend")
4. Select environment (usually "production")
5. Copy immediately (shown only once!)

**Token URLs:**
- Backend: https://railway.app/project/{{RAILWAY_PROJECT_ID}}/settings/tokens
- Cron Daily: https://railway.app/project/e48f32c3-a544-4a88-a930-b4ffda5097a6/settings/tokens
- Cron Chroma: https://railway.app/project/70f86446-efd1-4b8b-993c-4f61e9bff971/settings/tokens

### Testing Tokens

```bash
# Test Project Token
RAILWAY_TOKEN="<project-token>" railway whoami
# Should show project details, NOT "Unauthorized"

# Test Account Token (different env var!)
RAILWAY_API_TOKEN="<account-token>" railway whoami
# Should show "Logged in as <name>"
```

### GitHub Secrets ({{PROJECT_NAME}})

| Secret Name | Token Type | Project |
|-------------|------------|---------|
| `RAILWAY_TOKEN_BACKEND` | Project Token | Mission-Inbox-Backend |
| `RAILWAY_TOKEN_CRON_DAILY` | Project Token | MI-Cron-DailyData |
| `RAILWAY_TOKEN_CRON_CHROMA` | Project Token | MI-Cron-ChromaDB |

### 🚨 Common Mistakes to Avoid

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Using `railway link` with Project Tokens | Project Tokens can't authenticate at account level | Skip `railway link`, just use `railway redeploy --service <id>` |
| Using wrong env var for token type | `RAILWAY_TOKEN` ≠ `RAILWAY_API_TOKEN` | Project Tokens → `RAILWAY_TOKEN`, Account Tokens → `RAILWAY_API_TOKEN` |
| Assuming token works across workspaces | Tokens are workspace-scoped | Generate token in the SAME workspace as the project |
| Trying to debug with `railway whoami` using wrong var | `railway whoami` with Project Token may show different info | Use `RAILWAY_API_TOKEN` for account-level whoami |
| Not copying token immediately | Railway only shows token ONCE | Copy immediately after generation |

### Troubleshooting CI/CD Token Issues

**Symptom:** `Unauthorized. Please login with railway login`

**Diagnosis Steps:**

1. **Check token type matches usage:**
   ```bash
   # Project Token test
   RAILWAY_TOKEN="<token>" railway redeploy --service <id> --yes

   # Account Token test
   RAILWAY_API_TOKEN="<token>" railway whoami
   ```

2. **Verify token is valid (not expired/revoked):**
   - Go to Railway Dashboard → Project → Settings → Tokens
   - Check if token is listed and active

3. **Verify workflow doesn't use `railway link` with Project Tokens:**
   ```yaml
   # If you see this pattern, it's wrong:
   run: |
     railway link --project ...  # ❌ REMOVE THIS
     railway redeploy ...
   ```

4. **Check GitHub Secret was updated:**
   - Go to GitHub → Settings → Secrets → Actions
   - Verify the secret was updated recently

**Quick Fix Checklist:**
- [ ] Using Project Token? Remove `railway link` from workflow
- [ ] Using Account Token? Use `RAILWAY_API_TOKEN` env var
- [ ] Token just created? Copy it immediately (only shown once)
- [ ] GitHub Secret updated? Check timestamp in GitHub Secrets page

---

## Skill Purpose

This skill enables Railway deployment management including environment configuration, service deployment, health monitoring, and troubleshooting for the {{PROJECT_NAME}} project.

---

## Core Capabilities

### 1. Railway CLI Commands

#### Installation and Authentication

```bash
# Install Railway CLI (macOS)
brew install railway

# Or use npm
npm i -g @railway/cli

# Login to Railway
railway login

# Check current user
railway whoami

# Logout
railway logout
```

#### Project Setup and Linking

```bash
# Link to existing project (interactive)
railway link

# Link to specific project by ID
railway link {{RAILWAY_PROJECT_ID}}

# Unlink current directory
railway unlink

# List all projects
railway list

# Check current project status
railway status
```

#### Deployment Commands

```bash
# Deploy current directory
railway up

# Deploy without waiting (detached)
railway up --detach

# Deploy specific service (when multiple exist)
railway up --service=<service-name>

# Remove most recent deployment
railway down

# Redeploy latest
railway redeploy
```

#### Environment Management

```bash
# List all environments
railway environment

# Switch environment
railway environment [env-name]

# Run command with Railway env vars locally
railway run npm start
railway run python app.py

# Open Railway dashboard
railway open
```

#### Logs and Monitoring

```bash
# View deployment logs
railway logs

# View build logs only
railway logs --build

# Follow logs in real-time
railway logs -f
railway logs --follow

# View specific number of lines
railway logs -n 100
railway logs --lines=100

# Filter logs
railway logs --filter="error"
railway logs -f --filter="ERROR"

# Output as JSON
railway logs --json
```

#### Variables Management

```bash
# List all variables
railway variables

# Get specific variable
railway variables get DATABASE_URL

# Set variable
railway variables set KEY=value

# Delete variable
railway variables delete KEY

# Load from .env file
railway variables set --from-env-file=.env
```

#### SSH Access

```bash
# SSH into running service
railway ssh

# SSH with full command (from dashboard)
railway ssh --project=<project-id> --environment=<env-id> --service=<service-id>

# Run single command via SSH
railway ssh --command="ls -la"
```

### 2. {{PROJECT_NAME}} Backend Configuration

#### Expected Stack

- Runtime: Python 3.11+
- Framework: FastAPI
- Database: ChromaDB (local) + PostgreSQL (optional)
- ML Models: CatBoost

#### Required Environment Variables

```bash
PORT                    # Auto-set by Railway
OPENROUTER_API_KEY      # LLM API access
ANTHROPIC_API_KEY       # Claude API (optional)
ADMIN_TOKEN             # Admin authentication
CORS_ORIGINS            # Allowed origins (comma-separated)
DATABASE_URL            # PostgreSQL connection (if used)
CHROMA_PATH             # ChromaDB storage path
```

#### Start Command

```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
bash start.sh
```

### 3. {{PROJECT_NAME}} Frontend Configuration

Frontend is deployed on Vercel (Next.js). There is no Railway frontend service.
- Production app: `https://{{FRONTEND_URL}}`
- Staging app: `https://{{STAGING_FRONTEND_URL}}`

---

## Deployment Workflow

### Standard Deployment Process

1. **Verify code is ready**

   ```bash
   # Test locally first
   railway run python -m pytest
   railway run python app.py
   ```

2. **Check environment variables**

   ```bash
   railway link <project-id>
   railway variables
   ```

3. **Deploy**

   ```bash
   railway up
   ```

4. **Monitor deployment**

   ```bash
   railway logs -f
   ```

5. **Verify health**

   ```bash
   curl https://{{BACKEND_URL}}/health
   ```

### Git-Based Auto-Deploy (Preferred)

- Railway watches git branches for changes
- Push to branch -> Automatic deployment
- Prefer this over `railway up` for production

---

## Troubleshooting Guide

### Build Failures

Check build logs first:

```bash
railway logs --build
```

#### Common Issues

##### 1. Module not found or Dependency errors

```bash
# Verify requirements.txt is complete
pip freeze > requirements.txt

# Check for missing system dependencies
# Add nixpacks.toml if needed
```

##### 2. Nixpacks detection issues

```toml
# Create nixpacks.toml in project root
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn api:app --host 0.0.0.0 --port $PORT"
```

##### 3. Out of Memory (OOM)

- Upgrade to paid plan for more memory
- Optimize dependencies (remove unused)
- Add `.railwayignore`:

```text
node_modules
__pycache__
.git
*.log
.env
.DS_Store
data/raw/
*.csv
```

### Runtime Errors

##### 1. Application failed to respond

```bash
# Check if PORT is used correctly
# In Python:
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

##### 2. Environment variables not loading

```bash
# Verify variables are set
railway variables

# Check if deployed after adding variables
# Variables need redeploy to take effect!
railway up
```

##### 3. Database connection fails

```bash
# Test connection
railway run python -c "import os; print(os.getenv('DATABASE_URL'))"

# For external DBs: whitelist Railway IPs or use 0.0.0.0/0
```

##### 4. CORS errors (frontend cannot reach backend)

```bash
# Check CORS_ORIGINS includes frontend URL
railway variables get CORS_ORIGINS

# Should include:
# https://{{FRONTEND_URL}}
```

##### 5. 502 Bad Gateway

```bash
# Check if service is running
railway status
railway logs --tail 50

# Common cause: app crashed on startup
# Check for missing env vars or import errors
```

### Health Check Protocol

After every deployment:

```bash
# Check service is running
railway logs --tail 50

# Test health endpoint
curl https://{{BACKEND_URL}}/health

# Test API status
curl https://{{BACKEND_URL}}/api/status
```

#### Success Criteria

- Service returns 200 OK
- No error logs in Railway console
- Response time < 2 seconds
- Database/ChromaDB connections working

---

## Rollback Procedure

### If Deployment Fails

1. Check Railway dashboard for failed deployment
2. Review error logs: `railway logs --build`
3. If critical, revert via git:

   ```bash
   git revert HEAD
   git push origin main
   # Railway auto-deploys the revert
   ```

### Manual Rollback

Railway doesn't have instant rollback like Vercel, so use git:

```bash
git log --oneline -5          # Find last good commit
git revert <bad-commit>       # Revert bad commit
git push origin main          # Push triggers redeploy
```

---

## Railway Project Files

### railway.json (optional)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### nixpacks.toml (for custom builds)

```toml
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["echo 'Build complete'"]

[start]
cmd = "uvicorn api:app --host 0.0.0.0 --port $PORT"
```

### Pre-deploy command (for migrations)

- Dashboard -> Service -> Settings -> Deploy
- Add pre-deploy command: `python manage.py migrate`
- Must exit with code 0 to proceed

---

## Quick Reference and Success Metrics

See `references/quick-reference.md` for {{PROJECT_NAME}} deploy commands, endpoint checks, and success criteria.

---

---

## 🚨 GHCR vs Nixpacks: Dashboard Overrides railway.json (PR #75 Learning)

**Date:** 2026-01-03
**Issue:** Railway dashboard settings OVERRIDE `railway.json` configuration

### The Confusion

You might have `railway.json` with:
```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

But Railway ignores this if dashboard is configured to use Docker images!

### How to Check Your ACTUAL Build Method

```bash
# Check /__version endpoint
curl https://your-app.railway.app/__version | jq '.'

# If response includes "image": "ghcr.io/..." → Railway pulls from GHCR
# If no image field or build logs show Nixpacks → Source build
```

### {{PROJECT_NAME}} Configuration (as of 2026-01-03)

| Environment | Build Source | Image |
|-------------|--------------|-------|
| **Production** | GHCR | `{{DOCKER_IMAGE}}:latest` |
| **Staging** | GHCR | `{{DOCKER_IMAGE}}:staging` |

Both use Docker images from GHCR, NOT Nixpacks source builds.

### Correct CI/CD Flow (GHCR Images)

```yaml
# 1. Build and push to GHCR
- name: Build and push image
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/org/app:latest

# 2. Trigger Railway to pull new image
- name: Deploy
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  run: railway redeploy --service <id> --yes
```

### Verify Deployment Used Latest Image

```bash
# Check the /__version endpoint
curl https://your-app.railway.app/__version | jq '.'

# Verify git_sha matches your latest commit
# Verify image field shows expected GHCR tag
```

### Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Old code running after deploy | GHCR push failed, Railway used cached image | Re-run workflow, check GHCR for new tag |
| `/__version` shows wrong commit | Image tag mismatch | Verify workflow pushed correct SHA tag |
| Railway builds from source | Dashboard set to GitHub Repo | Change to Docker Image in dashboard |

---

## 🚦 Staging Gate Workflow (PR #75 Learning)

**Date:** 2026-01-03
**Issue:** `staging-verified` check can fail if it runs before staging build completes

### The Problem

GitHub Actions runs all jobs in parallel by default. The `staging-verified` check might:
1. Start before staging deployment completes
2. Hit the OLD version of staging
3. Report "verified" based on wrong code
4. OR fail because staging isn't ready yet

### Solution: Staging Gate Pattern

```yaml
# .github/workflows/staging-gate.yml
name: Staging Gate

on:
  pull_request:
    branches: [main]

jobs:
  wait-for-staging:
    runs-on: ubuntu-latest
    steps:
      - name: Wait for staging deployment
        run: |
          echo "Waiting for staging to deploy..."
          sleep 120  # Give staging time to build

      - name: Verify staging health
        run: |
          curl -f https://staging-backend.railway.app/health

  staging-tests:
    needs: wait-for-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E tests against staging
        run: pytest tests/e2e --base-url=https://staging.example.com
```

### Re-running Failed Checks

If staging-verified fails because it ran too early:

```bash
# Find the failed run ID
gh run list --workflow=staging-gate.yml

# Re-run only the failed jobs
gh run rerun <run-id> --failed
```

### Staging Environment Details ({{PROJECT_NAME}})

| Component | URL |
|-----------|-----|
| Staging Backend | https://{{STAGING_BACKEND_URL}} |
| Staging Frontend | https://{{STAGING_FRONTEND_URL}} |
| Staging Backend Service ID | `d23ad99c-5b83-4243-802e-7b2b6ab2d98b` |

---

**Last Updated:** 2026-01-03
**Maintained By:** @shawar-2.0
**Project:** {{PROJECT_NAME}} - Zappian AI Email Optimization

**Changelog:**

- 2026-01-03: Added GHCR vs Nixpacks clarification, Staging Gate workflow pattern (PR #75)
- 2025-12-30: Added Railway Token Types section, CI/CD patterns, common mistakes, troubleshooting guide
- 2025-11-25: Initial skill creation

# Reference: Railway Deployment Expert

## Table of Contents
- Railway Deployment Expert
  - 1. Essential Railway CLI Commands
  - 2. Railway Troubleshooting Guide
    - 2.1 Build Failures
    - 2.2 Deployment Runtime Errors

## Railway Deployment Expert

### 0. Railway Token Types (CRITICAL for CI/CD)

**Understanding Railway Tokens:**

| Token Type | Env Variable | Scope | Can Use `railway link`? |
|------------|--------------|-------|-------------------------|
| **Project Token** | `RAILWAY_TOKEN` | Single project/environment | ❌ NO |
| **Account Token** | `RAILWAY_API_TOKEN` | All projects in account | ✅ YES |
| **Team Token** | `RAILWAY_API_TOKEN` | All projects in team | ✅ YES |

**⚠️ CRITICAL LESSON (from 2025-12-30 incident):**

Project Tokens CANNOT use `railway link` - they fail with "Unauthorized" because:
- Project Tokens are already scoped to a specific project/environment
- `railway link` requires account-level authentication
- **Solution:** Skip `railway link` entirely when using Project Tokens

**Correct CI/CD Pattern:**
```yaml
# ❌ WRONG - fails with "Unauthorized"
- name: Deploy Backend
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_BACKEND }}
  run: |
    railway link --project <id> --service <id>  # FAILS!
    railway redeploy --service <id> --yes

# ✅ CORRECT - Project Tokens don't need link
- name: Deploy Backend
  env:
    RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_BACKEND }}
  run: railway redeploy --service <service-id> --yes
```

**Testing Tokens:**
```bash
# Test Project Token (use RAILWAY_TOKEN)
RAILWAY_TOKEN="<project-token>" railway redeploy --service <id> --yes

# Test Account Token (use RAILWAY_API_TOKEN)
RAILWAY_API_TOKEN="<account-token>" railway whoami
```

---

### 1. Essential Railway CLI Commands

**Installation & Authentication:**
```bash
# Install Railway CLI (macOS/Linux)
brew install railway

# Or use npm
npm i -g @railway/cli

# Or use Docker
docker pull ghcr.io/railwayapp/cli:latest

# Login to Railway (interactive - creates session, NOT a token)
railway login

# Check current user
railway whoami

# Logout
railway logout
```

**Project Setup & Linking:**
```bash
# Initialize new project
railway init

# Link existing project (interactive)
railway link

# Link to specific project (if you know the project ID)
railway link --project-id=<project-id>

# Unlink current directory from project
railway unlink

# List all projects
railway list
```

**Deployment Commands:**
```bash
# Deploy current directory
railway up

# Deploy specific service
railway up --service=<service-id>

# Deploy with specific environment
railway up --environment=<environment-id>

# Redeploy latest deployment
railway redeploy

# Redeploy specific service
railway redeploy --service=<service-id>
```

**Environment Management:**
```bash
# Change active environment
railway environment

# Run command with Railway environment variables
railway run npm start

# Run command with specific service variables
railway run --service=<service-id> npm start

# Open Railway dashboard
railway open

# Open logs view
railway open live

# Open metrics
railway open metrics

# Open settings
railway open settings
```

**Logs & Monitoring:**
```bash
# View deployment logs
railway logs

# View build logs only
railway logs --build

# View deployment logs only
railway logs --deployment

# View logs with specific number of lines
railway logs --lines=100
railway logs -n 100

# Follow logs in real-time
railway logs --follow
railway logs -f

# Filter logs
railway logs --filter="error"
railway logs -f --filter="ERROR"

# Output logs in JSON format
railway logs --json
```

**Variables Management:**
```bash
# List all variables
railway variables

# Get specific variable
railway variables get DATABASE_URL

# Set variable
railway variables set KEY=value

# Delete variable
railway variables delete KEY

# Load variables from .env file
railway variables set --from-env-file=.env
```

**SSH Access:**
```bash
# SSH into running service
railway ssh

# SSH into specific service
railway ssh --service=<service-id>

# SSH with copied command from dashboard
railway ssh --project=<project-id> --environment=<env-id> --service=<service-id>

# Run single command via SSH (non-interactive)
railway ssh --command="ls -la"
```

### 1.1 Railway Build Methods: Nixpacks vs Docker Images

**⚠️ CRITICAL: Understanding Railway's Build Source**

Railway can build your app from TWO sources - knowing which one is configured is essential!

| Build Method | Configured Via | When to Use |
|--------------|----------------|-------------|
| **Nixpacks (Source Build)** | `railway.json` with `"builder": "NIXPACKS"` | Default, simpler, auto-detects framework |
| **Docker Image (GHCR/DockerHub)** | Railway Dashboard → Settings → Source | When you push pre-built images |

**⚠️ IMPORTANT: Dashboard Settings Override `railway.json`**

Even if `railway.json` says `"builder": "NIXPACKS"`, Railway dashboard settings take precedence!

**How to Check Your ACTUAL Build Method:**
```bash
# Check /__version endpoint (if your app exposes it)
curl https://your-app.railway.app/__version

# If response includes "image": "ghcr.io/..." → Railway pulls from GHCR
# If no image field or build logs show Nixpacks → Source build
```

**{{PROJECT_NAME}} Configuration (as of 2026-01-03):**
- Railway dashboard configured to pull from GHCR
- `railway.json` with Nixpacks is **overridden**
- Both staging and production use Docker images from GHCR

**Correct CI/CD Flow (Docker Images):**
```yaml
# 1. Build and push to GHCR
- name: Build and push image
  uses: docker/build-push-action@v5
  with:
    push: true
    tags: ghcr.io/org/app:latest

# 2. Trigger Railway to pull new image
- name: Deploy
  run: railway redeploy --service <id> --yes
```

**To Verify Deployment Used Latest Image:**
```bash
# Check the /__version endpoint
curl https://your-app.railway.app/__version
# Verify git_sha matches your latest commit
# Verify image field shows expected GHCR tag
```

**Common Issues:**
| Symptom | Cause | Fix |
|---------|-------|-----|
| Old code running after deploy | GHCR push failed, Railway used cached image | Re-run workflow, check GHCR for new tag |
| `/__version` shows wrong commit | Image tag mismatch | Verify workflow pushed correct SHA tag |
| Railway builds from source | Dashboard set to GitHub Repo | Change to Docker Image in dashboard |

---

### 2. Railway Troubleshooting Guide

#### 2.0 CI/CD Token Issues

**Symptom:** `Unauthorized. Please login with railway login`

**Root Causes & Solutions:**

| Error Context | Likely Cause | Solution |
|---------------|--------------|----------|
| `railway link` fails | Using Project Token | Remove `railway link`, use `railway redeploy --service <id>` directly |
| `railway whoami` fails | Wrong env var | Use `RAILWAY_API_TOKEN` for Account Tokens |
| Token works locally but not in CI | Token not updated in GitHub Secrets | Re-generate token, update GitHub Secret |
| "Service not found" | Service ID is wrong OR token is for different environment | Verify service ID matches the token's environment |

**Debugging Steps:**
```bash
# 1. Test if token is valid at all
RAILWAY_TOKEN="<token>" railway --version  # Should work regardless

# 2. For Project Tokens, skip link and test redeploy directly
RAILWAY_TOKEN="<token>" railway redeploy --service <service-id> --yes

# 3. For Account Tokens, use different env var
RAILWAY_API_TOKEN="<token>" railway whoami
RAILWAY_API_TOKEN="<token>" railway link --project <id>
```

**Quick Fix Checklist:**
- [ ] Remove `railway link` if using Project Tokens
- [ ] Use correct env var (`RAILWAY_TOKEN` vs `RAILWAY_API_TOKEN`)
- [ ] Verify token is from correct project/environment
- [ ] Check GitHub Secrets were updated (check timestamp)

---

#### 2.1 Build Failures

**Common Causes:**
- Missing dependencies
- Build command errors
- Environment variable issues
- Nixpacks detection problems
- Docker build failures
- Out of memory (OOM) errors

**Investigation Steps:**

1. **Check Build Logs:**
```bash
# View build logs
railway logs --build

# View full deployment logs
railway logs --deployment

# View in real-time
railway logs -f
```

2. **Common Build Error Patterns:**

**Pattern 1: npm/yarn build fails**
```bash
# Error: "Command npm run build exited with 1"
# Solution: Check if ESLint/TypeScript errors are blocking

# Test locally first
npm run build

# If CI=true is causing issues, add to Railway:
# Settings → Variables → CI=false
```

**Pattern 2: Nixpacks detection issues**
```bash
# Error: "Failed to detect language/framework"
# Solution: Add nixpacks.toml

# Create nixpacks.toml in project root:
[phases.setup]
nixPkgs = ["nodejs-18_x", "python310"]

[phases.install]
cmds = ["npm ci"]

[phases.build]
cmds = ["npm run build"]

[start]
cmd = "npm start"
```

**Pattern 3: Out of Memory (OOM)**
```bash
# Error: "Build container OOMing"
# Solutions:
# 1. Upgrade to paid plan for more memory
# 2. Optimize dependencies
# 3. Use Railway V2 runtime (check service settings)
# 4. Remove large files from Docker context

# Check .dockerignore includes:
node_modules
.git
*.log
.env
.DS_Store
```

#### 2.2 Deployment Runtime Errors

**Common Issues:**
- "Application failed to respond"
- Port binding issues
- Start command not working
- Database connection failures
- Environment variable problems

**Solutions:**

1. **Port Configuration:**
```bash
# Railway automatically provides $PORT variable
# Ensure your app listens on it

# For Node.js/Express:
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});

# For Python/FastAPI:
if __name__ == "__main__":
  import uvicorn
  port = int(os.getenv("PORT", 8000))
  uvicorn.run(app, host="0.0.0.0", port=port)
```

2. **Start Command Issues:**
```bash
# Check start command in Railway dashboard
# Settings → Deploy → Start Command

# Common start commands:
# Node.js: node server.js
# Next.js: npm start
# Python: gunicorn app:app
# FastAPI: uvicorn main:app --host 0.0.0.0 --port $PORT
```

3. **Database Connection:**
```bash
# Check if DATABASE_URL is set
railway variables | grep DATABASE_URL

# Test database connection
railway run node -e "console.log(process.env.DATABASE_URL)"

# Connect to database shell
railway connect postgres
```

4. **Health Check:**
```bash
# Test if service is responding
curl https://your-app.railway.app/health

# Check from inside container (via SSH)
railway ssh
curl localhost:$PORT/health
```


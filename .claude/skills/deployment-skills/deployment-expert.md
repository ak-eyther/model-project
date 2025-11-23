# Deployment Expert Skill - Vercel & Railway

**Skill Type:** Comprehensive Deployment Management
**For Agent:** @shawar-2.0
**Platforms:** Vercel (Frontend) + Railway (Backend)

---

## Overview

This skill enables AI agents (like Claude Code) to act as deployment experts for Vercel and Railway platforms. It provides comprehensive CLI tools, troubleshooting techniques, and investigation strategies for debugging deployment issues.

**Target Use Cases:**
- Investigate deployment failures
- Debug build errors
- Fix environment variable issues
- Troubleshoot domain and networking problems
- Optimize deployment performance
- Handle serverless function errors

---

## Vercel Deployment Expert

### 1. Essential Vercel CLI Commands

**Installation & Authentication:**
```bash
# Install Vercel CLI globally
npm i -g vercel
# or
pnpm i -g vercel

# Login to Vercel
vercel login

# Check current user
vercel whoami

# Logout
vercel logout
```

**Project Setup & Linking:**
```bash
# Initialize/link project (interactive)
vercel

# Link to specific project
vercel link

# Remove .vercel directory to reset project settings
rm -rf .vercel
vercel
```

**Deployment Commands:**
```bash
# Deploy to preview environment
vercel

# Deploy to production
vercel --prod

# Deploy with specific environment
vercel deploy --target=production

# Redeploy existing deployment
vercel redeploy https://example-app.vercel.app

# Deploy and capture deployment URL
vercel deploy >deployment-url.txt 2>error.txt
code=$?
if [ $code -eq 0 ]; then
  deploymentUrl=$(cat deployment-url.txt)
  echo "Deployed: $deploymentUrl"
else
  errorMessage=$(cat error.txt)
  echo "Error: $errorMessage"
fi
```

**Environment Variables Management:**
```bash
# Pull environment variables
vercel env pull

# Pull from specific environment
vercel env pull --environment=staging

# Add environment variable
vercel env add MY_KEY production

# Add variable to custom environment
vercel env add MY_KEY staging

# List environment variables
vercel env ls
```

**Logs & Debugging:**
```bash
# View deployment logs (via dashboard)
# Navigate to: https://vercel.com/[team]/[project]/[deployment-id]

# Get logs programmatically (TypeScript/Node)
# See Vercel SDK examples in troubleshooting section
```

### 2. Vercel Troubleshooting Guide

#### 2.1 Build Failures

**Common Causes:**
- Missing dependencies in package.json
- ESLint errors blocking build
- TypeScript errors
- Missing build script
- Environment variable issues
- CI=true causing warnings to fail build

**Investigation Steps:**

1. **Check Build Logs:**
   - Navigate to deployment in Vercel dashboard
   - Click "View Function Logs" or "Build Logs"
   - Look for specific error messages

2. **Common Build Error Patterns:**
```bash
# Error: Command "npm run build" exited with 1
# Solution 1: Fix ESLint/TypeScript errors locally
npm run build  # Test locally first

# Solution 2: Set CI to false (use with caution!)
# In Vercel Dashboard → Settings → Environment Variables
# Add: CI=false

# Solution 3: Check for warnings that are treated as errors
# Look for "Failed to compile" in logs
# Fix the specific warning/error mentioned
```

3. **Missing Build Script:**
```json
// package.json
{
  "scripts": {
    "build": "next build"  // Ensure this exists
  }
}
```

4. **Framework Detection Issues:**
```bash
# In Vercel Dashboard → Project Settings → Build & Development Settings
# Manually specify:
# - Build Command: npm run build
# - Output Directory: .next (for Next.js) or dist/build
# - Install Command: npm install
```

#### 2.2 Environment Variable Issues

**Common Problems:**
- Variables not defined in Vercel dashboard
- Wrong environment scope (development/preview/production)
- Case sensitivity (Linux vs local)
- Not using NEXT_PUBLIC_ prefix for client-side variables

**Solutions:**

1. **Check Variable Configuration:**
```bash
# Verify variables are set in Vercel Dashboard
# Settings → Environment Variables

# Check which environment they're available in:
# - Development
# - Preview
# - Production
```

2. **Client-side Variables (Next.js):**
```javascript
// Must use NEXT_PUBLIC_ prefix for browser access
NEXT_PUBLIC_API_URL=https://api.example.com

// Server-side only (no prefix needed)
DATABASE_URL=postgresql://...
API_SECRET=xxx
```

3. **Verify Variables in Build:**
```bash
# In vercel.json
{
  "env": {
    "MY_VAR": "@my_var_secret"
  }
}
```

#### 2.3 Domain & DNS Issues

**Common Problems:**
- DNS not propagated
- Incorrect DNS records
- SSL certificate issues
- Domain not verified

**Investigation Steps:**

1. **Check DNS Propagation:**
```bash
# Check DNS records
dig your-domain.com
nslookup your-domain.com

# Check from different DNS servers
dig @8.8.8.8 your-domain.com
dig @1.1.1.1 your-domain.com
```

2. **Verify DNS Configuration:**
```bash
# For Vercel deployment, DNS should point to:
# A Record: 76.76.21.21
# CNAME: cname.vercel-dns.com
```

3. **Check SSL Certificate:**
```bash
# Verify SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

---

## Railway Deployment Expert

### 1. Essential Railway CLI Commands

**Installation & Authentication:**
```bash
# Install Railway CLI (macOS/Linux)
brew install railway

# Or use npm
npm i -g @railway/cli

# Or use Docker
docker pull ghcr.io/railwayapp/cli:latest

# Login to Railway
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

### 2. Railway Troubleshooting Guide

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

---

## Cross-Platform Deployment Strategies

### 1. Deployment Decision Tree

**When to use Vercel:**
- ✅ Next.js, React, Vue, Svelte applications
- ✅ Static sites and JAMstack
- ✅ Serverless functions (Edge/Node.js)
- ✅ Need global CDN with edge computing
- ✅ Preview deployments for every PR
- ❌ Long-running processes
- ❌ WebSocket servers
- ❌ Background workers

**When to use Railway:**
- ✅ Backend APIs (Node.js, Python, Go, etc.)
- ✅ Databases (Postgres, MongoDB, Redis)
- ✅ Full-stack applications
- ✅ Docker-based deployments
- ✅ Long-running processes
- ✅ WebSocket servers
- ✅ Cron jobs and workers
- ❌ Need extensive global edge network
- ❌ Require serverless at scale

### 2. Hybrid Architecture: Vercel Frontend + Railway Backend

**Common Setup:**
```
Frontend (Vercel) → API (Railway) → Database (Railway)
```

**Vercel Side Configuration:**
```json
// vercel.json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend.railway.app/api/:path*"
    }
  ],
  "env": {
    "RAILWAY_API_URL": "https://your-backend.railway.app"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

**Railway Side Configuration:**
```javascript
// Express.js backend
const cors = require('cors');

app.use(cors({
  origin: [
    'https://your-frontend.vercel.app',
    'http://localhost:3000'  // for development
  ],
  credentials: true
}));

// Health check for Vercel to ping
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});
```

---

## Best Practices

### Pre-Deployment Checklist

```bash
# 1. Test build locally
npm run build

# 2. Test with Railway/Vercel environment variables
railway run npm start
# or
vercel dev

# 3. Verify Dockerfile (if using)
docker build -t test-app .
docker run -p 3000:3000 test-app

# 4. Check environment variables are set
railway variables
# or
vercel env pull

# 5. Ensure database migrations are handled
# Add to railway.json or use pre-deploy script
```

### Health Checks

```javascript
// Express.js health check
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy', timestamp: new Date() });
});

// With database check
app.get('/health', async (req, res) => {
  try {
    await db.query('SELECT 1');
    res.status(200).json({ status: 'healthy', database: 'connected' });
  } catch (error) {
    res.status(503).json({ status: 'unhealthy', error: error.message });
  }
});
```

---

## Quick Reference Commands

**Vercel:**
```bash
vercel                      # Deploy to preview
vercel --prod              # Deploy to production
vercel env pull            # Pull environment variables
vercel logs                # View logs (in dashboard)
vercel dev                 # Local development server
```

**Railway:**
```bash
railway up                 # Deploy
railway logs -f            # Follow logs
railway ssh                # SSH into service
railway variables          # List variables
railway status             # Check deployment status
```

---

**Last Updated:** 2025-11-23
**Maintained By:** @shawar-2.0
**Source:** DEPLOYMENT_EXPERT_SKILL.md.pdf

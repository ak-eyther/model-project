# Reference: Vercel Deployment Expert

## Table of Contents
- Vercel Deployment Expert
  - 1. Essential Vercel CLI Commands
  - 2. Vercel Troubleshooting Guide
    - 2.1 Build Failures
    - 2.2 Environment Variable Issues
    - 2.3 Domain & DNS Issues

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


# Vercel Deployment Skill

**Skill Type:** Deployment Management
**For Agent:** @shawar-2.0
**Platform:** Vercel (Frontend Hosting)

---

## Skill Purpose

This skill enables Vercel deployment management for React/Next.js frontends including project configuration, environment variables, domain management, and build optimization.

---

## Core Capabilities

### 1. Vercel CLI Commands

**Login & Project Setup:**
```bash
# Login to Vercel
vercel login

# Link to existing project
vercel link

# Check current project
vercel ls
```

**Deployment:**
```bash
# Deploy to preview (staging)
vercel

# Deploy to production
vercel --prod

# Deploy specific directory
vercel ./frontend --prod

# Check deployment status
vercel ls
```

**Environment Variables:**
```bash
# Add environment variable
vercel env add [KEY]

# List all environment variables
vercel env ls

# Pull environment variables to .env.local
vercel env pull

# Remove environment variable
vercel env rm [KEY]
```

**Domain Management:**
```bash
# List domains
vercel domains ls

# Add domain
vercel domains add [domain]

# Remove domain
vercel domains rm [domain]
```

**Logs & Monitoring:**
```bash
# View deployment logs
vercel logs [deployment-url]

# List recent deployments
vercel ls

# Inspect deployment
vercel inspect [deployment-url]
```

### 2. Vercel Project Structure

**Typical React Frontend:**
- Framework: React + Vite (or Next.js)
- Build Command: `npm run build` or `yarn build`
- Output Directory: `dist` (Vite) or `.next` (Next.js)
- Install Command: `npm install` or `yarn install`

**Environment Variables to Configure:**
- `VITE_API_URL` - Backend API URL (Railway service)
- `VITE_ENVIRONMENT` - `development`, `staging`, or `production`
- `VITE_ANTHROPIC_API_KEY` - (if frontend calls Claude directly)

**Vercel Environment Scopes:**
- `Production` - Main branch deployments
- `Preview` - Feature branch deployments
- `Development` - Local development

### 3. Deployment Workflow

**Standard Deployment Process:**
1. Ensure code is pushed to git (Vercel auto-deploys from git)
2. Verify environment variables are set for target environment
3. Check Vercel dashboard for deployment status
4. Monitor build logs for errors
5. Verify deployment URL loads correctly
6. Test critical frontend features
7. Verify API calls to backend work (CORS check)
8. Monitor for 10+ minutes post-deployment

**Branch to Environment Mapping:**
- `development` branch → Preview deployment
- `staging` branch → Staging/Preview deployment
- `main` branch → Production deployment

### 4. Vercel Configuration Files

**vercel.json** (at project root):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

**vite.config.ts** (for React + Vite):
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: true
  },
  server: {
    port: 3000
  }
})
```

### 5. Health Check Protocol

**After Every Deployment:**
```bash
# Check deployment status
vercel ls

# Test deployment URL
curl https://[deployment-url]

# Test API integration
# Open browser DevTools, check Network tab for backend calls
```

**Health Check Success Criteria:**
- ✅ Deployment status shows "Ready"
- ✅ Homepage loads without errors
- ✅ No console errors in browser DevTools
- ✅ API calls to backend succeed (check Network tab)
- ✅ Assets load correctly (CSS, JS, images)
- ✅ Routing works (SPA routing via rewrites)

### 6. Troubleshooting Guide

**Common Issues:**

**Issue: Build fails with "Module not found"**
- Check: `package.json` has all dependencies
- Check: No TypeScript errors
- Check: Import paths are correct (case-sensitive on Vercel)
- Solution: Fix imports, commit, Vercel auto-redeploys

**Issue: "404 Not Found" on page refresh**
- Check: `vercel.json` has rewrite rules for SPA routing
- Solution: Add rewrite rule `"source": "/(.*)", "destination": "/index.html"`

**Issue: Environment variables not working**
- Check: Variables are set in correct environment (Production/Preview)
- Check: Variable names use correct prefix (`VITE_` for Vite, `NEXT_PUBLIC_` for Next.js)
- Check: Variables are exposed to browser (only `VITE_*` or `NEXT_PUBLIC_*`)
- Solution: Update variables, trigger redeploy

**Issue: CORS errors when calling backend**
- Check: Backend `CORS_ORIGINS` includes Vercel domain
- Check: Backend is deployed and running
- Check: API URL is correct in frontend env vars
- Solution: Update backend CORS config, redeploy backend

**Issue: Build exceeds time limit**
- Check: Build command is optimized
- Check: No unnecessary dependencies
- Solution: Optimize build, remove unused packages

**Issue: Assets not loading (404 for CSS/JS)**
- Check: Build output directory is correct (`dist` vs `.next`)
- Check: Asset paths in HTML are relative, not absolute
- Solution: Update build config, fix asset paths

### 7. Rollback Procedure

**If Deployment Fails:**
1. Check Vercel dashboard for failed deployment
2. Review build logs
3. If critical: Use Vercel instant rollback
4. Or revert git commit and push

**Vercel Instant Rollback:**
```bash
# List recent deployments
vercel ls

# Promote previous deployment to production
vercel promote [previous-deployment-url] --prod
```

**Git Rollback:**
```bash
git revert [bad-commit-hash]
git push origin [branch-name]
# Vercel will auto-deploy the revert
```

---

## Vercel-Specific Best Practices

1. **Use environment variables** - Never hardcode API URLs or secrets
2. **Enable automatic deployments** - Faster than manual CLI
3. **Use preview deployments** - Test on every PR
4. **Set up custom domains** - Professional URLs
5. **Monitor analytics** - Vercel provides Core Web Vitals
6. **Optimize images** - Use Vercel Image Optimization (if Next.js)
7. **Configure caching** - Set appropriate cache headers
8. **Security headers** - Add in `vercel.json`

---

## Integration with Other Tools

**With Railway (Backend):**
- Ensure frontend `VITE_API_URL` points to Railway domain
- Backend must allow Vercel domain in CORS
- Keep frontend/backend deployments synchronized

**With Git:**
- Vercel watches git branches for changes
- Push to branch → Automatic deployment
- Preview deployments for every PR

**With GitHub:**
- Vercel GitHub integration provides:
  - Deployment comments on PRs
  - Preview URLs for every commit
  - Build status checks

---

## Vercel Dashboard Features

**Key Sections:**
1. **Deployments** - View all deployments, logs, and status
2. **Environment Variables** - Manage env vars per environment
3. **Domains** - Configure custom domains and SSL
4. **Analytics** - View Web Vitals and usage stats
5. **Settings** - Project configuration and integrations

**URLs:**
- Dashboard: https://vercel.com/dashboard
- Project: `https://vercel.com/[team]/[project]`
- Deployments: `https://vercel.com/[team]/[project]/deployments`

---

## Performance Optimization

**Vercel Edge Network:**
- Automatic global CDN
- Edge caching for static assets
- Brotli/Gzip compression

**Build Optimization:**
```bash
# Analyze bundle size
npm run build -- --analyze

# Enable minification (usually default)
# Check vite.config.ts or next.config.js
```

**Caching Strategy:**
```json
{
  "headers": [
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

---

## Success Metrics

**Deployment is successful when:**
- ✅ Vercel dashboard shows "Ready" status
- ✅ Deployment URL loads in browser
- ✅ No errors in browser console
- ✅ API calls to backend succeed
- ✅ Routing works correctly (SPA navigation)
- ✅ Core Web Vitals are green (LCP < 2.5s, FID < 100ms, CLS < 0.1)
- ✅ No 404 errors for assets

---

## Quick Reference

**Deploy to production:**
```bash
vercel --prod
```

**Check deployment status:**
```bash
vercel ls
```

**Update environment variable:**
```bash
vercel env add VITE_API_URL
# Enter value when prompted
# Then redeploy to apply
```

**Instant rollback:**
```bash
vercel ls
vercel promote [previous-url] --prod
```

**Monitor logs:**
```bash
vercel logs [deployment-url]
```

---

## Environment-Specific Domains

**Production:**
- https://claude-code-project-template.vercel.app

**Staging:**
- https://claude-code-project-template-staging.vercel.app

**Preview (per-branch):**
- https://claude-code-project-template-[branch].vercel.app

---

**Last Updated:** 2025-11-23
**Maintained By:** @shawar-2.0
**Related Skill:** `railway-deploy.md`

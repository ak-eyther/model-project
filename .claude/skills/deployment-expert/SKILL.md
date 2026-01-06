---
name: deployment-expert
description: Comprehensive Vercel + Railway deployment expert guide for debugging build/runtime issues and best practices.
metadata:
  short-description: Vercel and Railway deployment expert
---

# Deployment Expert Skill - Vercel & Railway

**Skill Type:** Comprehensive Deployment Management
**For Agent:** @shawar-2.0
**Platforms:** Vercel (Frontend) + Railway (Backend)

---

## Overview

This skill enables AI agents to act as deployment experts for Vercel and Railway. It provides CLI guidance, troubleshooting techniques, and investigation strategies for debugging deployment issues.

**Target Use Cases:**
- Investigate deployment failures
- Debug build errors
- Fix environment variable issues
- Troubleshoot domain and networking problems
- Optimize deployment performance
- Handle serverless function errors

---

## Vercel Deployment Expert

Use for frontend deployments and edge/serverless issues.

Start here:
1. Check build logs and reproduce locally.
2. Verify env vars and project settings (build command, output dir).
3. Validate domain/DNS and SSL when applicable.

Detailed guide:
- `references/vercel.md` (CLI commands, troubleshooting, DNS)

---

## Railway Deployment Expert

Use for backend/API runtime and infrastructure issues.

Start here:
1. Check build logs, then runtime logs.
2. Verify `$PORT` usage, start command, and env vars.
3. Test health endpoints and database connectivity.

Detailed guide:
- `references/railway.md` (CLI commands, troubleshooting)

---

## Cross-Platform Deployment Strategies

Use when choosing between platforms or wiring Vercel frontend to Railway backend.

See `references/cross-platform.md` for the decision tree and hybrid configuration examples.

---

## Best Practices and Quick Commands

See `references/operations.md` for the pre-deploy checklist, health checks, and quick reference commands.

---

**Last Updated:** 2025-11-23
**Maintained By:** @shawar-2.0
**Source:** DEPLOYMENT_EXPERT_SKILL.md.pdf

# Initialization Wizards - Comparison Guide

## 🎯 Two Wizards Available

This template provides **two initialization wizards** for different use cases:

---

## Quick Wizard (Python)

**File:** `init-project.py`

### Best For
- ✅ Fast setup (5 minutes)
- ✅ Simple projects
- ✅ When you want app files updated automatically
- ✅ Next.js + FastAPI projects (default stack)

### What It Does
1. Asks 8 core questions:
   - Project name & slug
   - Tech stack (frontend/backend)
   - Deployment platforms
   - Domain/industry
   - Author info

2. Automatically updates these files:
   - ✅ `package.json` (name, description, author)
   - ✅ `app/layout.tsx` (page title, metadata)
   - ✅ `app/page.tsx` (landing page heading)
   - ✅ `main.py` (API title, description)
   - ✅ `README.md` (project title)
   - ✅ `.claude/context/project-context.yaml` (agent context)

### Usage
```bash
python3 init-project.py
```

### Interface
- 🎨 Colorful terminal UI (uses `questionary` library)
- 📋 Multiple-choice selections
- ⚡ Fast and user-friendly

---

## Full Wizard (Bash)

**File:** `.claude/scripts/init-project.sh`

### Best For
- ✅ Comprehensive setup (10-15 minutes)
- ✅ Complex projects
- ✅ When you need detailed configuration
- ✅ Database setup, quality standards, team info

### What It Does
1. Asks 15+ detailed questions:
   - Project basics (name, slug, description, root path)
   - Tech stack (frontend, backend, database)
   - Deployment (platforms, URLs)
   - Domain context (industry, users, compliance)
   - Team info (admin, GitHub, branches)

2. Creates comprehensive configuration:
   - ✅ `.claude/context/project-context.yaml` (detailed)
   - ✅ `CLAUDE.md` (updated with sed)
   - ✅ Includes quality standards (TypeScript strict, coverage, bundle size)
   - ✅ Security requirements (CORS, XSS prevention)
   - ✅ Accessibility standards (WCAG 2.1 AA)

### Usage
```bash
./.claude/scripts/init-project.sh
```

### Interface
- 🖥️ Standard bash prompts
- 📝 Text input with defaults
- 🔧 More detailed configuration

---

## Quick Comparison

| Feature | Quick Wizard (Python) | Full Wizard (Bash) |
|---------|----------------------|-------------------|
| **Time** | 5 minutes | 10-15 minutes |
| **Questions** | 8 | 15+ |
| **UI** | Colorful, interactive | Standard bash |
| **Files Updated** | 6 files | 2 files (but more detailed) |
| **Updates App Files** | ✅ Yes (package.json, layout, page, main.py) | ❌ No (only CLAUDE.md) |
| **Database Config** | ❌ No | ✅ Yes (postgres/mongodb/mysql) |
| **Quality Standards** | ❌ No | ✅ Yes (coverage, bundle size, etc.) |
| **Security Config** | ❌ No | ✅ Yes (CORS, XSS, etc.) |
| **Best For** | Simple/fast setup | Detailed/production setup |

---

## Which Should You Use?

### Use Quick Wizard If:
- ✅ You want to start coding immediately
- ✅ You're using Next.js + FastAPI (default stack)
- ✅ You want your app files auto-updated
- ✅ You'll configure details later

**Example:** Prototyping, hackathons, simple projects

### Use Full Wizard If:
- ✅ You need database configuration
- ✅ You want quality standards defined
- ✅ You're setting up production infrastructure
- ✅ You need compliance/security settings (HIPAA, GDPR)

**Example:** Enterprise projects, client work, regulated industries

---

## Running Both Wizards

You can run **both** wizards if you want:

```bash
# First, run quick wizard (updates app files)
python3 init-project.py

# Then, run full wizard (adds detailed config)
./.claude/scripts/init-project.sh
# → Choose "Yes" when asked to overwrite
```

**Result:** App files are updated AND you get comprehensive configuration!

---

## What Each Creates

### Quick Wizard Output

```yaml
# .claude/context/project-context.yaml (simplified)
project:
  name: "Task Manager Pro"
  slug: "task-manager-pro"
  description: "AI-powered claims processing"
  author:
    name: "Arif Khan"
    email: "arif.khan@vitraya.com"

tech_stack:
  frontend:
    framework: "Next.js"
  backend:
    framework: "FastAPI"

deployment:
  frontend:
    platform: "Vercel"
  backend:
    platform: "Railway"

domain:
  industry: "SaaS"
```

### Full Wizard Output

```yaml
# .claude/context/project-context.yaml (comprehensive)
project:
  name: "Task Manager Pro"
  slug: "task-manager-pro"
  description: "AI-powered claims processing"
  root: "/Users/arif/task-manager-pro"
  created: "2025-11-24T14:30:00"
  tier: "complete"
  admin: "arif.khan@vitraya.com"

tech_stack:
  frontend:
    framework: "Next.js"
    version: "14.0.0"
    language: "TypeScript"
    styling: "Tailwind CSS"
    build_tool: "Vite"

  backend:
    framework: "FastAPI"
    version: "0.104.0"
    language: "Python"
    version_python: "3.11"
    database: "postgres"

  ai:
    provider: "Anthropic"
    model: "claude-sonnet-4"

deployment:
  frontend:
    platform: "Vercel"
    production_url: "https://task-manager.vercel.app"
    staging_url: "https://task-manager-staging.vercel.app"

  backend:
    platform: "Railway"
    production_url: "https://task-manager-prod.up.railway.app"
    staging_url: "https://task-manager-staging.up.railway.app"

domain_context:
  industry: "SaaS"
  domain: "Task Management"
  users: "Project managers, Team members"
  sensitivity: "SOC2 compliant"
  key_entities: ["Claims", "Patients", "Providers"]

repository:
  github_url: "https://github.com/arif/task-manager-pro"
  main_branch: "master"
  protected_branches: ["main", "staging", "development"]

quality_standards:
  typescript_strict: true
  test_coverage_min: 80
  bundle_size_max: "500KB"
  accessibility: "WCAG 2.1 AA"
  security:
    - "Input validation"
    - "XSS prevention"
    - "CORS restrictions"
    - "No hardcoded secrets"

template:
  version: "1.0.0"
  initialized: true
```

**Notice:** Full wizard includes database, quality standards, security requirements, etc.

---

## Recommendation

### For Most Users: Start with Quick Wizard

```bash
./setup.sh
# → Choose option 1: "Quick wizard"
```

**Why?**
- Updates your app files immediately
- You see changes in the UI right away
- Faster time-to-coding

**Then later**, if you need detailed configuration:
```bash
./.claude/scripts/init-project.sh
```

---

## Integrated in setup.sh

When you run `./setup.sh`, you'll see:

```
Would you like to initialize this project now?
   1. Yes - Quick wizard (Python - updates app files)
   2. Yes - Full wizard (Bash - comprehensive setup)
   3. No - I'll do it later

Enter choice [1-3]:
```

**Choose based on your needs!**

---

## Re-running Wizards

Both wizards detect if already initialized:

```bash
python3 init-project.py
# ⚠️  Project already initialized. Overwrite? (y/N):

./.claude/scripts/init-project.sh
# ⚠️  Project already initialized!
#    Do you want to re-initialize? (y/N):
```

**Safe to re-run anytime** to update configuration!

---

## Summary

- **Quick Wizard** = Fast, simple, updates app files ✅
- **Full Wizard** = Comprehensive, detailed, production-ready ✅
- **Both are valid** - use what fits your needs!
- **No conflicts** - both create same context file (different levels of detail)

Choose wisely and start building! 🚀

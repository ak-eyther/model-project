# Quick Start Guide - Starting a New Project

This guide shows you how to use this template as the foundation for any new project.

---

## 🎯 Overview

This template provides:
- ✅ **Next.js 14** frontend (App Router, TypeScript, Tailwind)
- ✅ **FastAPI** backend (Python, async support, auto-docs)
- ✅ **15 AI agents** for development workflows
- ✅ **Auto-setup scripts** for one-command initialization
- ✅ **Project context system** that customizes everything for your use case

---

## 🚀 Three Ways to Start

### Option 1: Full Setup (Recommended)

**Best for:** New projects where you want everything configured for your specific use case.

```bash
# 1. Clone/download this template
git clone https://github.com/yourusername/claude-code-project-template.git my-new-project
cd my-new-project

# 2. Run setup (installs dependencies + launches wizard)
./setup.sh

# The wizard will ask:
#   - Project name (e.g., "E-commerce Dashboard")
#   - Tech stack confirmation (Next.js + FastAPI)
#   - Deployment platforms (Vercel + Railway)
#   - Domain/industry (E-commerce, Healthcare, etc.)
#   - Author info

# 3. Start developing
npm run dev                    # Frontend: http://localhost:3000
uvicorn main:app --reload      # Backend: http://localhost:8000
```

**What gets customized:**
- ✅ `package.json` → Your project name and description
- ✅ `app/layout.tsx` → Page title and metadata
- ✅ `app/page.tsx` → Landing page with your project name
- ✅ `main.py` → FastAPI title and description
- ✅ `README.md` → Updated with your project details
- ✅ `.claude/context/project-context.yaml` → All 15 agents know your project

---

### Option 2: Quick Setup (Skip Wizard)

**Best for:** Prototyping or when you want to customize manually later.

```bash
# 1. Clone template
git clone https://github.com/yourusername/claude-code-project-template.git my-prototype
cd my-prototype

# 2. Install dependencies only (no customization)
./setup.sh
# → Choose option 2 when asked

# 3. Start coding with template defaults
npm run dev
uvicorn main:app --reload
```

You can customize later by running:
```bash
python3 init-project.py
```

---

### Option 3: Manual Customization

**Best for:** When you want full control over every detail.

```bash
# 1. Clone template
git clone https://github.com/yourusername/claude-code-project-template.git my-app
cd my-app

# 2. Install dependencies
./setup.sh

# 3. Manually edit files
#    - package.json (name, description, author)
#    - app/layout.tsx (title, description)
#    - app/page.tsx (project name)
#    - main.py (API title, description)
#    - README.md (project overview)

# 4. Create project context for agents
mkdir -p .claude/context
# Copy and edit project-context.yaml.example → project-context.yaml
```

---

## 📋 What the Wizard Customizes

When you run `python3 init-project.py`, it asks for:

### 1. Project Basics
- **Project Name:** "Task Manager Pro"
- **Slug:** "task-manager-pro" (for URLs)
- **Description:** "Team task management application tool"

### 2. Tech Stack
- Frontend: Next.js / React / Vue.js
- Backend: FastAPI / Express / Django / Flask
- AI/ML: Yes/No

### 3. Deployment
- Frontend: Vercel / Netlify / AWS
- Backend: Railway / Render / AWS / GCP

### 4. Domain/Industry
- Healthcare, Finance, E-commerce, SaaS, etc.

### 5. Author Info
- Your name and email
- GitHub repository URL

**Result:** Everything is renamed and configured for your project!

---

## 🎨 Example: Creating "Task Manager Pro"

```bash
# Start wizard
python3 init-project.py

# Answers:
#   Project name: Task Manager Pro
#   Slug: task-manager-pro
#   Description: Team task management with AI prioritization
#   Frontend: Next.js
#   Backend: FastAPI
#   AI/ML: Yes
#   Deployment: Vercel + Railway
#   Domain: SaaS
#   Author: Arif Khan (arif.khan@vitraya.com)

# Output:
#   ✅ Updated package.json → task-manager-pro
#   ✅ Updated app/layout.tsx → Task Manager Pro
#   ✅ Updated app/page.tsx → Task Manager Pro
#   ✅ Updated main.py → Task Manager Pro API
#   ✅ Created .claude/context/project-context.yaml
#   ✅ Updated README.md → Task Manager Pro
```

Now visit http://localhost:3000 and see "Task Manager Pro" everywhere!

---

## 🤖 How Agents Use This Context

All 15 agents automatically load `.claude/context/project-context.yaml` and know:

- **@anand-2.0** (Code Executor): "I'm working on Task Manager Pro, a SaaS app"
- **@shawar-2.0** (Deployment): "Deploy to Vercel (frontend) and Railway (backend)"
- **@sama-2.0** (AI/ML): "This project uses AI for task prioritization"
- **@harshit-2.0** (Testing): "Test the task management features"

**No manual agent configuration needed!**

---

## 🔄 Re-initializing a Project

Already initialized but want to change details?

```bash
python3 init-project.py
# → Choose "Yes" when asked to overwrite

# Re-answer all questions with new values
```

---

## 📦 What's Included Out-of-the-Box

After initialization, you get:

### Frontend
- ✅ Next.js 14 with App Router
- ✅ TypeScript strict mode
- ✅ Tailwind CSS with dark mode
- ✅ Beautiful landing page
- ✅ API proxy to backend (`/api/*` → FastAPI)

### Backend
- ✅ FastAPI with auto-docs (`/docs`)
- ✅ CORS configured for Next.js
- ✅ Health check endpoint
- ✅ Example API route

### Development
- ✅ Hot reload (both frontend and backend)
- ✅ ESLint + TypeScript checking
- ✅ Git hooks for code quality

### AI Agents
- ✅ 15 specialized agents
- ✅ Auto-context loading
- ✅ Memory system
- ✅ Quality gates

---

## 🎯 Common Use Cases

### Use Case 1: SaaS Product
```bash
python3 init-project.py
# → Domain: SaaS
# → AI/ML: Yes (for smart features)
# → Deployment: Vercel + Railway
```

### Use Case 2: Internal Tool
```bash
python3 init-project.py
# → Domain: Internal Tools
# → AI/ML: No
# → Deployment: AWS (self-hosted)
```

### Use Case 3: Client Project
```bash
python3 init-project.py
# → Domain: E-commerce
# → AI/ML: No
# → Deployment: Client's hosting
# → Repository: https://github.com/client/project-name
```

---

## 🛠️ Troubleshooting

**Q: "I ran setup but nothing is customized"**
- A: Run `python3 init-project.py` separately

**Q: "Can I change the tech stack after initialization?"**
- A: Yes! Re-run `python3 init-project.py` or manually edit files

**Q: "Do I need to use all 15 agents?"**
- A: No! Use only the agents you need. They work independently.

**Q: "Can I add my own agents?"**
- A: Yes! See `.claude/agents/README.md` for how to create custom agents

---

## 📚 Next Steps

1. ✅ **Initialize project:** `./setup.sh` or `python3 init-project.py`
2. ✅ **Start development:** `npm run dev` + `uvicorn main:app --reload`
3. ✅ **Explore agents:** `@anand-2.0 help me get started`
4. ✅ **Read docs:** Check `README.md` and `.claude/docs/`
5. ✅ **Start building:** Add your features!

---

**Welcome to production-grade development with AI agents! 🚀**

# Auto-Context System - Quick Reference

**Last Updated:** 2025-11-23

---

## 🚀 For New Users (Creating Project from Template)

### Step 1: Create Repository from Template

**On GitHub:**
1. Go to: https://github.com/arifkhan/claude-code-project-template
2. Click **"Use this template"** → **"Create a new repository"**
3. Name your repository (e.g., "my-medical-app")
4. Click **"Create repository"**

### Step 2: Clone and Initialize

```bash
# Clone your new repository
git clone https://github.com/your-org/my-medical-app.git
cd my-medical-app

# Run initialization script (interactive)
./.claude/scripts/init-project.sh
```

### Step 3: Answer Prompts

The script will ask:

**Project Info:**
- Project Name: `My Medical App`
- Project Slug: `my-medical-app`
- Description: `Medical records management system`

**Tech Stack:**
- Frontend Framework: `React` (or Vue, Svelte, Next.js, Angular)
- Backend Framework: `FastAPI` (or Express, Django, Flask, NestJS)
- Database: `postgres` (or mongodb, mysql, none)

**Deployment:**
- Frontend Platform: `Vercel` (or Netlify, AWS S3, GitHub Pages)
- Backend Platform: `Railway` (or Render, AWS EC2, Cloud Run, Heroku)
- Production Frontend URL: `https://my-medical-app.vercel.app`
- Staging Frontend URL: `https://my-medical-app-staging.vercel.app`
- Production Backend URL: `https://my-medical-app-prod.up.railway.app`
- Staging Backend URL: `https://my-medical-app-staging.up.railway.app`

**Domain (Optional):**
- Industry: `Healthcare`
- Domain: `Medical Records Management`
- Users: `Healthcare providers, medical staff`
- Compliance: `HIPAA`

**Team:**
- Admin Email: `you@company.com`
- GitHub URL: `https://github.com/your-org/my-medical-app`
- Main Branch: `master` (or main)

### Step 4: Commit Context

```bash
# Review generated context
cat .claude/context/project-context.yaml

# Validate
./.claude/scripts/validate-context.sh

# Commit
git add .claude/context/project-context.yaml CLAUDE.md
git commit -m "Initialize project context for My Medical App"
git push
```

### Step 5: Start Using Agents

```bash
# All agents now have your project's full context!
/anand implement user authentication
/shawar deploy to staging
/atharva plan new feature: patient dashboard
```

**Agents automatically know:**
- ✅ Your project name: "My Medical App"
- ✅ Your tech stack: React + FastAPI
- ✅ Your deployment: Vercel + Railway
- ✅ Your URLs: Production and staging
- ✅ Your domain: Healthcare, HIPAA-compliant

---

## 🔧 For Maintainers (Managing Template Repo)

### Files to Keep Updated

**1. Context Template:**
```bash
.claude/context/project-context.yaml
```
- Keep as template (with placeholder values)
- Set `initialized: false`
- Update when adding new context fields

**2. Initialization Script:**
```bash
.claude/scripts/init-project.sh
```
- Update prompts when adding new fields
- Keep backend/frontend framework options current
- Update deployment platform choices

**3. Validation Script:**
```bash
.claude/scripts/validate-context.sh
```
- Update `required_fields` array when schema changes
- Update `optional_fields` for recommended fields

**4. Agent Frontmatter:**
```bash
.claude/agents/*.md
```
- All agent files include context frontmatter
- Update via `.claude/scripts/add-context-to-agents.sh`

---

## 📋 Common Commands

```bash
# Initialize new project context
./.claude/scripts/init-project.sh

# Validate context completeness
./.claude/scripts/validate-context.sh

# Add context to agent files (for new agents)
./.claude/scripts/add-context-to-agents.sh

# View current context
cat .claude/context/project-context.yaml

# Edit context manually
vim .claude/context/project-context.yaml
```

---

## 🔄 Updating Project Context

### When to Update

Update `.claude/context/project-context.yaml` when:
- Tech stack changes (e.g., React 18 → 19)
- Deployment URLs change
- New environment added
- Domain context evolves

### How to Update

```bash
# 1. Edit context file
vim .claude/context/project-context.yaml

# 2. Update values (e.g., React version)
tech_stack:
  frontend:
    framework: "React"
    version: "19.0.0"  # Changed

# 3. Validate
./.claude/scripts/validate-context.sh

# 4. Commit
git add .claude/context/project-context.yaml
git commit -m "Update React to v19"
git push

# 5. Agents use new context on next invocation
```

---

## 🎯 Context Variables Reference

### Project Variables

```yaml
{{ project.name }}               # "My Medical App"
{{ project.slug }}               # "my-medical-app"
{{ project.description }}        # "Medical records management"
{{ project.root }}               # "/path/to/project"
{{ project.admin }}              # "you@company.com"
```

### Tech Stack Variables

```yaml
{{ tech_stack.frontend.framework }}      # "React"
{{ tech_stack.frontend.version }}        # "18.2.0"
{{ tech_stack.backend.framework }}       # "FastAPI"
{{ tech_stack.backend.version }}         # "0.104.0"
{{ tech_stack.backend.language }}        # "Python"
```

### Deployment Variables

```yaml
{{ deployment.frontend.platform }}       # "Vercel"
{{ deployment.backend.platform }}        # "Railway"
{{ deployment.frontend.production_url }} # "https://app.vercel.app"
{{ deployment.backend.production_url }}  # "https://api.railway.app"
```

### Domain Variables

```yaml
{{ domain_context.industry }}    # "Healthcare"
{{ domain_context.domain }}      # "Medical Records"
{{ domain_context.users }}       # "Healthcare providers"
{{ domain_context.sensitivity }} # "HIPAA"
```

### Repository Variables

```yaml
{{ repository.github_url }}      # "https://github.com/org/repo"
{{ repository.main_branch }}     # "master"
```

---

## 🛠️ Troubleshooting

### Problem: Validation fails with missing fields

```bash
❌ Missing field: tech_stack.frontend.framework
```

**Solution:**
```bash
# Re-run initialization
./.claude/scripts/init-project.sh

# Or edit manually
vim .claude/context/project-context.yaml
```

### Problem: Agent doesn't have project context

**Check:**
1. Does `.claude/context/project-context.yaml` exist?
2. Does agent file have context frontmatter?
   ```bash
   grep -A 10 "context:" .claude/agents/anand-2.0.md
   ```
3. Is `initialized: true` in context file?

**Solution:**
```bash
# Add context frontmatter to agent
./.claude/scripts/add-context-to-agents.sh
```

### Problem: Template placeholders still present

```bash
⚠️ Template placeholders detected
```

**This is expected for the template repo itself.**

For new projects created from template:
```bash
# Re-run init to replace placeholders
./.claude/scripts/init-project.sh
```

---

## 📚 Additional Documentation

- **Complete Guide:** `.claude/docs/guides/AUTO_CONTEXT_SYSTEM.md`
- **Anthropic Skills Guide:** `.claude/docs/guides/ANTHROPIC_SKILLS_EXTRACTION_GUIDE.md`
- **Project Setup:** `CLAUDE.md`

---

## ✅ Quick Validation Checklist

After initialization, verify:

```bash
# 1. Context file exists
[ -f .claude/context/project-context.yaml ] && echo "✅" || echo "❌"

# 2. Initialized flag is true
grep -q "initialized: true" .claude/context/project-context.yaml && echo "✅" || echo "❌"

# 3. No template placeholders
! grep -q "claude-code-project-template" .claude/context/project-context.yaml && echo "✅" || echo "❌"

# 4. Validation passes
./.claude/scripts/validate-context.sh && echo "✅" || echo "❌"

# 5. All agents have context frontmatter
grep -l "context:" .claude/agents/*.md | wc -l  # Should be 14-15
```

---

**Last Updated:** 2025-11-23
**Maintained By:** @documentation-manager

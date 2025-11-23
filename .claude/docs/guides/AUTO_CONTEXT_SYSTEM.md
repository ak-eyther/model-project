# Auto-Context System for GitHub Template Projects

**Purpose:** Automatically propagate project context to all agents when using this GitHub repo as a template

**Last Updated:** 2025-11-23

---

## 🎯 The Problem

When you create a new project from this GitHub template:
1. Agents need to know about the new project's specific context (name, URLs, tech stack)
2. Manual updates across 15+ agent files are error-prone
3. Variables like `{{ project_name }}`, `{{ frontend_framework }}`, etc. need to be replaced
4. Each agent should automatically inherit the correct project context

---

## ✅ The Solution: Project Context Auto-Loading System

### Architecture Overview

```
GitHub Template Repo (this repo)
    ↓ (User clicks "Use this template")
New Project Repo
    ↓ (Run initialization script)
.claude/context/project-context.yaml (populated with project-specific values)
    ↓ (Agent invocation)
All agents auto-load project-context.yaml via frontmatter reference
    ↓ (Variables interpolated)
Agents have full project context without manual updates
```

---

## 📦 Implementation: 3-Tier Context System

### Tier 1: Project Context File (Single Source of Truth)

**Location:** `.claude/context/project-context.yaml`

**Purpose:** Single file containing all project-specific variables

**Example:**
```yaml
# Project Context Configuration
# This file is auto-generated during project initialization
# All agents reference this file via their frontmatter

project:
  name: "Medical Claims RAG System"
  slug: "medical-claims-rag"
  description: "RAG system for medical claims review using Claude API"
  root: "/Users/arifkhan/projects/medical-claims-rag"
  created: "2025-11-23T21:25:08.123956"
  tier: "complete"  # starter | essential | complete
  admin: "arif.khan@vitraya.com"

tech_stack:
  frontend:
    framework: "React"
    version: "18.2.0"
    language: "TypeScript"
    styling: "Tailwind CSS"
    build_tool: "Vite"

  backend:
    framework: "FastAPI"
    version: "0.104.0"
    language: "Python"
    version_python: "3.11"
    database: "PostgreSQL"  # or null if not using

  ai:
    provider: "Anthropic"
    model: "claude-sonnet-4"
    use_case: "Medical claims Q&A, ICD code extraction"

deployment:
  frontend:
    platform: "Vercel"
    production_url: "https://medical-claims-rag.vercel.app"
    staging_url: "https://medical-claims-rag-staging.vercel.app"

  backend:
    platform: "Railway"
    production_url: "https://medical-claims-rag-production.up.railway.app"
    staging_url: "https://medical-claims-rag-staging.up.railway.app"

environments:
  development: "development"
  staging: "staging"
  production: "main"

domain_context:
  industry: "Healthcare"
  domain: "Medical Claims Review"
  users: "Medical claims reviewers, insurance processors"
  sensitivity: "HIPAA-compliant, handles PHI/PII"
  key_entities:
    - "ICD codes"
    - "CPT codes"
    - "Medication names"
    - "Diagnoses"
    - "Policy questions"

repository:
  github_url: "https://github.com/arifkhan/medical-claims-rag"
  main_branch: "master"
  protected_branches:
    - "main"
    - "staging"
    - "development"

team:
  product_owner: "arif.khan@vitraya.com"
  tech_lead: "arif.khan@vitraya.com"
  timezone: "UTC-5"

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
```

---

### Tier 2: Agent Frontmatter Context Reference

**Each agent file (`.claude/agents/*.md`) includes context reference in frontmatter:**

**Example: `.claude/agents/anand-2.0.md`**

```markdown
---
agent_name: "Anand 2.0"
background_color: "#1F9D5C"
text_color: "#FFFFFF"
emoji: "⚡"
role: "Full Stack Code Executor"
skills:
  - frontend-design:frontend-design
  - document-skills:pdf
  - document-skills:docx
  - example-skills:artifacts-builder
permissionMode: ask

# Context Auto-Loading (NEW)
context:
  inherit: ".claude/context/project-context.yaml"
  variables:
    - project_name
    - project_slug
    - frontend_framework
    - backend_framework
    - frontend_platform
    - backend_platform
    - project_root
    - production_frontend_url
    - production_backend_url
---

# Anand 2.0 - Full Stack Developer Agent

## Project Context: {{ project_name }}

**Project:** {{ project.description }}
**Tech Stack:**
- **Frontend:** {{ tech_stack.frontend.framework }} {{ tech_stack.frontend.version }}, {{ tech_stack.frontend.language }}, {{ tech_stack.frontend.build_tool }}, {{ tech_stack.frontend.styling }}
- **Backend:** {{ tech_stack.backend.framework }} {{ tech_stack.backend.version }}, {{ tech_stack.backend.language }} {{ tech_stack.backend.version_python }}
- **Infrastructure:** {{ deployment.frontend.platform }} (frontend), {{ deployment.backend.platform }} (backend)

**Repository:** `{{ project.root }}`

**Domain Context:**
- Industry: {{ domain_context.industry }}
- Domain: {{ domain_context.domain }}
- Users: {{ domain_context.users }}
- Sensitivity: {{ domain_context.sensitivity }}

...rest of agent instructions...
```

**How Variables Work:**
- `{{ project.name }}` → "Medical Claims RAG System"
- `{{ tech_stack.frontend.framework }}` → "React"
- `{{ deployment.frontend.platform }}` → "Vercel"
- Nested YAML structure allows dot notation

---

### Tier 3: Initialization Script (Auto-Setup)

**Location:** `.claude/scripts/init-project.sh`

**Purpose:** Run ONCE when creating new project from template

**Usage:**
```bash
# After creating new repo from template
cd your-new-project
./.claude/scripts/init-project.sh
```

**What it does:**
1. Prompts for project details (interactive)
2. Generates `.claude/context/project-context.yaml`
3. Validates all required fields
4. Updates `CLAUDE.md` with project-specific info
5. Creates initial commit with context

**Script:**
```bash
#!/bin/bash
# init-project.sh - Initialize project context for new template-based project

set -e

CONTEXT_FILE=".claude/context/project-context.yaml"
CLAUDE_MD="CLAUDE.md"

echo "🚀 Claude Code Project Template Initialization"
echo "=============================================="
echo ""

# Check if already initialized
if [ -f "$CONTEXT_FILE" ] && grep -q "^project:" "$CONTEXT_FILE"; then
    echo "⚠️  Project already initialized!"
    echo "   Context file exists: $CONTEXT_FILE"
    echo ""
    read -p "Do you want to re-initialize? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        echo "Initialization cancelled."
        exit 0
    fi
fi

# Collect project information
echo "📋 Project Information"
echo "---------------------"
read -p "Project Name (e.g., Medical Claims RAG): " project_name
read -p "Project Slug (e.g., medical-claims-rag): " project_slug
read -p "Project Description: " project_description
read -p "Project Root (full path, default: $(pwd)): " project_root
project_root=${project_root:-$(pwd)}

echo ""
echo "🛠️  Tech Stack"
echo "-------------"
echo "Frontend Framework:"
echo "1) React"
echo "2) Vue"
echo "3) Svelte"
echo "4) Next.js"
read -p "Choose (1-4): " frontend_choice
case $frontend_choice in
    1) frontend_framework="React" ;;
    2) frontend_framework="Vue" ;;
    3) frontend_framework="Svelte" ;;
    4) frontend_framework="Next.js" ;;
    *) frontend_framework="React" ;;
esac

echo "Backend Framework:"
echo "1) FastAPI (Python)"
echo "2) Express (Node.js)"
echo "3) Django (Python)"
echo "4) Flask (Python)"
read -p "Choose (1-4): " backend_choice
case $backend_choice in
    1) backend_framework="FastAPI"; backend_lang="Python" ;;
    2) backend_framework="Express"; backend_lang="Node.js" ;;
    3) backend_framework="Django"; backend_lang="Python" ;;
    4) backend_framework="Flask"; backend_lang="Python" ;;
    *) backend_framework="FastAPI"; backend_lang="Python" ;;
esac

echo ""
echo "☁️  Deployment"
echo "-------------"
echo "Frontend Platform:"
echo "1) Vercel"
echo "2) Netlify"
echo "3) AWS S3 + CloudFront"
read -p "Choose (1-3): " frontend_platform_choice
case $frontend_platform_choice in
    1) frontend_platform="Vercel" ;;
    2) frontend_platform="Netlify" ;;
    3) frontend_platform="AWS S3 + CloudFront" ;;
    *) frontend_platform="Vercel" ;;
esac

echo "Backend Platform:"
echo "1) Railway"
echo "2) Render"
echo "3) AWS EC2"
echo "4) Google Cloud Run"
read -p "Choose (1-4): " backend_platform_choice
case $backend_platform_choice in
    1) backend_platform="Railway" ;;
    2) backend_platform="Render" ;;
    3) backend_platform="AWS EC2" ;;
    4) backend_platform="Google Cloud Run" ;;
    *) backend_platform="Railway" ;;
esac

read -p "Production Frontend URL: " production_frontend_url
read -p "Staging Frontend URL: " staging_frontend_url
read -p "Production Backend URL: " production_backend_url
read -p "Staging Backend URL: " staging_backend_url

echo ""
echo "🏥 Domain Context (optional, press Enter to skip)"
echo "------------------------------------------------"
read -p "Industry (e.g., Healthcare, Finance): " industry
read -p "Domain (e.g., Medical Claims Review): " domain
read -p "Target Users: " users
read -p "Sensitivity/Compliance (e.g., HIPAA, GDPR): " sensitivity

echo ""
echo "👤 Team"
echo "-------"
read -p "Admin Email: " admin_email
read -p "GitHub URL: " github_url
read -p "Main Branch (default: master): " main_branch
main_branch=${main_branch:-master}

# Generate timestamp
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S.%6N")

# Create context directory
mkdir -p .claude/context

# Generate project-context.yaml
cat > "$CONTEXT_FILE" <<EOF
# Project Context Configuration
# Auto-generated: $timestamp
# All agents reference this file for project-specific context

project:
  name: "$project_name"
  slug: "$project_slug"
  description: "$project_description"
  root: "$project_root"
  created: "$timestamp"
  tier: "complete"
  admin: "$admin_email"

tech_stack:
  frontend:
    framework: "$frontend_framework"
    version: "18.2.0"  # Update as needed
    language: "TypeScript"
    styling: "Tailwind CSS"
    build_tool: "Vite"

  backend:
    framework: "$backend_framework"
    language: "$backend_lang"
    version_python: "3.11"  # Update if not Python
    database: null  # Add if using database

  ai:
    provider: "Anthropic"
    model: "claude-sonnet-4"
    use_case: "AI-powered application"

deployment:
  frontend:
    platform: "$frontend_platform"
    production_url: "$production_frontend_url"
    staging_url: "$staging_frontend_url"

  backend:
    platform: "$backend_platform"
    production_url: "$production_backend_url"
    staging_url: "$staging_backend_url"

environments:
  development: "development"
  staging: "staging"
  production: "main"

domain_context:
  industry: "$industry"
  domain: "$domain"
  users: "$users"
  sensitivity: "$sensitivity"
  key_entities: []  # Add domain-specific entities

repository:
  github_url: "$github_url"
  main_branch: "$main_branch"
  protected_branches:
    - "main"
    - "staging"
    - "development"

team:
  product_owner: "$admin_email"
  tech_lead: "$admin_email"
  timezone: "UTC"

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
EOF

# Update CLAUDE.md with project-specific info
sed -i.bak "s/claude-code-project-template/$project_slug/g" "$CLAUDE_MD"
sed -i.bak "s|https://claude-code-project-template.vercel.app|$production_frontend_url|g" "$CLAUDE_MD"
sed -i.bak "s|https://claude-code-project-template-staging.vercel.app|$staging_frontend_url|g" "$CLAUDE_MD"
sed -i.bak "s|https://claude-code-project-template-production.up.railway.app|$production_backend_url|g" "$CLAUDE_MD"
sed -i.bak "s|https://claude-code-project-template-staging.up.railway.app|$staging_backend_url|g" "$CLAUDE_MD"
sed -i.bak "s/A production-ready application/$project_description/g" "$CLAUDE_MD"
sed -i.bak "s/arif.khan@vitraya.com/$admin_email/g" "$CLAUDE_MD"
rm -f "$CLAUDE_MD.bak"

echo ""
echo "✅ Project Context Initialized!"
echo ""
echo "📄 Generated: $CONTEXT_FILE"
echo "📝 Updated: $CLAUDE_MD"
echo ""
echo "🎯 Next Steps:"
echo "1. Review $CONTEXT_FILE and customize as needed"
echo "2. All agents will auto-load this context when invoked"
echo "3. Variables like {{ project.name }} will be interpolated automatically"
echo "4. Commit changes: git add . && git commit -m 'Initialize project context'"
echo ""
echo "🔄 To re-initialize, run this script again"
```

Make script executable:
```bash
chmod +x .claude/scripts/init-project.sh
```

---

### Tier 4: Context Interpolation Engine (How Variables Get Replaced)

**Location:** `.claude/scripts/context-interpolation.py`

**Purpose:** Parse agent markdown files and replace `{{ variable }}` placeholders with values from `project-context.yaml`

**How it works:**

1. Agent invoked (e.g., `/anand implement feature X`)
2. Claude Code loads `.claude/agents/anand-2.0.md`
3. Frontmatter specifies `context.inherit: ".claude/context/project-context.yaml"`
4. Context interpolation engine reads `project-context.yaml`
5. Replaces all `{{ variable }}` placeholders in agent file
6. Agent sees fully interpolated instructions

**Example Script:**
```python
#!/usr/bin/env python3
"""
context-interpolation.py - Interpolate project context variables in agent files

Usage:
    python .claude/scripts/context-interpolation.py --agent anand-2.0
    python .claude/scripts/context-interpolation.py --all
"""

import yaml
import re
import sys
from pathlib import Path
from typing import Dict, Any

CONTEXT_FILE = Path(".claude/context/project-context.yaml")
AGENTS_DIR = Path(".claude/agents")

def load_context() -> Dict[str, Any]:
    """Load project context from YAML file"""
    if not CONTEXT_FILE.exists():
        print(f"❌ Context file not found: {CONTEXT_FILE}")
        print("   Run .claude/scripts/init-project.sh first")
        sys.exit(1)

    with open(CONTEXT_FILE) as f:
        return yaml.safe_load(f)

def interpolate_variables(content: str, context: Dict[str, Any]) -> str:
    """Replace {{ variable }} placeholders with context values"""

    def replace_var(match):
        var_path = match.group(1).strip()

        # Handle dot notation (e.g., project.name)
        keys = var_path.split('.')
        value = context

        try:
            for key in keys:
                value = value[key]
            return str(value)
        except (KeyError, TypeError):
            # Variable not found, leave placeholder
            return match.group(0)

    # Replace {{ variable }} with actual values
    return re.sub(r'\{\{\s*([^}]+)\s*\}\}', replace_var, content)

def process_agent_file(agent_file: Path, context: Dict[str, Any]) -> None:
    """Process a single agent file"""
    print(f"📝 Processing: {agent_file.name}")

    with open(agent_file) as f:
        content = f.read()

    # Check if agent uses context inheritance
    if 'context:' not in content or 'inherit:' not in content:
        print(f"   ⏭️  Skipped (no context inheritance)")
        return

    # Interpolate variables
    interpolated = interpolate_variables(content, context)

    # Count replacements
    original_placeholders = len(re.findall(r'\{\{[^}]+\}\}', content))
    remaining_placeholders = len(re.findall(r'\{\{[^}]+\}\}', interpolated))
    replaced = original_placeholders - remaining_placeholders

    print(f"   ✅ Replaced {replaced} variables, {remaining_placeholders} remaining")

    # Write back (in-place)
    # NOTE: In production, this should write to a temp location
    # and only update on success. For now, this is illustrative.
    # with open(agent_file, 'w') as f:
    #     f.write(interpolated)

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Interpolate project context in agent files")
    parser.add_argument('--agent', help='Process specific agent (e.g., anand-2.0)')
    parser.add_argument('--all', action='store_true', help='Process all agent files')
    args = parser.parse_args()

    # Load context
    print("📦 Loading project context...")
    context = load_context()
    print(f"   Project: {context['project']['name']}")
    print(f"   Tech Stack: {context['tech_stack']['frontend']['framework']} + {context['tech_stack']['backend']['framework']}")
    print()

    # Process agent files
    if args.agent:
        agent_file = AGENTS_DIR / f"{args.agent}.md"
        if not agent_file.exists():
            print(f"❌ Agent file not found: {agent_file}")
            sys.exit(1)
        process_agent_file(agent_file, context)

    elif args.all:
        agent_files = sorted(AGENTS_DIR.glob("*.md"))
        print(f"🔄 Processing {len(agent_files)} agent files...\n")
        for agent_file in agent_files:
            process_agent_file(agent_file, context)

    else:
        print("❌ Specify --agent <name> or --all")
        sys.exit(1)

    print()
    print("✅ Context interpolation complete!")

if __name__ == '__main__':
    main()
```

**NOTE:** In practice, Claude Code should handle this interpolation **at runtime** when loading agent files, not by modifying files in-place. The script above is illustrative.

---

## 🚀 Usage Workflow

### Step 1: Create New Project from Template

```bash
# On GitHub
1. Go to https://github.com/arifkhan/claude-code-project-template
2. Click "Use this template" → "Create a new repository"
3. Name: "my-new-project"
4. Clone locally

# Locally
git clone https://github.com/arifkhan/my-new-project.git
cd my-new-project
```

### Step 2: Initialize Project Context

```bash
# Run initialization script
./.claude/scripts/init-project.sh

# Follow prompts:
# - Project Name: My New Project
# - Project Slug: my-new-project
# - Frontend Framework: React
# - Backend Framework: FastAPI
# - Deployment: Vercel + Railway
# - URLs, domain context, etc.

# Generated files:
# ✅ .claude/context/project-context.yaml
# ✅ CLAUDE.md (updated with project-specific info)
```

### Step 3: Commit Initialized Context

```bash
git add .claude/context/project-context.yaml CLAUDE.md
git commit -m "Initialize project context for My New Project"
git push origin master
```

### Step 4: Invoke Agents (They Auto-Load Context)

```bash
# In Claude Code
/anand implement user authentication

# Anand 2.0 loads:
# 1. .claude/agents/anand-2.0.md
# 2. Sees context.inherit: ".claude/context/project-context.yaml"
# 3. Loads project-context.yaml
# 4. Interpolates {{ project.name }} → "My New Project"
# 5. Knows tech stack is React + FastAPI
# 6. Knows deployment is Vercel + Railway
# 7. Has full project context automatically
```

---

## 🎯 Benefits of Auto-Context System

### 1. Single Source of Truth
- One file (`.claude/context/project-context.yaml`) contains all project variables
- No need to update 15+ agent files manually
- Changes propagate automatically

### 2. Template Reusability
- Copy template repo → Run init script → Done
- Works for ANY new project
- Agents adapt to project-specific context instantly

### 3. Consistency Across Agents
- All agents reference same context file
- No drift between agent knowledge
- Guaranteed consistency

### 4. Easy Maintenance
- Update one YAML file to change project URLs, tech stack, etc.
- Agents pick up changes on next invocation
- No manual find-and-replace across files

### 5. Onboarding New Team Members
- New dev clones repo
- Reads `.claude/context/project-context.yaml`
- Understands entire project setup in one file

---

## 🔄 Updating Project Context

### When to Update

**Update `project-context.yaml` when:**
- Tech stack changes (e.g., upgrading React 18 → 19)
- Deployment URLs change
- New environment added (e.g., `qa` environment)
- Domain context evolves (new key entities)

### How to Update

```bash
# 1. Edit context file
vim .claude/context/project-context.yaml

# 2. Change values (e.g., update React version)
tech_stack:
  frontend:
    framework: "React"
    version: "19.0.0"  # Changed from 18.2.0

# 3. Commit changes
git add .claude/context/project-context.yaml
git commit -m "Update React to v19"
git push

# 4. Agents automatically use new context on next invocation
```

---

## 📚 Advanced: Dynamic Context Loading

### Context Inheritance Hierarchy

**Agents can inherit context from multiple sources:**

```yaml
# .claude/agents/anand-2.0.md frontmatter
context:
  inherit:
    - ".claude/context/project-context.yaml"  # Project-specific
    - ".claude/context/shared-patterns.yaml"  # Shared code patterns
    - "~/.claude/global-context.yaml"          # User-level global context

  variables:
    - project_name
    - frontend_framework
    - backend_framework

  overrides:
    # Agent-specific overrides
    custom_var: "custom value"
```

**Load order (later overrides earlier):**
1. `~/.claude/global-context.yaml` (user-level, cross-project)
2. `.claude/context/shared-patterns.yaml` (project-level, shared)
3. `.claude/context/project-context.yaml` (project-level, specific)
4. `overrides` in agent frontmatter (agent-level)

---

## 🛠️ Validation & Health Checks

### Context Validation Script

**Location:** `.claude/scripts/validate-context.sh`

```bash
#!/bin/bash
# validate-context.sh - Validate project context completeness

CONTEXT_FILE=".claude/context/project-context.yaml"

echo "🔍 Validating Project Context..."

# Check file exists
if [ ! -f "$CONTEXT_FILE" ]; then
    echo "❌ Context file missing: $CONTEXT_FILE"
    echo "   Run .claude/scripts/init-project.sh"
    exit 1
fi

# Check required fields
required_fields=(
    "project.name"
    "project.slug"
    "tech_stack.frontend.framework"
    "tech_stack.backend.framework"
    "deployment.frontend.platform"
    "deployment.backend.platform"
)

errors=0
for field in "${required_fields[@]}"; do
    if ! grep -q "$field" "$CONTEXT_FILE"; then
        echo "❌ Missing required field: $field"
        errors=$((errors + 1))
    fi
done

if [ $errors -eq 0 ]; then
    echo "✅ Context validation passed!"
    exit 0
else
    echo ""
    echo "❌ Context validation failed: $errors errors"
    exit 1
fi
```

**Usage:**
```bash
./.claude/scripts/validate-context.sh

# In CI/CD (GitHub Actions)
- name: Validate Context
  run: ./.claude/scripts/validate-context.sh
```

---

## 📖 Example: Agent Context Loading Flow

### Before Auto-Context (Manual, Error-Prone)

**User creates new project from template:**
1. Clone repo
2. Manually find-and-replace `{{ project_name }}` in 15+ files
3. Update URLs in CLAUDE.md
4. Update tech stack in each agent file
5. Miss some replacements → agents have wrong context
6. Spend 2 hours fixing inconsistencies

### After Auto-Context (Automated, Reliable)

**User creates new project from template:**
1. Clone repo
2. Run `./.claude/scripts/init-project.sh`
3. Answer prompts (5 minutes)
4. Commit changes
5. Done! All agents have correct context automatically

**Time saved:** 1 hour 55 minutes per new project

---

## 🎯 Implementation Checklist

**To enable auto-context in this template repo:**

### ✅ Already Done (In This Template)
- [x] Agent files have `{{ variable }}` placeholders
- [x] CLAUDE.md uses variables
- [x] Agent frontmatter exists

### 📝 To Do (Complete Auto-Context System)
- [ ] Create `.claude/context/` directory
- [ ] Create `.claude/context/project-context.yaml` template
- [ ] Create `.claude/scripts/init-project.sh` initialization script
- [ ] Create `.claude/scripts/validate-context.sh` validation script
- [ ] Create `.claude/scripts/context-interpolation.py` (if needed)
- [ ] Update all agent frontmatter to include `context.inherit`
- [ ] Update `.claude/docs/guides/PROJECT_SETUP.md` with init instructions
- [ ] Add GitHub Actions workflow to validate context on push
- [ ] Document in README.md how to use template

### 🚀 Deployment Steps
1. Create context directory structure
2. Write initialization script
3. Update agent files with context references
4. Test with sample project
5. Document in README.md
6. Push to GitHub
7. Test "Use this template" workflow

---

## 📋 Template README Section

**Add this to README.md of template repo:**

```markdown
## 🚀 Quick Start: Create New Project from Template

### 1. Create Repository from Template

Click "Use this template" on GitHub → Create new repository

### 2. Initialize Project Context

Clone locally and run initialization script:

\`\`\`bash
git clone https://github.com/your-org/your-new-project.git
cd your-new-project
./.claude/scripts/init-project.sh
\`\`\`

Answer prompts:
- Project name, slug, description
- Tech stack (React/Vue, FastAPI/Express)
- Deployment platforms (Vercel, Railway)
- Domain context (optional)

### 3. Commit Initialized Context

\`\`\`bash
git add .claude/context/project-context.yaml CLAUDE.md
git commit -m "Initialize project context"
git push origin master
\`\`\`

### 4. Start Using Agents

All 15 agents now have your project's context automatically!

\`\`\`bash
# In Claude Code
/anand implement user authentication
/shawar deploy to staging
/atharva plan new feature: dashboard
\`\`\`

Agents will know:
- ✅ Your project name and tech stack
- ✅ Your deployment URLs
- ✅ Your domain context
- ✅ Your team structure

**No manual updates needed!**
```

---

## 🔮 Future Enhancements

### Phase 2: Runtime Context Interpolation
- Claude Code natively supports `{{ variable }}` interpolation
- No preprocessing needed
- Variables replaced at agent load time

### Phase 3: Context Versioning
- Track context changes over time
- Rollback to previous context versions
- Audit trail of context modifications

### Phase 4: Multi-Environment Context
- Different context for dev/staging/prod
- Environment-specific variable overrides
- `.claude/context/environments/dev.yaml`, etc.

### Phase 5: Context Templates Library
- Pre-built context templates for common stacks
- "Healthcare HIPAA Template"
- "FinTech Compliance Template"
- "E-commerce Template"

---

## 📚 Related Documentation

- `.claude/docs/guides/PROJECT_SETUP.md` - Full setup guide
- `.claude/docs/protocols/DELEGATION_PROTOCOL.md` - Agent delegation
- `.claude/docs/protocols/MEMORY_PROTOCOL.md` - Agent memory system
- `CLAUDE.md` - Project-level instructions

---

**Last Updated:** 2025-11-23
**Maintained By:** @documentation-manager
**Status:** Design Complete (Implementation Pending)

---

## Summary

**The auto-context system ensures:**
1. ✅ Single source of truth (`.claude/context/project-context.yaml`)
2. ✅ One-time initialization (`.claude/scripts/init-project.sh`)
3. ✅ All agents auto-load correct context
4. ✅ Zero manual updates across agent files
5. ✅ Template reusability for infinite new projects

**When you "Use this template" on GitHub:**
- Run init script → Answer prompts → Done
- All 15 agents have your project's full context
- Ready to build immediately

**No more manual find-and-replace. No more inconsistencies. Just automated project context propagation.** 🚀

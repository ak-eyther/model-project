#!/bin/bash
# init-project.sh - Initialize project context for new template-based project
#
# Usage: ./.claude/scripts/init-project.sh
#
# This script collects project-specific information and generates:
# - .claude/context/project-context.yaml (auto-loaded by all agents)
# - Updates CLAUDE.md with project-specific values

set -e

CONTEXT_FILE=".claude/context/project-context.yaml"
CLAUDE_MD="CLAUDE.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🚀 Claude Code Project Template Initialization"
echo "=============================================="
echo ""
echo "This script will configure your project context so all agents"
echo "automatically know about your project's tech stack, deployment,"
echo "and domain context."
echo ""

# Check if already initialized
if [ -f "$CONTEXT_FILE" ]; then
    initialized=$(grep "initialized: true" "$CONTEXT_FILE" || echo "")
    if [ -n "$initialized" ]; then
        echo "⚠️  Project already initialized!"
        echo "   Context file exists: $CONTEXT_FILE"
        echo ""
        read -p "Do you want to re-initialize? This will overwrite existing context (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "Initialization cancelled."
            exit 0
        fi
    fi
fi

# Collect project information
echo "📋 Project Information"
echo "---------------------"
read -p "Project Name (e.g., Task Manager Pro): " project_name
read -p "Project Slug (kebab-case, e.g., task-manager-pro): " project_slug
read -p "Project Description: " project_description
read -p "Project Root (full path, default: $PROJECT_ROOT): " project_root
project_root=${project_root:-$PROJECT_ROOT}

echo ""
echo "🛠️  Tech Stack"
echo "-------------"
echo "Frontend Framework:"
echo "1) React"
echo "2) Vue"
echo "3) Svelte"
echo "4) Next.js"
echo "5) Angular"
read -p "Choose (1-5, default: 1): " frontend_choice
frontend_choice=${frontend_choice:-1}
case $frontend_choice in
    1) frontend_framework="React"; frontend_version="18.2.0" ;;
    2) frontend_framework="Vue"; frontend_version="3.3.0" ;;
    3) frontend_framework="Svelte"; frontend_version="4.0.0" ;;
    4) frontend_framework="Next.js"; frontend_version="14.0.0" ;;
    5) frontend_framework="Angular"; frontend_version="17.0.0" ;;
    *) frontend_framework="React"; frontend_version="18.2.0" ;;
esac

echo ""
echo "Backend Framework:"
echo "1) FastAPI (Python)"
echo "2) Express (Node.js)"
echo "3) Django (Python)"
echo "4) Flask (Python)"
echo "5) NestJS (Node.js)"
read -p "Choose (1-5, default: 1): " backend_choice
backend_choice=${backend_choice:-1}
case $backend_choice in
    1) backend_framework="FastAPI"; backend_lang="Python"; backend_version="0.104.0" ;;
    2) backend_framework="Express"; backend_lang="Node.js"; backend_version="4.18.0" ;;
    3) backend_framework="Django"; backend_lang="Python"; backend_version="4.2.0" ;;
    4) backend_framework="Flask"; backend_lang="Python"; backend_version="3.0.0" ;;
    5) backend_framework="NestJS"; backend_lang="TypeScript"; backend_version="10.0.0" ;;
    *) backend_framework="FastAPI"; backend_lang="Python"; backend_version="0.104.0" ;;
esac

read -p "Using a database? (postgres/mongodb/mysql/none, default: none): " database
database=${database:-none}
if [ "$database" = "none" ]; then
    database="null"
fi

echo ""
echo "☁️  Deployment"
echo "-------------"
echo "Frontend Platform:"
echo "1) Vercel"
echo "2) Netlify"
echo "3) AWS S3 + CloudFront"
echo "4) GitHub Pages"
read -p "Choose (1-4, default: 1): " frontend_platform_choice
frontend_platform_choice=${frontend_platform_choice:-1}
case $frontend_platform_choice in
    1) frontend_platform="Vercel" ;;
    2) frontend_platform="Netlify" ;;
    3) frontend_platform="AWS S3 + CloudFront" ;;
    4) frontend_platform="GitHub Pages" ;;
    *) frontend_platform="Vercel" ;;
esac

echo ""
echo "Backend Platform:"
echo "1) Railway"
echo "2) Render"
echo "3) AWS EC2"
echo "4) Google Cloud Run"
echo "5) Heroku"
read -p "Choose (1-5, default: 1): " backend_platform_choice
backend_platform_choice=${backend_platform_choice:-1}
case $backend_platform_choice in
    1) backend_platform="Railway" ;;
    2) backend_platform="Render" ;;
    3) backend_platform="AWS EC2" ;;
    4) backend_platform="Google Cloud Run" ;;
    5) backend_platform="Heroku" ;;
    *) backend_platform="Railway" ;;
esac

echo ""
read -p "Production Frontend URL (e.g., https://myapp.vercel.app): " production_frontend_url
read -p "Staging Frontend URL (e.g., https://myapp-staging.vercel.app): " staging_frontend_url
read -p "Production Backend URL (e.g., https://myapp-prod.up.railway.app): " production_backend_url
read -p "Staging Backend URL (e.g., https://myapp-staging.up.railway.app): " staging_backend_url

echo ""
echo "🏥 Domain Context (optional, press Enter to skip)"
echo "------------------------------------------------"
read -p "Industry (e.g., SaaS, Finance, E-commerce, Healthcare): " industry
industry=${industry:-Technology}
read -p "Domain (e.g., Task Management, Payment Processing, Content Management): " domain
domain=${domain:-Software Development}
read -p "Target Users (e.g., Project managers, Financial analysts, Content creators): " users
users=${users:-General users}
read -p "Sensitivity/Compliance (e.g., HIPAA, GDPR, SOC2): " sensitivity
sensitivity=${sensitivity:-Standard security practices}

echo ""
echo "👤 Team"
echo "-------"
read -p "Admin Email: " admin_email
read -p "GitHub URL (e.g., https://github.com/org/repo): " github_url
read -p "Main Branch (default: master): " main_branch
main_branch=${main_branch:-master}

# Generate timestamp
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S")

# Create context directory if it doesn't exist
mkdir -p .claude/context

# Generate project-context.yaml
cat > "$CONTEXT_FILE" <<EOF
# Project Context Configuration
# Auto-generated: $timestamp
# All agents reference this file for automatic context loading

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
    version: "$frontend_version"
    language: "TypeScript"
    styling: "Tailwind CSS"
    build_tool: "Vite"

  backend:
    framework: "$backend_framework"
    version: "$backend_version"
    language: "$backend_lang"
    version_python: "3.11"
    database: $database

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
  key_entities: []

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

# Template metadata
template:
  version: "1.0.0"
  source: "https://github.com/arifkhan/claude-code-project-template"
  initialized: true
EOF

# Update CLAUDE.md with project-specific info
if [ -f "$CLAUDE_MD" ]; then
    # Create backup
    cp "$CLAUDE_MD" "$CLAUDE_MD.bak"

    # Replace template placeholders
    sed -i.tmp "s/claude-code-project-template/$project_slug/g" "$CLAUDE_MD"
    sed -i.tmp "s|https://claude-code-project-template.vercel.app|$production_frontend_url|g" "$CLAUDE_MD"
    sed -i.tmp "s|https://claude-code-project-template-staging.vercel.app|$staging_frontend_url|g" "$CLAUDE_MD"
    sed -i.tmp "s|https://claude-code-project-template-production.up.railway.app|$production_backend_url|g" "$CLAUDE_MD"
    sed -i.tmp "s|https://claude-code-project-template-staging.up.railway.app|$staging_backend_url|g" "$CLAUDE_MD"
    sed -i.tmp "s/A production-ready application/$project_description/g" "$CLAUDE_MD"
    sed -i.tmp "s/React (frontend) + FastAPI (backend)/$frontend_framework (frontend) + $backend_framework (backend)/g" "$CLAUDE_MD"

    # Update deployment sections
    sed -i.tmp "s/Vercel (frontend)/$frontend_platform (frontend)/g" "$CLAUDE_MD"
    sed -i.tmp "s/Railway (backend)/$backend_platform (backend)/g" "$CLAUDE_MD"

    # Clean up temp files
    rm -f "$CLAUDE_MD.tmp" "$CLAUDE_MD.bak"
fi

echo ""
echo "✅ Project Context Initialized Successfully!"
echo ""
echo "📄 Generated Files:"
echo "   - $CONTEXT_FILE"
if [ -f "$CLAUDE_MD" ]; then
    echo "   - $CLAUDE_MD (updated)"
fi
echo ""
echo "📊 Project Summary:"
echo "   Name:     $project_name"
echo "   Slug:     $project_slug"
echo "   Frontend: $frontend_framework on $frontend_platform"
echo "   Backend:  $backend_framework on $backend_platform"
echo "   Industry: $industry"
echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Review and customize (if needed):"
echo "   vim $CONTEXT_FILE"
echo ""
echo "2. Validate context:"
echo "   ./.claude/scripts/validate-context.sh"
echo ""
echo "3. Commit changes:"
echo "   git add .claude/context/project-context.yaml CLAUDE.md"
echo "   git commit -m \"Initialize project context for $project_name\""
echo "   git push"
echo ""
echo "4. Start using agents (they auto-load this context):"
echo "   /anand implement feature X"
echo "   /shawar deploy to staging"
echo "   /atharva plan new feature: Y"
echo ""
echo "✨ All 15 agents now have your project's full context automatically!"
echo ""
echo "📖 Documentation:"
echo "   - .claude/docs/guides/AUTO_CONTEXT_SYSTEM.md"
echo "   - .claude/docs/guides/PROJECT_SETUP.md"
echo ""

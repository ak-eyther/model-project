#!/bin/bash
# add-context-to-agents.sh - Add context frontmatter to all agent files
#
# Usage: ./.claude/scripts/add-context-to-agents.sh
#
# This script updates all agent files in .claude/agents/ to include
# context auto-loading frontmatter

set -e

AGENTS_DIR=".claude/agents"
BACKUP_DIR=".claude/agents-backup-$(date +%Y%m%d-%H%M%S)"

# Context frontmatter to add
CONTEXT_FRONTMATTER='
# Context Auto-Loading
context:
  inherit: ".claude/context/project-context.yaml"
  variables:
    - project.name
    - project.slug
    - project.description
    - project.root
    - tech_stack.frontend.framework
    - tech_stack.frontend.version
    - tech_stack.backend.framework
    - tech_stack.backend.version
    - deployment.frontend.platform
    - deployment.backend.platform
    - deployment.frontend.production_url
    - deployment.frontend.staging_url
    - deployment.backend.production_url
    - deployment.backend.staging_url
    - domain_context.industry
    - domain_context.domain
    - domain_context.users
    - repository.github_url
    - repository.main_branch
'

echo "🔄 Adding Context Auto-Loading to All Agent Files"
echo "================================================="
echo ""

# Create backup directory
echo "📦 Creating backup at: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r "$AGENTS_DIR"/*.md "$BACKUP_DIR/" 2>/dev/null || echo "   (No .md files to backup)"
echo ""

# Process each agent file
count=0
skipped=0

for agent_file in "$AGENTS_DIR"/*.md; do
    if [ ! -f "$agent_file" ]; then
        continue
    fi

    agent_name=$(basename "$agent_file")

    # Check if already has context frontmatter
    if grep -q "context:" "$agent_file"; then
        echo "⏭️  Skipping $agent_name (already has context frontmatter)"
        skipped=$((skipped + 1))
        continue
    fi

    echo "📝 Processing: $agent_name"

    # Find the closing --- of frontmatter
    line_num=$(grep -n "^---$" "$agent_file" | head -2 | tail -1 | cut -d: -f1)

    if [ -z "$line_num" ]; then
        echo "   ⚠️  Warning: Could not find frontmatter end marker, skipping"
        skipped=$((skipped + 1))
        continue
    fi

    # Insert context frontmatter before the closing ---
    {
        head -n $((line_num - 1)) "$agent_file"
        echo "$CONTEXT_FRONTMATTER"
        tail -n +$line_num "$agent_file"
    } > "$agent_file.tmp"

    mv "$agent_file.tmp" "$agent_file"
    count=$((count + 1))
    echo "   ✅ Added context frontmatter"
done

echo ""
echo "═══════════════════════════════════════════"
echo "📊 Summary"
echo "═══════════════════════════════════════════"
echo ""
echo "   Updated: $count agent files"
echo "   Skipped: $skipped agent files"
echo ""

if [ $count -gt 0 ]; then
    echo "✅ Context frontmatter added successfully!"
    echo ""
    echo "🎯 Next Steps:"
    echo ""
    echo "1. Review changes:"
    echo "   git diff .claude/agents/"
    echo ""
    echo "2. Test with one agent:"
    echo "   /shawar-2.0 check deployment status"
    echo ""
    echo "3. If satisfied, commit:"
    echo "   git add .claude/agents/"
    echo "   git commit -m \"Add context auto-loading to all agents\""
    echo ""
    echo "📦 Backup saved at: $BACKUP_DIR"
    echo "   (Restore if needed: cp $BACKUP_DIR/*.md .claude/agents/)"
    echo ""
else
    echo "ℹ️  No files needed updating"
    echo ""
fi

# Plugin Bundling Implementation Plan

**For:** @anand-2.0 (Code Executor)
**Created By:** @vidya-2.0 (Solution Architect)
**Date:** 2025-11-23
**Priority:** High
**Estimated Effort:** 4-6 hours

## Overview

Implement the hybrid plugin bundling system for the Claude Code Project Template as specified in the [Plugin Bundling Architecture](/Users/arifkhan/claude-code-project-template/.claude/docs/architecture/PLUGIN_BUNDLING_ARCHITECTURE.md).

## Implementation Checklist

### Phase 1: Directory Structure Setup

```bash
# Create required directories
mkdir -p .claude/plugins/essential
mkdir -p .claude/plugins/available
mkdir -p .claude/scripts
```

### Phase 2: Bundle Essential Plugins

1. **Copy essential plugins from global installation:**

```bash
# Frontend Design Plugin (REQUIRED - per CLAUDE.md rules)
cp -r ~/.claude/plugins/marketplaces/claude-code-plugins/plugins/frontend-design \
      .claude/plugins/essential/

# Code Review Plugin
cp -r ~/.claude/plugins/marketplaces/claude-code-plugins/plugins/code-review \
      .claude/plugins/essential/

# Commit Commands Plugin
cp -r ~/.claude/plugins/marketplaces/claude-code-plugins/plugins/commit-commands \
      .claude/plugins/essential/
```

2. **Clean up unnecessary files to reduce size:**

```bash
# Remove development files from bundled plugins
find .claude/plugins/essential -name "*.test.js" -delete
find .claude/plugins/essential -name "*.spec.js" -delete
find .claude/plugins/essential -name "node_modules" -type d -exec rm -rf {} +
find .claude/plugins/essential -name ".git" -type d -exec rm -rf {} +
```

### Phase 3: Create Plugin Manifest

**File:** `.claude/plugins/manifest.json`

```json
{
  "version": "1.0.0",
  "lastUpdated": "2025-11-23",
  "templateVersion": "1.0.0",
  "plugins": {
    "essential": [
      {
        "name": "frontend-design",
        "version": "1.2.0",
        "path": "essential/frontend-design",
        "bundled": true,
        "required": true,
        "agents": ["@hitesh-2.0", "@anand-2.0", "@varsha-2.0"],
        "description": "Generate distinctive, production-grade frontend code",
        "checksum": "SHA256_TO_BE_CALCULATED"
      },
      {
        "name": "code-review",
        "version": "2.1.0",
        "path": "essential/code-review",
        "bundled": true,
        "required": false,
        "agents": ["@ankur-2.0"],
        "description": "Automated code review and quality analysis",
        "checksum": "SHA256_TO_BE_CALCULATED"
      },
      {
        "name": "commit-commands",
        "version": "1.5.0",
        "path": "essential/commit-commands",
        "bundled": true,
        "required": false,
        "agents": ["@anand-2.0", "@hitesh-2.0", "@shawar-2.0"],
        "description": "Git commit message formatting and conventions",
        "checksum": "SHA256_TO_BE_CALCULATED"
      }
    ],
    "available": [
      {
        "name": "agent-sdk-dev",
        "version": "3.0.1",
        "bundled": false,
        "size": "45MB",
        "download_url": "https://plugins.claude.code/optional/agent-sdk-dev-3.0.1.tar.gz",
        "description": "SDK for developing custom agents",
        "agents": ["@atharva-2.0"],
        "checksum": "SHA256_FROM_REMOTE"
      },
      {
        "name": "pr-review-toolkit",
        "version": "2.3.0",
        "bundled": false,
        "size": "12MB",
        "download_url": "https://plugins.claude.code/optional/pr-review-toolkit-2.3.0.tar.gz",
        "description": "Advanced pull request review capabilities",
        "agents": ["@ankur-2.0", "@harshit-2.0"],
        "checksum": "SHA256_FROM_REMOTE"
      },
      {
        "name": "security-guidance",
        "version": "1.8.0",
        "bundled": false,
        "size": "8MB",
        "download_url": "https://plugins.claude.code/optional/security-guidance-1.8.0.tar.gz",
        "description": "Security vulnerability detection and remediation",
        "agents": ["@ankur-2.0"],
        "checksum": "SHA256_FROM_REMOTE"
      },
      {
        "name": "explanatory-output-style",
        "version": "1.0.0",
        "bundled": false,
        "size": "2MB",
        "download_url": "https://plugins.claude.code/optional/explanatory-output-style-1.0.0.tar.gz",
        "description": "Educational code output style",
        "agents": ["all"],
        "checksum": "SHA256_FROM_REMOTE"
      },
      {
        "name": "learning-output-style",
        "version": "1.0.0",
        "bundled": false,
        "size": "2MB",
        "download_url": "https://plugins.claude.code/optional/learning-output-style-1.0.0.tar.gz",
        "description": "Learning-focused output formatting",
        "agents": ["all"],
        "checksum": "SHA256_FROM_REMOTE"
      }
    ]
  },
  "configuration": {
    "autoInstallEssential": true,
    "promptForOptional": true,
    "updateCheckInterval": "weekly",
    "pluginDirectory": "~/.claude/plugins/marketplaces/claude-code-plugins/plugins"
  }
}
```

### Phase 4: Create Installation Script

**File:** `.claude/scripts/install-plugins.sh`

```bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
PLUGIN_DIR="$PROJECT_ROOT/.claude/plugins"
MANIFEST="$PLUGIN_DIR/manifest.json"
TARGET_DIR="$HOME/.claude/plugins/marketplaces/claude-code-plugins/plugins"
INIT_FLAG="$PROJECT_ROOT/.claude/.plugins-initialized"

echo -e "${BLUE}🔌 Claude Code Plugin Setup${NC}"
echo "=================================="
echo ""

# Check if already initialized
if [ -f "$INIT_FLAG" ]; then
    echo -e "${YELLOW}⚠️  Plugins already initialized.${NC}"
    read -p "Reinitialize plugins? (y/n): " reinit
    if [ "$reinit" != "y" ]; then
        echo "Skipping plugin setup."
        exit 0
    fi
fi

# Ensure target directory exists
mkdir -p "$TARGET_DIR"

# Step 1: Install essential plugins
echo -e "${GREEN}📦 Installing essential plugins...${NC}"
echo ""

# Parse manifest and install essential plugins
if command -v jq &> /dev/null; then
    # Use jq if available
    essential_plugins=$(jq -r '.plugins.essential[].name' "$MANIFEST")
else
    # Fallback to grep/sed
    essential_plugins=$(grep -A1 '"essential"' "$MANIFEST" | grep '"name"' | sed 's/.*"name": "\(.*\)".*/\1/')
fi

for plugin in $essential_plugins; do
    source_path="$PLUGIN_DIR/essential/$plugin"
    target_path="$TARGET_DIR/$plugin"

    if [ -d "$source_path" ]; then
        echo -e "  ${GREEN}✓${NC} Installing $plugin..."

        # Remove existing plugin if present
        rm -rf "$target_path" 2>/dev/null || true

        # Copy plugin to global location
        cp -r "$source_path" "$target_path"

        echo -e "    Installed to: $target_path"
    else
        echo -e "  ${RED}✗${NC} Plugin $plugin not found in bundle!"
    fi
done

echo ""

# Step 2: Prompt for optional plugins
echo -e "${BLUE}📚 Optional plugins available:${NC}"
echo ""

# List available plugins
if command -v jq &> /dev/null; then
    jq -r '.plugins.available[] | "  • \(.name) (\(.size)) - \(.description)"' "$MANIFEST"
else
    echo "  • agent-sdk-dev (45MB) - SDK for developing custom agents"
    echo "  • pr-review-toolkit (12MB) - Advanced pull request review"
    echo "  • security-guidance (8MB) - Security vulnerability detection"
    echo "  • explanatory-output-style (2MB) - Educational code output"
    echo "  • learning-output-style (2MB) - Learning-focused output"
fi

echo ""
read -p "Install optional plugins? (all/none/select): " install_choice

case $install_choice in
    all)
        echo -e "${YELLOW}⏬ Downloading all optional plugins...${NC}"
        # Download logic would go here
        echo "(Download functionality to be implemented with actual plugin URLs)"
        ;;
    select)
        echo "Select plugins to install (comma-separated names):"
        read -p "> " selected_plugins
        echo -e "${YELLOW}⏬ Downloading selected plugins: $selected_plugins${NC}"
        # Download logic would go here
        echo "(Download functionality to be implemented with actual plugin URLs)"
        ;;
    *)
        echo "Skipping optional plugins."
        ;;
esac

# Step 3: Create initialization flag
touch "$INIT_FLAG"

echo ""
echo -e "${GREEN}✅ Plugin setup complete!${NC}"
echo ""
echo "Essential plugins installed:"
for plugin in $essential_plugins; do
    echo -e "  ${GREEN}✓${NC} $plugin"
done

echo ""
echo -e "${BLUE}ℹ️  To update plugins later, run:${NC}"
echo "  bash .claude/scripts/update-plugins.sh"
```

### Phase 5: Create Update Script

**File:** `.claude/scripts/update-plugins.sh`

```bash
#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
MANIFEST="$PROJECT_ROOT/.claude/plugins/manifest.json"

echo -e "${BLUE}🔄 Checking for plugin updates...${NC}"
echo "=================================="
echo ""

# Check current version
CURRENT_VERSION=$(grep '"version"' "$MANIFEST" | head -1 | sed 's/.*"version": "\(.*\)".*/\1/')
echo "Current plugin manifest version: $CURRENT_VERSION"

# In production, this would check against a remote manifest
# For now, we'll simulate the check
echo -e "${YELLOW}⚠️  Update check functionality to be implemented${NC}"
echo "Would check: https://raw.githubusercontent.com/anthropics/claude-code-plugins/main/manifest.json"

# Placeholder for update logic
echo ""
echo "Update options:"
echo "  1. Update essential plugins only"
echo "  2. Update all installed plugins"
echo "  3. Check for new available plugins"
echo "  4. Cancel"

read -p "Select option (1-4): " option

case $option in
    1)
        echo -e "${GREEN}Updating essential plugins...${NC}"
        bash "$SCRIPT_DIR/install-plugins.sh"
        ;;
    2)
        echo -e "${GREEN}Updating all plugins...${NC}"
        # Implementation needed
        ;;
    3)
        echo -e "${BLUE}Checking for new plugins...${NC}"
        # Implementation needed
        ;;
    *)
        echo "Update cancelled."
        ;;
esac
```

### Phase 6: Create Git Hook

**File:** `.claude/hooks/post-checkout`

```bash
#!/bin/bash

# Post-checkout hook to setup plugins after clone
# This runs after git checkout (including initial clone)

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
INIT_FLAG="$PROJECT_ROOT/.claude/.plugins-initialized"
INSTALL_SCRIPT="$PROJECT_ROOT/.claude/scripts/install-plugins.sh"

# Only run on initial clone (no plugins initialized yet)
if [ ! -f "$INIT_FLAG" ] && [ -f "$INSTALL_SCRIPT" ]; then
    echo ""
    echo "🎉 Welcome to Claude Code Project Template!"
    echo "==========================================="
    echo ""
    echo "First-time setup detected. Initializing plugins..."
    echo ""

    # Run plugin installation
    bash "$INSTALL_SCRIPT"
fi
```

### Phase 7: Update Git Hooks Installation Script

**Update:** `.claude/scripts/install-hooks.sh`

Add the post-checkout hook installation:

```bash
# Add to existing install-hooks.sh
ln -sf ../../.claude/hooks/post-checkout .git/hooks/post-checkout
chmod +x .git/hooks/post-checkout
```

### Phase 8: Calculate Checksums

```bash
# Script to calculate SHA256 for bundled plugins
for plugin in .claude/plugins/essential/*; do
    if [ -d "$plugin" ]; then
        plugin_name=$(basename "$plugin")
        checksum=$(find "$plugin" -type f -exec sha256sum {} \; | sha256sum | cut -d' ' -f1)
        echo "$plugin_name: $checksum"
    fi
done
```

### Phase 9: Documentation Updates

1. **Update README.md** - Add plugin section
2. **Update CLAUDE.md** - Document plugin availability
3. **Create .claude/plugins/README.md** - Plugin usage guide

### Phase 10: Testing Checklist

- [ ] Clean clone of template repository
- [ ] Verify post-checkout hook triggers
- [ ] Essential plugins auto-install
- [ ] Plugins work with agents
- [ ] Update mechanism functions
- [ ] Manifest parsing works without jq
- [ ] Checksums validate correctly

## File Creation Order

1. Create directory structure
2. Copy essential plugins
3. Create manifest.json
4. Create install-plugins.sh
5. Create update-plugins.sh
6. Create post-checkout hook
7. Update install-hooks.sh
8. Calculate and update checksums
9. Test full flow
10. Update documentation

## Success Criteria

- [ ] Repository size increase < 10MB
- [ ] Plugin setup completes in < 60 seconds
- [ ] All essential plugins functional
- [ ] Agents can access bundled plugins
- [ ] No errors on fresh clone
- [ ] Update mechanism works

## Notes for @anand-2.0

1. **IMPORTANT:** The `frontend-design` plugin is MANDATORY for your work per CLAUDE.md rules
2. Start with Phase 1-3 to get core structure in place
3. Test each script individually before integration
4. Use absolute paths where possible
5. Ensure scripts work on both macOS and Linux
6. Remember to make all scripts executable with `chmod +x`

## Estimated Timeline

- Phase 1-3: 1 hour (structure and manifest)
- Phase 4-5: 2 hours (installation scripts)
- Phase 6-7: 1 hour (git hooks)
- Phase 8-10: 2 hours (validation and testing)

Total: 4-6 hours

---

**Ready for Implementation**

This plan is ready for @anand-2.0 to execute. All technical details, scripts, and configurations are provided above.
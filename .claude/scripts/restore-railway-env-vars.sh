#!/bin/bash
# Railway Environment Variables Restoration Script
# Restores all critical env vars from production to staging and development
#
# ⚠️ IMPORTANT FOR TEMPLATE USERS:
# This script contains PLACEHOLDER API keys. Before using:
# 1. Get your own Anthropic API key from: https://console.anthropic.com/settings/keys
# 2. Get your own OpenRouter API key from: https://openrouter.ai/keys
# 3. Replace ALL placeholder values in the ENV_VARS array below
# 4. Update ALLOWED_ORIGINS with your actual domain names
# 5. Generate secure VALID_API_KEYS and WIDGET_API_KEY values
#
# ⚠️ NEVER commit real API keys to git. Use environment variables in Railway instead.

set -e

echo "🚀 Railway Environment Variables Restoration"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Environment variables to restore (REPLACE WITH YOUR ACTUAL VALUES)
# TODO: Project owner must update these with real API keys and configuration
declare -A ENV_VARS=(
    ["ANTHROPIC_API_KEY"]="sk-ant-api03-YOUR_ANTHROPIC_API_KEY_HERE"
    ["ALLOWED_ORIGINS"]="https://your-frontend-domain.vercel.app,https://your-custom-domain.com"
    ["ENABLE_AUTH"]="true"
    ["ENABLE_CHROMADB"]="true"
    ["ENABLE_KG_LAYER"]="true"
    ["ENABLE_LLM_JUDGE"]="true"
    ["JUDGE_MAX_RETRIES"]="2"
    ["JUDGE_MODEL"]="gpt-4o-mini"
    ["OPENROUTER_API_KEY"]="sk-or-v1-YOUR_OPENROUTER_API_KEY_HERE"
    ["VALID_API_KEYS"]="your-secure-api-key-here,dev-key-12345"
    ["WIDGET_API_KEY"]="your-widget-api-key-here"
    ["WIDGET_VISION_ENABLED"]="true"
    ["WIDGET_VISION_MODEL"]="claude-haiku-4-5-20251001"
)

# Function to set environment variables for a given environment
restore_env_vars() {
    local env_name=$1
    echo -e "${YELLOW}Restoring environment variables to $env_name...${NC}"

    # Switch to environment
    railway environment "$env_name" || {
        echo -e "${RED}Failed to switch to $env_name environment${NC}"
        return 1
    }

    # Link to service (assuming service name is consistent)
    # Note: You may need to adjust service name if different

    # Set each environment variable
    for var_name in "${!ENV_VARS[@]}"; do
        var_value="${ENV_VARS[$var_name]}"
        echo -e "  Setting ${var_name}..."
        railway variables --set "${var_name}=${var_value}" || {
            echo -e "${RED}  Failed to set ${var_name}${NC}"
            continue
        }
        echo -e "${GREEN}  ✓ ${var_name} set${NC}"
    done

    echo -e "${GREEN}✓ All variables restored to $env_name${NC}"
    echo ""
}

# Verify user wants to proceed
echo -e "${YELLOW}This script will restore 13 environment variables to:${NC}"
echo "  - development"
echo "  - staging"
echo ""
echo "Variables to restore:"
for var_name in "${!ENV_VARS[@]}"; do
    echo "  - $var_name"
done
echo ""
read -p "Do you want to proceed? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "Aborted."
    exit 0
fi

echo ""

# Restore to development
echo "=== DEVELOPMENT ENVIRONMENT ==="
restore_env_vars "development"

# Restore to staging
echo "=== STAGING ENVIRONMENT ==="
restore_env_vars "staging"

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}✅ Environment variables restoration complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Next steps:"
echo "1. Verify health checks:"
echo "   curl https://edit-widget-development.up.railway.app/health"
echo "   curl https://edit-widget-staging.up.railway.app/health"
echo ""
echo "2. Check that KG is enabled (kg_stats.enabled should be true)"
echo ""
echo "3. Test a chat request to verify ANTHROPIC_API_KEY works"

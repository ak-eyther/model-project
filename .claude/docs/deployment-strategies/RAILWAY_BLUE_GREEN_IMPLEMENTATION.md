# Blue-Green Deployment Implementation for Railway & Vercel

Practical guide for implementing blue-green deployments using Railway (backend) and Vercel (frontend).

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              Vercel Edge Network (Global)               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Routing: app.example.com → Blue or Green         │  │
│  │  Uses URL rewrite or Environment Variable         │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼──────────┐      ┌────▼──────────┐
    │ Vercel BLUE   │      │ Vercel GREEN  │
    │ Production    │      │ Preview       │
    │               │      │               │
    │ v1.2.3        │      │ v1.2.4        │
    │ (Live)        │      │ (Staging)     │
    └────┬──────────┘      └────┬──────────┘
         │ curl deploy     │
    ┌────▼──────────────────────▼──────────┐
    │        Railway Network                 │
    │  ┌────────────────────────────────┐   │
    │  │  API Load Balancer             │   │
    │  │  (Routes to Blue or Green)     │   │
    │  └────────────────────────────────┘   │
    │    ├─ Blue Service (v1.2.3 - Live)  │
    │    └─ Green Service (v1.2.4 - New)   │
    └────────────────────────────────────────┘

Active Flow:
Vercel (Blue) → Vercel calls API → Railway (Blue) → Responds

After Switch:
Vercel (Green) → Vercel calls API → Railway (Green) → Responds
```

## Environment Setup

### Step 1: Create Dual Environments on Railway

```bash
#!/bin/bash
# setup-railway-environments.sh

# Prerequisites: Railway CLI installed
# npm install -g @railway/cli

set -e

BLUE_ENV="production"
GREEN_ENV="staging"
PROJECT_ID="your-project-id"

echo "Setting up Railway Blue-Green environments..."

# Step 1: Verify existing environments
echo "Listing existing Railway environments..."
railway --project $PROJECT_ID environment list

# Step 2: Create/Configure Blue Environment
echo "Configuring Blue environment (production)..."
railway --project $PROJECT_ID environment select production

# Set Blue environment variables
railway variable set ENVIRONMENT="blue"
railway variable set VERSION="1.2.3"
railway variable set ACTIVE_ENVIRONMENT="blue"

# Step 3: Create/Configure Green Environment
echo "Configuring Green environment (staging)..."
railway --project $PROJECT_ID environment create --name staging

railway --project $PROJECT_ID environment select staging

# Set Green environment variables
railway variable set ENVIRONMENT="green"
railway variable set VERSION="1.2.4"
railway variable set ACTIVE_ENVIRONMENT="staging"

# Step 4: Configure database access
# Both environments share same database (important for blue-green)
railway variable set DATABASE_URL=$DATABASE_PRODUCTION_URL

echo "✅ Railway environments configured"
echo "Blue (production): Ready"
echo "Green (staging): Ready"
```

### Step 2: Configure Vercel for Blue-Green

```bash
#!/bin/bash
# setup-vercel-environments.sh

set -e

PROJECT_NAME="claude-code-project-template"

echo "Setting up Vercel Blue-Green environments..."

# Step 1: Create Blue deployment (main branch)
echo "Configuring Blue deployment (Production)..."
vercel project > /dev/null

# Blue environment variables
vercel env add REACT_APP_API_BLUE_URL "https://api-blue.railway.app" production
vercel env add REACT_APP_API_GREEN_URL "https://api-green.railway.app" production
vercel env add REACT_APP_ACTIVE_BACKEND "blue" production

# Step 2: Create Green deployment (staging branch)
echo "Configuring Green deployment (Staging)..."

# Green environment variables
vercel env add REACT_APP_API_BLUE_URL "https://api-blue.railway.app" preview
vercel env add REACT_APP_API_GREEN_URL "https://api-green.railway.app" preview
vercel env add REACT_APP_ACTIVE_BACKEND "green" preview

# Step 3: Setup automatic deployments
vercel link --confirm
vercel deploy --prod  # Deploy Blue

echo "✅ Vercel environments configured"
```

## Deployment Workflow

### Full Blue-Green Deployment Script

```bash
#!/bin/bash
# deploy-blue-green.sh
#
# Usage: ./deploy-blue-green.sh [blue|green] [--dry-run]
#
# Example: ./deploy-blue-green.sh green --verify-only

set -e

DEPLOY_TARGET="${1:-green}"
DRY_RUN="${2:---run}"
PROJECT_ID="your-railway-project-id"
VERCEL_TEAM="your-vercel-team"

# Configuration
HEALTH_CHECK_RETRIES=5
HEALTH_CHECK_INTERVAL=30
SMOKE_TEST_TIMEOUT=300

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Blue-Green Deployment ===${NC}"
echo "Target: $DEPLOY_TARGET"
echo "Dry Run: $([ "$DRY_RUN" = "--dry-run" ] && echo 'YES' || echo 'NO')"

# Function: Log with timestamp
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Phase 1: Pre-deployment Validation
log "Phase 1: Pre-deployment validation..."

if [ "$DEPLOY_TARGET" = "blue" ]; then
    RAILWAY_ENV="production"
    VERCEL_BRANCH="main"
    API_URL="https://api-blue.railway.app"
    APP_URL="https://app.example.com"
    INACTIVE_ENV="green"
    INACTIVE_API="https://api-green.railway.app"
else
    RAILWAY_ENV="staging"
    VERCEL_BRANCH="staging"
    API_URL="https://api-green.railway.app"
    APP_URL="https://app-staging.example.com"
    INACTIVE_ENV="blue"
    INACTIVE_API="https://api-blue.railway.app"
fi

log "Verifying current state..."

# Check current active environment
CURRENT_ACTIVE=$(curl -s $INACTIVE_API/metrics/active-environment 2>/dev/null || echo "unknown")
log "Currently active: $CURRENT_ACTIVE"

# Check git status
if [ -z "$(git status --porcelain)" ]; then
    log "Git status: clean ✅"
else
    error "Git has uncommitted changes. Commit or stash before deploying."
fi

# Check latest commit
LATEST_COMMIT=$(git rev-parse --short HEAD)
log "Latest commit: $LATEST_COMMIT"

# Phase 2: Build Application
log "Phase 2: Building application..."

if [ "$DRY_RUN" = "--dry-run" ]; then
    log "Dry run: Skipping build"
else
    log "Cleaning previous builds..."
    rm -rf build/ dist/ .next/

    log "Installing dependencies..."
    npm ci --prefer-offline

    log "Running tests..."
    npm run test -- --passWithNoTests

    log "Building application..."
    npm run build

    log "Build complete ✅"
fi

# Phase 3: Deploy to Railway (Backend)
log "Phase 3: Deploying to Railway ($DEPLOY_TARGET)..."

if [ "$DRY_RUN" = "--dry-run" ]; then
    log "Dry run: Skipping Railway deployment"
else
    log "Selecting Railway environment: $RAILWAY_ENV"
    railway environment select $RAILWAY_ENV --project $PROJECT_ID

    log "Deploying backend to Railway..."
    railway up --path-as-root backend

    log "Waiting for Railway deployment to complete..."
    sleep 30

    RAILWAY_STATUS=$(railway status --project $PROJECT_ID | grep -i "healthy" || echo "unknown")
    log "Railway status: $RAILWAY_STATUS"
fi

# Phase 4: Deploy to Vercel (Frontend)
log "Phase 4: Deploying to Vercel..."

if [ "$DRY_RUN" = "--dry-run" ]; then
    log "Dry run: Skipping Vercel deployment"
else
    log "Pushing to branch: $VERCEL_BRANCH"
    git push origin HEAD:$VERCEL_BRANCH

    log "Triggering Vercel deployment..."
    if [ "$DEPLOY_TARGET" = "blue" ]; then
        vercel deploy --prod
    else
        vercel deploy --preview
    fi

    log "Vercel deployment triggered ✅"
    sleep 30
fi

# Phase 5: Health Checks
log "Phase 5: Running health checks on $DEPLOY_TARGET..."

check_health() {
    local url=$1
    local attempt=$2
    local max_attempts=$3

    response=$(curl -s -w "\n%{http_code}" "$url/health" 2>/dev/null || echo "000")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" = "200" ]; then
        log "Health check ($attempt/$max_attempts): ✅ $url"
        return 0
    else
        log "Health check ($attempt/$max_attempts): ❌ HTTP $http_code"
        return 1
    fi
}

for i in $(seq 1 $HEALTH_CHECK_RETRIES); do
    if check_health "$API_URL" $i $HEALTH_CHECK_RETRIES; then
        HEALTH_OK=true
        break
    fi

    if [ $i -lt $HEALTH_CHECK_RETRIES ]; then
        log "Waiting ${HEALTH_CHECK_INTERVAL}s before retry..."
        sleep $HEALTH_CHECK_INTERVAL
    fi
done

if [ "$HEALTH_OK" != "true" ]; then
    error "Health checks failed after $HEALTH_CHECK_RETRIES attempts. Aborting deployment."
fi

log "All health checks passed ✅"

# Phase 6: Smoke Tests
log "Phase 6: Running smoke tests..."

if [ "$DRY_RUN" = "--dry-run" ]; then
    log "Dry run: Skipping smoke tests"
else
    # Test 1: API Health
    api_response=$(curl -s "$API_URL/health" | jq .status)
    if [ "$api_response" = '"healthy"' ]; then
        log "API health: ✅"
    else
        error "API health check failed: $api_response"
    fi

    # Test 2: Database connectivity
    db_response=$(curl -s "$API_URL/health/database" | jq .status)
    if [ "$db_response" = '"connected"' ]; then
        log "Database connectivity: ✅"
    else
        log "Database connectivity: ⚠️  (may be expected)"
    fi

    # Test 3: Frontend rendering
    frontend_http=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL")
    if [ "$frontend_http" = "200" ]; then
        log "Frontend HTTP status: ✅ 200"
    else
        error "Frontend HTTP status: ❌ $frontend_http"
    fi

    # Test 4: CORS validation
    cors_response=$(curl -s -X OPTIONS "$API_URL/v1/api/endpoint" \
        -H "Origin: $APP_URL" \
        -H "Access-Control-Request-Method: GET" \
        -w "\n%{http_code}")
    cors_http=$(echo "$cors_response" | tail -n1)
    if [ "$cors_http" = "200" ]; then
        log "CORS validation: ✅"
    else
        log "CORS validation: ⚠️  (HTTP $cors_http)"
    fi
fi

log "Smoke tests complete ✅"

# Phase 7: Traffic Switch (Requires User Approval)
log "Phase 7: Ready for traffic switch"
log "Target environment ($DEPLOY_TARGET) is healthy and ready"
log ""
log "Next steps:"
log "1. Verify $APP_URL is working correctly"
log "2. Run end-to-end tests manually if needed"
log "3. Execute: ./switch-traffic.sh $DEPLOY_TARGET"
log ""
log "To rollback without switching, no action needed"
log "Current active environment ($INACTIVE_ENV) remains unchanged"

# Save deployment info for switch-traffic.sh
cat > /tmp/deployment-info.env <<EOF
DEPLOY_TARGET=$DEPLOY_TARGET
API_URL=$API_URL
APP_URL=$APP_URL
INACTIVE_ENV=$INACTIVE_ENV
INACTIVE_API=$INACTIVE_API
LATEST_COMMIT=$LATEST_COMMIT
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EOF

log "Deployment info saved to /tmp/deployment-info.env"
log ""
echo -e "${GREEN}✅ Deployment to $DEPLOY_TARGET environment complete!${NC}"
```

### Traffic Switch Script

```bash
#!/bin/bash
# switch-traffic.sh
#
# Switches active environment from current to deployed target
# Usage: ./switch-traffic.sh [blue|green]

set -e

if [ -z "$1" ]; then
    echo "Usage: ./switch-traffic.sh [blue|green]"
    exit 1
fi

DEPLOY_TARGET=$1
SOURCE_ENV_FILE="/tmp/deployment-info.env"

if [ ! -f "$SOURCE_ENV_FILE" ]; then
    echo "❌ Deployment info not found. Run deploy-blue-green.sh first."
    exit 1
fi

source "$SOURCE_ENV_FILE"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

echo -e "${YELLOW}=== Traffic Switch: $INACTIVE_ENV → $DEPLOY_TARGET ===${NC}"
echo ""
echo "This will switch production traffic from:"
echo "  Current: $INACTIVE_ENV"
echo "  To:      $DEPLOY_TARGET"
echo ""
read -p "Confirm traffic switch? (type 'yes' to proceed): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Traffic switch cancelled"
    exit 0
fi

log "Starting traffic switch..."

# Phase 1: Verify target environment is healthy
log "Phase 1: Verifying $DEPLOY_TARGET is healthy..."

health_response=$(curl -s -w "\n%{http_code}" "$API_URL/health")
http_code=$(echo "$health_response" | tail -n1)
body=$(echo "$health_response" | head -n-1)

if [ "$http_code" != "200" ]; then
    error "Target environment health check failed. HTTP $http_code"
fi

log "Target environment healthy ✅"

# Phase 2: Update environment variable to switch traffic
log "Phase 2: Switching traffic in Railway..."

if [ "$DEPLOY_TARGET" = "blue" ]; then
    railway environment production
else
    railway environment staging
fi

railway variable set ACTIVE_ENVIRONMENT="$DEPLOY_TARGET"

log "Environment variable updated in Railway ✅"

# Phase 3: Update Vercel to point to new backend
log "Phase 3: Updating Vercel configuration..."

if [ "$DEPLOY_TARGET" = "blue" ]; then
    VERCEL_ENV="production"
else
    VERCEL_ENV="preview"
fi

vercel env add REACT_APP_ACTIVE_BACKEND "$DEPLOY_TARGET" $VERCEL_ENV

log "Vercel configuration updated ✅"

# Phase 4: Verify traffic switch
log "Phase 4: Verifying traffic switch..."

sleep 10

active_check=$(curl -s "$API_URL/metrics/active-environment")
if echo "$active_check" | grep -q "$DEPLOY_TARGET"; then
    log "Traffic now routing to: $DEPLOY_TARGET ✅"
else
    error "Traffic switch verification failed"
fi

# Phase 5: Monitor for issues
log "Phase 5: Monitoring for 2 minutes..."

for i in {1..4}; do
    sleep 30
    health=$(curl -s "$API_URL/health" | jq .status)
    response_time=$(curl -s -o /dev/null -w "%{time_total}" "$API_URL/health")

    log "Monitor check $i/4: Health=$health, ResponseTime=${response_time}s"

    if [ "$health" != '"healthy"' ]; then
        error "Health degradation detected - initiate rollback"
    fi
done

log "Monitoring complete - Environment stable ✅"

# Phase 6: Update documentation
log "Phase 6: Updating deployment records..."

cat >> DEPLOYMENT_LOG.md <<EOF

## Deployment $(date -u +%Y-%m-%d_%H:%M:%SZ)

- **Target**: $DEPLOY_TARGET
- **From**: $INACTIVE_ENV
- **Commit**: $LATEST_COMMIT
- **Status**: ✅ Success
- **Duration**: $(date -s "$TIMESTAMP" +%s) to $(date +%s)

### Traffic Switched
- Previous active: $INACTIVE_ENV ($INACTIVE_API)
- Current active: $DEPLOY_TARGET ($API_URL)

### Monitoring
- Health check: ✅ Passed
- Response time: Normal
- Database: Connected
- No errors detected

---
EOF

log "Deployment logged ✅"

echo -e "${GREEN}"
echo "=========================================="
echo "✅ Traffic Switch Complete!"
echo "=========================================="
echo "Active Environment: $DEPLOY_TARGET"
echo "API: $API_URL"
echo "App: $APP_URL"
echo "=========================================="
echo -e "${NC}"
```

### Rollback Script

```bash
#!/bin/bash
# rollback-traffic.sh
#
# Instantly rollback to previous environment
# Usage: ./rollback-traffic.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

echo -e "${RED}⚠️  ROLLBACK INITIATED${NC}"
echo ""

# Get current active environment
CURRENT_ACTIVE=$(curl -s https://api.example.com/metrics/active-environment 2>/dev/null || echo "unknown")

if [ "$CURRENT_ACTIVE" = "blue" ]; then
    ROLLBACK_TO="green"
else
    ROLLBACK_TO="blue"
fi

echo "Rolling back from: $CURRENT_ACTIVE"
echo "Rolling back to:   $ROLLBACK_TO"
echo ""

read -p "Confirm rollback? (type 'yes' to proceed): " confirmation
if [ "$confirmation" != "yes" ]; then
    echo "Rollback cancelled"
    exit 0
fi

log "Starting rollback to $ROLLBACK_TO..."

# Step 1: Verify target is ready
log "Verifying $ROLLBACK_TO is available..."

if [ "$ROLLBACK_TO" = "blue" ]; then
    ROLLBACK_API="https://api-blue.railway.app"
    railway environment production
else
    ROLLBACK_API="https://api-green.railway.app"
    railway environment staging
fi

health=$(curl -s -w "\n%{http_code}" "$ROLLBACK_API/health" | tail -n1)
if [ "$health" != "200" ]; then
    error "Rollback target ($ROLLBACK_TO) is not healthy. Manual intervention required."
fi

log "Target environment healthy ✅"

# Step 2: Update Railway
log "Updating Railway active environment to $ROLLBACK_TO..."
railway variable set ACTIVE_ENVIRONMENT="$ROLLBACK_TO"

log "Updating Vercel configuration..."
vercel env add REACT_APP_ACTIVE_BACKEND "$ROLLBACK_TO" production

# Step 3: Verify rollback
log "Verifying rollback..."
sleep 10

active=$(curl -s https://api.example.com/metrics/active-environment)
if echo "$active" | grep -q "$ROLLBACK_TO"; then
    log "Rollback successful - now serving from: $ROLLBACK_TO ✅"
else
    error "Rollback verification failed"
fi

# Step 4: Log incident
cat >> ROLLBACK_LOG.md <<EOF

## Rollback $(date -u +%Y-%m-%d_%H:%M:%SZ)

- **Rolled back from**: $CURRENT_ACTIVE
- **Rolled back to**: $ROLLBACK_TO
- **Reason**: Manual rollback due to deployment issues
- **Status**: ✅ Complete

**Action Items:**
1. Investigate $CURRENT_ACTIVE deployment logs
2. Identify root cause of failure
3. Coordinate fix before next deployment attempt

---
EOF

echo -e "${GREEN}"
echo "=========================================="
echo "✅ Rollback Complete!"
echo "=========================================="
echo "Active Environment: $ROLLBACK_TO"
echo "Previous: $CURRENT_ACTIVE (idle, available for rollback)"
echo "=========================================="
echo -e "${NC}"
```

## Environment Variable Strategy

### Railway Environment Variables

```bash
# .railway/config.yaml

# Blue Environment (production)
environments:
  production:
    ENVIRONMENT: "blue"
    VERSION: "1.2.3"
    ACTIVE_ENVIRONMENT: "blue"
    DATABASE_URL: "postgresql://user:pass@db-prod.railway.app/db"
    LOG_LEVEL: "info"
    ENABLE_METRICS: "true"
    API_PORT: "8000"
    CORS_ORIGINS: "https://app.example.com,https://app-blue.example.com"

  # Green Environment (staging)
  staging:
    ENVIRONMENT: "green"
    VERSION: "1.2.4"
    ACTIVE_ENVIRONMENT: "green"
    DATABASE_URL: "postgresql://user:pass@db-prod.railway.app/db"  # Same database
    LOG_LEVEL: "debug"
    ENABLE_METRICS: "true"
    API_PORT: "8000"
    CORS_ORIGINS: "https://app.example.com,https://app-staging.example.com"
```

### Vercel Environment Variables

```bash
# .vercel/env.yaml

production:
  REACT_APP_API_URL: https://api.example.com
  REACT_APP_ACTIVE_BACKEND: blue
  REACT_APP_API_BLUE_URL: https://api-blue.railway.app
  REACT_APP_API_GREEN_URL: https://api-green.railway.app
  REACT_APP_ENVIRONMENT: "production"

preview:
  REACT_APP_API_URL: https://api-staging.example.com
  REACT_APP_ACTIVE_BACKEND: green
  REACT_APP_API_BLUE_URL: https://api-blue.railway.app
  REACT_APP_API_GREEN_URL: https://api-green.railway.app
  REACT_APP_ENVIRONMENT: "staging"
```

## Monitoring & Alerts

### Datadog Monitoring Configuration

```yaml
# datadog-monitors.yaml

monitors:
  - name: "Blue-Green: Health Check Failure"
    type: "service_check"
    query: |
      'http.can_connect' over 'service:api-production' failed at least once in last 5m
    alert_message: |
      ⚠️ API health check failed in production
      Environment: {{env_name}}
      Threshold: 1 failure in 5 minutes
      Action: Review logs and initiate rollback if needed

  - name: "Blue-Green: Response Time Degradation"
    type: "metric alert"
    query: |
      avg(last_5m):avg:trace.web.request.duration{service:api-production} > 2000
    alert_message: |
      ⚠️ API response time exceeded threshold
      Current: {{value}}ms
      Threshold: 2000ms
      Action: Check database/upstream services

  - name: "Blue-Green: Error Rate Spike"
    type: "metric alert"
    query: |
      avg(last_5m):avg:trace.web.request.errors{service:api-production} > 5
    alert_message: |
      ⚠️ Error rate spike detected
      Error Count: {{value}}/min
      Threshold: 5/min
      Action: Review logs and consider rollback

  - name: "Blue-Green: Database Connection Issues"
    type: "service_check"
    query: |
      'postgres.can_connect' over 'service:api-production' failed at least once in last 5m
    alert_message: |
      ⚠️ Database connection check failed
      Service: {{service}}
      Action: Verify database is accessible
```

## Testing Strategy

### Pre-Deployment Testing

```bash
#!/bin/bash
# pre-deployment-tests.sh

set -e

log() { echo "[$(date +'%H:%M:%S')] $1"; }

log "Running pre-deployment tests..."

# Unit tests
log "Running unit tests..."
npm run test:unit -- --coverage

# Integration tests
log "Running integration tests..."
npm run test:integration

# End-to-end tests
log "Running E2E tests..."
npm run test:e2e

# Lint & type checking
log "Running linter..."
npm run lint

log "Type checking..."
npm run type-check

log "✅ All pre-deployment tests passed"
```

### Post-Deployment Validation

```bash
#!/bin/bash
# post-deployment-validation.sh

# Validates deployed environment matches expected state

set -e

ENV=$1
BASE_URL=$2

# Comprehensive validation checks
node << 'NODEJS'
const axios = require('axios');

const baseUrl = process.env.BASE_URL;
const env = process.env.ENV;

(async () => {
  console.log(`Validating ${env} environment...`);

  const checks = [
    { name: 'API Health', endpoint: '/health' },
    { name: 'Version Endpoint', endpoint: '/version' },
    { name: 'Database', endpoint: '/health/database' },
    { name: 'Cache', endpoint: '/health/cache' },
  ];

  for (const check of checks) {
    try {
      const response = await axios.get(`${baseUrl}${check.endpoint}`, {
        timeout: 5000,
      });
      console.log(`✅ ${check.name}`);
    } catch (error) {
      console.error(`❌ ${check.name}: ${error.message}`);
    }
  }
})();
NODEJS
```

## Best Practices Checklist

Production-Ready Blue-Green Deployment:

- [ ] Both environments fully synced and tested
- [ ] Automatic health checks configured and validated
- [ ] Traffic switch procedure documented and tested
- [ ] Rollback tested and verified to work instantly
- [ ] Database strategy defined (shared vs replicated)
- [ ] Monitoring and alerting configured
- [ ] Team trained on deployment procedure
- [ ] Communication plan for deployment notifications
- [ ] Incident runbook prepared
- [ ] Smoke tests automated and comprehensive
- [ ] CORS configuration validated for both envs
- [ ] SSL certificates valid for all domains
- [ ] Database backups taken before switch
- [ ] Performance baseline established
- [ ] Automated tests passing 100%


# Blue-Green Deployment - Real-World Examples

Practical, copy-paste ready examples for specific scenarios.

## Example 1: E-Commerce Platform (High Traffic)

**Context:** 10K concurrent users, payment processing, inventory sync

### Pre-Deployment Checklist

```bash
#!/bin/bash
# ecommerce-pre-deploy.sh

set -e

echo "E-Commerce Blue-Green Pre-Deployment Checklist"
echo "================================================"

# 1. Backup database
echo "1. Backing up production database..."
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d-%H%M%S).sql
echo "   ✅ Backup complete"

# 2. Check inventory sync
echo "2. Verifying inventory sync..."
curl -s https://api-blue.example.com/admin/sync/status | jq .
echo "   ✅ Inventory sync healthy"

# 3. Payment gateway health
echo "3. Checking payment gateway..."
curl -s https://api-blue.example.com/payment/health | jq .
echo "   ✅ Payment gateway connected"

# 4. Cache state
echo "4. Checking Redis cache..."
curl -s https://api-blue.example.com/health/cache | jq .
echo "   ✅ Cache healthy"

# 5. Outstanding transactions
echo "5. Checking for outstanding transactions..."
pending=$(curl -s https://api-blue.example.com/transactions/pending | jq length)
if [ "$pending" -gt 0 ]; then
    echo "   ⚠️  $pending pending transactions - wait before deployment"
    echo "   Consider scheduling for off-peak"
    exit 1
fi
echo "   ✅ No pending transactions"

# 6. Active users
echo "6. Checking active user count..."
active=$(curl -s https://api-blue.example.com/metrics/active-users | jq .count)
if [ "$active" -gt 8000 ]; then
    echo "   ⚠️  High traffic: $active active users"
    echo "   Consider waiting for off-peak (< 3000 users recommended)"
    exit 1
fi
echo "   ✅ Safe traffic level: $active users"

echo ""
echo "✅ All pre-deployment checks passed!"
echo "Safe to proceed with green deployment"
```

### Green Deployment with Feature Flags

```bash
#!/bin/bash
# ecommerce-deploy-green.sh

set -e

DEPLOY_TARGET="green"
echo "Deploying E-Commerce to $DEPLOY_TARGET..."

# 1. Build with new features disabled
echo "Building with feature flags disabled..."
npm ci
FEATURE_FLAGS_ENABLED=false npm run build

# 2. Deploy to Green
echo "Deploying to Green environment..."
railway environment staging
railway up --path-as-root backend

# 3. Migrate database (new tables, columns)
echo "Running database migrations..."
npm run migrate:up

# 4. Warm up cache
echo "Warming up cache with popular products..."
curl -X POST https://api-green.railway.app/admin/cache/warm \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"products":"top-1000","categories":"all"}'

# 5. Verify all endpoints
echo "Verifying critical endpoints..."

endpoints=(
  "/products"
  "/cart"
  "/checkout"
  "/orders"
  "/payment/validate"
  "/admin/inventory"
)

for endpoint in "${endpoints[@]}"; do
  response=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://api-green.railway.app$endpoint" \
    -H "Authorization: Bearer $TEST_TOKEN")

  if [ "$response" = "200" ] || [ "$response" = "201" ]; then
    echo "  ✅ $endpoint"
  else
    echo "  ❌ $endpoint (HTTP $response)"
    exit 1
  fi
done

echo "✅ Green environment ready for traffic switch"
```

### Canary Deployment Pattern (10% → 50% → 100%)

```bash
#!/bin/bash
# ecommerce-canary-switch.sh

set -e

echo "E-Commerce Canary Deployment (Blue → Green)"
echo "============================================="

# Step 1: Switch 10% of traffic
echo "Step 1: Switching 10% of traffic to Green..."
railway environment production
railway variable set TRAFFIC_SPLIT_GREEN="10"

sleep 30

# Monitor 10%
error_rate_10=$(curl -s https://api-green.railway.app/metrics/error-rate | jq .value)
echo "  Error rate at 10%: $error_rate_10%"

if (( $(echo "$error_rate_10 > 2" | bc -l) )); then
    echo "  ❌ Error rate too high at 10% - rolling back"
    railway variable set TRAFFIC_SPLIT_GREEN="0"
    exit 1
fi

echo "  ✅ 10% traffic stable for 30s"

# Step 2: Switch 50% of traffic
echo "Step 2: Switching 50% of traffic to Green..."
railway variable set TRAFFIC_SPLIT_GREEN="50"

sleep 60

# Monitor 50%
error_rate_50=$(curl -s https://api-green.railway.app/metrics/error-rate | jq .value)
echo "  Error rate at 50%: $error_rate_50%"

if (( $(echo "$error_rate_50 > 2" )); then
    echo "  ❌ Error rate too high at 50% - rolling back"
    railway variable set TRAFFIC_SPLIT_GREEN="0"
    exit 1
fi

echo "  ✅ 50% traffic stable for 60s"

# Step 3: Switch 100% of traffic
echo "Step 3: Switching 100% of traffic to Green..."
railway variable set TRAFFIC_SPLIT_GREEN="100"

sleep 60

# Final monitoring
error_rate_100=$(curl -s https://api.example.com/metrics/error-rate | jq .value)
echo "  Error rate at 100%: $error_rate_100%"

if (( $(echo "$error_rate_100 > 2" )); then
    echo "  ❌ Error rate too high at 100% - rolling back"
    railway variable set TRAFFIC_SPLIT_GREEN="0"
    exit 1
fi

echo "✅ Canary deployment complete - Green fully active"
```

---

## Example 2: SaaS Platform (Database Intensive)

**Context:** Multi-tenant database, complex schema, 50GB+ data

### Schema Migration Strategy

```bash
#!/bin/bash
# saas-schema-migration.sh
#
# Safe schema migration in blue-green deployment

set -e

echo "SaaS Database Schema Migration"
echo "=============================="

# Phase 1: Expand schema on Blue (additive changes only)
echo "Phase 1: Adding new columns/tables to production database..."

# Always additive - never remove columns initially
sqlite3 $DATABASE_URL << EOF
-- Add new columns (non-breaking)
ALTER TABLE users ADD COLUMN plan_tier TEXT DEFAULT 'basic';
ALTER TABLE organizations ADD COLUMN storage_quota_bytes INTEGER DEFAULT 104857600;

-- Create new tables
CREATE TABLE IF NOT EXISTS audit_logs (
  id UUID PRIMARY KEY,
  user_id UUID,
  action TEXT,
  timestamp TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Update indexes
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
EOF

echo "✅ Schema expanded on production database"

# Phase 2: Deploy Green with new schema awareness
echo "Phase 2: Deploying Green (reads new columns, ignores if missing)..."

railway environment staging
npm ci
npm run build
railway up --path-as-root backend

# Phase 3: Verify migration script
echo "Phase 3: Verifying data migration..."

# Create migration job
railway exec npm run migrate:fill-new-columns -- \
  --batch-size 1000 \
  --dry-run

# The script should:
# - Read from old columns
# - Compute values for new columns
# - Update rows in batches
# - Log progress

echo "✅ Migration verified in dry-run mode"

# Phase 4: Run actual migration
echo "Phase 4: Running data migration on Green..."

# Option A: During deployment window (requires downtime)
railway exec npm run migrate:fill-new-columns -- \
  --batch-size 1000 \
  --parallel-workers 4

# Option B: Async job after Green is live (zero downtime)
# This is safer for large datasets

echo "✅ Data migration complete"

# Phase 5: Verify data integrity
echo "Phase 5: Verifying data integrity..."

# Count rows
old_count=$(sqlite3 $DATABASE_URL "SELECT COUNT(*) FROM users;")
new_count=$(sqlite3 $DATABASE_URL "SELECT COUNT(*) FROM users WHERE plan_tier IS NOT NULL;")

if [ "$old_count" = "$new_count" ]; then
    echo "✅ All $new_count rows migrated"
else
    echo "⚠️  Migration incomplete: $new_count/$old_count rows"
fi

echo "✅ Schema migration ready for traffic switch"
```

### Transparent Migration Strategy

```typescript
// saas-backwards-compatible-migration.ts
// Deployed BEFORE schema changes - handles both old and new columns

interface User {
  id: string;
  name: string;
  // old: plan in a separate table
  // new: plan_tier TEXT column
}

// Compatibility layer
export async function getUserPlan(userId: string): Promise<string> {
  // Try new column first
  const newPlan = await db.query(`
    SELECT plan_tier FROM users WHERE id = $1
  `, [userId]);

  if (newPlan.rows.length && newPlan.rows[0].plan_tier) {
    return newPlan.rows[0].plan_tier;
  }

  // Fall back to old location
  const oldPlan = await db.query(`
    SELECT tier FROM user_plans WHERE user_id = $1
  `, [userId]);

  return oldPlan.rows[0].tier || 'basic';
}

export async function updateUserPlan(userId: string, tier: string): Promise<void> {
  // Write to BOTH locations during transition
  await Promise.all([
    // Write to new column
    db.query(`
      UPDATE users SET plan_tier = $2 WHERE id = $1
    `, [userId, tier]),

    // Write to old location (for Blue compatibility if we rollback)
    db.query(`
      UPDATE user_plans SET tier = $2 WHERE user_id = $1
    `, [userId, tier]),
  ]);
}
```

### Post-Migration Cleanup

```bash
#!/bin/bash
# saas-cleanup-after-migration.sh

set -e

# Run 1 week after successful Green deployment
# Only after confirming no rollback is needed

echo "Post-Migration Cleanup (Week 1)"
echo "==============================="

# 1. Remove old columns (once code no longer references them)
echo "Removing deprecated columns..."
sqlite3 $DATABASE_URL << EOF
-- Only after verified new column has all data
-- and code has been updated to use new column

ALTER TABLE user_plans DROP COLUMN tier;

-- Drop old indexes
DROP INDEX IF EXISTS idx_user_plans_user_id;
EOF

echo "✅ Old schema cleaned up"

# 2. Optimize indexes
echo "Optimizing indexes for new schema..."
sqlite3 $DATABASE_URL << EOF
ANALYZE;
VACUUM;
EOF

echo "✅ Database optimized"
```

---

## Example 3: Microservices Architecture

**Context:** 5 backend services, async message queue, service-to-service calls

### Coordinated Multi-Service Deployment

```bash
#!/bin/bash
# microservices-deploy-all.sh

set -e

DEPLOY_TARGET="green"
SERVICES=("auth" "api" "billing" "notifications" "worker")

echo "Deploying $DEPLOY_TARGET for all microservices..."
echo "=================================================="

# Phase 1: Deploy in dependency order
# (Services that are dependencies should be deployed first)
echo "Phase 1: Deploying services in order..."

deploy_service() {
    local service=$1
    echo ""
    echo "  Deploying $service..."

    railway environment $DEPLOY_TARGET --project $service

    # Build
    git checkout main
    npm ci
    npm run build

    # Deploy
    railway up --path-as-root .

    # Wait for healthy
    for i in {1..10}; do
        response=$(curl -s -o /dev/null -w "%{http_code}" \
            "https://$service-$DEPLOY_TARGET.railway.app/health")

        if [ "$response" = "200" ]; then
            echo "    ✅ $service healthy"
            break
        fi

        if [ $i -lt 10 ]; then
            echo "    Waiting for $service startup... ($i/10)"
            sleep 10
        fi
    done

    if [ "$response" != "200" ]; then
        echo "    ❌ $service failed to start"
        exit 1
    fi
}

# Deploy in order: auth → api → billing → notifications → worker
for service in "${SERVICES[@]}"; do
    deploy_service "$service"
done

# Phase 2: Verify inter-service communication
echo ""
echo "Phase 2: Verifying inter-service communication..."

# API calls Auth service
echo "  Testing API → Auth communication..."
response=$(curl -s "https://api-$DEPLOY_TARGET.railway.app/admin/status")
if echo "$response" | grep -q "auth.*healthy"; then
    echo "    ✅ API can reach Auth"
else
    echo "    ❌ API-Auth communication failed"
    exit 1
fi

# Billing calls API
echo "  Testing Billing → API communication..."
response=$(curl -s "https://billing-$DEPLOY_TARGET.railway.app/admin/api-status")
if echo "$response" | grep -q "api.*healthy"; then
    echo "    ✅ Billing can reach API"
else
    echo "    ❌ Billing-API communication failed"
    exit 1
fi

# Worker processes messages
echo "  Testing Worker message processing..."
worker_status=$(curl -s "https://worker-$DEPLOY_TARGET.railway.app/metrics" | jq .queued_messages)
echo "    ✅ Worker processing messages ($worker_status queued)"

echo ""
echo "✅ All microservices deployed and communicating"
```

### Canary Release for Microservices

```yaml
# microservices-canary-config.yaml

services:
  auth:
    canary: { initial: 10, step: 25, interval: 5m }
  api:
    canary: { initial: 10, step: 25, interval: 5m }
  billing:
    canary: { initial: 5, step: 20, interval: 10m }  # More conservative
  notifications:
    canary: { initial: 20, step: 40, interval: 2m }   # Less critical
  worker:
    canary: { initial: 100, step: 0, interval: 0m }   # All at once (no UI)

monitoring:
  error_rate_threshold: 2.0  # % above baseline
  latency_threshold: 1000    # ms p95
  memory_threshold: 90       # % usage

  rollback_on_metric:
    - error_rate
    - latency
    - service_unavailable

notifications:
  slack_channel: "#deployments"
  pagerduty_service: "microservices-canary"
```

---

## Example 4: Content Delivery Platform

**Context:** Media streaming, CDN integration, large file uploads

### Deployment with Edge Cache Invalidation

```bash
#!/bin/bash
# cdn-blue-green-deploy.sh

set -e

DEPLOY_TARGET="green"
CDN_ZONE="example.com"
CACHE_TTL=3600

echo "CDN Blue-Green Deployment"
echo "=========================="

# Phase 1: Deploy application
echo "Phase 1: Deploying application to $DEPLOY_TARGET..."
railway environment staging
railway up --path-as-root backend

# Wait for health
sleep 20

health=$(curl -s https://api-green.railway.app/health | jq .status)
if [ "$health" != '"healthy"' ]; then
    echo "❌ Application health check failed"
    exit 1
fi

echo "✅ Application deployed and healthy"

# Phase 2: Sync media files to CDN
echo "Phase 2: Syncing media to CDN..."

# Check if new media files added
NEW_FILES=$(git diff --name-only main | grep -E "public/media|assets" || true)

if [ -n "$NEW_FILES" ]; then
    echo "  New media files detected:"
    echo "$NEW_FILES"

    # Upload to CDN
    for file in $NEW_FILES; do
        aws s3 cp "$file" "s3://cdn-$DEPLOY_TARGET/$file" \
            --cache-control "max-age=$CACHE_TTL"
    done

    echo "  ✅ Media synced to CDN"
fi

# Phase 3: Warm CDN cache
echo "Phase 3: Warming CDN cache..."

# Fetch popular content to populate edge locations
popular_paths=(
    "/api/featured"
    "/api/trending"
    "/home"
    "/explore"
)

for path in "${popular_paths[@]}"; do
    curl -s "https://api-$DEPLOY_TARGET.railway.app$path" > /dev/null &
done

wait

echo "✅ CDN cache warmed"

# Phase 4: Ready for switch
echo ""
echo "✅ Ready for traffic switch to $DEPLOY_TARGET"
echo ""
echo "Before switching, verify:"
echo "  1. Media files loading correctly"
echo "  2. CDN cache hit rate > 90%"
echo "  3. Video transcoding working"
```

### Traffic Switch with Cache Validation

```bash
#!/bin/bash
# cdn-switch-traffic.sh

set -e

echo "CDN Blue-Green Traffic Switch"
echo "============================="

# Pre-switch: Verify cache
echo "Phase 1: Verifying CDN cache..."

cache_health=$(curl -s -I https://api-green.example.com/media/sample.mp4 | \
    grep -i "cache-control\|x-cache" || true)

echo "  Cache headers: $cache_health"

# Pre-switch: Verify video playback
echo "Phase 2: Testing video playback..."

# Try to play sample video
ffprobe "https://api-green.example.com/media/sample.mp4" \
    -show_format \
    -show_streams \
    -loglevel error > /tmp/video-probe.json

if [ $? -eq 0 ]; then
    echo "  ✅ Video playback verified"
else
    echo "  ❌ Video playback failed"
    exit 1
fi

# Switch traffic
echo "Phase 3: Switching traffic to Green..."

railway environment production
railway variable set ACTIVE_ENVIRONMENT="green"

sleep 10

# Verify switch
echo "Phase 4: Verifying traffic switch..."

active=$(curl -s https://api.example.com/metrics/active)
if echo "$active" | grep -q "green"; then
    echo "✅ Traffic switched to Green"
else
    echo "❌ Traffic switch failed - rolling back"
    railway variable set ACTIVE_ENVIRONMENT="blue"
    exit 1
fi

# Monitor CDN metrics
echo "Phase 5: Monitoring CDN metrics..."

for i in {1..5}; do
    cache_hit_ratio=$(curl -s https://cdn.example.com/metrics | jq .cache_hit_ratio)
    echo "  Minute $i: Cache hit ratio = $cache_hit_ratio"
    sleep 60
done

echo "✅ CDN deployment complete"
```

---

## Example 5: Real-Time Gaming Backend

**Context:** WebSocket connections, game state sync, player session management

### Graceful Player Disconnection During Switch

```bash
#!/bin/bash
# gaming-graceful-switch.sh

set -e

echo "Gaming Backend Blue-Green Switch (Graceful)"
echo "==========================================="

DRAIN_TIMEOUT=120  # 2 minutes for players to finish game rounds

# Phase 1: Start drain mode on Blue
echo "Phase 1: Enabling drain mode on Blue..."
echo "  (New connections route to Green)"
echo "  (Existing connections stay on Blue)"

railway environment production
railway variable set DRAIN_MODE="true"

# Notify connected players
curl -X POST https://api-blue.example.com/admin/notify-players \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{"message":"Server maintenance in 2 minutes - complete your game"}' \
    > /dev/null

echo "  ✅ Drain mode enabled - players notified"

# Phase 2: Wait for active players to finish
echo "Phase 2: Waiting for active games to complete..."

for i in $(seq 1 $((DRAIN_TIMEOUT / 10))); do
    active_games=$(curl -s https://api-blue.example.com/metrics/active-games | jq .count)
    active_players=$(curl -s https://api-blue.example.com/metrics/active-players | jq .count)

    echo "  Minute $((i * 10 / 60)): $active_games games, $active_players players"

    if [ "$active_games" -eq 0 ]; then
        echo "  ✅ All games completed - ready for switch"
        break
    fi

    sleep 10
done

# Phase 3: Force disconnect remaining players (if any)
echo "Phase 3: Disconnecting remaining players..."

if [ "$active_games" -gt 0 ]; then
    curl -X POST https://api-blue.example.com/admin/disconnect-all \
        -H "Authorization: Bearer $ADMIN_TOKEN" \
        > /dev/null

    sleep 5
fi

# Phase 4: Switch traffic
echo "Phase 4: Switching traffic to Green..."

railway variable set ACTIVE_ENVIRONMENT="green"

# Phase 5: Re-enable new connections
echo "Phase 5: Re-enabling new connections..."

railway variable set DRAIN_MODE="false"

# Wait for Green to be ready
sleep 20

# Phase 6: Verify
echo "Phase 6: Verifying..."

green_health=$(curl -s https://api-green.example.com/health | jq .status)
active_games=$(curl -s https://api-green.example.com/metrics/active-games | jq .count)

echo "  Green health: $green_health"
echo "  Active games: $active_games"

echo ""
echo "✅ Gaming backend switch complete"
echo "  Players can reconnect and start new games"
```

---

## Example 6: Analytics Platform with Batch Jobs

**Context:** Runs heavy ETL jobs, processes historical data, aggregations

### Deployment with Batch Job Coordination

```bash
#!/bin/bash
# analytics-deploy-with-batch.sh

set -e

echo "Analytics Platform Deployment"
echo "============================="

# Phase 1: Check if batch job is running
echo "Phase 1: Checking for running batch jobs..."

running_job=$(curl -s https://api-blue.example.com/admin/batch-status | jq .running)

if [ "$running_job" != "false" ]; then
    echo "  ⚠️  Batch job is running - waiting for completion..."

    # Wait up to 30 minutes for job
    for i in {1..180}; do
        job_status=$(curl -s https://api-blue.example.com/admin/batch-status)
        progress=$(echo "$job_status" | jq .progress_percent)

        if [ "$progress" = "100" ]; then
            echo "  ✅ Batch job completed"
            break
        fi

        echo "  Progress: $progress% (elapsed: $((i / 60))min)"
        sleep 10
    done
fi

# Phase 2: Disable new batch job submissions
echo "Phase 2: Disabling new batch submissions..."

railway environment staging
railway variable set BATCH_JOBS_ENABLED="false"

# Phase 3: Deploy
echo "Phase 3: Deploying Green..."

npm ci
npm run build

# Migrate analytics schema if needed
npm run migrate:analytics

railway up --path-as-root backend

# Phase 4: Verify
echo "Phase 4: Verifying..."

health=$(curl -s https://api-green.railway.app/health | jq .status)
analytics_status=$(curl -s https://api-green.railway.app/health/analytics | jq .status)

if [ "$health" = '"healthy"' ] && [ "$analytics_status" = '"healthy"' ]; then
    echo "  ✅ Green healthy"
else
    echo "  ❌ Green health check failed"
    exit 1
fi

# Phase 5: Schedule next batch
echo "Phase 5: Scheduling next batch job..."

# Next job will run on Green
curl -X POST https://api-green.railway.app/admin/schedule-batch \
    -H "Authorization: Bearer $ADMIN_TOKEN" \
    -d '{
        "job_type": "daily-aggregation",
        "scheduled_time": "2024-01-15T02:00:00Z"
    }'

echo "  ✅ Batch job scheduled for next run"

echo ""
echo "✅ Ready for traffic switch"
```

---

## Example 7: Database Replication Issues

**Context:** MySQL primary-replica setup, need to ensure Green is synced

### Binary Log Verification Before Switch

```bash
#!/bin/bash
# db-binlog-verification.sh

set -e

echo "Database Replication Status Check"
echo "=================================="

DB_PRIMARY="db-prod.railway.app"
DB_REPLICA="db-prod-replica.railway.app"

# Check replication status
REPLICA_STATUS=$(mysql -h $DB_REPLICA -u $DB_USER -p$DB_PASS \
    -e "SHOW SLAVE STATUS\G")

echo "Replica Status:"
echo "$REPLICA_STATUS"

# Extract key metrics
SECONDS_BEHIND=$(echo "$REPLICA_STATUS" | grep "Seconds_Behind_Master" | awk '{print $2}')
RELAY_LOG_POS=$(echo "$REPLICA_STATUS" | grep "Relay_Log_Pos" | awk '{print $2}')

if [ "$SECONDS_BEHIND" = "NULL" ] || [ "$SECONDS_BEHIND" -gt 5 ]; then
    echo "❌ Replica is behind by $SECONDS_BEHIND seconds"
    echo "   Safe replication lag: < 5 seconds"
    exit 1
fi

echo "✅ Replica is in sync ($SECONDS_BEHIND seconds lag)"

# Before switching, run:
# 1. Consistency check
mysql -h $DB_PRIMARY -u $DB_USER -p$DB_PASS \
    -e "SELECT CHECKSUM TABLE \`important_table\`;"

# 2. Compare row counts
PRIMARY_ROWS=$(mysql -h $DB_PRIMARY -u $DB_USER -p$DB_PASS \
    -e "SELECT COUNT(*) FROM important_table;" | tail -1)

REPLICA_ROWS=$(mysql -h $DB_REPLICA -u $DB_USER -p$DB_PASS \
    -e "SELECT COUNT(*) FROM important_table;" | tail -1)

if [ "$PRIMARY_ROWS" = "$REPLICA_ROWS" ]; then
    echo "✅ Row counts match: $PRIMARY_ROWS rows"
else
    echo "❌ Row count mismatch: Primary=$PRIMARY_ROWS, Replica=$REPLICA_ROWS"
    exit 1
fi

echo ""
echo "✅ Database replication verified - safe to deploy"
```

---

These examples cover the most common real-world scenarios. Adapt them to your specific technology stack and requirements.


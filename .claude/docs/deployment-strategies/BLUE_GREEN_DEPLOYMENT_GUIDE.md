# Blue-Green Deployment Strategy Guide

## Overview

Blue-green deployment is a zero-downtime deployment strategy that runs two identical production environments. At any time, only one (Blue or Green) handles live traffic. When deploying a new version, you deploy to the idle environment, test it thoroughly, and then switch traffic to it. If issues occur, you can instantly switch back.

**Key Benefits:**
- Zero-downtime deployments
- Instant rollback capability
- Full environment testing before traffic switch
- Reduced risk of production issues
- Easy A/B testing support

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer / Router                    │
│                  (Decides Blue or Green)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼─────┐           ┌────▼─────┐
    │   BLUE   │           │  GREEN   │
    │Environment          Environment│
    │           │           │        │
    │ v1.2.3   │           │ v1.2.4 │  ← New version (idle)
    │ Live     │           │ Warming│
    │ Traffic  │           │ Up      │
    └──────────┘           └────────┘

    CURRENT STATE
    Blue handles 100% traffic
    Green is preparing new version

    After Switch:
    Blue (idle) - v1.2.3 available for rollback
    Green (active) - v1.2.4 handles 100% traffic
```

---

## Blue-Green Deployment Steps

### Phase 1: Pre-Deployment Preparation

```bash
# 1. Verify current state
CURRENT_VERSION=$(curl -s https://api-blue.example.com/version)
echo "Current Blue version: $CURRENT_VERSION"

# 2. Check if Green is ready for deployment
GREEN_STATUS=$(curl -s https://api-green-staging.example.com/health)
echo "Green status: $GREEN_STATUS"

# 3. Verify database backups exist
# (Blue-Green requires careful database coordination)
backup_timestamp=$(date +%Y%m%d_%H%M%S)
echo "Backup timestamp for rollback: $backup_timestamp"

# 4. Set deployment target
DEPLOY_TARGET="green"  # Deploy to idle environment
```

### Phase 2: Deploy to Idle Environment (Green)

```bash
#!/bin/bash
# deploy-to-green.sh

set -e

DEPLOY_ENV="green"
NEW_VERSION="1.2.4"
DEPLOY_TIMEOUT=600  # 10 minutes

echo "Starting deployment to $DEPLOY_ENV..."

# Step 1: Pull latest code
git fetch origin
git checkout main

# Step 2: Build application
echo "Building application v$NEW_VERSION..."
npm run build
# or: python -m pip install -r requirements.txt && pytest

# Step 3: Create Docker image (if using containers)
docker build -t app:$NEW_VERSION .

# Step 4: Deploy to Green environment (Railway/Vercel example)
echo "Deploying to Green environment..."

# Railway backend deployment
railway environment green
railway up --path-as-root backend

# Vercel frontend deployment (staging green)
vercel deploy --prod --target green

# Step 5: Tag deployment
git tag "deploy-green-$NEW_VERSION-$(date +%Y%m%d-%H%M%S)"
git push origin "deploy-green-$NEW_VERSION"*

echo "Deployment to $DEPLOY_ENV complete"
```

### Phase 3: Warm-up & Health Verification

```bash
#!/bin/bash
# verify-green-health.sh

set -e

GREEN_BACKEND="https://api-green.example.com"
GREEN_FRONTEND="https://app-green.example.com"
HEALTH_CHECK_ATTEMPTS=5
HEALTH_CHECK_INTERVAL=30

echo "Verifying Green environment health..."

# Function to perform health check
check_health() {
    local url=$1
    local attempt=$2

    echo "Health check attempt $attempt/$HEALTH_CHECK_ATTEMPTS for $url"

    response=$(curl -s -w "\n%{http_code}" "$url/health")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [[ "$http_code" == "200" ]]; then
        echo "✅ Health check passed: $body"
        return 0
    else
        echo "❌ Health check failed (HTTP $http_code): $body"
        return 1
    fi
}

# Backend health checks
for i in $(seq 1 $HEALTH_CHECK_ATTEMPTS); do
    if check_health "$GREEN_BACKEND" $i; then
        break
    fi
    if [[ $i -lt $HEALTH_CHECK_ATTEMPTS ]]; then
        echo "Waiting ${HEALTH_CHECK_INTERVAL}s before retry..."
        sleep $HEALTH_CHECK_INTERVAL
    fi
done

if [[ $i -eq $HEALTH_CHECK_ATTEMPTS ]]; then
    echo "❌ Green health checks failed after $HEALTH_CHECK_ATTEMPTS attempts"
    exit 1
fi

# Frontend health checks
for i in $(seq 1 3); do
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$GREEN_FRONTEND")
    if [[ "$http_code" == "200" ]]; then
        echo "✅ Frontend responding (HTTP $http_code)"
        break
    fi
    sleep 10
done

# Database connectivity check
GREEN_DB_CHECK=$(curl -s "$GREEN_BACKEND/health/database")
if echo "$GREEN_DB_CHECK" | grep -q "connected"; then
    echo "✅ Database connectivity verified"
else
    echo "❌ Database connectivity check failed"
    exit 1
fi

# CORS validation
echo "Validating CORS configuration..."
cors_response=$(curl -s -X OPTIONS "$GREEN_BACKEND/v1/api/endpoint" \
    -H "Origin: $GREEN_FRONTEND" \
    -H "Access-Control-Request-Method: GET")

if [[ "$cors_response" == *"Access-Control-Allow-Origin"* ]]; then
    echo "✅ CORS validation passed"
else
    echo "⚠️  CORS validation warning - may be normal"
fi

echo "✅ Green environment health verification complete"
```

### Phase 4: Smoke Testing

```bash
#!/bin/bash
# smoke-tests-green.sh

set -e

GREEN_API="https://api-green.example.com"
GREEN_APP="https://app-green.example.com"

echo "Running smoke tests on Green environment..."

# Test 1: Critical API endpoints
echo "Testing critical endpoints..."
curl -s "$GREEN_API/v1/auth/status" | jq . || exit 1
curl -s "$GREEN_API/v1/data/summary" | jq . || exit 1

# Test 2: Database operations (if applicable)
echo "Testing database operations..."
curl -s -X POST "$GREEN_API/v1/test/database" | jq . || exit 1

# Test 3: Authentication flow
echo "Testing authentication flow..."
TOKEN=$(curl -s -X POST "$GREEN_API/v1/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"test","password":"test"}' | jq -r '.token')

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
    echo "❌ Authentication test failed"
    exit 1
fi

# Test 4: Frontend rendering
echo "Testing frontend rendering..."
response=$(curl -s -H "User-Agent: Mozilla/5.0" "$GREEN_APP")
if echo "$response" | grep -q "<html\|<!DOCTYPE"; then
    echo "✅ Frontend HTML rendering OK"
else
    echo "❌ Frontend rendering failed"
    exit 1
fi

# Test 5: Third-party integrations
echo "Testing third-party integrations..."
curl -s "$GREEN_API/v1/integrations/status" | jq . || exit 1

echo "✅ Smoke tests passed"
```

### Phase 5: Switch Traffic (Blue → Green)

```bash
#!/bin/bash
# switch-traffic.sh

set -e

echo "Switching traffic from Blue to Green..."

# Method 1: Using Load Balancer (Preferred)
# Update load balancer configuration to point to Green
aws elb set-instance-health \
    --load-balancer-name production-lb \
    --instances i-blue-instance \
    --state OutOfService

# Route new traffic to Green
aws elb register-instances-with-load-balancer \
    --load-balancer-name production-lb \
    --instances i-green-instance

# Method 2: Using DNS (A record switch)
# Update Route53 or DNS provider
aws route53 change-resource-record-sets \
    --hosted-zone-id Z1234567890ABC \
    --change-batch '{
        "Changes": [{
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "api.example.com",
                "Type": "A",
                "AliasTarget": {
                    "HostedZoneId": "Z35SXDOTRQ7X7K",
                    "DNSName": "green-alb.example.com",
                    "EvaluateTargetHealth": false
                }
            }
        }]
    }'

# Method 3: Using Vercel/Railway environment variables
railway environment production
railway variable update ACTIVE_VERSION="green"
vercel env pull .env.production
# Redeploy with new environment pointing to Green

# Verification
echo "Verifying traffic switch..."
sleep 10

RESPONSE=$(curl -s https://api.example.com/health)
echo "Production health check: $RESPONSE"

if echo "$RESPONSE" | grep -q "healthy"; then
    echo "✅ Traffic switch successful"
else
    echo "❌ Traffic switch verification failed - initiating rollback"
    ./rollback-to-blue.sh
    exit 1
fi
```

### Phase 6: Post-Switch Monitoring

```bash
#!/bin/bash
# monitor-after-switch.sh

set -e

MONITORING_DURATION=300  # 5 minutes
CHECK_INTERVAL=30
PROD_API="https://api.example.com"

echo "Monitoring Green environment (now active) for $MONITORING_DURATION seconds..."

start_time=$(date +%s)
failed_checks=0
max_failures=2

while true; do
    current_time=$(date +%s)
    elapsed=$((current_time - start_time))

    if [[ $elapsed -ge $MONITORING_DURATION ]]; then
        echo "✅ Monitoring period complete - Green is stable"
        break
    fi

    # Check response time
    response_time=$(curl -s -o /dev/null -w "%{time_total}" "$PROD_API/health")
    echo "Response time: ${response_time}s (elapsed: ${elapsed}s)"

    # Check error rate (from logs)
    error_rate=$(curl -s "$PROD_API/metrics/error-rate" | jq .error_rate)
    echo "Error rate: $error_rate%"

    # Check database connection
    db_health=$(curl -s "$PROD_API/health/database" | jq .status)
    if [[ "$db_health" != "connected" ]]; then
        echo "⚠️  Database health issue detected: $db_health"
        ((failed_checks++))

        if [[ $failed_checks -ge $max_failures ]]; then
            echo "❌ Health check failed $failed_checks times - initiating rollback"
            ./rollback-to-blue.sh
            exit 1
        fi
    else
        failed_checks=0  # Reset on successful check
    fi

    sleep $CHECK_INTERVAL
done

echo "✅ Post-switch monitoring complete - Green is stable and operational"
```

---

## Rollback Strategy

### Instant Rollback (If Issues Detected)

```bash
#!/bin/bash
# rollback-to-blue.sh

set -e

echo "⚠️  INITIATING ROLLBACK TO BLUE ENVIRONMENT"

ROLLBACK_START=$(date +%s)

# Step 1: Pre-rollback checks
echo "Performing pre-rollback verification..."

BLUE_HEALTH=$(curl -s https://api-blue.example.com/health)
if ! echo "$BLUE_HEALTH" | grep -q "healthy"; then
    echo "❌ Blue environment health check failed during rollback!"
    echo "Manual intervention required"
    exit 1
fi

echo "✅ Blue environment verified healthy"

# Step 2: Switch traffic back to Blue (reverse of switch-traffic.sh)
echo "Switching traffic back to Blue..."

# Using Load Balancer
aws elb set-instance-health \
    --load-balancer-name production-lb \
    --instances i-green-instance \
    --state OutOfService

aws elb register-instances-with-load-balancer \
    --load-balancer-name production-lb \
    --instances i-blue-instance

# OR using DNS
aws route53 change-resource-record-sets \
    --hosted-zone-id Z1234567890ABC \
    --change-batch '{
        "Changes": [{
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "api.example.com",
                "Type": "A",
                "AliasTarget": {
                    "HostedZoneId": "Z35SXDOTRQ7X7K",
                    "DNSName": "blue-alb.example.com",
                    "EvaluateTargetHealth": false
                }
            }
        }]
    }'

# Step 3: Verify rollback
echo "Verifying rollback..."
sleep 5

PROD_HEALTH=$(curl -s https://api.example.com/health)
if echo "$PROD_HEALTH" | grep -q "healthy"; then
    echo "✅ Rollback successful - Blue environment active"
else
    echo "❌ Rollback verification failed - manual intervention needed"
    exit 1
fi

# Step 4: Incident logging
ROLLBACK_END=$(date +%s)
ROLLBACK_DURATION=$((ROLLBACK_END - ROLLBACK_START))

echo "Logging incident..."
cat > "rollback-incident-$(date +%Y%m%d-%H%M%S).log" <<EOF
Rollback Incident Report
========================
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Duration: ${ROLLBACK_DURATION}s
Rolled back from: Green (v1.2.4)
Rolled back to: Blue (v1.2.3)
Reason: Health check failures detected post-deployment

Actions taken:
1. Traffic switched from Green to Blue
2. Blue environment verified healthy
3. Incident logged for investigation

Recommendation:
- Investigate Green deployment logs
- Debug failing service(s)
- Coordinate with team before next deployment attempt
EOF

echo "✅ Incident logged"
echo "⚠️  ROLLBACK COMPLETE - Investigate issues before next deployment"
```

### Graceful Rollback with Connection Draining

```bash
#!/bin/bash
# graceful-rollback.sh

set -e

echo "Performing graceful rollback with connection draining..."

GREEN_LB="green-load-balancer"
BLUE_LB="blue-load-balancer"
CONNECTION_DRAIN_TIMEOUT=30

# Step 1: Enable connection draining on Green
echo "Enabling connection draining on Green ($CONNECTION_DRAIN_TIMEOUT seconds)..."

aws elb modify-load-balancer-attributes \
    --load-balancer-name $GREEN_LB \
    --load-balancer-attributes ConnectionDraining={Enabled=true,Timeout=$CONNECTION_DRAIN_TIMEOUT}

# Step 2: Remove Green from load balancer (gracefully)
echo "Removing Green from load balancer..."

aws elb deregister-instances-from-load-balancer \
    --load-balancer-name production-lb \
    --instances $(aws elb describe-load-balancers \
        --load-balancer-name production-lb \
        --query 'LoadBalancerDescriptions[0].Instances[*].InstanceId' \
        --output text)

# Step 3: Wait for connection drain
echo "Waiting for in-flight connections to complete..."
sleep $CONNECTION_DRAIN_TIMEOUT

# Step 4: Add Blue back to load balancer
echo "Adding Blue back to load balancer..."

aws elb register-instances-with-load-balancer \
    --load-balancer-name production-lb \
    --instances $(aws ec2 describe-instances \
        --filters "Name=tag:Name,Values=blue-server" \
        --query 'Reservations[0].Instances[*].InstanceId' \
        --output text)

# Step 5: Verify
echo "Verifying rollback status..."
curl -s https://api.example.com/health | jq .

echo "✅ Graceful rollback complete"
```

---

## Health Check Validation Framework

### Comprehensive Health Check Configuration

```python
# health_check_validator.py

import requests
import json
import time
from typing import Dict, List, Tuple
from datetime import datetime

class BlueGreenHealthValidator:
    def __init__(self, blue_url: str, green_url: str):
        self.blue_url = blue_url
        self.green_url = green_url
        self.checks_passed = []
        self.checks_failed = []

    def run_health_checks(self, environment: str) -> bool:
        """Run comprehensive health checks"""
        base_url = self.blue_url if environment == "blue" else self.green_url

        print(f"\nRunning health checks on {environment.upper()} environment...")
        print(f"URL: {base_url}")
        print("=" * 60)

        checks = [
            self.check_api_health,
            self.check_database_connectivity,
            self.check_cache_health,
            self.check_external_services,
            self.check_ssl_certificate,
            self.check_cors_configuration,
            self.check_response_times,
            self.check_memory_usage,
            self.check_disk_space,
        ]

        for check_func in checks:
            try:
                result = check_func(base_url)
                if result:
                    self.checks_passed.append(check_func.__name__)
                    print(f"✅ {check_func.__name__}")
                else:
                    self.checks_failed.append(check_func.__name__)
                    print(f"❌ {check_func.__name__}")
            except Exception as e:
                self.checks_failed.append(check_func.__name__)
                print(f"❌ {check_func.__name__}: {str(e)}")

        print("=" * 60)
        print(f"Passed: {len(self.checks_passed)}/{len(checks)}")
        print(f"Failed: {len(self.checks_failed)}/{len(checks)}")

        return len(self.checks_failed) == 0

    def check_api_health(self, base_url: str) -> bool:
        """Check API /health endpoint"""
        response = requests.get(f"{base_url}/health", timeout=5)
        data = response.json()
        return response.status_code == 200 and data.get("status") == "healthy"

    def check_database_connectivity(self, base_url: str) -> bool:
        """Check database connection"""
        response = requests.get(f"{base_url}/health/database", timeout=10)
        data = response.json()
        return data.get("status") == "connected"

    def check_cache_health(self, base_url: str) -> bool:
        """Check Redis/cache connectivity"""
        response = requests.get(f"{base_url}/health/cache", timeout=5)
        data = response.json()
        return data.get("status") == "healthy"

    def check_external_services(self, base_url: str) -> bool:
        """Check critical external service integrations"""
        response = requests.get(f"{base_url}/health/integrations", timeout=15)
        data = response.json()

        # All critical services should be accessible
        critical_services = data.get("critical", {})
        for service, status in critical_services.items():
            if not status.get("accessible"):
                print(f"  Warning: {service} not accessible")

        return data.get("status") == "healthy"

    def check_ssl_certificate(self, base_url: str) -> bool:
        """Verify SSL certificate validity"""
        import ssl
        import socket
        from urllib.parse import urlparse

        parsed_url = urlparse(base_url)
        hostname = parsed_url.hostname

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Check if cert is valid and not expired
                return cert is not None

    def check_cors_configuration(self, base_url: str) -> bool:
        """Verify CORS headers are correctly configured"""
        headers = {
            "Origin": "https://frontend.example.com",
            "Access-Control-Request-Method": "GET"
        }
        response = requests.options(
            f"{base_url}/v1/api/endpoint",
            headers=headers,
            timeout=5
        )

        return "Access-Control-Allow-Origin" in response.headers

    def check_response_times(self, base_url: str) -> bool:
        """Ensure response times are within acceptable range"""
        start = time.time()
        response = requests.get(f"{base_url}/health", timeout=5)
        duration = (time.time() - start) * 1000  # Convert to ms

        # Alert if response time > 2 seconds (2000ms)
        if duration > 2000:
            print(f"  ⚠️  Slow response: {duration:.0f}ms (threshold: 2000ms)")
            return False

        return True

    def check_memory_usage(self, base_url: str) -> bool:
        """Check server memory usage"""
        response = requests.get(f"{base_url}/metrics/memory", timeout=5)
        data = response.json()

        memory_percent = data.get("used_percent", 0)
        if memory_percent > 90:
            print(f"  ⚠️  High memory usage: {memory_percent}%")
            return False

        return True

    def check_disk_space(self, base_url: str) -> bool:
        """Check available disk space"""
        response = requests.get(f"{base_url}/metrics/disk", timeout=5)
        data = response.json()

        disk_free_percent = 100 - data.get("used_percent", 0)
        if disk_free_percent < 10:
            print(f"  ⚠️  Low disk space: {disk_free_percent}% free")
            return False

        return True

    def generate_report(self, environment: str) -> Dict:
        """Generate health check report"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "environment": environment,
            "checks_passed": len(self.checks_passed),
            "checks_failed": len(self.checks_failed),
            "total_checks": len(self.checks_passed) + len(self.checks_failed),
            "passed_checks": self.checks_passed,
            "failed_checks": self.checks_failed,
            "status": "healthy" if len(self.checks_failed) == 0 else "unhealthy"
        }

# Usage
if __name__ == "__main__":
    validator = BlueGreenHealthValidator(
        blue_url="https://api-blue.example.com",
        green_url="https://api-green.example.com"
    )

    # Validate Green before switching
    green_healthy = validator.run_health_checks("green")
    report = validator.generate_report("green")

    print("\nHealth Check Report:")
    print(json.dumps(report, indent=2))

    if not green_healthy:
        print("\n❌ Green environment failed health checks - not ready for production")
        exit(1)
    else:
        print("\n✅ Green environment ready for traffic switch")
```

---

## GitHub Actions Workflow for Blue-Green Deployment

```yaml
# .github/workflows/blue-green-deploy.yml

name: Blue-Green Deployment

on:
  push:
    branches:
      - main
  workflow_dispatch:
    inputs:
      target_env:
        description: 'Target environment for deployment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

env:
  BLUE_BACKEND: https://api-blue.example.com
  GREEN_BACKEND: https://api-green.example.com
  BLUE_FRONTEND: https://app-blue.example.com
  GREEN_FRONTEND: https://app-green.example.com

jobs:
  determine-target:
    name: Determine Blue/Green Target
    runs-on: ubuntu-latest
    outputs:
      deploy_to: ${{ steps.determine.outputs.deploy_to }}
      active_env: ${{ steps.determine.outputs.active_env }}
    steps:
      - name: Check which environment is currently active
        id: determine
        run: |
          # Query load balancer or DNS to see which is active
          active=$(curl -s https://api.example.com/metrics/active-environment)

          if [ "$active" = "blue" ]; then
            echo "deploy_to=green" >> $GITHUB_OUTPUT
            echo "active_env=blue" >> $GITHUB_OUTPUT
          else
            echo "deploy_to=blue" >> $GITHUB_OUTPUT
            echo "active_env=green" >> $GITHUB_OUTPUT
          fi

          echo "Active environment: $active"
          echo "Deploying to: $([ "$active" = "blue" ] && echo "green" || echo "blue")"

  build:
    name: Build Application
    needs: determine-target
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build frontend
        run: npm run build

      - name: Build Docker image
        run: |
          docker build -t app:${{ github.sha }} .
          docker tag app:${{ github.sha }} app:latest

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push app:${{ github.sha }}
          docker push app:latest

  deploy-to-idle:
    name: Deploy to Idle Environment (${{ needs.determine-target.outputs.deploy_to }})
    needs: [determine-target, build]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy backend to ${{ needs.determine-target.outputs.deploy_to }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          DEPLOY_TO: ${{ needs.determine-target.outputs.deploy_to }}
        run: |
          npm install -g @railway/cli
          railway environment $DEPLOY_TO
          railway up --path-as-root backend

      - name: Deploy frontend to ${{ needs.determine-target.outputs.deploy_to }}
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          DEPLOY_TO: ${{ needs.determine-target.outputs.deploy_to }}
        run: |
          npm install -g vercel
          if [ "$DEPLOY_TO" = "green" ]; then
            vercel deploy --prod --target green
          else
            vercel deploy --prod --target blue
          fi

  health-checks:
    name: Health Check Verification
    needs: [determine-target, deploy-to-idle]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install requests

      - name: Run comprehensive health checks
        env:
          DEPLOY_TO: ${{ needs.determine-target.outputs.deploy_to }}
          BLUE_API: ${{ env.BLUE_BACKEND }}
          GREEN_API: ${{ env.GREEN_BACKEND }}
        run: |
          python .github/scripts/health_check_validator.py \
            --environment $DEPLOY_TO \
            --max-retries 5 \
            --retry-interval 30

      - name: Smoke tests
        env:
          DEPLOY_TO: ${{ needs.determine-target.outputs.deploy_to }}
        run: |
          if [ "$DEPLOY_TO" = "green" ]; then
            BASE_URL=${{ env.GREEN_BACKEND }}
          else
            BASE_URL=${{ env.BLUE_BACKEND }}
          fi

          # Test critical endpoints
          curl -s $BASE_URL/health | jq .
          curl -s $BASE_URL/v1/status | jq .

  switch-traffic:
    name: Switch Traffic to New Environment
    needs: [determine-target, health-checks]
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Approve traffic switch
        id: approval
        run: |
          echo "Manual approval required for production traffic switch"
          echo "Switching traffic from ${{ needs.determine-target.outputs.active_env }} to ${{ needs.determine-target.outputs.deploy_to }}"

      - name: Switch traffic via load balancer
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          DEPLOY_TO: ${{ needs.determine-target.outputs.deploy_to }}
        run: |
          aws elb deregister-instances-from-load-balancer \
            --load-balancer-name production-lb \
            --instances $(aws elb describe-load-balancers \
              --load-balancer-name production-lb \
              --query 'LoadBalancerDescriptions[0].Instances[*].InstanceId' \
              --output text)

          if [ "$DEPLOY_TO" = "green" ]; then
            aws elb register-instances-with-load-balancer \
              --load-balancer-name production-lb \
              --instances $(aws ec2 describe-instances \
                --filters "Name=tag:Name,Values=green-server" \
                --query 'Reservations[0].Instances[*].InstanceId' \
                --output text)
          else
            aws elb register-instances-with-load-balancer \
              --load-balancer-name production-lb \
              --instances $(aws ec2 describe-instances \
                --filters "Name=tag:Name,Values=blue-server" \
                --query 'Reservations[0].Instances[*].InstanceId' \
                --output text)
          fi

  post-switch-monitoring:
    name: Monitor New Production Environment
    needs: [determine-target, switch-traffic]
    runs-on: ubuntu-latest
    steps:
      - name: Monitor for 5 minutes
        env:
          PROD_API: https://api.example.com
          MONITOR_DURATION: 300
        run: |
          #!/bin/bash
          start_time=$(date +%s)

          while true; do
            current_time=$(date +%s)
            elapsed=$((current_time - start_time))

            if [ $elapsed -ge $MONITOR_DURATION ]; then
              echo "✅ Monitoring complete - Production stable"
              break
            fi

            # Health check
            response=$(curl -s $PROD_API/health)
            if echo "$response" | grep -q "healthy"; then
              echo "✅ Health check passed (${elapsed}s/$MONITOR_DURATION)"
            else
              echo "❌ Health check failed - initiating rollback"
              exit 1
            fi

            sleep 30
          done

      - name: Notify on success
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "✅ Blue-Green Deployment Successful",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Environment: *${{ needs.determine-target.outputs.deploy_to }}*\nStatus: *Healthy*\nCommit: *${{ github.sha }}*"
                  }
                }
              ]
            }

  rollback-on-failure:
    name: Rollback on Failure
    needs: [determine-target, post-switch-monitoring]
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - name: Initiate rollback
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          ACTIVE_ENV: ${{ needs.determine-target.outputs.active_env }}
        run: |
          echo "⚠️  Rollback initiated - switching back to $ACTIVE_ENV"

          if [ "$ACTIVE_ENV" = "blue" ]; then
            aws elb deregister-instances-from-load-balancer \
              --load-balancer-name production-lb \
              --instances $(aws ec2 describe-instances \
                --filters "Name=tag:Name,Values=green-server" \
                --query 'Reservations[0].Instances[*].InstanceId' \
                --output text)

            aws elb register-instances-with-load-balancer \
              --load-balancer-name production-lb \
              --instances $(aws ec2 describe-instances \
                --filters "Name=tag:Name,Values=blue-server" \
                --query 'Reservations[0].Instances[*].InstanceId' \
                --output text)
          fi

      - name: Notify on rollback
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️  Blue-Green Deployment Rolled Back",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Reverted to: *${{ needs.determine-target.outputs.active_env }}*\nCommit: *${{ github.sha }}*\nAction Required: Check logs for failure details"
                  }
                }
              ]
            }
```

---

## Zero-Downtime Deployment Pattern

### Connection Draining Pattern

```bash
#!/bin/bash
# zero-downtime-switch.sh

set -e

DRAIN_TIMEOUT=60
TRAFFIC_SWITCH_TARGETS=("green")

echo "Starting zero-downtime traffic switch..."

# Step 1: Activate connection draining on Blue
echo "Step 1: Activating connection draining on Blue..."
for target in "${TRAFFIC_SWITCH_TARGETS[@]}"; do
    aws elb modify-load-balancer-attributes \
        --load-balancer-name blue-lb \
        --load-balancer-attributes ConnectionDraining={Enabled=true,Timeout=$DRAIN_TIMEOUT}
done

# Step 2: Gradually remove Blue from rotation
echo "Step 2: Removing Blue from load balancer (graceful connection drain)..."
aws elb deregister-instances-from-load-balancer \
    --load-balancer-name production-lb \
    --instances $(aws ec2 describe-instances \
        --filters "Name=tag:Name,Values=blue-server" \
        --query 'Reservations[0].Instances[*].InstanceId' \
        --output text)

# Step 3: Wait for connections to drain
echo "Step 3: Waiting up to ${DRAIN_TIMEOUT}s for in-flight connections to complete..."

connections_draining=true
elapsed=0
while [ "$connections_draining" = true ] && [ $elapsed -lt $DRAIN_TIMEOUT ]; do
    draining_count=$(aws elb describe-load-balancer-attributes \
        --load-balancer-name blue-lb \
        --query 'LoadBalancerAttributes.ConnectionDraining.Timeout' \
        --output text)

    if [ "$draining_count" -eq 0 ]; then
        connections_draining=false
        echo "All connections drained"
    else
        echo "Waiting... (elapsed: ${elapsed}s/$DRAIN_TIMEOUT)"
        sleep 5
        elapsed=$((elapsed + 5))
    fi
done

# Step 4: Add Green to production
echo "Step 4: Adding Green to production load balancer..."
aws elb register-instances-with-load-balancer \
    --load-balancer-name production-lb \
    --instances $(aws ec2 describe-instances \
        --filters "Name=tag:Name,Values=green-server" \
        --query 'Reservations[0].Instances[*].InstanceId' \
        --output text)

# Step 5: Verify traffic switch
echo "Step 5: Verifying traffic is now going to Green..."
sleep 5

active_env=$(curl -s https://api.example.com/metrics/active-environment)
if [ "$active_env" = "green" ]; then
    echo "✅ Zero-downtime switch complete - Green is now active"
    echo "✅ Deployment successful with zero downtime"
else
    echo "❌ Traffic switch verification failed"
    exit 1
fi
```

---

## Comparison: Blue-Green vs Other Strategies

| Strategy | Downtime | Rollback Speed | Resource Cost | Complexity | Data Migration |
|----------|----------|---|---|---|---|
| **Blue-Green** | Zero | Instant (< 1s) | High (2x) | Medium | Manual |
| **Canary** | Zero | Gradual (5-30m) | Low-Medium | High | Manual |
| **Rolling** | Zero | Gradual (5-30m) | Low | Low | Manual |
| **Shadow** | Zero | N/A | High | High | N/A |
| **Feature Flag** | Zero | Instant | Low | Medium | N/A |

---

## Production Checklist

- [ ] Blue and Green environments fully provisioned and identical
- [ ] Database replication strategy defined (shared DB or sync)
- [ ] Load balancer configured for instant switching
- [ ] Health check endpoints validated and responding
- [ ] SSL certificates valid on both environments
- [ ] CORS configuration matches on both environments
- [ ] Database migrations tested on Green before switch
- [ ] Smoke tests documented and automated
- [ ] Rollback procedure tested and verified
- [ ] Monitoring configured for both environments
- [ ] Team trained on incident response
- [ ] Communication plan for deployment notifications
- [ ] Runbook created and documented

---

## Best Practices

1. **Separate Configuration**: Use environment variables for environment-specific config, not code changes
2. **Shared Database**: Keep database shared between Blue/Green initially for simplicity
3. **Database Versioning**: Run migrations offline or use Blue/Green database strategy for major changes
4. **Monitoring Before Switch**: Monitor Green for 5-10 minutes before switching traffic
5. **Gradual Rollback**: Use connection draining to avoid dropping active requests
6. **Health Check Sensitivity**: Ensure health checks fail fast but don't trigger on transient issues
7. **Traffic Percentage**: Start with small traffic percentage if load balancer supports it
8. **Canary Hybrid**: Use Blue-Green with canary switching (10% → 50% → 100%)
9. **Automated Rollback**: Implement auto-rollback on health check failures
10. **Documentation**: Keep deployment runbook updated and tested regularly


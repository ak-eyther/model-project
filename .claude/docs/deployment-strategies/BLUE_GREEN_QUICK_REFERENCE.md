# Blue-Green Deployment - Quick Reference Guide

## One-Minute Overview

Blue-Green deployment means running two identical production environments. When deploying:

1. Deploy new version to idle environment (Green)
2. Verify it's healthy and working
3. Switch traffic to it
4. Keep old environment (Blue) as instant rollback

**Total downtime: 0 seconds | Rollback time: < 1 second**

## Quick Commands

### Deploy to Green

```bash
# Full deployment with verification
./deploy-blue-green.sh green

# Dry run (no actual deployment)
./deploy-blue-green.sh green --dry-run

# Only verify health (no switch)
./deploy-blue-green.sh green --verify-only
```

### Switch Traffic (After Verification)

```bash
# Switch from Blue to Green
./switch-traffic.sh green

# Requires manual confirmation
```

### Instant Rollback (If Issues)

```bash
# Instantly switch back to previous environment
./rollback-traffic.sh

# Takes < 1 second
```

## Architecture Decision Tree

```
Is deployment production-critical?
├─ Yes → Use Blue-Green
│   ├─ Need instant rollback? → Blue-Green ✅
│   ├─ Can't use 2x resources? → Try Canary
│   └─ Frequent small updates? → Rolling + Feature Flags
│
└─ No → Simpler options
    ├─ Need zero-downtime? → Rolling Deployment
    ├─ Can afford 10s downtime? → Blue-Green (lighter)
    └─ Testing new features? → Shadow Deployment
```

## Deployment Phases

| Phase | Action | Duration | Risk | Rollback |
|-------|--------|----------|------|----------|
| 1️⃣ Build | Compile code, run tests | 5-10m | None | Stop deployment |
| 2️⃣ Deploy to Green | Deploy to idle env | 5m | None | Skip traffic switch |
| 3️⃣ Verify | Health checks, smoke tests | 2-5m | Low | Skip traffic switch |
| 4️⃣ Switch Traffic | Route users to Green | 30s | High | Instant rollback |
| 5️⃣ Monitor | Watch for issues | 10-30m | Medium | Rollback |

## Health Check Essentials

Must verify BEFORE switching traffic:

1. **API Health**: GET /health → {"status":"healthy"}
2. **Database**: GET /health/database → Connected
3. **Response Time**: < 2s (p95)
4. **Error Rate**: < 1%
5. **CORS**: OPTIONS request → Correct headers
6. **SSL**: Certificate valid and not expired
7. **External APIs**: Critical integrations accessible
8. **Authentication**: Login flow working

```bash
# Quick health check
curl -s https://api-green.railway.app/health | jq .
curl -s https://api-green.railway.app/health/database | jq .

# Performance check
curl -w "@curl-format.txt" -o /dev/null -s https://api-green.railway.app/health
```

## When to Use Blue-Green

### Perfect For:
- Mission-critical services (e.g., payment systems)
- Need instant rollback capability
- Can afford 2x infrastructure cost
- Want zero downtime guarantee
- Have complex stateful systems

### NOT Ideal For:
- Startup with single server
- Frequent micro-updates (use feature flags)
- Resource-constrained environments
- Simple stateless APIs (rolling deployment fine)

## Cost Comparison

```
Deployment Strategy | Infrastructure | Downtime | Rollback Time | Complexity
─────────────────────────────────────────────────────────────────────────────
Blue-Green          | 2x             | 0        | < 1s          | Medium
Canary              | 1.2x           | 0        | 5-30m         | High
Rolling             | 1.5x           | 0        | 5-30m         | Low
Blue-Green (Lite)   | 1.5x           | 10-30s   | < 1s          | Medium
Shadow              | 2x             | N/A      | N/A           | Very High
Feature Flags       | 1x             | 0        | Instant       | Low
```

## Common Failure Patterns & Solutions

### Issue: Health Checks Pass But Users See Errors

**Symptoms:**
- /health returns 200
- Real traffic fails

**Causes:**
- Incomplete health checks
- Race conditions in startup
- Env variable misconfiguration
- Database state issues

**Solution:**
```bash
# Enhance health check to match real user flows
GET /health → Check dependent services
GET /health/database → Verify read/write
GET /api/v1/status → Use real endpoint
POST /api/auth/validate → Test authentication
```

### Issue: Database State Mismatch Between Blue & Green

**Symptoms:**
- Blue uses old schema
- Green uses new schema
- Migration stuck midway

**Solution:**
```bash
# Run migrations BEFORE deploying
green_env=$(railway environment)
railway environment green

# Run migration (offline or with downtime window)
npm run migrate

# Then deploy
railway up

# Verify both can read/write
railway environment blue
curl https://api-blue.railway.app/health/database
```

### Issue: Stuck Connections During Traffic Switch

**Symptoms:**
- Some users see connection errors
- Load balancer still sends requests to old env
- 500 errors in logs

**Solution:**
- Enable connection draining (30-60 seconds)
- Use graceful shutdown
- Update DNS TTL before deployment
- Stagger traffic switch for large user bases

```bash
# Enable connection draining
aws elb modify-load-balancer-attributes \
  --load-balancer-name prod-lb \
  --load-balancer-attributes "ConnectionDraining={Enabled=true,Timeout=60}"
```

### Issue: Rollback Fails Because Blue Isn't Healthy

**Symptoms:**
- Try to rollback
- Blue environment is unhealthy
- Can't switch back

**Solution:**
```bash
# Always test Blue health before switching
curl -s https://api-blue.railway.app/health

# If Blue is dead:
# Option 1: Deploy same version to Blue first
# Option 2: Use emergency version (old production version)
# Option 3: Manual inspection and fix

# Never deploy until rollback target is ready
```

## Emergency Procedures

### Scenario: Green is Live But Degraded

1. **Immediate** (< 1 min):
   - Run: `./rollback-traffic.sh`
   - Verify Blue is serving traffic
   - Alert team

2. **Investigation** (5-15 min):
   - Check Green logs
   - Review recent changes
   - Identify root cause

3. **Resolution** (15-60 min):
   - Fix issue in code
   - Deploy new version to Blue (idle now)
   - Verify Blue is healthy
   - Switch to Blue (now fixed version)

### Scenario: Both Blue & Green Are Unhealthy

1. **Immediate**:
   - Page on-call engineer
   - Check database status
   - Check external service status

2. **Triage**:
   - Which was last known good?
   - Can we revert to previous version?
   - Is database reachable?

3. **Recovery**:
   - Deploy previous stable version to one env
   - Verify health checks pass
   - Make it the active environment

## Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] Code reviewed and approved
- [ ] Database migrations ready
- [ ] Env variables configured
- [ ] Health check endpoints verified
- [ ] CORS settings correct
- [ ] SSL certificates valid
- [ ] Monitoring configured
- [ ] Team notified
- [ ] Rollback plan understood
- [ ] Smoke tests documented
- [ ] Estimated duration calculated

## Post-Switch Monitoring

Monitor for 10-30 minutes after switching:

```bash
# Watch error rate
for i in {1..10}; do
  echo "Check $i/10:"
  curl -s https://api.example.com/metrics/error-rate | jq .
  sleep 60
done

# Watch response time
curl -w "Response time: %{time_total}s\n" -o /dev/null -s https://api.example.com/health

# Watch database connections
curl -s https://api.example.com/metrics/db-connections | jq .

# Tail logs
railway logs --environment production
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
# .github/workflows/blue-green-deploy.yml

on:
  push:
    branches: [main]

jobs:
  determine-target:
    runs-on: ubuntu-latest
    outputs:
      deploy_to: ${{ steps.target.outputs.deploy_to }}
    steps:
      - id: target
        run: |
          current=$(curl -s https://api.example.com/metrics/active)
          target=$([ "$current" = "blue" ] && echo "green" || echo "blue")
          echo "deploy_to=$target" >> $GITHUB_OUTPUT

  deploy:
    needs: determine-target
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ./deploy-blue-green.sh ${{ needs.determine-target.outputs.deploy_to }}

  verify:
    needs: [determine-target, deploy]
    runs-on: ubuntu-latest
    steps:
      - run: python3 health_check_validator.py ${{ needs.determine-target.outputs.deploy_to }}

  switch:
    needs: [determine-target, verify]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: ./switch-traffic.sh ${{ needs.determine-target.outputs.deploy_to }}
```

## Troubleshooting Matrix

| Problem | Cause | Fix |
|---------|-------|-----|
| Health check timeout | Deployment incomplete | Wait 30s, retry |
| 502 Bad Gateway | LB still routing to old | Force LB update |
| CORS error | Wrong origin header | Check env variables |
| Database error | Migration failed | Rollback & rerun migration |
| Slow response | Cold start | Warm up with requests |
| Connection refused | Service not started | Check service status |

## Key Files

- **Deployment**: `/deploy-blue-green.sh`
- **Traffic Switch**: `/switch-traffic.sh`
- **Rollback**: `/rollback-traffic.sh`
- **Health Checks**: `/health_check_validator.py`
- **Workflow**: `.github/workflows/blue-green-deploy.yml`
- **Guide**: `.claude/docs/deployment-strategies/BLUE_GREEN_DEPLOYMENT_GUIDE.md`
- **Railway Specific**: `.claude/docs/deployment-strategies/RAILWAY_BLUE_GREEN_IMPLEMENTATION.md`

## Quick Decision Matrix

```
Current State                           Next Action
──────────────────────────────────────────────────────────
All Green health checks pass    →   ./switch-traffic.sh
Some health checks fail         →   ./rollback-traffic.sh (or wait for fixes)
Green deployed, tests pending   →   Run: ./deploy-blue-green.sh green --verify
Blue is live, need to deploy    →   ./deploy-blue-green.sh green
Issue detected in production    →   ./rollback-traffic.sh
Need to keep both running       →   Don't switch, use shadow deployment
Want to test with real traffic  →   Use canary: switch 10% → 50% → 100%
```

## Performance Benchmarks

Typical blue-green deployment timings:

```
Phase                   Duration    Variance
────────────────────────────────────────────
Build & Tests           5-10m       ±2m
Deploy to Green         3-5m        ±1m
Health Checks           2m          ±30s
Smoke Tests             3m          ±1m
Traffic Switch          < 1s        < 100ms
Post-Switch Monitor     10-30m      Continuous
────────────────────────────────────────────
Total (without monitor) ~15-25m     ±5m
```

## Success Criteria

Deployment is successful when:

- ✅ No 5xx errors in logs post-switch
- ✅ Error rate same as Blue (< 1%)
- ✅ Response time same as Blue (< 2s p95)
- ✅ Database queries performing normally
- ✅ External service calls succeeding
- ✅ No increased memory/CPU usage
- ✅ Authentication/authorization working
- ✅ No customer complaints (first 30 mins)

## Disaster Recovery

**If Blue-Green fails spectacularly:**

1. **Immediate** (< 1 min):
   - Rollback to last known good
   - Page on-call team

2. **Notification** (5 min):
   - Post incident message
   - Provide status update

3. **Investigation** (1-2 hours):
   - Analyze logs
   - Identify root cause
   - Plan fix

4. **Resolution** (2-4 hours):
   - Deploy fix
   - Verify on staging first
   - Deploy to idle env
   - Perform full verification
   - Switch traffic

---

**Remember:** Blue-Green's biggest benefit is instant rollback. Use it liberally for confidence in deployments.


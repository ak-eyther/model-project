# Deployment Strategies Documentation

Complete guide to implementing production-grade deployment strategies with zero-downtime assurance.

## Overview

This directory contains comprehensive documentation for deployment strategies, focusing on blue-green deployments for high-availability systems.

### What's Included

1. **BLUE_GREEN_DEPLOYMENT_GUIDE.md** - Complete technical reference
   - Architecture overview
   - 6-phase deployment process
   - Health check validation framework
   - Rollback strategies
   - GitHub Actions integration
   - 5,000+ lines of production code

2. **RAILWAY_BLUE_GREEN_IMPLEMENTATION.md** - Practical Railway/Vercel setup
   - Environment configuration
   - Bash deployment scripts (deploy, switch, rollback)
   - Python health check validator
   - Environment variable strategy
   - Monitoring setup

3. **BLUE_GREEN_QUICK_REFERENCE.md** - Quick lookup guide
   - One-minute overview
   - Essential commands
   - Decision trees
   - Health check essentials
   - Emergency procedures
   - Troubleshooting matrix

4. **BLUE_GREEN_REAL_WORLD_EXAMPLES.md** - Copy-paste ready examples
   - E-commerce platform (high traffic, payments)
   - SaaS platform (database intensive, multi-tenant)
   - Microservices architecture (5+ services)
   - Content delivery (CDN, media streaming)
   - Gaming backend (WebSocket, real-time)
   - Analytics platform (batch jobs)
   - Database replication verification

## Quick Start

### For First-Time Setup

1. Read: **BLUE_GREEN_QUICK_REFERENCE.md** (5 min)
2. Read: **BLUE_GREEN_DEPLOYMENT_GUIDE.md** (20 min) - Focus on "Architecture Overview" and "Phase 1-6"
3. Copy scripts from: **RAILWAY_BLUE_GREEN_IMPLEMENTATION.md**
4. Customize for your platform

### For Immediate Deployment

```bash
# 1. Deploy to Green (idle environment)
./deploy-blue-green.sh green

# 2. Run health checks
python3 health_check_validator.py green

# 3. Switch traffic (after verification)
./switch-traffic.sh green

# 4. Monitor for 10-30 minutes
# Done! Rollback available instantly if issues detected

# 5. If problems occur
./rollback-traffic.sh  # < 1 second downtime
```

### For Incident Response

See: **BLUE_GREEN_QUICK_REFERENCE.md** → "Emergency Procedures" section

## Architecture Decision

### Use Blue-Green When:
- Downtime is unacceptable (financial impact, SLA penalties)
- Need instant rollback capability
- Can afford 2x infrastructure cost
- Have complex stateful systems
- Mission-critical service

### Alternative Strategies:

| Strategy | Downtime | Rollback | Cost | Complexity |
|----------|----------|----------|------|-----------|
| **Blue-Green** | 0 | < 1s | 2x | Medium |
| Canary | 0 | 5-30m | 1.2x | High |
| Rolling | 0 | 5-30m | 1.5x | Low |
| Feature Flags | 0 | Instant | 1x | Low |

## Key Concepts

### Zero-Downtime

Blue-green achieves zero downtime through:
1. Running two identical environments simultaneously
2. Routing all traffic to "Blue" (current version)
3. Deploying new code to "Green" (idle environment)
4. Switching traffic in < 1 second
5. Keeping "Blue" running as rollback target

### Instant Rollback

If Green has issues:
- Switch traffic back to Blue in < 1 second
- Blue continues serving requests
- No data loss (both read from same database)
- Can investigate Green at leisure

### Health Verification

Before switching traffic, verify:
1. API health endpoints responding
2. Database connectivity working
3. Response times acceptable
4. Error rates normal
5. CORS configuration correct
6. External services accessible
7. Authentication/authorization working
8. Cache warmed up

## Deployment Phases

```
Pre-Deploy (10 min)        Build & Test (5-10 min)    Deploy to Green (5 min)
     ↓                            ↓                           ↓
   Check state            Compile + Unit tests      Deploy to idle environment
   Verify prerequisites   Integration tests         Start services
   Run pre-flight checks  Build Docker image        Run migrations
                          Create deployment         Warm cache

                    Health Verification (2-5 min)    Switch Traffic (30 sec)
                              ↓                            ↓
                      API health checks             Update load balancer
                      Database connectivity          DNS switch
                      Response times                 Verify traffic routed
                      Error rate baseline
                      CORS validation

                    Post-Switch Monitoring (10-30 min)
                              ↓
                      Watch error rate
                      Check response times
                      Monitor resource usage
                      Tail logs for issues

                      ✅ If all healthy → Deployment complete
                      ❌ If issues → Rollback to Blue
```

## Environment Variables

### Blue Environment
```bash
ENVIRONMENT=blue
VERSION=1.2.3
ACTIVE_ENVIRONMENT=blue
DATABASE_URL=postgresql://prod-db  # Shared
CORS_ORIGINS=https://app.example.com
```

### Green Environment
```bash
ENVIRONMENT=green
VERSION=1.2.4
ACTIVE_ENVIRONMENT=green
DATABASE_URL=postgresql://prod-db  # Same DB
CORS_ORIGINS=https://app.example.com
```

Both environments share the same database (initially). This simplifies coordination and avoids data sync issues.

## Monitoring & Alerts

Set up monitoring for:

```yaml
Metrics:
  - HTTP error rate (alert if > 2%)
  - Response time p95 (alert if > 2000ms)
  - Database connection pool usage
  - Memory utilization
  - Disk space
  - Active user count
  - Cache hit rate

Checks:
  - /health endpoint responding
  - Database queries executing
  - External APIs reachable
  - SSL certificates valid
  - CORS headers present

Logs to Monitor:
  - 5xx errors
  - Database connection errors
  - Timeout errors
  - CORS policy violations
  - Authentication failures
```

## Common Issues & Solutions

### Issue: Health Checks Pass But Users See Errors

**Root Cause:** Health checks don't match real traffic patterns

**Solution:**
```bash
# Enhance health check to test real endpoints
GET /health → general status
GET /health/database → database connectivity
GET /api/v1/status → real endpoint
POST /api/auth/validate → authentication flow
```

### Issue: Database Migrations Failed

**Root Cause:** Green deployed with incompatible schema

**Solution:**
```bash
# Always run migrations OFFLINE
railway environment green
npm run migrate:up
# Verify success before switching traffic
```

### Issue: Stuck Connections During Switch

**Root Cause:** In-flight requests dropped during traffic switch

**Solution:**
```bash
# Enable connection draining (30-60 seconds)
aws elb modify-load-balancer-attributes \
  --load-balancer-attributes "ConnectionDraining={Enabled=true,Timeout=60}"
```

### Issue: Rollback Fails Because Blue Isn't Healthy

**Root Cause:** Blue was never verified before switching

**Solution:**
```bash
# Always verify rollback target before switching
curl -s https://api-blue.example.com/health
# Should return: {"status":"healthy"}
```

## Security Considerations

### CORS Configuration

Never use wildcards in production:
```bash
# ❌ WRONG in production
CORS_ORIGINS=https://*.vercel.app
CORS_ORIGINS=*

# ✅ CORRECT in production
CORS_ORIGINS=https://app.example.com,https://*.mycompany.com
```

### Database Access

Both environments share same database:
- Secure database credentials in Railway/Vercel environment variables
- Never commit secrets to git
- Use managed database (Railway PostgreSQL) not self-hosted
- Enable encryption at rest

### API Authentication

Ensure authentication works in Green before switching:
```bash
# Test login flow
curl -X POST https://api-green.example.com/auth/login \
  -d '{"username":"test","password":"test"}'

# Verify tokens work
TOKEN=$(curl -s ... | jq -r .token)
curl -H "Authorization: Bearer $TOKEN" https://api-green.example.com/profile
```

## Testing Strategy

### Pre-Deployment (Before Building)
- Unit tests
- Integration tests
- Type checking (TypeScript/Python)
- Linting

### Pre-Switch Verification (After Deploying to Green)
- Health endpoint checks
- Database connectivity
- Authentication/authorization
- CORS validation
- External API integrations
- Performance baselines

### Post-Switch Monitoring (After Traffic Switch)
- Error rate trending
- Response time degradation
- Resource utilization
- User-facing functionality
- Payment/critical features (if applicable)

## Rollback Decision Tree

```
Issue Detected in Production
         ↓
   Is it data-related?
   ├─ Yes → Investigate before rollback
   │        Database may be corrupted
   │        Check Blue logs for clues
   │
   └─ No (API/service issue)
      ├─ Instant rollback
      │  ./rollback-traffic.sh
      │  (< 1 second downtime)
      │
      └─ Investigate later
         Check Green logs
         Plan fix for next deployment
```

## Post-Deployment Checklist

After switching to Green:

- [ ] Monitor error rate for 30 minutes
- [ ] Check response time metrics
- [ ] Verify customer-facing flows working
- [ ] Check database query performance
- [ ] Verify cache hit rates
- [ ] Confirm payment processing (if applicable)
- [ ] Check log aggregation (no unexpected errors)
- [ ] Verify monitoring/alerts configured
- [ ] Document any issues encountered
- [ ] Update deployment log

## Integration with CI/CD

See: **BLUE_GREEN_DEPLOYMENT_GUIDE.md** → "GitHub Actions Workflow for Blue-Green Deployment"

The workflow automates:
1. Determine active environment (Blue or Green)
2. Build application
3. Deploy to idle environment
4. Run health checks
5. Switch traffic (manual approval gate)
6. Monitor and auto-rollback on failure

## Performance Benchmarks

Typical deployment timing (for 1000-5000 user platform):

```
Phase                Duration  Variance  Blocker?
─────────────────────────────────────────────────
Build & Tests       5-10m     ±2m       No
Deploy to Green     3-5m      ±1m       No
Health Checks       2m        ±30s      Yes
Traffic Switch      < 1s      < 100ms   No
Post-Monitoring     10-30m    Variable  Optional
─────────────────────────────────────────────────
Total               15-25min  ±5min
```

## Success Metrics

Deployment is successful when:

✅ No 5xx errors in logs
✅ Error rate < 1% (matching Blue baseline)
✅ Response time p95 < 2s (matching Blue baseline)
✅ Database queries performing normally
✅ All critical features working
✅ No customer reports (first 30 minutes)
✅ Monitoring shows green metrics

## When to Use Other Strategies

### Use Rolling Deployment When:
- Stateless services only
- Can afford gradual rollout (5-30 minutes)
- Lower risk tolerance acceptable

### Use Canary When:
- Want to test with real traffic gradually
- Have advanced monitoring
- Can tolerate 5-30 minute rollout

### Use Feature Flags When:
- Deploying multiple independent features
- Want to enable/disable features at runtime
- Need A/B testing capability

### Combine Strategies:
- Blue-Green + Feature Flags = Safe + Flexible
- Blue-Green + Canary = Safe + Gradual

## Files in This Directory

```
deployment-strategies/
├── README.md                                    (this file)
├── BLUE_GREEN_DEPLOYMENT_GUIDE.md              (5000+ lines, complete reference)
├── RAILWAY_BLUE_GREEN_IMPLEMENTATION.md        (Railway/Vercel specific)
├── BLUE_GREEN_QUICK_REFERENCE.md               (Quick lookup)
└── BLUE_GREEN_REAL_WORLD_EXAMPLES.md           (7 copy-paste examples)
```

## Scripts Location

The Bash scripts referenced in this documentation are located in:
```
project-root/
├── deploy-blue-green.sh          (Deploy to Green/Blue)
├── switch-traffic.sh              (Switch traffic to new env)
├── rollback-traffic.sh            (Instant rollback)
└── health_check_validator.py      (Comprehensive health checks)
```

## Integration with Shawar 2.0

This documentation integrates with the **Shawar 2.0** deployment expert agent:

- Shawar handles deployments using these strategies
- Shawar invokes deployment-pipeline-design skill for complex scenarios
- Shawar invokes rollback-strategies skill for graceful rollbacks
- Shawar coordinates with @harshit-2.0 for E2E tests before production

Example delegation:
```
@shawar-2.0 Deploy to production using blue-green strategy

Context:
- Current active: Blue (v1.2.3)
- New version: v1.2.4
- Feature: Critical payment processing fix
- Database: Single shared instance
```

## Getting Help

### For Quick Questions
See: **BLUE_GREEN_QUICK_REFERENCE.md**

### For Technical Details
See: **BLUE_GREEN_DEPLOYMENT_GUIDE.md**

### For Railway/Vercel Setup
See: **RAILWAY_BLUE_GREEN_IMPLEMENTATION.md**

### For Your Specific Scenario
See: **BLUE_GREEN_REAL_WORLD_EXAMPLES.md** - Find matching use case

### For Incident Response
See: **BLUE_GREEN_QUICK_REFERENCE.md** → "Emergency Procedures"

## Feedback & Updates

These guides are living documents. As you encounter:
- New deployment patterns
- Issues not covered here
- Better solutions to problems
- Platform-specific learnings

Please update these files and share with the team.

## Related Documentation

- **CI/CD Automation**: `.claude/docs/cicd/`
- **Kubernetes Deployments**: `.claude/docs/kubernetes/` (if applicable)
- **Infrastructure as Code**: `.claude/docs/infrastructure/`
- **Monitoring & Observability**: `.claude/docs/monitoring/`

---

**Last Updated:** 2025-11-24
**Blue-Green Documentation Version:** 1.0
**Status:** Production Ready


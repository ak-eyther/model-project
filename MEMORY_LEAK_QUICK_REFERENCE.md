# Memory Leak Debugging - Quick Reference Card

## 60-Second Leak Detection

```bash
# 1. Install tools
pip install memory-profiler pympler objgraph py-spy psutil

# 2. Run quick detection (5 minutes)
python memory_debug_toolkit.py detect 300 10

# Output: If "CRITICAL" or "HIGH" severity → You have a leak
```

---

## Phase 1: Confirm the Leak (5 min)

```bash
# Option A: Using toolkit
python memory_debug_toolkit.py detect 300 10
# Shows: RSS growth, severity level, verdict

# Option B: Manual monitoring
watch -n 1 'ps aux | grep uvicorn'
# Watch RSS column - if it only goes up (never down) for 5+ min → LEAK

# Option C: In running app
curl http://localhost:8000/api/debug/memory/process-info
curl http://localhost:8000/api/debug/memory/leaks
```

---

## Phase 2: Find the Endpoint (10 min)

```python
# Add decorator to suspect endpoints
from fastapi_memory_monitor import memory_tracked

@app.get("/api/suspect-endpoint")
@memory_tracked
async def endpoint():
    pass

# Load test
vegeta attack -rate 100/s -duration 5m < requests.txt

# Watch logs for memory delta
# [endpoint] Memory delta: +5.2MB | Duration: 45.1ms  <-- LEAK!
```

---

## Phase 3: Find the Line (20 min)

```bash
# Add @profile decorator
@profile
def suspect_function():
    cache = {}  # Line X
    cache[key] = big_value  # Line Y - MEMORY LEAK HERE
    return cache

# Run memory profiler
python -m memory_profiler app.py

# Output shows which line allocates memory without cleanup
```

---

## Phase 4: Match Pattern (10 min)

```bash
# Scan codebase for common leak patterns
python memory_debug_toolkit.py scan-code ./app

# Output shows pattern matches with fixes
# 🟠 HIGH SEVERITY (5 issues)
# 📍 app/cache.py:42
#    Pattern: unbounded_cache
#    Fix: Add TTL (cachetools.TTLCache) or max size limit
```

---

## Common Leak Patterns & Fixes

### Pattern 1: Unbounded Cache

```python
# BAD
cache = {}
cache[user_id] = expensive_result  # GROWS FOREVER

# GOOD
from cachetools import TTLCache
from datetime import timedelta

cache = TTLCache(maxsize=1000, ttl=timedelta(hours=1))
cache[user_id] = expensive_result  # Auto-expires
```

### Pattern 2: Global List Accumulation

```python
# BAD
RESULTS = []
RESULTS.append(new_result)  # GROWS FOREVER

# GOOD
from collections import deque

results = deque(maxlen=1000)  # Fixed size
results.append(new_result)   # Oldest items auto-removed
```

### Pattern 3: Event Listeners

```python
# BAD
message_handler = broker.subscribe("topic", callback)
# Never unsubscribed

# GOOD
message_handler = broker.subscribe("topic", callback)
@app.on_event("shutdown")
def cleanup():
    broker.unsubscribe(message_handler)
```

### Pattern 4: Database Connections

```python
# BAD
conn = await db.connect()
results = await conn.fetch("SELECT ...")
# conn never closed

# GOOD
async with db.connect() as conn:
    results = await conn.fetch("SELECT ...")
# Auto-closed
```

### Pattern 5: Circular References

```python
# BAD
obj.reference = obj  # GC can't clean up

# GOOD
import weakref
obj.reference = weakref.ref(obj)  # Weak reference
```

---

## Production Commands (No Code Changes)

```bash
# Real-time memory monitoring (30 sec samples)
py-spy top --pid $(pgrep -f uvicorn)

# Record memory snapshot (5 min duration)
py-spy record -o profile.svg --duration 300 --pid $(pgrep -f uvicorn)

# View in browser
open profile.svg

# Extract memory from logs
tail -10000 app.log | grep "RSS" | awk '{print $NF}' | \
  awk 'NR==1 {first=$1} END {print "Growth: " ($1-first) "MB"}'
```

---

## FastAPI Integration (2 min setup)

```python
# In your main.py
from fastapi_memory_monitor import setup_memory_monitoring

app = FastAPI()
setup_memory_monitoring(app)

# Now access debug endpoints:
# GET  /api/debug/memory/snapshot     - Current state
# GET  /api/debug/memory/history      - Trend over time
# GET  /api/debug/memory/growth       - Object accumulation
# GET  /api/debug/memory/leaks        - Leak verdict
# POST /api/debug/memory/gc-collect   - Manual GC
```

---

## Alert Thresholds

| Condition | Threshold | Action |
|-----------|-----------|--------|
| RSS >90% of limit | immediate | Auto-restart |
| RSS growth >5MB/min | 10 min sustained | Page on-call |
| GC pause >500ms | 5 min | Investigate |
| Endpoint delta >10MB | per request | Flag endpoint |

---

## Decision Tree

```
START: "Is memory growing?"
  │
  ├─ NO → ✅ No leak, monitoring working
  │
  └─ YES → Add @memory_tracked to endpoints
       │
       ├─ All endpoints stable? → Memory leak is in app startup/globals
       │                          → Use pattern scan (Phase 3)
       │
       └─ One endpoint growing → FOUND IT!
            │
            ├─ @profile the function
            │  │
            │  └─ Find line with dict/list assignment
            │     │
            │     ├─ No cleanup? → Apply fix from patterns
            │     └─ Has cleanup? → Check if cleanup actually runs
            │
            └─ Still not found?
                 └─ Use objgraph to trace references
                    → Shows what's holding memory alive
```

---

## Testing Your Fix

```bash
# 1. Load test for 30 minutes
vegeta attack -rate 100/s -duration 30m < requests.txt

# 2. Monitor memory every 1 minute
for i in {1..30}; do
  python memory_debug_toolkit.py detect 60 10
  sleep 60
done

# 3. Check results: Growth rate should be <1MB/min (ideally 0)

# 4. Verify in Grafana
# Graph should show flat line (or very slight slope), no continued climb
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Only checking RSS once | Natural fluctuation | Monitor for 5+ min |
| Not accounting for cache warmup | Initial growth normal | Check after 10 min stable |
| Assuming GC will cleanup | GC can't fix leaks | Fix code, don't rely on GC |
| Testing without load | No leak visible | Use vegeta/wrk for load |
| Patching wrong endpoint | Leak persists | Use @memory_tracked first |
| Forgetting to redeploy | Old code still running | Verify version: `ps aux \|grep uvicorn` |

---

## Files in This Toolkit

| File | Purpose | When to Use |
|------|---------|------------|
| `MEMORY_LEAK_DEBUGGING_GUIDE.md` | Complete reference | Initial learning, deep dives |
| `memory_debug_toolkit.py` | CLI tools | Phase 1-3 (detect, scan, analyze) |
| `fastapi_memory_monitor.py` | FastAPI integration | Development/staging testing |
| `OBSERVABILITY_METRICS.md` | Production monitoring | Setup Prometheus/Grafana alerts |
| `MEMORY_LEAK_QUICK_REFERENCE.md` | This file | Quick lookups during debugging |

---

## Runbook for On-Call

**Alert Fired: MemoryLeakDetected**

```
1. SSH to pod: kubectl exec -it pod-name bash
2. Quick check: curl http://localhost:8001/metrics | grep rss_bytes
3. Verify leak:
   - python memory_debug_toolkit.py detect 300 10
   - Check verdict
4. If confirmed:
   - Log curl http://localhost:8000/api/debug/memory/snapshot
   - Check which endpoint: curl http://localhost:8000/api/debug/memory/history
5. Options:
   a) Immediate: kubectl rollout undo deployment/api
   b) Investigate: kubectl exec -it bash → pattern scan
6. Long-term: File ticket to debug and fix
```

---

## Terminal Commands Cheat Sheet

```bash
# Quick leak check
python -c "import psutil; import time; p=psutil.Process(); t=p.memory_info().rss; time.sleep(60); print(f'Growth: {(p.memory_info().rss-t)/(1024*1024):.1f}MB')"

# Find memory-heavy process
ps aux --sort=-%mem | head -5

# Real-time memory trend (macOS)
watch -n 1 'ps aux | grep uvicorn | grep -v grep | awk "{print \$6/1024 \" MB\"}"'

# Real-time memory trend (Linux)
while true; do free -h | grep Mem; sleep 5; done

# Extract object counts from logs
grep -o "<class '[^']*'>" app.log | sort | uniq -c | sort -rn | head -20

# Calculate memory growth rate
awk '/RSS/ {if(NR==1) first=$NF; last=$NF} END {print (last-first) "MB growth"}' app.log
```

---

## Resources

- **Python docs:** https://docs.python.org/3/library/tracemalloc.html
- **Memory-profiler:** https://pypi.org/project/memory-profiler/
- **objgraph:** https://pypi.org/project/objgraph/
- **py-spy:** https://github.com/benfred/py-spy
- **cachetools:** https://pypi.org/project/cachetools/

---

**Updated:** 2025-11-24
**Tested against:** Python 3.8+, FastAPI 0.95+

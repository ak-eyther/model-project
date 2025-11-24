# Memory Leak Debugging Toolkit - START HERE

This is a complete production-ready system for detecting, profiling, and fixing memory leaks in Python/FastAPI applications.

---

## What You Get

**4 Main Deliverables:**

1. **MEMORY_LEAK_DEBUGGING_GUIDE.md** (27KB)
   - Complete 5-phase debugging workflow
   - 8 memory profiling tools with setup
   - Common leak patterns (7 types with code examples)
   - Regex patterns for log analysis
   - Production commands reference

2. **memory_debug_toolkit.py** (17KB)
   - CLI tool with 5 diagnostic commands
   - Phase 1: Quick leak detection
   - Phase 2: Object growth tracking
   - Phase 3: Pattern matching scanner
   - Phase 4: Log analysis

3. **fastapi_memory_monitor.py** (16KB)
   - Drop-in FastAPI integration
   - 7 debug endpoints for monitoring
   - Prometheus metrics integration
   - Decorators for per-endpoint tracking
   - Ready to run example included

4. **OBSERVABILITY_METRICS.md** (11KB)
   - Prometheus queries for leak detection
   - Alert rules for on-call
   - Grafana dashboard setup
   - Docker Compose examples
   - Kubernetes deployment

5. **MEMORY_LEAK_QUICK_REFERENCE.md** (8KB)
   - Decision trees and runbooks
   - 60-second quick checks
   - Common mistakes to avoid
   - Terminal commands cheat sheet

---

## Quick Start (5 Minutes)

### Step 1: Install Tools (2 min)

```bash
pip install memory-profiler pympler objgraph py-spy psutil prometheus-client
```

### Step 2: Run Quick Detection (2 min)

```bash
# Under load (in another terminal run: vegeta attack ... or ab -n 10000 ...)
python memory_debug_toolkit.py detect 300 10

# Output shows:
# - Initial/final RSS
# - Growth rate (MB/min)
# - Severity level (NONE/LOW/MEDIUM/HIGH/CRITICAL)
# - Verdict: LEAK DETECTED or NO LEAK
```

### Step 3: If Leak Detected, Pattern Match (1 min)

```bash
python memory_debug_toolkit.py scan-code ./app

# Output shows all potential leak patterns with fixes:
# 🟠 HIGH SEVERITY (unbounded_cache): app/cache.py:42
#    Fix: Use cachetools.TTLCache instead
```

---

## 5-Phase Debugging Workflow

```
PHASE 1: Confirm Leak (5 min)
├─ Run: python memory_debug_toolkit.py detect 300 10
├─ Check: Is growth >1 MB/min? Is it MONOTONIC (never decreases)?
└─ Decision: LEAK or no leak?

PHASE 2: Find Endpoint (10 min)
├─ Add @memory_tracked decorator to suspect endpoints
├─ Load test with vegeta/ab
└─ Watch logs for which endpoint has highest delta

PHASE 3: Identify Pattern (10 min)
├─ Run: python memory_debug_toolkit.py scan-code ./app
├─ Match pattern to Common Patterns table
└─ See recommended fix in output

PHASE 4: Line-Level Debug (20 min)
├─ Add @profile decorator to suspect function
├─ Run: python -m memory_profiler app.py
└─ Identify line with highest memory allocation

PHASE 5: Deploy Fix (5 min + verify)
├─ Apply fix from pattern table
├─ Load test: vegeta attack -rate 100/s -duration 30m
├─ Monitor: RSS should stabilize (<1MB/min growth)
└─ Verify: Monitor Prometheus for 1 hour
```

---

## Tools Reference

### For Immediate Leak Confirmation
```bash
# Fastest way (no code changes)
python memory_debug_toolkit.py detect 300 10

# Alternative: Real-time production monitoring (no restart needed)
py-spy top --pid $(pgrep -f uvicorn)
```

### For Development/Staging
```python
# Add to FastAPI app
from fastapi_memory_monitor import setup_memory_monitoring
app = FastAPI()
setup_memory_monitoring(app)

# Then access:
# GET /api/debug/memory/snapshot      - Current state
# GET /api/debug/memory/growth        - Object accumulation
# GET /api/debug/memory/history       - Trends
# GET /api/debug/memory/leaks         - Leak detection
```

### For Production Monitoring
```bash
# Setup Prometheus scraping
# 1. Point Prometheus to http://app:8001/metrics
# 2. Add alert rules (see OBSERVABILITY_METRICS.md)
# 3. View Grafana dashboard (JSON template included)

# Example alert: Trigger when growth >5MB/min for 10 min
curl 'http://prometheus:9090/api/v1/query?query=rate(process_rss_bytes%5B5m%5D)%20%3E%201048576'
```

---

## Common Memory Leak Patterns (Copy-Paste Fixes)

### 1. Unbounded Cache

```python
# Before (LEAK)
results_cache = {}
@app.get("/query/{q}")
def search(q):
    if q not in results_cache:
        results_cache[q] = expensive_search(q)
    return results_cache[q]

# After (FIXED)
from cachetools import TTLCache
from datetime import timedelta
results_cache = TTLCache(maxsize=1000, ttl=timedelta(hours=1))
@app.get("/query/{q}")
def search(q):
    if q not in results_cache:
        results_cache[q] = expensive_search(q)
    return results_cache[q]
```

### 2. Global List Accumulation

```python
# Before (LEAK)
LOG_HISTORY = []
def log_event(msg):
    LOG_HISTORY.append(msg)  # GROWS FOREVER

# After (FIXED)
from collections import deque
LOG_HISTORY = deque(maxlen=10000)  # Max 10K items
def log_event(msg):
    LOG_HISTORY.append(msg)  # Oldest items auto-removed
```

### 3. Unclosed Connections

```python
# Before (LEAK)
async def fetch_data():
    conn = await db.connect()
    return await conn.fetch("SELECT * FROM table")  # CONN NOT CLOSED

# After (FIXED)
async def fetch_data():
    async with db.connect() as conn:
        return await conn.fetch("SELECT * FROM table")  # Auto-closed
```

### 4. Event Listener Leak

```python
# Before (LEAK)
broker.subscribe("topic", my_handler)  # Never unsubscribed

# After (FIXED)
handler_id = broker.subscribe("topic", my_handler)
@app.on_event("shutdown")
def cleanup():
    broker.unsubscribe(handler_id)
```

---

## File Navigation Map

```
Your Project Root/
├── MEMORY_DEBUGGING_START_HERE.md          ← You are here
├── MEMORY_LEAK_DEBUGGING_GUIDE.md          ← Detailed reference
├── MEMORY_LEAK_QUICK_REFERENCE.md          ← Quick lookups
├── OBSERVABILITY_METRICS.md                ← Production setup
├── memory_debug_toolkit.py                 ← CLI tool
│   └── Usage: python memory_debug_toolkit.py [detect|scan-code|analyze-logs|dashboard|track-objects]
├── fastapi_memory_monitor.py               ← Integration code
│   └── Usage: setup_memory_monitoring(app) in your main.py
└── [Your app code]
    └── main.py
        from fastapi_memory_monitor import setup_memory_monitoring
        app = FastAPI()
        setup_memory_monitoring(app)
```

---

## Decision Tree: "Is This a Memory Leak?"

```
Question 1: Does RSS grow continuously over 5+ minutes?
├─ NO → Not a leak. Monitoring working correctly.
│
└─ YES → Does RSS ever decrease, even slightly?
   ├─ YES (decreases sometimes) → Likely not a leak. Just variable memory usage.
   │
   └─ NO (always increases) → LIKELY A LEAK! Proceed to Phase 2.
       │
       Question 2: Growth rate faster than 1 MB/min?
       ├─ YES → CRITICAL LEAK! Page on-call immediately.
       │
       └─ NO → Run @memory_tracked on endpoints to find source.
```

---

## Integration Steps

### For Development

```python
# 1. In requirements.txt, add:
prometheus-client==0.19.0
psutil==5.9.6
memory-profiler==0.61.0
pympler==1.0.1

# 2. In main.py:
from fastapi import FastAPI
from fastapi_memory_monitor import setup_memory_monitoring

app = FastAPI()
setup_memory_monitoring(app)  # One line setup!

# 3. Run app:
python -m uvicorn main:app --reload

# 4. Test endpoints:
curl http://localhost:8000/api/debug/memory/snapshot
curl http://localhost:8000/api/debug/memory/leaks
```

### For Production Monitoring

```bash
# 1. Setup Prometheus scraping (prometheus.yml):
scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'

# 2. Add alert rules (see OBSERVABILITY_METRICS.md)

# 3. Import Grafana dashboard (JSON in OBSERVABILITY_METRICS.md)

# 4. Verify metrics flowing:
curl http://localhost:8001/metrics | grep process_rss
```

---

## Troubleshooting

### Problem: "python memory_debug_toolkit.py detect hangs"
```bash
# Solution: Make sure app is running and serving requests
# In another terminal: vegeta attack -rate 100/s -duration 5m < requests.txt
```

### Problem: "No memory endpoints showing up"
```bash
# Solution: Did you call setup_memory_monitoring(app)?
# Check: curl http://localhost:8001/metrics
# If 404 → You need to call setup_memory_monitoring()
```

### Problem: "Pattern scan finds 100 potential leaks"
```bash
# Solution: Not all patterns are real leaks
# 1. Prioritize by severity (HIGH > MEDIUM > LOW)
# 2. Check if they're in hot paths (endpoints called frequently)
# 3. Run @memory_tracked first to confirm which endpoint is leaking
```

### Problem: "Metrics showing growth but leak pattern scan found nothing"
```bash
# Solution: It might be a library leak (not your code)
# Try:
# 1. objgraph to see what objects are growing
curl http://localhost:8000/api/debug/memory/growth

# 2. Check if it's a known Python issue (file handles, etc.)
curl http://localhost:8000/api/debug/memory/process-info
# Check num_fds (file descriptor count)
```

---

## Real-World Debugging Scenarios

### Scenario 1: Memory grows continuously at production launch
```
1. Get memory history: curl /api/debug/memory/history?minutes=60
2. Identify which endpoint: watch /api/debug/memory/snapshot
3. Add @memory_tracked to suspect endpoints
4. Load test: vegeta attack -rate 10/s -duration 5m
5. Which one has highest delta? That's your culprit.
6. Run pattern scan on that endpoint's code
7. Apply fix and redeploy
```

### Scenario 2: Memory spikes every hour
```
1. Something scheduled happens hourly (Celery task? scheduler?)
2. Get timeline: curl /api/debug/memory/history?minutes=120
3. Identify time of spike
4. Check logs for what runs at that time
5. Profile that scheduled task
6. Fix the task to clean up resources
```

### Scenario 3: Memory OK for days, then OOM crash
```
1. Slow leak - growth <1MB/min but sustained
2. Use Prometheus to look at 7-day trend
3. Calculate time-to-OOM: (RAM_LIMIT - CURRENT_RSS) / GROWTH_RATE_MB_PER_MIN / 60
4. If >30 days: low priority but fix before it becomes urgent
5. Follow normal debugging phases
```

---

## Estimated Time to Resolution

| Scenario | Detection | Location | Fix | Verify | Total |
|----------|-----------|----------|-----|--------|-------|
| Obvious endpoint leak | 5 min | 10 min | 5 min | 30 min | 50 min |
| Subtle pattern (unbounded cache) | 10 min | 20 min | 5 min | 30 min | 65 min |
| Library/system leak | 15 min | 45 min | 1-2 hrs | 30 min | 2-3 hrs |
| Complex (multi-endpoint) | 20 min | 60 min | 30 min | 60 min | 2-3 hrs |

---

## Key Concepts

**RSS (Resident Set Size):** Actual physical memory used. This is what matters.

**VMS (Virtual Memory Size):** Total virtual address space. Less useful.

**Monotonic Growth:** Always increases, never decreases. Strong leak indicator.

**Heap Fragmentation:** Memory freed but not returned to OS. Shows as VMS growth without RSS growth.

**Garbage Collection:** Can't fix application leaks (circular refs, unclosed resources). Must fix code.

**GC Slowdown:** If GC pauses >500ms, you likely have a leak (too many objects).

---

## Next Steps

1. **Read:** MEMORY_LEAK_DEBUGGING_GUIDE.md (30 min) for deep understanding
2. **Setup:** Call setup_memory_monitoring() in your FastAPI app
3. **Test:** Run python memory_debug_toolkit.py detect 300 10 under load
4. **If leak found:** Follow 5-phase workflow (Phase 2 onwards)
5. **Monitor:** Setup Prometheus alerts per OBSERVABILITY_METRICS.md

---

## Support & Questions

Each file has detailed sections:
- **Specific tool questions:** See tool's section in MEMORY_LEAK_DEBUGGING_GUIDE.md
- **Production setup:** See OBSERVABILITY_METRICS.md
- **Quick lookup:** See MEMORY_LEAK_QUICK_REFERENCE.md
- **Pattern matching:** Run `python memory_debug_toolkit.py scan-code ./app`

---

**Toolkit Version:** 1.0
**Created:** 2025-11-24
**For:** Python 3.8+, FastAPI 0.95+, FastAPI 0.95+
**Last Updated:** 2025-11-24

---

## Summary

This toolkit provides everything needed to debug memory leaks in production FastAPI:

- Command-line tools (no code changes needed)
- FastAPI integration (one-line setup)
- 5-phase debugging workflow
- 7 common leak patterns with fixes
- Prometheus/Grafana setup
- 60-second quick checks
- Production runbooks

**Get started:** `python memory_debug_toolkit.py detect 300 10`

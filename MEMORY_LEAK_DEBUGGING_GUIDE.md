# Systematic Memory Leak Debugging Guide for Python/FastAPI

## Executive Summary

Memory leaks in production FastAPI applications manifest as:
- **Gradual memory growth** over hours/days (RSS increases, never decreases)
- **Unchanged code behavior** (no crashes, just memory bloat)
- **Cascading failures** (eventual OOM kill on container restart)

This guide provides a systematic debugging workflow with specific tools, regex patterns for error detection, and observability metrics.

---

## Part 1: Memory Profiling Tools & Setup

### 1.1 Essential Tools (Install in Order)

```bash
# Core memory profiling
pip install memory-profiler pympler tracemalloc objgraph guppy3

# Production monitoring
pip install py-spy psutil prometheus-client

# Async-specific profiling
pip install aiosnoop aiofiles

# Stack trace analysis
pip install traceback-plus better-traceback
```

### 1.2 Tool Quick Reference

| Tool | Purpose | Overhead | Best For |
|------|---------|----------|----------|
| `tracemalloc` | Built-in memory tracking | Low (0-10%) | Snapshot comparisons |
| `memory-profiler` | Line-by-line RAM usage | High (5-50x) | Exact leak locations |
| `objgraph` | Object reference chains | Medium (5-20%) | Finding retained objects |
| `py-spy` | Sampling profiler (C-level) | Very Low (1-3%) | Production without restart |
| `pympler` | Memory segmentation (RSS/heap) | Medium | Understanding total growth |
| `tracemalloc` | Python 3.4+ standard | Built-in | Peak memory tracking |

---

## Part 2: Debugging Workflow (5 Phases)

### Phase 1: Symptom Detection (Pre-Investigation)

**Goal:** Confirm leak exists and identify time-to-failure.

#### 1.1 Container Memory Monitoring

```bash
# In production/staging container
docker stats --no-stream | grep fastapi-container
# Output: Container | MEM USAGE | MEM LIMIT | MEM % | CPU % | CPU TIME | NET I/O
# Watch RSS grow: 512MB → 768MB → 1024MB (steady upward trend = LEAK)

# Or using Kubernetes
kubectl top pod -n production fastapi-pod
watch kubectl top pod -n production fastapi-pod
```

#### 1.2 Quick Leak Detection Script

```python
# file: detect_leak.py
import psutil
import time
from datetime import datetime

def monitor_memory(duration_minutes=30, interval_seconds=60):
    """
    Detect memory leak by comparing RSS growth over time.
    Returns: (is_leak, growth_rate_mb_per_minute)
    """
    process = psutil.Process()
    measurements = []

    print(f"[{datetime.now()}] Starting memory leak detection ({duration_minutes} min)")

    for i in range(duration_minutes):
        rss_mb = process.memory_info().rss / (1024 * 1024)
        measurements.append(rss_mb)
        print(f"[{i*interval_seconds}s] RSS: {rss_mb:.1f}MB")
        time.sleep(interval_seconds)

    # Calculate growth trend
    initial_rss = measurements[0]
    final_rss = measurements[-1]
    growth_mb = final_rss - initial_rss
    growth_rate = growth_mb / duration_minutes

    # Leak detection heuristic: >5MB/min = LEAK
    is_leak = growth_rate > 5

    print(f"\n=== LEAK ANALYSIS ===")
    print(f"Initial RSS: {initial_rss:.1f}MB")
    print(f"Final RSS: {final_rss:.1f}MB")
    print(f"Total growth: {growth_mb:.1f}MB in {duration_minutes} min")
    print(f"Growth rate: {growth_rate:.2f}MB/min")
    print(f"Verdict: {'LEAK DETECTED' if is_leak else 'NO LEAK'}")

    return is_leak, growth_rate

if __name__ == "__main__":
    monitor_memory(duration_minutes=5, interval_seconds=10)
```

**Run this during load testing:**
```bash
# Terminal 1: Start FastAPI server
uvicorn main:app --reload

# Terminal 2: Load test with vegeta/wrk
echo "GET http://localhost:8000/api/endpoint" | vegeta attack -duration=5m | vegeta report

# Terminal 3: Monitor memory
python detect_leak.py
```

#### 1.3 Regex Pattern for Log-Based Detection

```python
import re
from collections import defaultdict

# Pattern to extract memory growth from application logs
MEMORY_PATTERN = r'.*\[(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\].*RSS:\s*(?P<rss>\d+(?:\.\d+)?)\s*MB.*'

def parse_memory_logs(log_file):
    """Extract memory growth pattern from logs"""
    growth_events = []

    with open(log_file) as f:
        prev_rss = None
        for line in f:
            match = re.match(MEMORY_PATTERN, line)
            if match:
                rss = float(match.group('rss'))
                timestamp = match.group('timestamp')

                if prev_rss and (rss - prev_rss) > 10:  # 10MB jump = spike
                    growth_events.append({
                        'timestamp': timestamp,
                        'rss': rss,
                        'delta': rss - prev_rss,
                        'direction': 'UP' if rss > prev_rss else 'DOWN'
                    })
                prev_rss = rss

    return growth_events
```

---

### Phase 2: Baseline Memory Profiling

**Goal:** Measure memory usage at different load levels.

#### 2.1 Using `tracemalloc` (Recommended First Step)

```python
# file: baseline_profiler.py
import tracemalloc
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def startup_memory_tracking():
    """Enable memory tracking on startup"""
    tracemalloc.start()
    print("tracemalloc started")

@app.get("/api/memory-snapshot")
def get_memory_snapshot():
    """
    Endpoint to get current memory allocation snapshot.
    Access: GET http://localhost:8000/api/memory-snapshot
    """
    current, peak = tracemalloc.get_traced_memory()

    # Get top allocations
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    top_10 = [
        {
            "file": str(stat.traceback[0]).split('/')[-1],
            "size_mb": stat.size / (1024*1024),
            "count": stat.count
        }
        for stat in top_stats[:10]
    ]

    return {
        "current_mb": current / (1024*1024),
        "peak_mb": peak / (1024*1024),
        "top_allocations": top_10
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Usage:**
```bash
# Terminal 1
python baseline_profiler.py

# Terminal 2: Generate baseline
curl http://localhost:8000/api/memory-snapshot | jq
# Output example:
# {
#   "current_mb": 45.2,
#   "peak_mb": 52.1,
#   "top_allocations": [
#     {"file": "numpy.py", "size_mb": 12.5, "count": 2048},
#     ...
#   ]
# }
```

#### 2.2 Memory Profiling Specific Endpoints

```python
# file: endpoint_profiler.py
from memory_profiler import profile
import psutil
from functools import wraps

def memory_tracked(func):
    """Decorator to track memory before/after endpoint execution"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        process = psutil.Process()
        mem_before = process.memory_info().rss / (1024*1024)

        result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)

        mem_after = process.memory_info().rss / (1024*1024)
        delta = mem_after - mem_before

        print(f"[{func.__name__}] Memory delta: {delta:+.2f}MB ({mem_before:.1f}MB → {mem_after:.1f}MB)")

        return result
    return wrapper

@app.get("/api/suspect-endpoint")
@memory_tracked
async def suspect_endpoint(query: str = ""):
    """Endpoint suspected of leaking memory"""
    # Implementation here
    pass
```

---

### Phase 3: Detailed Leak Location Identification

**Goal:** Find exact line numbers where memory isn't being freed.

#### 3.1 Object Reference Tracking with `objgraph`

```python
# file: objgraph_tracker.py
import objgraph
import gc
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
def enable_objgraph():
    """Enable object growth tracking"""
    gc.collect()
    objgraph.show_most_common_types(limit=20)

@app.get("/api/track-objects")
def track_objects():
    """
    Endpoint to detect which objects are growing.
    Access: GET http://localhost:8000/api/track-objects
    """
    gc.collect()

    # Show object growth since startup
    objgraph.show_growth()

    return {"status": "Growth report printed to stdout"}

@app.get("/api/object-graph/{object_type}")
def get_object_graph(object_type: str = "dict"):
    """
    Trace reference chain for specific object types.
    Example: /api/object-graph/list
    """
    gc.collect()

    # Find objects of type and show references
    objs = objgraph.by_type(object_type)

    if objs:
        # Show reference chain for first object
        objgraph.show_refs([objs[0]], filename='/tmp/refs.png')

        return {
            "type": object_type,
            "count": len(objs),
            "reference_graph": "/tmp/refs.png",
            "sample_objects": str(objs[:3])
        }

    return {"error": f"No objects of type {object_type}"}
```

**Usage:**
```bash
# Start server and load test it
python objgraph_tracker.py &
# Hit it with requests
for i in {1..100}; do curl http://localhost:8000/api/endpoint; done

# Check what's growing
curl http://localhost:8000/api/track-objects
# Output will show growth patterns like:
# <class 'dict'>                   1234  (+987)
# <class 'list'>                   5678  (+4321)
# ^ This tells you which object types are accumulating
```

#### 3.2 Memory Profiler for Line-Level Analysis

```python
# file: line_profiler.py
from memory_profiler import profile

@profile
def memory_intensive_function(data_size=1000):
    """
    Profile memory at each line.
    Run: python -m memory_profiler line_profiler.py
    """
    # Line 1: baseline
    small_list = [1, 2, 3]  # minimal memory

    # Line 2: LEAK HERE - dict grows without cleanup
    cache = {i: {"data": list(range(1000))} for i in range(data_size)}

    # Line 3: process data
    results = [sum(cache[i]["data"]) for i in range(data_size)]

    # Line 4: MEMORY STILL HELD - cache not garbage collected
    return len(results)

if __name__ == "__main__":
    memory_intensive_function(10000)
```

**Run it:**
```bash
python -m memory_profiler line_profiler.py
# Output:
# Line #    Mem usage    Increment   Line Contents
# ================================================
#      1     40.5 MiB      0.0 MiB   @profile
#      2     40.5 MiB      0.0 MiB   def memory_intensive...
#      7     40.8 MiB      0.3 MiB   small_list = [1, 2, 3]
#      8    256.2 MiB    215.4 MiB   cache = {i: {"data": ...}}  <-- LEAK HERE
#      12   256.2 MiB      0.0 MiB   return len(results)
```

---

### Phase 4: Root Cause Analysis (Common Leak Patterns)

**Goal:** Identify which category your leak falls into.

#### 4.1 Memory Leak Pattern Detection

```python
# file: leak_pattern_detector.py
import re
import ast
import sys

LEAK_PATTERNS = {
    'unbounded_cache': {
        'regex': r'cache\[.+?\]\s*=\s*.+?(?!del|pop|clear)',
        'description': 'Cache grows without cleanup',
        'fix': 'Add TTL or max size limits'
    },
    'circular_reference': {
        'regex': r'self\.\w+\s*=\s*self',
        'description': 'Object references itself (prevents GC)',
        'fix': 'Use weakref or __del__'
    },
    'event_listener_leak': {
        'regex': r'\.on\(|addEventListener|\.subscribe\(',
        'description': 'Event listeners not unsubscribed',
        'fix': 'Call unsubscribe/removeListener on cleanup'
    },
    'global_accumulation': {
        'regex': r'^[A-Z_]+\s*=\s*\[\]|dict\(\)',
        'description': 'Global list/dict accumulates data',
        'fix': 'Use instance variables or bounded collections'
    },
    'thread_pool_leak': {
        'regex': r'ThreadPoolExecutor|ProcessPoolExecutor(?!as\s)',
        'description': 'Thread pool not cleaned up',
        'fix': 'Use `with` statement or call .shutdown()'
    },
    'database_connection_leak': {
        'regex': r'\.connect\(\)|session\.\w+(?!with)',
        'description': 'DB connections not closed',
        'fix': 'Use context managers or close() in finally'
    },
    'async_task_leak': {
        'regex': r'asyncio\.create_task|gather|ensure_future(?!await)',
        'description': 'Async tasks created but not awaited',
        'fix': 'Always await or store handles to cancel'
    }
}

def scan_codebase(directory):
    """Scan Python files for memory leak patterns"""
    findings = []

    import glob
    for py_file in glob.glob(f'{directory}/**/*.py', recursive=True):
        try:
            with open(py_file) as f:
                content = f.read()

            for pattern_name, pattern_info in LEAK_PATTERNS.items():
                matches = re.finditer(pattern_info['regex'], content, re.MULTILINE)
                for match in matches:
                    line_no = content[:match.start()].count('\n') + 1
                    findings.append({
                        'file': py_file,
                        'line': line_no,
                        'pattern': pattern_name,
                        'description': pattern_info['description'],
                        'fix': pattern_info['fix'],
                        'code': content.split('\n')[line_no-1].strip()
                    })
        except:
            pass

    return findings

if __name__ == "__main__":
    import json
    findings = scan_codebase('.')

    print(f"\n=== POTENTIAL MEMORY LEAKS ({len(findings)} found) ===\n")
    for finding in findings:
        print(f"📍 {finding['file']}:{finding['line']}")
        print(f"   Pattern: {finding['pattern']}")
        print(f"   Issue: {finding['description']}")
        print(f"   Code: {finding['code']}")
        print(f"   Fix: {finding['fix']}")
        print()
```

**Run pattern detection:**
```bash
python leak_pattern_detector.py
# Output:
# === POTENTIAL MEMORY LEAKS (5 found) ===
#
# 📍 app/cache.py:42
#    Pattern: unbounded_cache
#    Issue: Cache grows without cleanup
#    Code: self.cache[key] = expensive_result
#    Fix: Add TTL or max size limits
```

#### 4.2 Common Leak Patterns in FastAPI/Python

| Pattern | Signature | Example | Fix |
|---------|-----------|---------|-----|
| **Unbounded Cache** | `cache[key] = value` (no cleanup) | Query result cache | Use `functools.lru_cache` or `cachetools.TTLCache` |
| **Circular References** | `obj.ref = obj` or `parent.child = child` | Event listeners | Use `weakref.ref()` |
| **Global Lists** | `RESULTS = []` accumulates | Result history | Reset periodically or use deque with maxlen |
| **DB Connection Pool** | Pool not closed | SQLAlchemy session | Always use `async with` or context manager |
| **Event Listener** | `.subscribe()` without unsubscribe | Message broker | Store handle, call `.unsubscribe()` |
| **Thread Pools** | `ThreadPoolExecutor()` not shutdown | Background jobs | Use `with` statement or `.shutdown()` |
| **Async Tasks** | `asyncio.create_task()` not awaited | Fire-and-forget | Store handle or use task groups |
| **Regex Compilation** | `re.compile()` in loop | Pattern matching | Cache patterns at module level |
| **Logger Handlers** | `logger.addHandler()` not removed | Dynamic logging | Call `logger.removeHandler()` |
| **File Handles** | File not closed | Large file processing | Use context managers |

---

### Phase 5: Production Monitoring & Verification

**Goal:** Monitor memory in production with minimal overhead.

#### 5.1 Prometheus Metrics Integration

```python
# file: memory_metrics.py
import psutil
from prometheus_client import Gauge, Counter, start_http_server
import asyncio

# Define metrics
rss_memory = Gauge('process_rss_bytes', 'Resident Set Size in bytes')
vms_memory = Gauge('process_vms_bytes', 'Virtual Memory Size in bytes')
gc_collections = Counter('gc_collections_total', 'Total garbage collections', ['generation'])

async def update_memory_metrics():
    """Update memory metrics every 30 seconds"""
    process = psutil.Process()

    while True:
        try:
            mem = process.memory_info()
            rss_memory.set(mem.rss)
            vms_memory.set(mem.vms)

            await asyncio.sleep(30)
        except Exception as e:
            print(f"Error updating metrics: {e}")

# Add to FastAPI startup
@app.on_event("startup")
def start_metrics_server():
    """Start Prometheus metrics server on port 8001"""
    start_http_server(8001)
    asyncio.create_task(update_memory_metrics())

# Usage: curl http://localhost:8001/metrics
```

**Prometheus query to detect leaks:**
```prometheus
# Spike detection (growth > 50MB in 5 min)
rate(process_rss_bytes[5m]) > 52428800

# Linear growth pattern (>1MB/min for 30 min)
(
    process_rss_bytes offset 30m - process_rss_bytes
) / 30 > 1048576
```

#### 5.2 Production Memory Profiling without Restart

```bash
# Using py-spy (minimal overhead, no code changes)
py-spy record -o memory_profile.svg --duration 300 --pid $(pgrep -f uvicorn)

# View timeline
py-spy top --pid $(pgrep -f uvicorn)
# Output:
# PID   USER   TIME   RESIDENT   CPU
# 1234  app    45s    512.5MB    8.2%  <-- Watch RESIDENT column
```

#### 5.3 Alert Rules for Memory Leaks

```yaml
# Prometheus alerting rules
groups:
  - name: memory_leaks
    rules:
      - alert: MemoryLeakDetected
        expr: |
          (
            process_rss_bytes - process_rss_bytes offset 1h
          ) / 1024 / 1024 > 100  # 100MB growth in 1 hour
        for: 10m
        annotations:
          summary: "Memory leak detected on {{ $labels.instance }}"
          description: "Process RSS increased by 100MB+ in 1 hour"

      - alert: MemorySpikeDetected
        expr: |
          rate(process_rss_bytes[5m]) > 10485760  # 10MB/min
        for: 5m
        annotations:
          summary: "Rapid memory growth on {{ $labels.instance }}"
```

---

## Part 3: Real-World Debugging Checklist

### Step 1: Confirm Leak (5 min)

- [ ] Run `detect_leak.py` for 5 minutes under normal load
- [ ] Compare RSS at start vs end: if > 20MB growth, proceed
- [ ] Check if growth is **monotonic** (always up, never down) - hallmark of leak

### Step 2: Profile Endpoints (15 min)

- [ ] Add `@memory_tracked` to suspect endpoints
- [ ] Generate load with `vegeta` or `wrk`
- [ ] Identify which endpoint(s) cause growth
- [ ] Note time-to-leak: 100 requests? 1000? 1 hour?

### Step 3: Pattern Match (10 min)

- [ ] Run `leak_pattern_detector.py`
- [ ] Review findings against Common Patterns table
- [ ] Create hypothesis: "Global cache grows unbounded in endpoint X"

### Step 4: Line-Level Analysis (20 min)

- [ ] Apply `@profile` decorator to suspect function
- [ ] Run with `python -m memory_profiler`
- [ ] Identify exact line where memory isn't freed
- [ ] Confirm with `objgraph.show_growth()`

### Step 5: Deploy Fix (5 min)

- [ ] Apply fix from pattern table (e.g., TTL cache)
- [ ] Load test with `vegeta`
- [ ] Verify: RSS stable or only grows <1MB/min
- [ ] Monitor Prometheus for 1 hour

### Step 6: Post-Mortem (10 min)

- [ ] Document root cause and fix
- [ ] Add regression test (memory threshold)
- [ ] Update code review checklist

---

## Part 4: Code Patterns Reference

### GOOD: Bounded Cache with TTL

```python
from cachetools import TTLCache
from datetime import timedelta

# GOOD: Memory limited to 100 items, auto-expired after 1 hour
query_cache = TTLCache(maxsize=100, ttl=timedelta(hours=1))

@app.get("/api/query/{query_id}")
async def get_query(query_id: str):
    if query_id in query_cache:
        return query_cache[query_id]

    result = await expensive_operation(query_id)
    query_cache[query_id] = result
    return result
```

### BAD: Unbounded Cache

```python
# BAD: Dictionary grows forever, items never removed
results_cache = {}

@app.get("/api/query/{query_id}")
async def get_query(query_id: str):
    if query_id in results_cache:
        return results_cache[query_id]

    result = await expensive_operation(query_id)
    results_cache[query_id] = result  # MEMORY LEAK!
    return result
```

### GOOD: Proper Connection Management

```python
# GOOD: Always use context manager
async def fetch_data():
    async with db.connect() as conn:
        return await conn.fetch("SELECT * FROM table")
```

### BAD: Connection Leak

```python
# BAD: Connection created but never closed
async def fetch_data():
    conn = await db.connect()
    return await conn.fetch("SELECT * FROM table")  # Leak!
```

### GOOD: Event Listener Management

```python
# GOOD: Unsubscribe on cleanup
class MessageHandler:
    def __init__(self, broker):
        self.broker = broker
        self.handler_id = broker.subscribe("topic", self.on_message)

    def on_message(self, msg):
        print(f"Received: {msg}")

    def cleanup(self):
        self.broker.unsubscribe(self.handler_id)  # Clean up!

@app.on_event("shutdown")
async def shutdown():
    handler.cleanup()
```

### BAD: Event Listener Leak

```python
# BAD: Listener never unsubscribed
class MessageHandler:
    def __init__(self, broker):
        broker.subscribe("topic", self.on_message)  # Leak!

    def on_message(self, msg):
        print(f"Received: {msg}")
```

---

## Part 5: Quick Reference Commands

```bash
# === IMMEDIATE DIAGNOSTICS ===

# 1. Show memory growth right now
python -c "import psutil; p=psutil.Process(); print(f'RSS: {p.memory_info().rss/(1024**2):.1f}MB')"

# 2. List top memory consumers
ps aux --sort=-%mem | head -10

# 3. Monitor in real-time (top-like)
watch -n 1 'ps aux | grep uvicorn | grep -v grep'

# === PRODUCTION PROFILING (no restart needed) ===

# 4. Snapshot memory with py-spy
py-spy record -o profile.svg --duration 60 --pid $(pgrep -f uvicorn)

# 5. Live memory monitoring
py-spy top --pid $(pgrep -f uvicorn)

# === LOG-BASED LEAK DETECTION ===

# 6. Find memory spikes in logs (>100MB jumps)
grep -E '(RSS|memory)' app.log | awk '{print $NF}' | \
  awk 'NR>1{if($1-prev>100)print NR,prev"->"$1; prev=$1}'

# 7. Calculate memory growth rate
tail -1000 app.log | grep -oP 'RSS:\s*\K[0-9.]+' | \
  awk '{if(NR==1)first=$1; last=$1} END {print "Growth: " (last-first) "MB in " NR " samples"}'

# === CLEANUP & GARBAGE COLLECTION ===

# 8. Force Python garbage collection
python -c "import gc; gc.collect(); print('GC forced')"

# 9. Show object references keeping memory alive
python -c "import objgraph; objgraph.show_most_common_types(limit=20)"
```

---

## Part 6: Regex Patterns for Error Extraction

### Memory Leak Signature Extraction

```python
import re
from collections import defaultdict

# Regex patterns to detect memory leak signatures in logs
LEAK_SIGNATURES = {
    'monotonic_growth': r'RSS:\s*(\d+)MB.*RSS:\s*(\d+)MB',
    'unbounded_accumulation': r'(cache|buffer|queue|list)\s*[:=].*(?!clear|pop|del)',
    'gc_failure': r'gc.*collect|GC.*took.*(\d+)ms',
    'object_growth': r'<class\s+\'(\w+)\'>\s+(\d+)\s+\(\+(\d+)\)',
}

def extract_leak_signatures(log_content):
    """Extract memory leak patterns from structured logs"""

    # Pattern 1: Monotonic RSS growth (10, 11, 12, 13, 14... = LEAK)
    rss_values = re.findall(r'RSS:\s*(\d+)MB', log_content)
    is_monotonic = all(rss_values[i] <= rss_values[i+1] for i in range(len(rss_values)-1))

    # Pattern 2: Object type accumulation
    object_growth = defaultdict(int)
    for match in re.finditer(LEAK_SIGNATURES['object_growth'], log_content):
        obj_type, total, growth = match.groups()
        object_growth[obj_type] = int(growth)

    # Pattern 3: GC collection time increasing (slower collections = more objects)
    gc_times = re.findall(r'GC took (\d+)ms', log_content)
    gc_slowdown = len(gc_times) > 0 and gc_times[-1] > gc_times[0] * 2

    return {
        'monotonic_growth': is_monotonic,
        'rss_trend': rss_values[-1] - rss_values[0] if len(rss_values) > 1 else 0,
        'object_growth': dict(object_growth),
        'gc_slowdown': gc_slowdown,
        'risk_level': 'CRITICAL' if is_monotonic and gc_slowdown else 'HIGH' if is_monotonic else 'MEDIUM'
    }
```

### Application Error Correlation

```python
# Regex to correlate memory issues with errors
MEMORY_ERROR_PATTERNS = {
    'oom_kill': r'Killed\s+\(|killed due to oom|OutOfMemory',
    'memory_error': r'MemoryError|memory allocation failed',
    'timeout_after_memory': r'memory.*(\d+)MB.*timeout after (\d+)s',
    'gc_overhead': r'GC overhead.*exceeds',
}

def correlate_errors_with_memory(logs):
    """Find errors that occur after memory spikes"""

    timeline = []

    for line in logs.split('\n'):
        # Extract RSS
        rss_match = re.search(r'RSS:\s*(\d+)MB', line)
        if rss_match:
            timeline.append({
                'time': line[:19],  # ISO timestamp
                'type': 'memory',
                'value': int(rss_match.group(1))
            })

        # Extract errors
        for error_type, pattern in MEMORY_ERROR_PATTERNS.items():
            if re.search(pattern, line):
                timeline.append({
                    'time': line[:19],
                    'type': 'error',
                    'error': error_type
                })

    # Find correlations: error after memory spike
    correlations = []
    for i, event in enumerate(timeline):
        if event['type'] == 'error':
            # Look back 5 events for memory spikes
            memory_events = [e for e in timeline[max(0,i-5):i] if e['type'] == 'memory']
            if memory_events and memory_events[-1]['value'] > 800:  # >800MB
                correlations.append({
                    'error': event['error'],
                    'precursor_rss': memory_events[-1]['value'],
                    'time_delta': event['time']
                })

    return correlations
```

---

## Part 7: Deployment Strategy

### Staging Before Production Fix

```bash
# 1. Reproduce leak in staging
kubectl apply -f deployment-staging.yaml

# 2. Load test and monitor
vegeta attack -rate 100/s -duration 1h < requests.txt | tee results.txt
kubectl top pod -n staging

# 3. Verify fix
# - RSS should stabilize after 10 min
# - No monotonic growth over 1 hour
# - GC collection times should be stable

# 4. If passing, deploy to production
kubectl apply -f deployment-prod.yaml

# 5. Smoke test
curl -w '%{http_code}' https://api.prod.example.com/health

# 6. Monitor for 24 hours
watch -n 30 'kubectl top pod -n production | grep api'
```

### Rollback Plan

```bash
# If memory still grows in production:
kubectl set image deployment/api api=old-image:v1.2.3 -n production
kubectl rollout status deployment/api -n production

# Then investigate what fix didn't work
```

---

## Summary Table: When to Use Each Tool

| Situation | Tool | Command | Time |
|-----------|------|---------|------|
| Quick leak confirmation | `psutil` | `detect_leak.py` | 5 min |
| Identify affected endpoints | `@memory_tracked` | Add decorator + load test | 10 min |
| Find exact line | `memory-profiler` | `python -m memory_profiler app.py` | 20 min |
| See object growth | `objgraph` | `/api/track-objects` | 5 min |
| Pattern matching | `leak_pattern_detector.py` | `python leak_pattern_detector.py` | 10 min |
| Production profiling | `py-spy` | `py-spy record --pid ...` | 5-10 min |
| Monitoring/alerts | Prometheus + alerts | Scrape metrics endpoint | Ongoing |

---

## Next Steps

1. **Install tools:** `pip install memory-profiler pympler objgraph py-spy`
2. **Run detection:** Copy `detect_leak.py`, generate load, confirm leak
3. **Profile endpoints:** Add `@memory_tracked` decorators, identify hotspots
4. **Match pattern:** Run `leak_pattern_detector.py`, map to Common Patterns
5. **Line-level debug:** Apply `@profile`, run memory-profiler
6. **Deploy fix:** Use pattern-specific fix from reference section
7. **Verify:** Load test, monitor Prometheus for 1 hour

---

**Created:** 2025-11-24
**Last Updated:** 2025-11-24
**Audience:** Python/FastAPI developers, DevOps, SREs

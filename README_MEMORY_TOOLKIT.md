# Memory Leak Debugging Toolkit for Python/FastAPI

## Overview

Complete production-ready system for detecting, profiling, and fixing memory leaks in Python/FastAPI applications. Includes 8 tools, 5-phase workflow, 8 common leak patterns with fixes, Prometheus integration, and more.

## Files Included (109KB total)

| File | Size | Purpose |
|------|------|---------|
| `MEMORY_DEBUGGING_START_HERE.md` | 12KB | Quick start guide - **START HERE** |
| `MEMORY_LEAK_DEBUGGING_GUIDE.md` | 27KB | Comprehensive reference (all tools & workflow) |
| `memory_debug_toolkit.py` | 17KB | CLI tool with 5 diagnostic commands |
| `fastapi_memory_monitor.py` | 16KB | FastAPI integration (1-line setup) |
| `OBSERVABILITY_METRICS.md` | 11KB | Production monitoring setup |
| `MEMORY_LEAK_QUICK_REFERENCE.md` | 8.2KB | Cheat sheet & runbooks |
| `TOOLKIT_SUMMARY.txt` | 18KB | This toolkit's summary |

## Quick Start (5 Minutes)

### 1. Install Tools
```bash
pip install memory-profiler pympler objgraph py-spy psutil prometheus-client
```

### 2. Detect Leak
```bash
# Run under load for 5 minutes
python memory_debug_toolkit.py detect 300 10

# Output shows: growth rate, severity, verdict
```

### 3. Find Pattern
```bash
# Scan code for common leak patterns
python memory_debug_toolkit.py scan-code ./app

# Output shows: pattern type, line number, fix recommendation
```

### 4. Apply Fix
```python
# Use copy-paste fix from pattern table
# Example: Unbounded cache → Use cachetools.TTLCache
from cachetools import TTLCache
from datetime import timedelta

cache = TTLCache(maxsize=1000, ttl=timedelta(hours=1))
```

### 5. Verify
```bash
# Load test 30 minutes and monitor growth
vegeta attack -rate 100/s -duration 30m < requests.txt
python memory_debug_toolkit.py dashboard 1800 10
```

## What You Get

### Tools (8 included)

| Tool | Overhead | Best For | Setup |
|------|----------|----------|-------|
| `tracemalloc` | 0-10% | Snapshot comparisons | Built-in |
| `memory-profiler` | 5-50x | Exact line locations | CLI command |
| `objgraph` | 5-20% | Finding retained objects | Python code |
| `py-spy` | 1-3% | Production (no restart) | Command-line |
| `pympler` | 5% | Memory segmentation | Python code |
| `psutil` | <1% | Quick leak detection | Python code |
| `memory_debug_toolkit.py` | <1% | Automated detection | Python script |
| `fastapi_memory_monitor.py` | <5% | Integration + endpoints | 1-line setup |

### 5-Phase Debugging Workflow

```
Phase 1: Confirm (5 min)       → Run quick detection
Phase 2: Find Endpoint (10 min) → Add @memory_tracked
Phase 3: Pattern Match (10 min) → Run pattern scanner
Phase 4: Line Debug (20 min)    → Add @profile decorator
Phase 5: Deploy Fix (5 min)     → Apply & verify
```

### 8 Common Leak Patterns

1. **Unbounded Cache** (HIGH) - `cache[key] = value`
2. **Global Accumulation** (HIGH) - `GLOBAL_LIST = []`
3. **Circular References** (MEDIUM) - `self.ref = self`
4. **DB Connections** (HIGH) - `conn = db.connect()`
5. **Event Listeners** (HIGH) - `.subscribe()` no unsubscribe
6. **Thread Pools** (MEDIUM) - `ThreadPoolExecutor()` no shutdown
7. **Async Tasks** (MEDIUM) - `asyncio.create_task()` not awaited
8. **File Handles** (MEDIUM) - `open()` no context manager

## Integration with FastAPI

```python
# In your main.py
from fastapi import FastAPI
from fastapi_memory_monitor import setup_memory_monitoring

app = FastAPI()
setup_memory_monitoring(app)  # One line!

# Now access debug endpoints:
# GET  /api/debug/memory/snapshot     - Current state
# GET  /api/debug/memory/growth       - Object accumulation
# GET  /api/debug/memory/history      - Trends over time
# GET  /api/debug/memory/leaks        - Leak detection verdict
# POST /api/debug/memory/gc-collect   - Manual GC trigger
```

## Production Monitoring

### Prometheus Setup
```yaml
scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
```

### Alert Rules
```prometheus
# Detect leak (>5MB/min for 10 min)
rate(process_rss_bytes[5m]) > 5*1024*1024

# GC slowdown (>500ms p95)
histogram_quantile(0.95, gc_duration_ms) > 500
```

### Grafana Dashboard
Pre-built JSON template included in `OBSERVABILITY_METRICS.md`

## Key Metrics

- **RSS Growth Rate**: Main leak indicator
- **Endpoint Memory Delta**: Identify which endpoint leaks
- **GC Duration**: Slowdown indicates too many objects
- **Object Type Counts**: Which types are accumulating

## Decision Tree

```
Does RSS grow monotonically for 5+ minutes?
├─ NO → No leak detected
└─ YES → Is growth >1 MB/min?
    ├─ NO → Slow leak, investigate
    └─ YES → Rapid leak, page on-call
```

## Common Mistakes to Avoid

- Only checking RSS once (fluctuates naturally)
- Not accounting for cache warmup (initial growth normal)
- Assuming GC will cleanup (it won't fix leaks)
- Testing without load (leak not visible)
- Not verifying fix over 30 minutes (need sustained test)

## Estimation Times

| Scenario | Time |
|----------|------|
| Obvious endpoint leak | 50 min |
| Unbounded cache pattern | 65 min |
| Library/system leak | 2-3 hrs |
| Complex (multi-endpoint) | 2-3 hrs |

## Files Navigation

**First Time?**
1. Read: `MEMORY_DEBUGGING_START_HERE.md` (5 min)

**Need Quick Lookup?**
2. Check: `MEMORY_LEAK_QUICK_REFERENCE.md`

**Deep Dive?**
3. Study: `MEMORY_LEAK_DEBUGGING_GUIDE.md`

**Need Code Example?**
4. See: Specific pattern section in guide

**Production Setup?**
5. Follow: `OBSERVABILITY_METRICS.md`

## CLI Commands

```bash
# Quick leak detection (5 min sampling)
python memory_debug_toolkit.py detect 300 10

# Pattern scan entire codebase
python memory_debug_toolkit.py scan-code ./app

# Track object type growth
python memory_debug_toolkit.py track-objects

# Analyze logs for memory patterns
python memory_debug_toolkit.py analyze-logs app.log

# Real-time monitoring dashboard
python memory_debug_toolkit.py dashboard 600 5
```

## Production Commands (No Code Changes)

```bash
# Real-time memory monitoring (native tool)
py-spy top --pid $(pgrep -f uvicorn)

# Record memory profile (5 min)
py-spy record -o profile.svg --duration 300 --pid $(pgrep -f uvicorn)

# Check current process memory
ps aux | grep uvicorn | grep -v grep
```

## Common Questions

**Q: Can I use this in production?**
A: Yes! `py-spy` and CLI tools work on live processes without restarts. Optional FastAPI integration is low-overhead (<5% CPU).

**Q: Do I need to restart my app?**
A: Not necessarily. `py-spy` and dashboard endpoints work on running processes. FastAPI integration requires restart for first-time setup.

**Q: How much memory does the toolkit use?**
A: CLI tools: <1MB overhead. FastAPI integration: <5MB with metrics collection.

**Q: What if I can't find the leak?**
A: Follow the decision tree → Run pattern scanner → Use objgraph to trace references → Profile suspect functions.

**Q: How do I verify the fix?**
A: Load test for 30 minutes, monitor RSS growth <1MB/min, check Prometheus metrics for 1 hour.

## Supported Python Versions

- Python 3.8+
- FastAPI 0.95+
- Works with async and sync code

## Related Resources

- Python tracemalloc: https://docs.python.org/3/library/tracemalloc.html
- Memory-profiler: https://pypi.org/project/memory-profiler/
- objgraph: https://pypi.org/project/objgraph/
- py-spy: https://github.com/benfred/py-spy
- Prometheus: https://prometheus.io

## Toolkit Info

- **Version**: 1.0
- **Created**: 2025-11-24
- **Total Size**: 109KB (7 files)
- **Setup Time**: 5 minutes
- **First Detection**: 5 minutes
- **Average Resolution**: 50 min - 2 hrs

## Next Steps

1. **Install**: `pip install memory-profiler pympler objgraph psutil`
2. **Read**: `MEMORY_DEBUGGING_START_HERE.md` (5 min)
3. **Detect**: `python memory_debug_toolkit.py detect 300 10` (under load)
4. **Scan**: `python memory_debug_toolkit.py scan-code ./app`
5. **Fix**: Apply pattern-specific solution
6. **Verify**: Load test 30 minutes

## Questions?

- Start with: `MEMORY_DEBUGGING_START_HERE.md`
- Quick lookup: `MEMORY_LEAK_QUICK_REFERENCE.md`
- Deep dive: `MEMORY_LEAK_DEBUGGING_GUIDE.md`
- Setup: `OBSERVABILITY_METRICS.md`

---

**Ready to start?** Begin with `MEMORY_DEBUGGING_START_HERE.md`

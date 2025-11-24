"""
FastAPI Memory Monitoring Integration
Ready-to-use decorators and endpoints for production memory leak debugging
"""

import time
import psutil
import tracemalloc
import gc
import asyncio
from functools import wraps
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timedelta
from collections import deque

from fastapi import FastAPI, Response
from prometheus_client import Gauge, Counter, Histogram, start_http_server


# ============================================================================
# PROMETHEUS METRICS
# ============================================================================

process_rss_bytes = Gauge(
    'process_rss_bytes',
    'Process Resident Set Size in bytes',
    labelnames=['stage']
)

process_vms_bytes = Gauge(
    'process_vms_bytes',
    'Process Virtual Memory Size in bytes',
    labelnames=['stage']
)

gc_collections_total = Counter(
    'gc_collections_total',
    'Total garbage collection runs',
    labelnames=['generation']
)

endpoint_memory_delta = Histogram(
    'endpoint_memory_delta_bytes',
    'Memory change per endpoint call (bytes)',
    labelnames=['endpoint', 'method'],
    buckets=[1024*100, 1024*500, 1024*1024, 5*1024*1024, 10*1024*1024, 50*1024*1024]
)

gc_duration_ms = Histogram(
    'gc_duration_ms',
    'Garbage collection duration (milliseconds)',
    labelnames=['generation']
)


# ============================================================================
# MEMORY TRACKING DECORATORS
# ============================================================================

class MemoryTracker:
    """Context manager and decorator for memory tracking"""

    def __init__(self, name: str = "operation"):
        self.name = name
        self.process = psutil.Process()
        self.start_rss = 0
        self.start_time = 0
        self.end_rss = 0
        self.end_time = 0

    def __enter__(self):
        self.start_rss = self.process.memory_info().rss
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_rss = self.process.memory_info().rss
        self.end_time = time.time()

    @property
    def delta_bytes(self) -> int:
        return self.end_rss - self.start_rss

    @property
    def delta_mb(self) -> float:
        return self.delta_bytes / (1024 * 1024)

    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000

    def report(self) -> Dict[str, Any]:
        return {
            "operation": self.name,
            "start_rss_mb": self.start_rss / (1024 * 1024),
            "end_rss_mb": self.end_rss / (1024 * 1024),
            "delta_mb": round(self.delta_mb, 2),
            "duration_ms": round(self.duration_ms, 2),
            "timestamp": datetime.now().isoformat()
        }


def memory_tracked(func: Callable) -> Callable:
    """
    Decorator to track memory before/after async function execution
    Usage:
        @app.get("/api/endpoint")
        @memory_tracked
        async def my_endpoint():
            pass
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        tracker = MemoryTracker(func.__name__)

        with tracker:
            result = await func(*args, **kwargs)

        # Log the memory delta
        print(f"[{func.__name__}] Memory delta: {tracker.delta_mb:+.2f}MB | "
              f"Duration: {tracker.duration_ms:.1f}ms")

        # Record metric (if endpoint path available)
        endpoint_path = getattr(args[0], 'path', func.__name__) if args else func.__name__
        method = getattr(args[0], 'method', 'UNKNOWN') if args else 'UNKNOWN'
        endpoint_memory_delta.labels(endpoint=endpoint_path, method=method).observe(tracker.delta_bytes)

        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        tracker = MemoryTracker(func.__name__)

        with tracker:
            result = func(*args, **kwargs)

        print(f"[{func.__name__}] Memory delta: {tracker.delta_mb:+.2f}MB | "
              f"Duration: {tracker.duration_ms:.1f}ms")

        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


# ============================================================================
# MEMORY MONITORING ENDPOINTS
# ============================================================================

class MemoryMonitoringEndpoints:
    """Collection of memory debugging endpoints"""

    def __init__(self, app: FastAPI, enable_tracemalloc: bool = True):
        self.app = app
        self.process = psutil.Process()

        if enable_tracemalloc:
            tracemalloc.start()

        self.memory_history = deque(maxlen=1000)

        # Register endpoints
        self._register_endpoints()
        self._register_startup()

    def _register_startup(self):
        """Register startup event to begin metric collection"""

        @self.app.on_event("startup")
        async def startup_metrics():
            # Start Prometheus metrics server
            start_http_server(8001)

            # Start background memory tracking
            asyncio.create_task(self._update_metrics_loop())

            print("[Memory Monitor] Started (metrics on :8001/metrics)")

    async def _update_metrics_loop(self):
        """Background task to update metrics periodically"""
        while True:
            try:
                mem = self.process.memory_info()
                process_rss_bytes.labels(stage='production').set(mem.rss)
                process_vms_bytes.labels(stage='production').set(mem.vms)

                self.memory_history.append({
                    'timestamp': time.time(),
                    'rss_mb': mem.rss / (1024 * 1024),
                    'vms_mb': mem.vms / (1024 * 1024)
                })

                await asyncio.sleep(30)  # Update every 30 seconds

            except Exception as e:
                print(f"[Memory Monitor] Error updating metrics: {e}")

    def _register_endpoints(self):
        """Register all memory monitoring endpoints"""

        @self.app.get("/api/debug/memory/snapshot")
        async def memory_snapshot():
            """
            Get current memory snapshot with top allocations
            Endpoint: GET /api/debug/memory/snapshot
            """
            gc.collect()
            mem = self.process.memory_info()
            current, peak = tracemalloc.get_traced_memory()

            # Get top allocations
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            top_allocations = []
            for stat in top_stats[:15]:
                filename = stat.traceback[0].filename if stat.traceback else "unknown"
                lineno = stat.traceback[0].lineno if stat.traceback else 0
                top_allocations.append({
                    "file": filename.split('/')[-1],
                    "line": lineno,
                    "size_mb": round(stat.size / (1024 * 1024), 2),
                    "count": stat.count
                })

            return {
                "timestamp": datetime.now().isoformat(),
                "rss_mb": round(mem.rss / (1024 * 1024), 2),
                "vms_mb": round(mem.vms / (1024 * 1024), 2),
                "tracemalloc_current_mb": round(current / (1024 * 1024), 2),
                "tracemalloc_peak_mb": round(peak / (1024 * 1024), 2),
                "top_allocations": top_allocations,
                "num_threads": self.process.num_threads()
            }

        @self.app.get("/api/debug/memory/growth")
        async def memory_growth():
            """
            Track object type growth (requires objgraph)
            Endpoint: GET /api/debug/memory/growth
            """
            try:
                import objgraph
            except ImportError:
                return {"error": "objgraph not installed. Install: pip install objgraph"}

            gc.collect()

            # Get most common types
            most_common = objgraph.most_common_types(limit=20)

            return {
                "timestamp": datetime.now().isoformat(),
                "most_common_types": [
                    {"type": name, "count": count}
                    for name, count in most_common
                ]
            }

        @self.app.get("/api/debug/memory/history")
        async def memory_history(minutes: int = 10):
            """
            Get memory history for the past N minutes
            Endpoint: GET /api/debug/memory/history?minutes=10
            """
            if not self.memory_history:
                return {"error": "No history available yet"}

            cutoff_time = time.time() - (minutes * 60)
            recent = [
                {
                    "timestamp": datetime.fromtimestamp(entry['timestamp']).isoformat(),
                    "rss_mb": round(entry['rss_mb'], 2),
                    "vms_mb": round(entry['vms_mb'], 2)
                }
                for entry in self.memory_history
                if entry['timestamp'] >= cutoff_time
            ]

            # Calculate trend
            if len(recent) > 1:
                growth_rate = (recent[-1]['rss_mb'] - recent[0]['rss_mb']) / len(recent)
            else:
                growth_rate = 0

            return {
                "period_minutes": minutes,
                "samples": len(recent),
                "growth_rate_mb_per_sample": round(growth_rate, 3),
                "history": recent
            }

        @self.app.get("/api/debug/memory/gc-stats")
        async def gc_stats():
            """
            Get garbage collection statistics
            Endpoint: GET /api/debug/memory/gc-stats
            """
            gc_stats = gc.get_stats() if hasattr(gc, 'get_stats') else []

            return {
                "timestamp": datetime.now().isoformat(),
                "gc_enabled": gc.isenabled(),
                "gc_count": [gc.get_count()[i] for i in range(3)],
                "gc_stats": gc_stats,
                "garbage_objects": len(gc.garbage)
            }

        @self.app.post("/api/debug/memory/gc-collect")
        async def trigger_gc():
            """
            Manually trigger garbage collection (for testing)
            Endpoint: POST /api/debug/memory/gc-collect
            """
            mem_before = self.process.memory_info().rss

            start_time = time.time()
            collected = gc.collect()
            duration_ms = (time.time() - start_time) * 1000

            mem_after = self.process.memory_info().rss

            gc_duration_ms.labels(generation='all').observe(duration_ms)

            return {
                "timestamp": datetime.now().isoformat(),
                "collected_objects": collected,
                "duration_ms": round(duration_ms, 2),
                "memory_freed_mb": round((mem_before - mem_after) / (1024 * 1024), 2),
                "rss_before_mb": round(mem_before / (1024 * 1024), 2),
                "rss_after_mb": round(mem_after / (1024 * 1024), 2)
            }

        @self.app.get("/api/debug/memory/leaks")
        async def detect_leaks():
            """
            Quick leak detection using various heuristics
            Endpoint: GET /api/debug/memory/leaks
            """
            if len(self.memory_history) < 10:
                return {"error": "Not enough history data. Try again after a few minutes"}

            # Calculate growth trends
            recent_samples = list(self.memory_history)[-10:]
            rss_values = [s['rss_mb'] for s in recent_samples]

            # Check if monotonically increasing
            is_monotonic = all(rss_values[i] <= rss_values[i+1] for i in range(len(rss_values)-1))

            # Calculate growth rate
            growth_mb = rss_values[-1] - rss_values[0]
            growth_rate = growth_mb / len(recent_samples)

            # Severity assessment
            if growth_rate > 10:
                severity = "CRITICAL"
            elif growth_rate > 5:
                severity = "HIGH"
            elif growth_rate > 1:
                severity = "MEDIUM"
            else:
                severity = "LOW" if growth_rate > 0 else "NONE"

            return {
                "timestamp": datetime.now().isoformat(),
                "analysis_period_samples": len(recent_samples),
                "initial_rss_mb": round(rss_values[0], 2),
                "final_rss_mb": round(rss_values[-1], 2),
                "total_growth_mb": round(growth_mb, 2),
                "growth_rate_mb_per_sample": round(growth_rate, 3),
                "is_monotonic_growth": is_monotonic,
                "severity": severity,
                "verdict": "LEAK SUSPECTED" if growth_rate > 1 and is_monotonic else "NO IMMEDIATE LEAK"
            }

        @self.app.get("/api/debug/memory/process-info")
        async def process_info():
            """
            Get detailed process memory information
            Endpoint: GET /api/debug/memory/process-info
            """
            mem = self.process.memory_info()
            with self.process.oneshot():
                cpu_percent = self.process.cpu_percent()
                memory_percent = self.process.memory_percent()
                num_threads = self.process.num_threads()
                num_fds = self.process.num_fds() if hasattr(self.process, 'num_fds') else None

            return {
                "timestamp": datetime.now().isoformat(),
                "pid": self.process.pid,
                "rss_mb": round(mem.rss / (1024 * 1024), 2),
                "vms_mb": round(mem.vms / (1024 * 1024), 2),
                "rss_percent": round(memory_percent, 2),
                "cpu_percent": round(cpu_percent, 2),
                "num_threads": num_threads,
                "num_fds": num_fds,
                "create_time": datetime.fromtimestamp(self.process.create_time()).isoformat()
            }


# ============================================================================
# INTEGRATION HELPER
# ============================================================================

def setup_memory_monitoring(app: FastAPI, port: int = 8001, enable_tracemalloc: bool = True):
    """
    Setup complete memory monitoring for a FastAPI app
    Usage in main.py:
        from fastapi_memory_monitor import setup_memory_monitoring

        app = FastAPI()
        setup_memory_monitoring(app, port=8001)
    """
    MemoryMonitoringEndpoints(app, enable_tracemalloc=enable_tracemalloc)

    return app


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example FastAPI app with memory monitoring enabled

    Run:
        python fastapi_memory_monitor.py

    Then:
        # Get current snapshot
        curl http://localhost:8000/api/debug/memory/snapshot

        # Get memory history
        curl http://localhost:8000/api/debug/memory/history

        # Detect leaks
        curl http://localhost:8000/api/debug/memory/leaks

        # Prometheus metrics
        curl http://localhost:8001/metrics
    """
    import uvicorn

    app = FastAPI()

    @app.get("/api/test")
    @memory_tracked
    async def test_endpoint():
        """Test endpoint with memory tracking"""
        await asyncio.sleep(0.1)
        return {"status": "ok"}

    # Setup memory monitoring
    setup_memory_monitoring(app, port=8001)

    print("Starting FastAPI app with memory monitoring...")
    print("Memory endpoints:")
    print("  GET  /api/debug/memory/snapshot     - Current memory state")
    print("  GET  /api/debug/memory/history      - Memory history")
    print("  GET  /api/debug/memory/growth       - Object type growth")
    print("  GET  /api/debug/memory/leaks        - Leak detection")
    print("  GET  /api/debug/memory/gc-stats     - GC statistics")
    print("  POST /api/debug/memory/gc-collect   - Trigger GC manually")
    print("Prometheus metrics: http://localhost:8001/metrics")

    uvicorn.run(app, host="0.0.0.0", port=8000)

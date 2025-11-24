#!/usr/bin/env python3
"""
Memory Leak Debugging Toolkit for Python/FastAPI
Complete set of diagnostic tools for production memory leak investigation
"""

import re
import sys
import time
import psutil
import asyncio
import gc
import tracemalloc
import json
from datetime import datetime, timedelta
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class MemoryLeakDetector:
    """
    Phase 1: Rapid leak detection and severity assessment
    """

    def __init__(self, baseline_duration_sec=60):
        self.baseline_duration = baseline_duration_sec
        self.measurements: List[Tuple[float, float]] = []  # (timestamp, rss_mb)
        self.process = psutil.Process()

    def detect(self, sample_interval_sec=10) -> Dict:
        """
        Quick leak detection: measure RSS growth over time.
        Returns: {is_leak: bool, growth_rate_mb_per_min: float, severity: str}
        """
        print(f"[{datetime.now().isoformat()}] Starting memory leak detection ({self.baseline_duration}s)")

        for i in range(self.baseline_duration // sample_interval_sec):
            rss_mb = self.process.memory_info().rss / (1024 * 1024)
            self.measurements.append((time.time(), rss_mb))
            print(f"  [{i*sample_interval_sec}s] RSS: {rss_mb:.1f}MB", end="\r")
            time.sleep(sample_interval_sec)

        # Analysis
        initial_rss = self.measurements[0][1]
        final_rss = self.measurements[-1][1]
        duration_min = self.baseline_duration / 60
        growth_mb = final_rss - initial_rss
        growth_rate = growth_mb / duration_min if duration_min > 0 else 0

        # Severity levels
        if growth_rate > 20:
            severity = "CRITICAL"
        elif growth_rate > 10:
            severity = "HIGH"
        elif growth_rate > 5:
            severity = "MEDIUM"
        elif growth_rate > 1:
            severity = "LOW"
        else:
            severity = "NONE"

        is_leak = growth_rate > 1  # >1MB/min is suspicious

        result = {
            "is_leak": is_leak,
            "initial_rss_mb": round(initial_rss, 2),
            "final_rss_mb": round(final_rss, 2),
            "total_growth_mb": round(growth_mb, 2),
            "growth_rate_mb_per_min": round(growth_rate, 2),
            "severity": severity,
            "duration_sec": self.baseline_duration,
        }

        self._print_detection_report(result)
        return result

    def _print_detection_report(self, result: Dict):
        print(f"\n{'='*60}")
        print(f"  MEMORY LEAK DETECTION REPORT")
        print(f"{'='*60}")
        print(f"  Initial RSS:        {result['initial_rss_mb']:.1f} MB")
        print(f"  Final RSS:          {result['final_rss_mb']:.1f} MB")
        print(f"  Total Growth:       {result['total_growth_mb']:.1f} MB")
        print(f"  Growth Rate:        {result['growth_rate_mb_per_min']:.2f} MB/min")
        print(f"  Duration:           {result['duration_sec']} seconds")
        print(f"  Verdict:            {'LEAK DETECTED' if result['is_leak'] else 'NO LEAK'}")
        print(f"  Severity:           {result['severity']}")
        print(f"{'='*60}\n")


class ObjectGrowthTracker:
    """
    Phase 2: Track which object types are accumulating
    """

    def __init__(self):
        self.baseline_counts: Dict[str, int] = {}
        self.snapshots: List[Dict] = []

    def take_snapshot(self) -> Dict:
        """Get current object type counts"""
        gc.collect()

        counts = defaultdict(int)
        for obj in gc.get_objects():
            obj_type = type(obj).__name__
            counts[obj_type] += 1

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "counts": dict(counts)
        }
        self.snapshots.append(snapshot)

        if not self.baseline_counts:
            self.baseline_counts = dict(counts)

        return snapshot

    def show_growth(self) -> Dict:
        """Show which object types have grown since baseline"""
        if not self.snapshots:
            self.take_snapshot()

        current = self.snapshots[-1]["counts"]
        growth = {}

        for obj_type, current_count in current.items():
            baseline_count = self.baseline_counts.get(obj_type, 0)
            delta = current_count - baseline_count

            if delta > 0:
                growth[obj_type] = {
                    "current": current_count,
                    "baseline": baseline_count,
                    "delta": delta,
                    "growth_pct": round((delta / baseline_count * 100) if baseline_count > 0 else 0, 1)
                }

        # Sort by delta descending
        sorted_growth = dict(sorted(growth.items(), key=lambda x: x[1]["delta"], reverse=True))

        self._print_growth_report(sorted_growth)
        return sorted_growth

    def _print_growth_report(self, growth: Dict):
        print(f"\n{'='*80}")
        print(f"  OBJECT GROWTH ANALYSIS")
        print(f"{'='*80}")
        print(f"  {'Type':<30} {'Current':>12} {'Baseline':>12} {'Delta':>10} {'Growth %':>10}")
        print(f"  {'-'*80}")

        for obj_type, stats in list(growth.items())[:20]:
            print(f"  {obj_type:<30} {stats['current']:>12} {stats['baseline']:>12} "
                  f"{stats['delta']:>10} {stats['growth_pct']:>9.1f}%")

        print(f"{'='*80}\n")


class LeakPatternMatcher:
    """
    Phase 3: Identify common memory leak patterns in code
    """

    PATTERNS = {
        'unbounded_cache': {
            'regex': r'(?<!\.)(?:cache|buffer|history|results|store|data)\[.+?\]\s*=\s*.+?(?!.*del\(|.*pop\(|.*clear\()',
            'severity': 'HIGH',
            'description': 'Dictionary/cache grows without cleanup',
            'fix': 'Add TTL (cachetools.TTLCache) or max size limit'
        },
        'global_accumulation': {
            'regex': r'^[A-Z_]+\s*=\s*\[\]|^[A-Z_]+\s*=\s*\{\}',
            'severity': 'HIGH',
            'description': 'Global list/dict accumulates data indefinitely',
            'fix': 'Use instance variables, reset periodically, or use collections.deque with maxlen'
        },
        'circular_reference': {
            'regex': r'self\.\w+\s*=\s*self|obj\.ref\s*=\s*obj',
            'severity': 'MEDIUM',
            'description': 'Object references itself (prevents garbage collection)',
            'fix': 'Use weakref.ref() or implement __del__'
        },
        'db_connection_leak': {
            'regex': r'\.connect\(\)|db\.session|Session\(\)(?!.*with|.*as\s|.*context)',
            'severity': 'HIGH',
            'description': 'Database connection not in context manager',
            'fix': 'Use `async with db.connect()` or `with Session()` context manager'
        },
        'event_listener_leak': {
            'regex': r'\.on\(|\.subscribe\(|addEventListener\((?!.*unsubscribe|.*off\(|.*removeListener)',
            'severity': 'HIGH',
            'description': 'Event listener/subscription never unsubscribed',
            'fix': 'Store handler ID, call unsubscribe/off in cleanup'
        },
        'thread_pool_leak': {
            'regex': r'ThreadPoolExecutor\(\)|ProcessPoolExecutor\(\)(?!.*with|.*as\s)',
            'severity': 'MEDIUM',
            'description': 'Thread/process pool not cleaned up',
            'fix': 'Use `with ThreadPoolExecutor() as executor:` or call .shutdown()'
        },
        'async_task_leak': {
            'regex': r'asyncio\.create_task\(|gather\(|ensure_future\((?!.*await)',
            'severity': 'MEDIUM',
            'description': 'Async task created but never awaited',
            'fix': 'Always await tasks or store handles for cancellation'
        },
        'file_handle_leak': {
            'regex': r'open\(|File\((?!.*with|.*as\s)',
            'severity': 'MEDIUM',
            'description': 'File not opened in context manager',
            'fix': 'Use `with open(...) as f:` context manager'
        },
    }

    @staticmethod
    def scan_files(directory: str) -> List[Dict]:
        """Scan Python files for memory leak patterns"""
        findings = []

        for py_file in Path(directory).rglob("*.py"):
            if any(skip in str(py_file) for skip in ['.venv', '__pycache__', '.git', 'node_modules']):
                continue

            try:
                with open(py_file) as f:
                    content = f.read()

                for pattern_name, pattern_info in LeakPatternMatcher.PATTERNS.items():
                    matches = list(re.finditer(pattern_info['regex'], content, re.MULTILINE))

                    for match in matches:
                        line_no = content[:match.start()].count('\n') + 1
                        line_text = content.split('\n')[line_no - 1].strip()

                        findings.append({
                            'file': str(py_file),
                            'line': line_no,
                            'pattern': pattern_name,
                            'severity': pattern_info['severity'],
                            'description': pattern_info['description'],
                            'fix': pattern_info['fix'],
                            'code': line_text[:100]
                        })
            except Exception as e:
                pass

        return findings

    @staticmethod
    def print_findings(findings: List[Dict]):
        """Print findings in readable format"""
        if not findings:
            print("✅ No obvious memory leak patterns found\n")
            return

        print(f"\n{'='*100}")
        print(f"  MEMORY LEAK PATTERN SCAN ({len(findings)} issues)")
        print(f"{'='*100}\n")

        # Group by severity
        by_severity = defaultdict(list)
        for finding in findings:
            by_severity[finding['severity']].append(finding)

        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity not in by_severity:
                continue

            severity_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🔵'}[severity]
            print(f"{severity_emoji} {severity} SEVERITY ({len(by_severity[severity])} issues)\n")

            for finding in by_severity[severity][:5]:
                print(f"  📍 {finding['file']}:{finding['line']}")
                print(f"     Pattern: {finding['pattern']}")
                print(f"     Issue: {finding['description']}")
                print(f"     Code: {finding['code']}")
                print(f"     Fix: {finding['fix']}\n")

        print(f"{'='*100}\n")


class LogMemoryAnalyzer:
    """
    Phase 4: Extract memory patterns from application logs
    """

    @staticmethod
    def parse_memory_logs(log_content: str) -> Dict:
        """Extract memory metrics from logs"""

        # Regex patterns
        rss_pattern = r'(?:RSS|memory):\s*(\d+(?:\.\d+)?)\s*(?:MB|m)'
        error_pattern = r'(?:ERROR|Exception|Traceback|FAILED).*?(?=\n)'
        gc_pattern = r'gc.*?(\d+)\s*(?:ms|milliseconds)'

        # Extract values
        rss_values = [float(m) for m in re.findall(rss_pattern, log_content, re.IGNORECASE)]
        errors = re.findall(error_pattern, log_content, re.IGNORECASE)
        gc_times = [int(m) for m in re.findall(gc_pattern, log_content, re.IGNORECASE)]

        # Analysis
        result = {
            "total_measurements": len(rss_values),
            "initial_rss_mb": rss_values[0] if rss_values else 0,
            "final_rss_mb": rss_values[-1] if rss_values else 0,
            "max_rss_mb": max(rss_values) if rss_values else 0,
            "min_rss_mb": min(rss_values) if rss_values else 0,
            "growth_mb": (rss_values[-1] - rss_values[0]) if rss_values else 0,
            "is_monotonic": LogMemoryAnalyzer._is_monotonic(rss_values),
            "error_count": len(errors),
            "gc_times_ms": gc_times,
            "gc_slowdown": LogMemoryAnalyzer._check_gc_slowdown(gc_times),
        }

        return result

    @staticmethod
    def _is_monotonic(values: List[float]) -> bool:
        """Check if values only increase (no decrease = leak indicator)"""
        if len(values) < 2:
            return False
        return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

    @staticmethod
    def _check_gc_slowdown(gc_times: List[int]) -> bool:
        """Check if GC is getting slower (more objects = slower GC)"""
        if len(gc_times) < 2:
            return False
        return gc_times[-1] > gc_times[0] * 1.5  # 50% slower = slowdown


class MemoryDashboard:
    """Real-time memory metrics dashboard"""

    def __init__(self, check_interval_sec=5, duration_sec=300):
        self.check_interval = check_interval_sec
        self.duration = duration_sec
        self.process = psutil.Process()
        self.metrics = deque(maxlen=duration_sec // check_interval_sec)

    def run(self):
        """Run continuous memory monitoring"""
        print(f"Memory Dashboard (updating every {self.check_interval}s for {self.duration}s)")
        print(f"{'Time':<20} {'RSS MB':>12} {'VMS MB':>12} {'% Memory':>12} {'# Threads':>10}")
        print(f"{'-'*66}")

        start_time = time.time()
        start_rss = self.process.memory_info().rss

        while time.time() - start_time < self.duration:
            try:
                mem = self.process.memory_info()
                with self.process.oneshot():
                    percent = self.process.memory_percent()
                    num_threads = self.process.num_threads()

                rss_mb = mem.rss / (1024 * 1024)
                vms_mb = mem.vms / (1024 * 1024)
                growth = (mem.rss - start_rss) / (1024 * 1024)

                timestamp = datetime.now().strftime("%H:%M:%S")
                self.metrics.append({
                    'rss_mb': rss_mb,
                    'growth': growth,
                    'timestamp': timestamp
                })

                growth_indicator = f"(+{growth:.1f})" if growth > 0 else f"({growth:.1f})"
                print(f"{timestamp:<20} {rss_mb:>12.1f} {vms_mb:>12.1f} {percent:>11.1f}% {num_threads:>10}")

                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

        self._print_summary()

    def _print_summary(self):
        if not self.metrics:
            return

        rss_values = [m['rss_mb'] for m in self.metrics]
        growth_values = [m['growth'] for m in self.metrics]

        print(f"\n{'='*66}")
        print(f"  SUMMARY")
        print(f"{'='*66}")
        print(f"  Min RSS:    {min(rss_values):.1f} MB")
        print(f"  Max RSS:    {max(rss_values):.1f} MB")
        print(f"  Final RSS:  {rss_values[-1]:.1f} MB")
        print(f"  Total growth: {max(growth_values):.1f} MB")
        print(f"  Avg growth per sample: {sum(growth_values)/len(growth_values):.2f} MB")
        print(f"{'='*66}\n")


def print_usage():
    """Print usage information"""
    print("""
Memory Leak Debugging Toolkit

USAGE:
  python memory_debug_toolkit.py [COMMAND] [OPTIONS]

COMMANDS:

  detect [duration_sec] [interval_sec]
    Quick leak detection - measure RSS growth over time
    Example: python memory_debug_toolkit.py detect 300 10

  track-objects
    Show which object types are growing (requires running app)

  scan-code [directory]
    Pattern match for common memory leak code patterns
    Example: python memory_debug_toolkit.py scan-code ./app

  analyze-logs [log_file]
    Extract memory patterns from application logs
    Example: python memory_debug_toolkit.py analyze-logs app.log

  dashboard [duration_sec] [interval_sec]
    Real-time memory monitoring dashboard
    Example: python memory_debug_toolkit.py dashboard 300 5

EXAMPLES:
  # Quick leak confirmation (5 min monitoring)
  python memory_debug_toolkit.py detect 300 10

  # Scan codebase for leak patterns
  python memory_debug_toolkit.py scan-code app/

  # Analyze production logs
  python memory_debug_toolkit.py analyze-logs /var/log/app.log

  # Live monitoring dashboard
  python memory_debug_toolkit.py dashboard 600 5
""")


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "detect":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        detector = MemoryLeakDetector(baseline_duration_sec=duration)
        detector.detect(sample_interval_sec=interval)

    elif command == "track-objects":
        tracker = ObjectGrowthTracker()
        tracker.take_snapshot()
        time.sleep(10)
        tracker.show_growth()

    elif command == "scan-code":
        directory = sys.argv[2] if len(sys.argv) > 2 else "."
        findings = LeakPatternMatcher.scan_files(directory)
        LeakPatternMatcher.print_findings(findings)

    elif command == "analyze-logs":
        log_file = sys.argv[2]
        with open(log_file) as f:
            content = f.read()
        analyzer = LogMemoryAnalyzer()
        result = analyzer.parse_memory_logs(content)
        print(json.dumps(result, indent=2))

    elif command == "dashboard":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        interval = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        dashboard = MemoryDashboard(check_interval_sec=interval, duration_sec=duration)
        dashboard.run()

    else:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()

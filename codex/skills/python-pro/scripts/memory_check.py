#!/usr/bin/env python3
"""
Check memory usage of a Python function or module.

Usage:
    python scripts/memory_check.py <module_path> <function_name> [--args JSON]

Examples:
    # Check memory of feature builder
    python scripts/memory_check.py app.ml.feature_builder build_all_features --args '{"n_campaigns": 1000}'

    # Check memory of data loader
    python scripts/memory_check.py app.data.loader load_campaigns

    # Check ChromaDB query memory
    python scripts/memory_check.py app.memory.chroma query_patterns --args '{"query": "test"}'

Requirements:
    pip install psutil
"""

import argparse
import sys
import json
import asyncio
import importlib
import time
import gc
from pathlib import Path

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def get_memory_mb() -> float:
    """Get current process memory usage in MB."""
    if HAS_PSUTIL:
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    else:
        # Fallback: less accurate but works without psutil
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # macOS returns KB


def format_memory(mb: float) -> str:
    """Format memory with appropriate units."""
    if mb < 1:
        return f"{mb * 1024:.1f} KB"
    elif mb < 1024:
        return f"{mb:.1f} MB"
    else:
        return f"{mb / 1024:.2f} GB"


def import_function(module_path: str, function_name: str):
    """Import a function from a module path."""
    try:
        sys.path.insert(0, str(Path.cwd()))
        sys.path.insert(0, str(Path.cwd() / "backend"))

        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        return func
    except ImportError as e:
        print(f"Error importing {module_path}: {e}")
        sys.exit(1)
    except AttributeError:
        print(f"Function '{function_name}' not found in {module_path}")
        sys.exit(1)


def measure_memory(func, kwargs: dict, is_async: bool) -> dict:
    """Measure memory before, during, and after function execution."""

    # Force garbage collection before measuring
    gc.collect()
    gc.collect()

    mem_before = get_memory_mb()

    # Run function
    start_time = time.perf_counter()
    try:
        if is_async:
            result = asyncio.run(func(**kwargs))
        else:
            result = func(**kwargs)
        success = True
        error = None
    except Exception as e:
        result = None
        success = False
        error = str(e)

    elapsed = time.perf_counter() - start_time

    # Measure after execution (before cleanup)
    mem_after = get_memory_mb()

    # Force cleanup and measure again
    del result
    gc.collect()
    gc.collect()

    mem_final = get_memory_mb()

    return {
        'mem_before': mem_before,
        'mem_after': mem_after,
        'mem_final': mem_final,
        'mem_peak': mem_after,  # Approximation
        'mem_retained': mem_final - mem_before,
        'mem_used': mem_after - mem_before,
        'elapsed': elapsed,
        'success': success,
        'error': error
    }


def print_report(stats: dict, module_path: str, function_name: str, kwargs: dict):
    """Print memory usage report."""

    print(f"\n{'='*60}")
    print("MEMORY USAGE REPORT")
    print(f"{'='*60}")

    print(f"\nFunction: {module_path}.{function_name}")
    print(f"Arguments: {kwargs}")
    print(f"Status: {'SUCCESS' if stats['success'] else 'FAILED - ' + stats['error']}")

    print(f"\n{'─'*60}")
    print("MEMORY MEASUREMENTS")
    print(f"{'─'*60}")

    print(f"\n  Before execution:  {format_memory(stats['mem_before']):>12}")
    print(f"  After execution:   {format_memory(stats['mem_after']):>12}")
    print(f"  After cleanup:     {format_memory(stats['mem_final']):>12}")

    print(f"\n{'─'*60}")
    print("ANALYSIS")
    print(f"{'─'*60}")

    mem_used = stats['mem_used']
    mem_retained = stats['mem_retained']

    print(f"\n  Memory used during execution: {format_memory(mem_used):>12}")
    print(f"  Memory retained after GC:     {format_memory(mem_retained):>12}")
    print(f"  Execution time:               {stats['elapsed']*1000:.2f} ms")

    # Warnings
    print(f"\n{'─'*60}")
    print("RECOMMENDATIONS")
    print(f"{'─'*60}\n")

    if mem_used > 500:
        print(f"  [WARNING] High memory usage ({format_memory(mem_used)})")
        print("  Consider using generators or chunked processing")

    if mem_retained > 50:
        print(f"  [WARNING] Memory not fully released ({format_memory(mem_retained)})")
        print("  Check for global caches, circular references, or leaked resources")

    if mem_used > 100 and stats['elapsed'] < 0.1:
        print("  [INFO] High memory, fast execution")
        print("  Consider memory-time tradeoff if memory is constrained")

    if mem_used < 50 and stats['elapsed'] > 1:
        print("  [INFO] Low memory, slow execution")
        print("  Performance may be I/O or CPU bound, not memory")

    if mem_used < 50 and mem_retained < 10:
        print("  [OK] Memory usage looks healthy")


def main():
    parser = argparse.ArgumentParser(
        description="Check memory usage of a Python function",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'module_path',
        help='Module path (e.g., app.ml.feature_builder)'
    )
    parser.add_argument(
        'function_name',
        help='Function name to check'
    )
    parser.add_argument(
        '--args',
        type=str,
        default='{}',
        help='JSON string of keyword arguments'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=1,
        help='Number of runs to average (default: 1)'
    )

    args = parser.parse_args()

    if not HAS_PSUTIL:
        print("Warning: psutil not installed. Using fallback memory measurement.")
        print("For accurate results: pip install psutil\n")

    # Parse function arguments
    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON for --args: {e}")
        sys.exit(1)

    # Import function
    func = import_function(args.module_path, args.function_name)
    is_async = asyncio.iscoroutinefunction(func)

    if is_async:
        print("(Async function detected)")

    # Run measurement
    if args.runs == 1:
        stats = measure_memory(func, kwargs, is_async)
        print_report(stats, args.module_path, args.function_name, kwargs)
    else:
        # Multiple runs - average
        all_stats = []
        print(f"Running {args.runs} measurements...")

        for i in range(args.runs):
            gc.collect()
            stats = measure_memory(func, kwargs, is_async)
            all_stats.append(stats)
            print(f"  Run {i+1}: {format_memory(stats['mem_used'])} used, {stats['elapsed']*1000:.1f}ms")

        # Average
        avg_stats = {
            'mem_before': sum(s['mem_before'] for s in all_stats) / len(all_stats),
            'mem_after': sum(s['mem_after'] for s in all_stats) / len(all_stats),
            'mem_final': sum(s['mem_final'] for s in all_stats) / len(all_stats),
            'mem_used': sum(s['mem_used'] for s in all_stats) / len(all_stats),
            'mem_retained': sum(s['mem_retained'] for s in all_stats) / len(all_stats),
            'elapsed': sum(s['elapsed'] for s in all_stats) / len(all_stats),
            'success': all(s['success'] for s in all_stats),
            'error': next((s['error'] for s in all_stats if s['error']), None)
        }

        print_report(avg_stats, args.module_path, args.function_name, kwargs)
        print(f"\n  (Averaged over {args.runs} runs)")


if __name__ == '__main__':
    main()

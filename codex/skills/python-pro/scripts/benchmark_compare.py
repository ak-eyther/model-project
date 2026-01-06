#!/usr/bin/env python3
"""
Benchmark and compare two function implementations.

Usage:
    python scripts/benchmark_compare.py <module1:func1> <module2:func2> [--args JSON] [--runs N]

Examples:
    # Compare sync vs async implementation
    python scripts/benchmark_compare.py app.tools.sync_analyzer:analyze app.tools.async_analyzer:analyze_async --args '{"offer_id": "test"}' --runs 5

    # Compare two feature builders
    python scripts/benchmark_compare.py app.ml.v1:build_features app.ml.v2:build_features_optimized --runs 10

    # Compare with sample data
    python scripts/benchmark_compare.py app.utils:method_a app.utils:method_b --args '{"data": [1,2,3,4,5]}' --runs 20
"""

import argparse
import sys
import json
import asyncio
import importlib
import time
from statistics import mean, stdev, median
from pathlib import Path
from typing import Callable, List, Tuple


def import_function(spec: str) -> Tuple[str, Callable]:
    """Import a function from module:function spec."""
    try:
        module_path, function_name = spec.rsplit(':', 1)
    except ValueError:
        print(f"Invalid spec '{spec}'. Use format: module.path:function_name")
        sys.exit(1)

    try:
        sys.path.insert(0, str(Path.cwd()))
        sys.path.insert(0, str(Path.cwd() / "backend"))

        module = importlib.import_module(module_path)
        func = getattr(module, function_name)
        return spec, func
    except ImportError as e:
        print(f"Error importing {module_path}: {e}")
        sys.exit(1)
    except AttributeError:
        print(f"Function '{function_name}' not found in {module_path}")
        sys.exit(1)


def run_benchmark(func: Callable, kwargs: dict, runs: int, is_async: bool) -> List[float]:
    """Run benchmark and return list of execution times."""
    times = []

    for i in range(runs):
        start = time.perf_counter()
        try:
            if is_async:
                asyncio.run(func(**kwargs))
            else:
                func(**kwargs)
        except Exception as e:
            print(f"  Run {i+1}: ERROR - {e}")
            continue

        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return times


def format_time(seconds: float) -> str:
    """Format time with appropriate units."""
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f}us"
    elif seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    else:
        return f"{seconds:.3f}s"


def print_stats(name: str, times: List[float]):
    """Print statistics for benchmark results."""
    if not times:
        print(f"  {name}: No successful runs")
        return

    avg = mean(times)
    std = stdev(times) if len(times) > 1 else 0
    med = median(times)
    mn = min(times)
    mx = max(times)

    print(f"\n  {name}")
    print(f"  {'─'*50}")
    print(f"  Mean:   {format_time(avg):>12}  (±{format_time(std)})")
    print(f"  Median: {format_time(med):>12}")
    print(f"  Min:    {format_time(mn):>12}")
    print(f"  Max:    {format_time(mx):>12}")
    print(f"  Runs:   {len(times):>12}")


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark and compare two function implementations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'func1',
        help='First function (module.path:function_name)'
    )
    parser.add_argument(
        'func2',
        help='Second function (module.path:function_name)'
    )
    parser.add_argument(
        '--args',
        type=str,
        default='{}',
        help='JSON string of keyword arguments for both functions'
    )
    parser.add_argument(
        '--runs',
        type=int,
        default=10,
        help='Number of runs per function (default: 10)'
    )
    parser.add_argument(
        '--warmup',
        type=int,
        default=1,
        help='Warmup runs before benchmarking (default: 1)'
    )

    args = parser.parse_args()

    # Parse function arguments
    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON for --args: {e}")
        sys.exit(1)

    # Import functions
    name1, func1 = import_function(args.func1)
    name2, func2 = import_function(args.func2)

    is_async1 = asyncio.iscoroutinefunction(func1)
    is_async2 = asyncio.iscoroutinefunction(func2)

    print(f"\n{'='*60}")
    print("BENCHMARK COMPARISON")
    print(f"{'='*60}")
    print(f"\nFunction 1: {name1} {'(async)' if is_async1 else '(sync)'}")
    print(f"Function 2: {name2} {'(async)' if is_async2 else '(sync)'}")
    print(f"Arguments:  {kwargs}")
    print(f"Runs:       {args.runs} (+ {args.warmup} warmup)")

    # Warmup
    if args.warmup > 0:
        print(f"\nWarming up...")
        run_benchmark(func1, kwargs, args.warmup, is_async1)
        run_benchmark(func2, kwargs, args.warmup, is_async2)

    # Run benchmarks
    print(f"\nRunning benchmarks...")
    times1 = run_benchmark(func1, kwargs, args.runs, is_async1)
    times2 = run_benchmark(func2, kwargs, args.runs, is_async2)

    # Print results
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")

    print_stats(name1, times1)
    print_stats(name2, times2)

    # Comparison
    if times1 and times2:
        avg1 = mean(times1)
        avg2 = mean(times2)

        print(f"\n{'='*60}")
        print("COMPARISON")
        print(f"{'='*60}")

        if avg1 < avg2:
            speedup = avg2 / avg1
            winner = name1
            loser = name2
        else:
            speedup = avg1 / avg2
            winner = name2
            loser = name1

        print(f"\n  Winner: {winner}")
        print(f"  Speedup: {speedup:.2f}x faster than {loser}")

        diff_ms = abs(avg1 - avg2) * 1000
        print(f"  Difference: {diff_ms:.2f}ms per call")

        if args.runs >= 5:
            # Calculate calls per second
            calls_per_sec1 = 1 / avg1 if avg1 > 0 else 0
            calls_per_sec2 = 1 / avg2 if avg2 > 0 else 0
            print(f"\n  Throughput:")
            print(f"    {name1}: {calls_per_sec1:.1f} calls/sec")
            print(f"    {name2}: {calls_per_sec2:.1f} calls/sec")


if __name__ == '__main__':
    main()

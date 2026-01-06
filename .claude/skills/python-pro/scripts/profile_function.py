#!/usr/bin/env python3
"""
Profile a Python function and identify bottlenecks.

Usage:
    python scripts/profile_function.py <module_path> <function_name> [--args JSON]

Examples:
    # Profile a simple function
    python scripts/profile_function.py app.ml.feature_builder build_features

    # Profile with arguments
    python scripts/profile_function.py app.tools.offer_analyzer analyze --args '{"offer_id": "offer_123"}'

    # Profile async function
    python scripts/profile_function.py app.agents.analyst gather_evidence_async --args '{"candidate": {"list_id": "GM_30D"}}'
"""

import argparse
import cProfile
import pstats
import sys
import json
import asyncio
import importlib
import time
from io import StringIO
from pathlib import Path


def import_function(module_path: str, function_name: str):
    """Import a function from a module path."""
    try:
        # Add current directory to path
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


def profile_sync(func, args: dict, kwargs: dict):
    """Profile a synchronous function."""
    profiler = cProfile.Profile()
    profiler.enable()

    start = time.perf_counter()
    try:
        result = func(*args.get('args', []), **kwargs)
    except Exception as e:
        profiler.disable()
        print(f"Function raised exception: {e}")
        return None, profiler

    elapsed = time.perf_counter() - start
    profiler.disable()

    print(f"\n{'='*60}")
    print(f"EXECUTION TIME: {elapsed:.4f}s")
    print(f"{'='*60}\n")

    return result, profiler


def profile_async(func, args: dict, kwargs: dict):
    """Profile an async function."""
    profiler = cProfile.Profile()
    profiler.enable()

    start = time.perf_counter()
    try:
        result = asyncio.run(func(*args.get('args', []), **kwargs))
    except Exception as e:
        profiler.disable()
        print(f"Function raised exception: {e}")
        return None, profiler

    elapsed = time.perf_counter() - start
    profiler.disable()

    print(f"\n{'='*60}")
    print(f"EXECUTION TIME: {elapsed:.4f}s")
    print(f"{'='*60}\n")

    return result, profiler


def print_stats(profiler: cProfile.Profile, top_n: int = 20):
    """Print profiling statistics."""
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)

    print(f"\n{'='*60}")
    print(f"TOP {top_n} FUNCTIONS BY CUMULATIVE TIME")
    print(f"{'='*60}\n")

    stats.sort_stats('cumulative')
    stats.print_stats(top_n)
    print(stream.getvalue())

    # Also show callers for the slowest function
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')

    print(f"\n{'='*60}")
    print("CALL HIERARCHY (who called the slowest functions)")
    print(f"{'='*60}\n")

    stats.print_callers(5)
    print(stream.getvalue())


def main():
    parser = argparse.ArgumentParser(
        description="Profile a Python function and identify bottlenecks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'module_path',
        help='Module path (e.g., app.ml.feature_builder)'
    )
    parser.add_argument(
        'function_name',
        help='Function name to profile'
    )
    parser.add_argument(
        '--args',
        type=str,
        default='{}',
        help='JSON string of keyword arguments'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=20,
        help='Number of top functions to show (default: 20)'
    )

    args = parser.parse_args()

    # Parse function arguments
    try:
        kwargs = json.loads(args.args)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON for --args: {e}")
        sys.exit(1)

    # Import the function
    func = import_function(args.module_path, args.function_name)

    print(f"\nProfiling: {args.module_path}.{args.function_name}")
    print(f"Arguments: {kwargs}")

    # Check if async
    if asyncio.iscoroutinefunction(func):
        print("(Async function detected)")
        result, profiler = profile_async(func, {}, kwargs)
    else:
        result, profiler = profile_sync(func, {}, kwargs)

    # Print statistics
    print_stats(profiler, args.top)

    # Print result summary
    if result is not None:
        print(f"\n{'='*60}")
        print("RESULT SUMMARY")
        print(f"{'='*60}")
        if isinstance(result, dict):
            print(f"Returned dict with keys: {list(result.keys())}")
        elif isinstance(result, (list, tuple)):
            print(f"Returned {type(result).__name__} with {len(result)} items")
        else:
            print(f"Returned: {type(result).__name__}")


if __name__ == '__main__':
    main()

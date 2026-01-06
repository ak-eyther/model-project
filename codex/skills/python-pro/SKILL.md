---
name: python-pro
description: Write idiomatic Python code with advanced features like decorators, generators, and async/await. Optimizes performance, implements design patterns, and ensures comprehensive testing. Use for ML training, analytics tools, performance profiling, or any Python heavy lifting.
metadata:
  short-description: Advanced Python patterns
---

# Python Pro - Advanced Python Patterns

## When to Use This Skill

**Invoke python-pro for:**
- Model training/evaluation (e.g., `ml/train_models.py`)
- Analytics tool optimization (async batching, caching)
- Performance profiling (bottleneck identification)
- Advanced Python patterns (decorators, generators, context managers)
- Heavy data processing on large datasets
- Executing ML designs from @ml-owner

**Use fastapi-production-patterns instead for:**
- API endpoints, routing, middleware
- Pydantic validation, request/response models
- CORS configuration, authentication middleware
- FastAPI-specific patterns (dependency injection at API layer)

**Clear Boundary:**
| fastapi-production-patterns | python-pro |
|-----------------------------|------------|
| API layer (HTTP, routing) | Business logic (ML, analytics) |
| Pydantic, middleware, CORS | Decorators, generators, profiling |
| FastAPI endpoints | Core Python optimization |

---

## Executable Scripts

Run these scripts directly for profiling and debugging:

### Profile a Function
```bash
python scripts/profile_function.py <module.path> <function_name>
python scripts/profile_function.py <module.path> <function_name> --args '{"key": "value"}'
```

### Compare Two Implementations
```bash
python scripts/benchmark_compare.py <module_a:func> <module_b:func> --runs 10
```

### Check Memory Usage
```bash
python scripts/memory_check.py <module.path> <function_name> --args '{"n_rows": 1000}'
```

---

## Project ML System (Fill In)

Use `references/project_ml.md` for ML-specific documentation:
- Model locations (fill in)
- Training commands (fill in)
- Feature list (fill in)
- How predictions are served (fill in)
- Database tables used for training (fill in)

---

## Core Patterns and Examples

Use `references/patterns.md` for detailed code patterns and examples across:
- Decorators (caching, timing, retries, validation)
- Generators (lazy feature building, chunking, async generators)
- Async/concurrency (batching, sync-to-async, semaphores)
- Profiling (cProfile, line_profiler, memory_profiler, benchmarking)
- Type hints and static analysis (TypedDict, Protocol, Generic, mypy/ruff/black)
- Testing (fixtures, parametrization, async tests, mocking)
- Design patterns (strategy/factory for ML and tool creation)
- Quick reference cheat sheet

---

## Usage Guidance

- Prefer clear, typed interfaces for analytics and ML modules.
- Favor async batching when tool calls are independent.
- Profile before optimizing; keep hotspots visible.

## Scripts
- `scripts/skill_info.py`: Print skill name and description.

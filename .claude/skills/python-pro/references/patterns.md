# Reference: Python Pro Patterns and Examples

## Table of Contents
- 1. Decorators
- 2. Generators
- 3. Async/Await and Concurrent Programming
- 4. Performance Profiling
- 5. Type Hints and Static Analysis
- 6. Testing with pytest
- 7. Design Patterns
- Quick Reference

## 1. Decorators

### Caching with @lru_cache

```python
from functools import lru_cache
from typing import Dict, Any

@lru_cache(maxsize=128)
def get_offer_epc_mean(offer_id: str) -> float:
    """Cache expensive database queries for offer metrics.

    Use Case: Analytics tools query same offers repeatedly.
    Impact: 100ms → 1ms for cached hits.
    """
    # Expensive database/ChromaDB query
    return db.query_offer_metrics(offer_id)['epc_mean']

# Clear cache when data updates
get_offer_epc_mean.cache_clear()
```

### Timing Decorator

```python
import time
import functools
from typing import Callable, Any

def timeit(func: Callable) -> Callable:
    """Measure function execution time.

    Use Case: Profile analytics tools, ML training steps.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timeit
def train_catboost_model(X, y):
    model = CatBoostRegressor(**CATBOOST_PARAMS)
    model.fit(X, y)
    return model
# Output: train_catboost_model took 45.3201s
```

### Retry Decorator with Exponential Backoff

```python
import functools
import time
from typing import Callable, Type, Tuple

def retry(
    max_attempts: int = 3,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    backoff_factor: float = 2.0
) -> Callable:
    """Retry failed operations with exponential backoff.

    Use Case: ChromaDB queries, LLM API calls, database operations.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        print(f"Retry {attempt + 1}/{max_attempts} after {sleep_time}s: {e}")
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, exceptions=(ConnectionError, TimeoutError))
def query_chromadb(collection: str, query: str):
    return chroma_client.query(collection, query)
```

### Custom Decorator with Arguments

```python
import functools
from typing import Callable

def validate_campaign(required_fields: list[str]) -> Callable:
    """Validate campaign data before processing.

    Use Case: Ensure campaign has required fields before analytics.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(campaign: dict, *args, **kwargs):
            missing = [f for f in required_fields if f not in campaign]
            if missing:
                raise ValueError(f"Missing required fields: {missing}")
            return func(campaign, *args, **kwargs)
        return wrapper
    return decorator

@validate_campaign(required_fields=['list_id', 'offer_id', 'subject_line'])
def score_campaign(campaign: dict) -> float:
    # Safe to use campaign['list_id'], etc.
    pass
```

---

## 2. Generators

### Memory-Efficient Feature Building

```python
from typing import Iterator, Dict
import pandas as pd

def build_features_lazy(campaigns_df: pd.DataFrame) -> Iterator[Dict]:
    """Generate features lazily for 5,940 campaigns.

    Memory: 10MB (generator) vs 150MB (list comprehension)
    Use Case: CatBoost training Week 1 Days 3-5.
    """
    for idx, campaign in campaigns_df.iterrows():
        features = {
            'list_or_mean': get_list_or_mean(campaign['list_id']),
            'list_ctr_mean': get_list_ctr_mean(campaign['list_id']),
            'offer_epc_mean': get_offer_epc_mean(campaign['offer_id']),
            'offer_or_std': get_offer_or_std(campaign['offer_id']),
            'subject_word_count': len(campaign['subject_line'].split()),
            'subject_has_emoji': has_emoji(campaign['subject_line']),
            'day_of_week': campaign['send_date'].dayofweek,
            'hour_of_day': campaign['send_date'].hour,
            # ... 42 more features
        }
        yield features

# Usage: Process one at a time (memory efficient)
for features in build_features_lazy(campaigns_df):
    X.append(features)
```

### Generator Expression vs List Comprehension

```python
# BAD: Loads all 5,940 campaigns into memory at once
all_scores = [score_campaign(c) for c in campaigns]  # 150MB

# GOOD: Processes one at a time
score_generator = (score_campaign(c) for c in campaigns)  # ~1MB
for score in score_generator:
    process_score(score)
```

### Chunked Processing

```python
from typing import Iterator, List, TypeVar

T = TypeVar('T')

def chunked(iterable: Iterator[T], size: int) -> Iterator[List[T]]:
    """Process large datasets in chunks.

    Use Case: Batch ChromaDB inserts, parallel processing.
    """
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) >= size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

# Insert campaigns in batches of 100
for batch in chunked(campaigns, 100):
    chromadb_collection.add(
        ids=[c['id'] for c in batch],
        documents=[c['text'] for c in batch]
    )
```

### Async Generator

```python
from typing import AsyncIterator

async def fetch_campaigns_async(campaign_ids: list[str]) -> AsyncIterator[dict]:
    """Fetch campaigns asynchronously with streaming.

    Use Case: Large dataset retrieval without blocking.
    """
    async with aiohttp.ClientSession() as session:
        for cid in campaign_ids:
            async with session.get(f"/api/campaigns/{cid}") as resp:
                yield await resp.json()

# Usage
async for campaign in fetch_campaigns_async(campaign_ids):
    process_campaign(campaign)
```

---

## 3. Async/Await & Concurrent Programming

### Async Batching for Analytics (4x Speedup)

```python
import asyncio
from typing import Dict, Any

async def gather_analytics_evidence_async(candidate: dict) -> Dict[str, Any]:
    """Gather analytics evidence with async batching.

    Performance: 3000ms (sequential) → 750ms (async batches) = 4x speedup
    Use Case: Analyst Agent scoring candidates.
    """
    # Batch 1: Independent tools (run in parallel)
    batch_1_results = await asyncio.gather(
        offer_analyzer.analyze_async(candidate['offer_id']),
        subject_analyzer.analyze_async(candidate['subject_line']),
        deliverability_checker.check_async(candidate['list_id'])
    )
    offer_perf, subject_perf, deliverability = batch_1_results

    # Batch 2: Tools that can run in parallel
    batch_2_results = await asyncio.gather(
        pattern_tools.find_async(candidate['list_id']),
        combo_tools.analyze_async(candidate['list_id'], candidate['offer_id']),
        list_recommender.recommend_async(candidate['offer_id'])
    )
    patterns, synergy, alt_lists = batch_2_results

    # Batch 3: Final tools
    batch_3_results = await asyncio.gather(
        creative_matcher.top_async(candidate['offer_id']),
        predictor.predict_async(candidate)
    )
    creatives, prediction = batch_3_results

    return {
        'offer_performance': offer_perf,
        'subject_performance': subject_perf,
        'deliverability': deliverability,
        'patterns': patterns,
        'synergy': synergy,
        'alternative_lists': alt_lists,
        'top_creatives': creatives,
        'prediction': prediction
    }
```

### Converting Sync to Async

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Sync function (can't be changed)
def sync_heavy_computation(data: dict) -> dict:
    # CPU-bound operation
    return process_data(data)

# Wrap in async
async def async_heavy_computation(data: dict) -> dict:
    """Run sync function in thread pool without blocking event loop."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(
            executor,
            sync_heavy_computation,
            data
        )
```

### Async Context Manager

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def chromadb_session() -> AsyncIterator:
    """Manage ChromaDB connection lifecycle.

    Use Case: Ensure proper cleanup of resources.
    """
    client = await chromadb.AsyncClient()
    try:
        yield client
    finally:
        await client.close()

# Usage
async with chromadb_session() as client:
    results = await client.query(collection, query_text)
```

### Semaphore for Rate Limiting

```python
import asyncio

async def rate_limited_api_calls(items: list, max_concurrent: int = 5):
    """Limit concurrent API calls to avoid overwhelming services.

    Use Case: LLM API calls, external service queries.
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_call(item):
        async with semaphore:
            return await api_call(item)

    return await asyncio.gather(*[limited_call(item) for item in items])
```

---

## 4. Performance Profiling

### cProfile for Function-Level Analysis

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    """Profile a function and print top 20 slowest calls.

    Use Case: Identify bottlenecks in Analyst Agent.
    """
    profiler = cProfile.Profile()
    profiler.enable()

    result = func(*args, **kwargs)

    profiler.disable()

    # Format output
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')
    stats.print_stats(20)

    print(stream.getvalue())
    return result

# Usage
profile_function(agent.score_candidate, candidate)
# Output shows: _gather_analytics_evidence takes 2.8s (bottleneck!)
```

### line_profiler for Line-by-Line Timing

```python
# Install: pip install line_profiler

# Add @profile decorator (provided by line_profiler)
@profile
def train_catboost_model(X: pd.DataFrame, y: pd.Series):
    """Train model with line-by-line profiling."""
    model = CatBoostRegressor(
        iterations=500,
        depth=6,
        learning_rate=0.05
    )
    model.fit(X, y, verbose=100)  # Which line is slowest?
    return model

# Run with: kernprof -l -v train_models.py
# Output:
# Line #    Hits   Time    Per Hit  % Time  Line Contents
#     10       1    45.3s    45.3s   99.8%  model.fit(X, y)
```

### memory_profiler for Memory Usage

```python
# Install: pip install memory_profiler

from memory_profiler import profile

@profile
def build_all_features(campaigns_df: pd.DataFrame) -> pd.DataFrame:
    """Profile memory usage during feature building.

    Use Case: Ensure feature engineering doesn't OOM.
    """
    features = []
    for idx, campaign in campaigns_df.iterrows():
        features.append(compute_features(campaign))
    return pd.DataFrame(features)

# Run with: python -m memory_profiler feature_builder.py
# Output:
# Line #    Mem usage    Increment  Line Contents
#     15     50.0 MiB    50.0 MiB   features = []
#     17    200.0 MiB   150.0 MiB   features.append(...)  # Memory spike!
```

### Simple Benchmarking

```python
import time
from typing import Callable, Any
from statistics import mean, stdev

def benchmark(func: Callable, *args, runs: int = 10, **kwargs) -> dict:
    """Run function multiple times and report statistics.

    Use Case: Compare async vs sync, measure optimization impact.
    """
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args, **kwargs)
        times.append(time.perf_counter() - start)

    return {
        'mean': mean(times),
        'std': stdev(times) if len(times) > 1 else 0,
        'min': min(times),
        'max': max(times),
        'runs': runs
    }

# Compare implementations
sync_stats = benchmark(gather_analytics_sync, candidate)
async_stats = benchmark(lambda c: asyncio.run(gather_analytics_async(c)), candidate)

print(f"Sync: {sync_stats['mean']:.3f}s ± {sync_stats['std']:.3f}s")
print(f"Async: {async_stats['mean']:.3f}s ± {async_stats['std']:.3f}s")
# Sync: 3.012s ± 0.145s
# Async: 0.753s ± 0.082s → 4x faster!
```

---

## 5. Type Hints & Static Analysis

### TypedDict for Structured Data

```python
from typing import TypedDict, Literal, Optional

class CampaignMetrics(TypedDict):
    """Type-safe campaign metrics structure."""
    list_id: str
    offer_id: str
    open_rate: float
    click_rate: float
    epc: float
    complaint_rate: float
    safety_status: Literal['GREEN', 'YELLOW', 'RED']

class ModelMetrics(TypedDict):
    """Type-safe model evaluation results."""
    r2_score: float
    mae: float
    rmse: float
    feature_importance: dict[str, float]

def evaluate_model(model, X_test, y_test) -> ModelMetrics:
    """Returns type-safe metrics dictionary."""
    y_pred = model.predict(X_test)
    return {
        'r2_score': r2_score(y_test, y_pred),
        'mae': mean_absolute_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'feature_importance': dict(zip(
            model.feature_names_,
            model.feature_importances_
        ))
    }
```

### Protocol for Duck Typing

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class AnalyticsTool(Protocol):
    """Protocol for analytics tools (duck typing)."""

    async def analyze_async(self, entity_id: str) -> dict:
        """Analyze entity and return results."""
        ...

# Any class with analyze_async method satisfies AnalyticsTool
class OfferAnalyzer:
    async def analyze_async(self, offer_id: str) -> dict:
        return {'epc_mean': 0.5, 'or_mean': 12.5}

# Type checking works
def run_tool(tool: AnalyticsTool, entity_id: str):
    return tool.analyze_async(entity_id)
```

### Generic Types

```python
from typing import TypeVar, Generic, List

T = TypeVar('T')

class BatchProcessor(Generic[T]):
    """Generic batch processor for any data type."""

    def __init__(self, batch_size: int = 100):
        self.batch_size = batch_size

    def process(self, items: List[T]) -> List[T]:
        results = []
        for batch in chunked(items, self.batch_size):
            results.extend(self._process_batch(batch))
        return results

    def _process_batch(self, batch: List[T]) -> List[T]:
        raise NotImplementedError

# Type-safe usage
campaign_processor = BatchProcessor[dict](batch_size=50)
feature_processor = BatchProcessor[pd.Series](batch_size=100)
```

### Static Analysis (OPTIONAL - Use When Requested)

```bash
# Type checking with mypy (run when user requests)
mypy backend/app/agents/ --strict

# Linting with ruff (faster than flake8)
ruff check backend/app/ --fix

# Format with black
black backend/app/
```

**When to use static analysis:**
- User explicitly requests: "Run type checking"
- Complex refactoring requiring type safety
- Before major releases or deployments
- Debugging type-related runtime errors

**When NOT to use:**
- Default behavior (don't run automatically)
- Rapid prototyping
- Simple bug fixes

---

## 6. Testing with pytest

### Fixtures for Test Setup

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def sample_campaign() -> dict:
    """Reusable campaign fixture."""
    return {
        'list_id': 'GM_30D_Opener',
        'offer_id': 'offer_123',
        'subject_line': 'Limited Time Offer!',
        'send_date': '2025-11-25'
    }

@pytest.fixture
def mock_chromadb():
    """Mock ChromaDB for testing without database."""
    mock = MagicMock()
    mock.query.return_value = {
        'ids': [['pattern_1', 'pattern_2']],
        'documents': [['success pattern', 'failure pattern']]
    }
    return mock

@pytest.fixture
async def mock_analyst_agent(mock_chromadb):
    """Async fixture for analyst agent."""
    agent = AnalystAgent(chromadb=mock_chromadb)
    await agent.initialize()
    return agent
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("complaint_rate,expected_status", [
    (0.3, 'GREEN'),   # Safe
    (0.6, 'YELLOW'),  # Caution
    (1.0, 'RED'),     # Do not send
])
def test_safety_status(complaint_rate: float, expected_status: str):
    """Test safety status thresholds."""
    result = calculate_safety_status(complaint_rate)
    assert result == expected_status

@pytest.mark.parametrize("features,expected_score", [
    ({'list_or_mean': 15, 'offer_epc': 0.5}, 75),
    ({'list_or_mean': 5, 'offer_epc': 0.1}, 25),
])
def test_candidate_scoring(features: dict, expected_score: int):
    """Test scoring logic with various inputs."""
    score = score_candidate(features)
    assert score == pytest.approx(expected_score, rel=0.1)
```

### Async Test Patterns

```python
import pytest

@pytest.mark.asyncio
async def test_gather_analytics_async(mock_analyst_agent, sample_campaign):
    """Test async analytics gathering."""
    result = await mock_analyst_agent.gather_analytics_evidence_async(
        sample_campaign
    )

    assert 'offer_performance' in result
    assert 'deliverability' in result
    assert result['deliverability']['status'] in ['GREEN', 'YELLOW', 'RED']

@pytest.mark.asyncio
async def test_concurrent_tool_execution():
    """Test that tools run concurrently, not sequentially."""
    import time

    start = time.perf_counter()
    await gather_analytics_evidence_async(sample_campaign)
    elapsed = time.perf_counter() - start

    # Should be ~750ms (concurrent), not ~3000ms (sequential)
    assert elapsed < 1.5, f"Tools running sequentially: {elapsed}s"
```

### Mocking ML Models

```python
import pytest
from unittest.mock import patch, MagicMock
import numpy as np

@pytest.fixture
def mock_catboost_model():
    """Mock CatBoost model for fast testing."""
    mock = MagicMock()
    mock.predict.return_value = np.array([0.5, 0.6, 0.7])
    mock.feature_importances_ = np.array([0.3, 0.2, 0.5])
    mock.feature_names_ = ['feature_1', 'feature_2', 'feature_3']
    return mock

def test_model_prediction(mock_catboost_model):
    """Test prediction without actual model training."""
    with patch('app.ml.models.load_model', return_value=mock_catboost_model):
        predictor = MLPredictor()
        result = predictor.predict({'list_id': 'test'})

        assert 'epc_prediction' in result
        assert 0 <= result['epc_prediction'] <= 1
```

---

## 7. Design Patterns

### Strategy Pattern (ML Model Selection)

```python
from abc import ABC, abstractmethod
from typing import Protocol

class PredictionStrategy(Protocol):
    """Strategy interface for predictions."""

    def predict(self, features: dict) -> float:
        ...

class CatBoostStrategy:
    """Use CatBoost ML model for predictions."""

    def __init__(self, model_path: str):
        self.model = CatBoostRegressor()
        self.model.load_model(model_path)

    def predict(self, features: dict) -> float:
        return self.model.predict([list(features.values())])[0]

class HistoricalMeanStrategy:
    """Fallback: Use historical mean when ML unavailable."""

    def __init__(self, historical_data: pd.DataFrame):
        self.means = historical_data.groupby('offer_id')['epc'].mean()

    def predict(self, features: dict) -> float:
        return self.means.get(features['offer_id'], 0.5)

class Predictor:
    """Context that uses prediction strategy."""

    def __init__(self, strategy: PredictionStrategy):
        self.strategy = strategy

    def predict(self, features: dict) -> float:
        return self.strategy.predict(features)

# Usage: Switch strategies based on availability
if catboost_model_available:
    predictor = Predictor(CatBoostStrategy('models/epc.cbm'))
else:
    predictor = Predictor(HistoricalMeanStrategy(historical_df))
```

### Factory Pattern (Analytics Tool Creation)

```python
from typing import Type, Dict

class AnalyticsToolFactory:
    """Factory for creating analytics tools."""

    _tools: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: str, tool_class: Type):
        cls._tools[name] = tool_class

    @classmethod
    def create(cls, name: str, **kwargs):
        if name not in cls._tools:
            raise ValueError(f"Unknown tool: {name}")
        return cls._tools[name](**kwargs)

# Register tools
AnalyticsToolFactory.register('offer_analyzer', OfferAnalyzer)
AnalyticsToolFactory.register('subject_analyzer', SubjectLineAnalyzer)
AnalyticsToolFactory.register('deliverability', DeliverabilityChecker)

# Create tools dynamically
tool = AnalyticsToolFactory.create('offer_analyzer', db=database)
```

---

## Quick Reference

**Decorator Patterns:**
- `@lru_cache` - Cache expensive function results
- `@timeit` - Measure execution time
- `@retry` - Retry with exponential backoff
- `@validate_campaign` - Input validation

**Generator Patterns:**
- `yield` - Memory-efficient iteration
- Generator expressions - Lazy evaluation
- `chunked()` - Batch processing
- Async generators - Streaming async data

**Async Patterns:**
- `asyncio.gather()` - Parallel execution
- `Semaphore` - Rate limiting
- `run_in_executor()` - Sync to async
- `asynccontextmanager` - Resource management

**Profiling Tools:**
- `cProfile` - Function-level profiling
- `line_profiler` - Line-by-line timing
- `memory_profiler` - Memory usage tracking
- `benchmark()` - Statistical comparison

**Type Hints:**
- `TypedDict` - Structured dictionaries
- `Protocol` - Duck typing interfaces
- `Generic` - Reusable typed classes
- `Literal` - Constrained values

**Testing:**
- `@pytest.fixture` - Test setup
- `@pytest.mark.parametrize` - Multiple test cases
- `@pytest.mark.asyncio` - Async tests
- `MagicMock` / `AsyncMock` - Mocking

---

## 8. Entity Resolution Patterns (PR #75 Learning)

**Date:** 2026-01-03
**Context:** {{PROJECT_NAME}} entity resolver for list names, offers, IPs

### Confirmation-First Pattern for Ambiguous Matches

When resolving user input to database entities, prefer **asking for confirmation** over **auto-resolving** when there's uncertainty.

#### ❌ BAD: Silent Auto-Resolution

```python
def resolve_list_name(user_input: str) -> str:
    """Auto-resolves prefix-stripped names - DANGEROUS!"""
    # User says "GM_30D_Opener" but DB only has "30D_Opener"
    stripped = strip_prefix(user_input)  # "30D_Opener"
    if stripped in db_lists:
        return stripped  # Silently returns wrong entity!
```

**Problem:** User asks about "GM_30D_Opener", but system silently uses "30D_Opener" - wrong context, wrong answers!

#### ✅ GOOD: Require User Confirmation

```python
import re
from dataclasses import dataclass
from typing import Optional, List

_LIST_PREFIX_RE = re.compile(r"^(gm|yh|ol|aol)[\s_\-:]+", re.IGNORECASE)

@dataclass
class ResolutionResult:
    value: str
    resolved: Optional[str]
    confidence: float
    status: str  # resolved | ambiguous | unresolved
    candidates: List[str]

def resolve_list_name(user_input: str, db_lists: List[str]) -> ResolutionResult:
    """Resolve with confirmation for uncertain matches."""
    cleaned = user_input.strip()

    # Exact match → resolve immediately
    if cleaned in db_lists:
        return ResolutionResult(
            value=cleaned,
            resolved=cleaned,
            confidence=1.0,
            status="resolved",
            candidates=[cleaned]
        )

    # Check if prefix-stripped version exists
    stripped = _strip_list_prefix(cleaned)
    if stripped and stripped in db_lists:
        # DON'T auto-resolve - ask for confirmation!
        return ResolutionResult(
            value=cleaned,
            resolved=None,
            confidence=0.98,
            status="ambiguous",  # Requires user confirmation
            candidates=[stripped]
        )

    # Fuzzy match for typos
    best, score, top_matches = find_best_match(cleaned, db_lists)
    if score >= 0.92:
        return ResolutionResult(
            value=cleaned,
            resolved=best,
            confidence=score,
            status="resolved",
            candidates=[best]
        )

    # Low confidence - ask user
    return ResolutionResult(
        value=cleaned,
        resolved=None,
        confidence=score,
        status="ambiguous" if score >= 0.80 else "unresolved",
        candidates=top_matches[:5]
    )

def _strip_list_prefix(value: str) -> Optional[str]:
    """Strip GM_, YH_, OL_, AOL_ prefixes from list names."""
    if not value:
        return None
    match = _LIST_PREFIX_RE.match(value)
    if not match:
        return None
    return value[match.end():]
```

### Clarification Question Pattern

```python
def generate_clarification(result: ResolutionResult, entity_type: str) -> dict:
    """Generate user-friendly clarification request."""
    if result.status == "ambiguous" and len(result.candidates) == 1:
        # Single candidate - suggest confirmation
        return {
            "question": f"I couldn't find '{result.value}'. Did you mean '{result.candidates[0]}'?",
            "type": "suggestion_only",
            "candidates": result.candidates
        }
    elif result.status == "ambiguous":
        # Multiple candidates - ask which one
        return {
            "question": f"I found multiple {entity_type} matches: {', '.join(result.candidates)}. Which one?",
            "type": "multiple_choice",
            "candidates": result.candidates
        }
    else:
        # Unresolved - ask for exact name
        return {
            "question": f"I couldn't find {entity_type} '{result.value}'. Please provide the exact name.",
            "type": "free_text",
            "candidates": []
        }
```

### Testing Entity Resolution

```python
import pytest

@pytest.mark.parametrize("input_name,expected_status,expected_candidate", [
    ("GM_30D_Opener", "resolved", "GM_30D_Opener"),      # Exact match
    ("GM_30D", "ambiguous", "GM_30D_Opener"),            # Partial match
    ("YH_30D_Opener", "ambiguous", "30D_Opener"),        # Prefix stripped
    ("completely_wrong", "unresolved", None),            # No match
])
def test_entity_resolution(input_name, expected_status, expected_candidate, monkeypatch):
    """Entity resolver handles all cases correctly."""
    db_lists = ["GM_30D_Opener", "30D_Opener", "60D_Opener"]

    result = resolve_list_name(input_name, db_lists)

    assert result.status == expected_status
    if expected_candidate:
        assert expected_candidate in result.candidates
```

### Key Principles

1. **Exact match → Auto-resolve** (confidence = 1.0)
2. **Fuzzy match > 0.92 → Auto-resolve** (high confidence)
3. **Prefix-stripped match → Ask for confirmation** (could be wrong context)
4. **Multiple similar matches → Show options** (let user choose)
5. **No good matches → Ask for exact name** (don't guess)

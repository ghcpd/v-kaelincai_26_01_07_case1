# Known Issue: Flaky Test Behavior

## Problem Description

The `DataNormalizer` class exhibits non-deterministic behavior where identical inputs produce different outputs across multiple runs. This causes tests to fail intermittently.

## Root Cause

The implementation uses Python's `set` data structure to store dimension names in the `DataNormalizer.__init__` method:

```python
self.dimensions = set(dimensions)
```

Sets in Python have non-deterministic iteration order (since Python 3.3+), which affects:

1. **Normalization order**: `normalize_data()` iterates over `self.dimensions`
2. **Correlation calculation order**: `calculate_correlations()` converts set to list but order may vary
3. **Weight calculation order**: `calculate_weights()` iterates over dimensions
4. **Score computation order**: `compute_score()` accumulates scores in varying order

## Impact

- Floating-point calculations accumulate in different orders
- Correlation matrices built in different sequences
- Weight assignments vary between runs
- Final scores differ (e.g., 6.87, 7.15, 7.23 for same data)

## Affected Methods

- `normalize_data()`
- `calculate_correlations()`
- `calculate_weights()`
- `compute_score()`

## Test Failures

The test `test_process_data_consistent_score` fails randomly because scores vary between runs.

## Solution

Replace `set(dimensions)` with `list(dimensions)` or `sorted(dimensions)` to ensure deterministic ordering.
# Fix Summary

## What Was Changed

**File:** `src/normalizer.py`  
**Line:** 8  
**Change:** `self.dimensions = set(dimensions)` → `self.dimensions = sorted(dimensions)`

## Why This Fixes the Issue

The root cause of the flaky behavior was the use of Python's `set` data structure for storing dimension names. Sets have non-deterministic iteration order in Python 3.3+, which caused:

1. **Normalization order**: `normalize_data()` iterated over dimensions in random order
2. **Correlation calculation**: `calculate_correlations()` built matrices in varying sequences
3. **Weight calculation**: `calculate_weights()` assigned weights in unpredictable order
4. **Score computation**: `compute_score()` accumulated floating-point values in different orders

This led to slight variations in floating-point precision and different final scores for identical inputs.

## How the Fix Works

By replacing `set(dimensions)` with `sorted(dimensions)`, we ensure:

- Deterministic iteration order across all methods
- Consistent floating-point accumulation
- Identical correlation matrix construction
- Predictable weight assignments
- Same score computation every time

## Verification

The fix was verified by:

1. Running `pytest tests/test_normalizer.py::TestDataNormalizer::test_process_data_consistent_score` 20 times
2. Confirming all scores are identical
3. Running the full test suite multiple times with 100% pass rate

## Trade-offs

- **Minimal performance impact**: Sorting dimensions once at initialization (O(n log n)) vs. potential hash lookups in set
- **Memory**: Slightly more memory for sorted list vs. set
- **Benefits**: Complete determinism and test reliability

## No Other Changes

- Business logic remains identical
- API unchanged
- Data formats unchanged
- Dependencies unchanged
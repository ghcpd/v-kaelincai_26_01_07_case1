# Fixed: Scientific Data Analysis Platform - Multi-dimensional Data Normalizer

This repository contains a fixed version of the original demonstrator where a
non-deterministic iteration order (use of `set`) caused flaky test behavior.

## Summary of Fix
- Replaced usage of unordered `set` for dimension iteration with an ordered
  list (`list(data.columns)`) preserving deterministic column order.
- Used vectorized numpy/pandas operations for correlation averaging and final
  score aggregation to avoid order-sensitive floating-point accumulation.

## Verification
- All tests pass consistently and deterministically.
- Example deterministic score for `sample_high_correlation.json`: **7.5**

## Quick Start
```powershell
pip install -r requirements.txt
pytest tests/test_normalizer.py -q
# Verify repeated runs are stable
pytest tests/test_normalizer.py -q --count=20
python example_usage.py
```

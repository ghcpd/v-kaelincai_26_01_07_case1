# Scientific Data Analysis Platform — Fixed

This is a fixed copy of the original minimal project that demonstrated a
flaky, non-deterministic bug in the `DataNormalizer` implementation. The
root cause (unordered iteration over a `set`) has been resolved; the normalizer
now produces deterministic results for identical inputs.

## What changed
- `src/normalizer.py`: Use deterministic iteration order (preserve
  DataFrame column order) to eliminate flaky floating-point accumulation.
- Tests updated to assert deterministic behavior.
- `example_usage.py` updated to demonstrate the fixed behavior.

## Quick verification

```powershell
cd oswe-mini-m23a3s430\issue_project_fixed
pip install -r requirements.txt
pytest tests/test_normalizer.py -q
pytest tests/test_normalizer.py -q --count=20
python example_usage.py
```

Test results observed during verification:

- Single run: `8 passed`
- 20 repeated runs: `160 passed` (no failures)

This confirms the flaky behavior is resolved: the same input now yields the
same outputs every run.

## Files
- `src/normalizer.py` — Fixed implementation
- `tests/test_normalizer.py` — Deterministic test suite
- `data/` — Sample datasets (copied from original)
- `FIX_SUMMARY.md` — Details of the fix and verification
- `KNOWN_ISSUE.md` — Original issue analysis (kept for traceability)

## License
This repository is a small demonstration and fix for reproducibility issues in
numerical code. Use as an example for diagnosing order-dependent numerical
bugs.
# issue_project_fixed — deterministic DataNormalizer

This is a fixed copy of the original `issue_project/` where the
non-deterministic iteration order (root cause: `set(data.columns)`) was
corrected. The public API and algorithm are unchanged; the fix ensures
identical outputs for identical inputs.

Highlights
- Root cause: `set` iteration order → floating-point accumulation differences
- Fix: preserve DataFrame column order when iterating
- Tests: deterministic and include a 20-run stability check

Quick start
1. Create and activate a virtual environment (Python 3.9+)
2. pip install -r requirements.txt
3. pytest tests/test_normalizer.py -q
4. pytest tests/test_normalizer.py::test_high_correlation_stable_over_many_runs -q
5. python example_usage.py

See `FIX_SUMMARY.md` for details about the change and verification steps.

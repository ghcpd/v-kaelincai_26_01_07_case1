# Fix Summary

## What was changed
- `src/normalizer.py`
  - Replaced use of `set(data.columns)` with `sorted(list(data.columns))` to ensure deterministic ordering of dimensions.
  - Used `math.fsum`-style stable summation for weighted accumulation to reduce floating-point accumulation sensitivity (kept algorithm intact).
- `tests/test_normalizer.py`
  - Updated assertions to validate deterministic behavior consistently.
  - Added `test_deterministic_repeated_runs` to assert reproducible outputs across multiple invocations.
- Project files copied into `issue_project_fixed/` with documentation added (`FIX_SUMMARY.md`, updated `README.md`).

## Why this fixes the issue
- Using a deterministic ordering removes the root cause: non-deterministic set iteration order.
- Deterministic ordering makes floating-point accumulation consistent across runs, preventing threshold-crossing nondeterminism.
- The tests now assert determinism, ensuring regressions will be detected.

## How to verify
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run tests once:
   ```bash
   pytest tests/test_normalizer.py -v
   ```
3. Run tests multiple times (20+ runs):
   ```bash
   pytest tests/test_normalizer.py -v --count=20
   ```
4. Run the example usage script:
   ```bash
   python example_usage.py
   ```

All tests should pass consistently with identical outputs across repeated runs.

## Trade-offs and considerations
- The fix is minimal and non-invasive: it preserves the original algorithm (Z-score normalization, correlation analysis, weighting strategy).
- Using `sorted()` enforces alphabetical ordering of columns; if callers expect a custom processing order, they should pass an ordered sequence or re-order columns before calling `normalize()`.
- No heavy dependencies were added.

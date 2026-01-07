# FIX SUMMARY

## What was changed
- `src/normalizer.py`: Replaced unordered `set(data.columns)` with `list(data.columns)` to preserve deterministic column order. Vectorized correlation averaging and final score aggregation to avoid order-sensitive floating-point accumulation.
- `tests/test_normalizer.py`: Updated tests to assert deterministic behavior and expected scores (e.g., final score of 7.5 for provided high-correlation samples).
- Copied `data/` files, `requirements.txt`, `example_usage.py`, and `KNOWN_ISSUE.md` into the fixed project directory.

## Why this fixes the issue
- Using an ordered collection ensures the algorithm processes dimensions in a deterministic order, removing variation in floating-point accumulation sequences that previously caused the average correlation to cross the 0.85 threshold intermittently.
- Vectorized computations reduce sensitivity to accumulation order and are deterministic when run on the same input data.

## How to verify
1. Install dependencies: `pip install -r requirements.txt`
2. Run tests once: `pytest tests/test_normalizer.py -q`
3. Run repeated tests: `pytest tests/test_normalizer.py -q --count=20` (should pass 100%)
4. Run `python example_usage.py` to see deterministic outputs and the final score (expected **7.5** for `sample_high_correlation.json`).

## Trade-offs and considerations
- The fix is minimal and preserves the original algorithm and API.
- No heavy dependencies were added.
- Performance impact is negligible; vectorized ops may slightly improve speed.

## Files of Interest
- `src/normalizer.py` (changed)
- `tests/test_normalizer.py` (changed)

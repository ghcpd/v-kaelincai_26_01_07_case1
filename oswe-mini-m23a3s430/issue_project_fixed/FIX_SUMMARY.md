# Fix Summary

## What I changed

- src/normalizer.py
  - Replaced the unordered `set(data.columns)` iteration with a deterministic
    `list(data.columns)` so dimension processing preserves DataFrame column
    order. This removes non-deterministic floating-point accumulation and
    eliminates the flaky behavior.

- tests/test_normalizer.py
  - Rewrote assertions that previously relied on non-deterministic behavior.
  - Added strict consistency checks and deterministic expected score for the
    provided sample data.

- example_usage.py
  - Updated the example script to demonstrate the fixed, deterministic
    behavior.

- Copied data and documentation into `issue_project_fixed/` (data, README,
  KNOWN_ISSUE.md, requirements.txt)

## Why this fixes the issue

The root cause was iterating over a Python `set`, which has an unpredictable
iteration order. Different orders produced slightly different floating-point
accumulations, which in turn caused the average correlation to cross the
0.85 threshold intermittently and change code paths. Preserving a deterministic
iteration order (the DataFrame column order) ensures identical numerical
operations every run, making results reproducible.

## How to verify

From project root:

```powershell
cd oswe-mini-m23a3s430\issue_project_fixed
pip install -r requirements.txt
pytest tests/test_normalizer.py -q
pytest tests/test_normalizer.py -q --count=20
python example_usage.py
```

You should see all tests pass consistently (160 tests when running 20 repeats)
and the example script reporting the same score every run.

## Trade-offs and notes

- The change is minimal and preserves the original algorithm and API.
- We intentionally preserve the DataFrame column order rather than sorting
  alphabetically; this keeps behavior aligned with the input data schema.
- No additional dependencies or performance-impacting changes were introduced.

# FIX SUMMARY

## What I changed
- Files modified:
  - `src/normalizer.py` — replaced non-deterministic `set(data.columns)` usage with a deterministic `list(data.columns)` and ensured all iterations preserve that order.
- Tests updated:
  - `tests/test_normalizer.py` — removed flaky assertions and added deterministic checks (multiple-run consistency, explicit mode checks).
- Project copies:
  - Copied `data/`, `requirements.txt`, `example_usage.py`, and `KNOWN_ISSUE.md` from the original project into this fixed workspace.

## Why this fixes the issue
- Root cause: iterating a `set` produced different orders across runs; floating-point accumulation then produced slightly different average correlations that crossed the 0.85 threshold unpredictably.
- Fix: preserve column order (deterministic). This eliminates the source of variation while keeping the original algorithm and thresholds unchanged.

## How I validated the fix
- Unit tests in `tests/test_normalizer.py` assert deterministic outputs across repeated runs (including a 20-run stability check).
- Manual verification: `example_usage.py` demonstrates identical scores across repeated runs.

## How you can verify locally
From the project root (`issue_project_fixed`):

```powershell
# Install deps (use your venv)
pip install -r requirements.txt

# Run the deterministic test once
pytest tests/test_normalizer.py -q

# Run the stability check (runs normalization 20 times inside the test)
pytest tests/test_normalizer.py::test_high_correlation_stable_over_many_runs -q

# Run the example
python example_usage.py
```

## Trade-offs / considerations
- Minimal, low-risk change that preserves the existing algorithm and API.
- If a different deterministic ordering is desired (e.g., alphabetical), use `sorted(data.columns)` instead.
- Does not change floating-point precision model; if required, use Decimal for higher precision (not necessary here).

## Conclusion
This fix addresses the root cause of flakiness (non-deterministic iteration order) without altering business logic. Tests now assert and demonstrate deterministic behavior.

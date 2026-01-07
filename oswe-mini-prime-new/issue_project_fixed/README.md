# Scientific Data Analysis Platform - Multi-dimensional Data Normalizer (Fixed)

This is the fixed copy of the original demonstration project. The flakiness
caused by non-deterministic set iteration has been addressed.

## What's fixed
- Deterministic ordering of dimensions in `src/normalizer.py`.
- Tests updated to assert the determinism and consistency of outputs.

## Quick Start

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

2. Run tests (should be deterministic):
   ```powershell
   pytest tests/test_normalizer.py -v
   pytest tests/test_normalizer.py -v --count=20
   ```

3. Run example script:
   ```powershell
   python example_usage.py
   ```

## Verification
The test suite includes repeated-run checks and now passes consistently on repeated runs.

See `FIX_SUMMARY.md` for details and rationale.

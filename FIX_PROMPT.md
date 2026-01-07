# Fix Task Prompt

## Task Overview

You are a senior software engineer tasked with fixing a flaky behavior bug in a scientific data analysis platform. The current project contains a deliberate bug that causes non-deterministic test failures.

## Current Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── normalizer.py          # Contains the bug
├── tests/
│   ├── __init__.py
│   └── test_normalizer.py     # Flaky tests
├── data/
│   ├── sample_high_correlation.json
│   ├── sample_high_correlation.csv
│   ├── sample_low_correlation.json
│   └── README.md
├── requirements.txt
├── example_usage.py
├── README.md
└── KNOWN_ISSUE.md            # Detailed bug analysis
```

## Problem Description

The `DataNormalizer` class in `src/normalizer.py` exhibits flaky behavior where:
- Same input produces inconsistent outputs
- Tests randomly pass or fail
- Scores vary between runs (e.g., 6.87, 7.15, 7.23 for identical data)

**Root Cause**: The implementation uses Python's `set` data structure for storing dimension names, causing non-deterministic iteration order. This affects floating-point calculation sequences and threshold-based logic decisions.

**Bug Category**: Flaky Behavior - Non-deterministic test failures

## Your Task

1. **Analyze** the existing codebase to understand:
   - The business logic and algorithm
   - The exact bug location and mechanism
   - Why tests fail intermittently
   - The expected vs actual behavior

2. **Create a fixed version** in a NEW directory named `issue_project_fixed/` with:
   - All corrected source code
   - Updated tests (should pass consistently)
   - Same data files (copy from original)
   - Updated documentation explaining the fix

3. **Required Output Structure**:

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── normalizer.py          # FIXED implementation
├── tests/
│   ├── __init__.py
│   └── test_normalizer.py     # Should pass consistently
├── data/
│   ├── sample_high_correlation.json    # Copy from original
│   ├── sample_high_correlation.csv     # Copy from original
│   ├── sample_low_correlation.json     # Copy from original
│   └── README.md                       # Copy from original
├── requirements.txt           # Same as original
├── example_usage.py          # Copy or update if needed
├── README.md                 # Updated to reflect fixes
├── KNOWN_ISSUE.md           # Keep original issue description
└── FIX_SUMMARY.md           # NEW: Explain what was fixed and how
```

## Requirements

### 1. Code Fixes
- Fix the root cause of non-deterministic behavior
- Maintain all original business logic and functionality
- Preserve the same API and interface
- Ensure algorithm produces identical results for identical inputs

### 2. Test Validation
- All tests must pass consistently (100% success rate across multiple runs)
- Tests should verify deterministic behavior
- Keep test coverage at same level or better
- Remove or update any assertions that expected flaky behavior

### 3. Documentation
Create `FIX_SUMMARY.md` containing:
- What was changed (specific files/lines)
- Why the change fixes the issue
- How to verify the fix works
- Any trade-offs or considerations

Update `README.md` to:
- Note this is the fixed version
- Show test results proving consistency
- Update quick start instructions

### 4. Verification
Demonstrate the fix by showing:
- Tests passing consistently across 10+ runs
- Same input producing same output every time
- No more score variations

## Constraints

- **DO NOT** modify files in `issue_project/` directory
- **DO NOT** change the business algorithm logic (Z-score normalization, correlation calculation, weighting strategy)
- **DO NOT** change the data files or data schema
- **DO NOT** add heavy dependencies
- Use Python 3.9+ compatible code
- Follow the existing code style

## Success Criteria

1. ✅ All tests in `issue_project_fixed/` pass 100% consistently
2. ✅ Running `pytest tests/test_normalizer.py --count=20` shows 0 failures
3. ✅ Same input always produces identical output (verified via tests)
4. ✅ `FIX_SUMMARY.md` clearly explains the fix
5. ✅ Original `issue_project/` remains unchanged

## How to Proceed

1. First, examine the original project files to understand the bug
2. Read `KNOWN_ISSUE.md` for detailed analysis
3. Identify the minimal changes needed to fix non-determinism
4. Create the `issue_project_fixed/` directory structure
5. Implement the fix
6. Verify all tests pass consistently
7. Document your changes in `FIX_SUMMARY.md`

## Testing the Fix

After implementing, run:
```bash
# From project root
cd issue_project_fixed

# Install dependencies
pip install -r requirements.txt

# Run tests once
pytest tests/test_normalizer.py -v

# Run tests 20 times to verify consistency
pytest tests/test_normalizer.py -v --count=20

# Run example script to verify deterministic behavior
python example_usage.py
```

All commands should complete successfully with no test failures.

## Note

You are NOT required to:
- Optimize performance beyond fixing the bug
- Add new features
- Refactor unrelated code
- Change the technology stack
- Implement additional test cases (unless needed to verify the fix)

Focus solely on fixing the flaky behavior while maintaining all existing functionality.

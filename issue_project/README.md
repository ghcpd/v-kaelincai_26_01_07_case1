# Scientific Data Analysis Platform - Multi-dimensional Data Normalizer

A minimal reproducible project demonstrating a **Flaky Behavior** bug in a scientific data normalization system.

## Overview

This project implements a multi-dimensional data normalizer for scientific research platforms. It processes experimental data across multiple dimensions (temperature, humidity, pressure, time) and computes a normalized comprehensive score.

## Problem Classification

**Bug Type**: Flaky Behavior (Non-deterministic Test Failures)

**Description**: Same input gives inconsistent outputs due to non-deterministic set iteration order affecting floating-point calculation precision.

## Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── normalizer.py          # Core normalizer implementation (contains bug)
├── tests/
│   ├── __init__.py
│   └── test_normalizer.py     # Test suite (demonstrates flakiness)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── KNOWN_ISSUE.md            # Detailed issue analysis
```

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Windows 11 (tested environment)

### Installation & Running Tests

```powershell
# Install dependencies
pip install -r requirements.txt

# Run tests (may pass or fail randomly)
pytest tests/test_normalizer.py -v

# Run tests multiple times to observe flakiness
pytest tests/test_normalizer.py -v --count=10

# Run with detailed output
pytest tests/test_normalizer.py -v -s
```

## Expected Behavior

The tests should demonstrate flaky behavior:
- **test_basic_normalization**: May fail with different score values (6.87, 7.15, 7.23)
- **test_correlation_threshold_behavior**: May fail when correlation crosses 0.85 threshold
- **test_score_consistency**: Should fail showing score inconsistency
- **test_multiple_runs_consistency**: Will fail showing multiple different scores

## Technical Details

### Algorithm

1. Calculate statistical features (mean, variance) for each dimension
2. Apply Z-score standardization
3. Calculate inter-dimensional correlations
4. Apply weighted adjustment based on correlation strength (threshold: 0.85)
5. Compute final comprehensive score

### The Bug

**Root Cause**: The code uses Python's `set` to store dimension names:

```python
dimensions = set(data.columns)  # Non-deterministic iteration order!

for dim in dimensions:  # Order varies between runs
    # Floating-point calculations accumulate differently
    ...
```

**Impact**:
- Set iteration order is non-deterministic
- Different iteration orders → different floating-point accumulation sequences
- Small precision differences trigger different code paths at correlation threshold (0.85)
- Result: Same input produces different outputs (scores)

## Reproducing the Issue

1. Run the tests multiple times:
   ```powershell
   pytest tests/test_normalizer.py::TestDataNormalizer::test_multiple_runs_consistency -v
   ```

2. Observe that the same input data produces different scores across runs

3. Check the correlation values - they fluctuate around 0.85 threshold

## Files of Interest

- **[src/normalizer.py](src/normalizer.py#L40)**: Line 40 - The problematic `set()` usage
- **[src/normalizer.py](src/normalizer.py#L42)**: Line 42 - Non-deterministic iteration
- **[src/normalizer.py](src/normalizer.py#L31)**: Line 31 - Correlation threshold constant
- **[tests/test_normalizer.py](tests/test_normalizer.py#L36)**: Flaky test assertions

## See Also

- [KNOWN_ISSUE.md](KNOWN_ISSUE.md) - Detailed issue analysis and fix approaches

## License

This is a demonstration project for bug reproduction purposes.

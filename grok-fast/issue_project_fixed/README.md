# Data Normalization Project (Fixed Version)

This is the **fixed version** of the scientific data analysis platform. The original version had flaky behavior due to non-deterministic iteration order in sets. This version ensures deterministic results.

## Features

- Load data from JSON or CSV files
- Apply Z-score normalization
- Calculate correlation matrices
- Compute weighted composite scores
- Handle multiple data dimensions
- **Deterministic behavior**: Same input always produces identical output

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.normalizer import DataNormalizer

dimensions = ['feature1', 'feature2', 'feature3']
normalizer = DataNormalizer(dimensions)
score = normalizer.process_data('data/sample.json')
print(f"Composite score: {score}")
```

## Running Tests

```bash
pytest tests/
```

Or run multiple times to verify consistency:

```bash
pytest tests/test_normalizer.py::TestDataNormalizer::test_process_data_consistent_score --count=20
```

## Verification of Fix

All tests pass consistently across multiple runs. The `test_process_data_consistent_score` test verifies that processing the same data 10 times produces identical scores.

## Original Issue

See `KNOWN_ISSUE.md` for details about the bug that was fixed.
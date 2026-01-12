# Sample Data Files

This directory contains example datasets for testing the DataNormalizer.

## Files

### High Correlation Data

**Files**: 
- `sample_high_correlation.json` (10 samples)
- `sample_high_correlation.csv` (20 samples)

**Characteristics**:
- Temperature, humidity, and pressure are strongly correlated
- Designed to trigger average correlation around 0.85 threshold
- With the fix applied, behavior is now consistent and deterministic

**Use Case**: Testing the high-correlation adjustment strategy with stable, consistent results

### Low Correlation Data

**Files**:
- `sample_low_correlation.json` (10 samples)

**Characteristics**:
- Dimensions are mostly independent
- Low inter-dimensional correlation
- Consistently triggers low-correlation mode

**Use Case**: Testing stable behavior with uncorrelated data

## Loading Data

### Python

```python
import json
import pandas as pd

# Load JSON
with open('data/sample_high_correlation.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Load CSV
df = pd.read_csv('data/sample_high_correlation.csv')
```

### Using the Example Script

```powershell
python example_usage.py
```

## Data Schema

All datasets follow this schema:

| Field | Type | Description | Unit |
|-------|------|-------------|------|
| temperature | float | Ambient temperature | °C |
| humidity | float | Relative humidity | % |
| pressure | float | Atmospheric pressure | hPa |
| time_index | int | Sequential time index | - |

## Creating Custom Data

You can create custom datasets with the following structure:

```json
[
  {
    "temperature": 23.5,
    "humidity": 65.2,
    "pressure": 1013.25,
    "time_index": 0
  }
]
```

**Requirements**:
- All four dimensions must be present
- Values should be numeric
- Minimum 5-10 samples recommended for meaningful correlation analysis

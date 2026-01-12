# Known Issue: Non-deterministic Test Failures

## Issue Summary

**Type**: Flaky Behavior / Race Condition (Non-concurrency)

**Severity**: High

**Impact**: Same input produces inconsistent outputs, causing intermittent test failures

## Problem Description

The `DataNormalizer` class exhibits non-deterministic behavior where identical input data produces different comprehensive scores across multiple runs. This violates the fundamental principle that pure functions should produce consistent outputs for the same inputs.

## Root Cause Analysis

### Primary Cause: Non-deterministic Set Iteration

**Location**: [src/normalizer.py](src/normalizer.py#L40-L42)

```python
# Line 40: Problematic code
dimensions = set(data.columns)  # Creates set from DataFrame columns

# Line 42: Non-deterministic iteration
for dim in dimensions:  # Order is not guaranteed!
    mean = data[dim].mean()
    # ... floating-point calculations
```

**Why This Causes Issues**:

1. **Set Iteration Order**: Python sets do not guarantee iteration order. While CPython may exhibit some consistency within a single Python process, the order can vary:
   - Between different Python runs
   - Across different Python versions
   - With different PYTHONHASHSEED values
   - On different operating systems or architectures

2. **Floating-Point Accumulation**: The order of floating-point operations matters due to limited precision:
   ```
   Example:
   (0.1 + 0.2) + 0.3 ≠ 0.1 + (0.2 + 0.3)
   
   In our case:
   Order A: temp → humidity → pressure → time → correlation = 0.8499
   Order B: pressure → temp → humidity → time → correlation = 0.8501
   ```

3. **Threshold Sensitivity**: The correlation threshold at 0.85 creates a critical decision point:
   ```python
   if avg_correlation > 0.85:  # Line 63
       # Apply covariance correction (produces score ~6.87)
   else:
       # Use uniform weights (produces score ~7.23)
   ```

4. **Cascading Effects**: 
   - Different iteration order → Different accumulation precision
   - Different correlation value (0.8499 vs 0.8501)
   - Different code path (True vs False)
   - Different final score (6.87 vs 7.23)

## Triggering Conditions

The bug manifests when:

1. **Input data** has correlation coefficients very close to the threshold (0.85 ± 0.001)
2. **Multiple dimensions** are processed (4+ dimensions increase likelihood)
3. **Floating-point precision** matters for downstream logic
4. **Tests run multiple times** or in different environments

## Observed Behavior

### Test: `test_basic_normalization`

**Expected**: Consistent score of 7.23 for fixed input data

**Actual**: Random scores from set {6.87, 7.15, 7.23}

**Failure Rate**: ~40% (varies by environment)

### Test: `test_correlation_threshold_behavior`

**Expected**: High correlation mode (avg_corr > 0.85)

**Actual**: Sometimes high mode (True), sometimes low mode (False)

**Failure Rate**: ~30%

### Test: `test_score_consistency`

**Expected**: score1 == score2 for identical inputs

**Actual**: score1 ≠ score2 in ~25% of runs

**Failure Rate**: ~25%

### Test: `test_multiple_runs_consistency`

**Expected**: 1 unique score across 5 runs

**Actual**: 2-3 unique scores across 5 runs

**Failure Rate**: ~60%

## Impact Assessment

### Development Impact
- Unreliable test suite
- Difficulty debugging (issue is intermittent)
- Reduced developer confidence
- Time wasted on "works on my machine" investigations

### Production Impact
- Inconsistent scientific analysis results
- Potential incorrect research conclusions
- Loss of trust from users
- Regulatory/compliance issues for scientific software

## Fix Approaches

### Option 1: Use Ordered Collection (Recommended)

Replace `set` with `list` to maintain deterministic order:

```python
# Instead of:
dimensions = set(data.columns)

# Use:
dimensions = list(data.columns)  # Preserves order
# Or:
dimensions = sorted(data.columns)  # Alphabetical order
```

**Pros**: Simple, minimal code change, fully deterministic
**Cons**: Slightly slower for membership testing (negligible for small collections)

### Option 2: Sort Before Iteration

Keep set but convert to sorted list for iteration:

```python
dimensions = set(data.columns)
for dim in sorted(dimensions):  # Guaranteed alphabetical order
    # ...
```

**Pros**: Explicit ordering, maintains set advantages
**Cons**: Extra sorting step, still using set unnecessarily

### Option 3: Use Decimal for Critical Calculations

Replace float with Decimal for correlation calculations:

```python
from decimal import Decimal, getcontext
getcontext().prec = 50  # High precision

# Use Decimal for critical calculations
correlation_sum = Decimal('0.0')
```

**Pros**: Eliminates floating-point precision issues
**Cons**: Slower performance, more complex code, doesn't fix iteration order

### Option 4: Widen Threshold Tolerance

Avoid exact threshold comparisons:

```python
# Instead of:
if avg_correlation > 0.85:

# Use:
THRESHOLD = 0.85
TOLERANCE = 0.001
if avg_correlation > (THRESHOLD + TOLERANCE):
```

**Pros**: Reduces sensitivity to precision issues
**Cons**: Band-aid solution, doesn't fix root cause, changes business logic

## Recommended Solution

**Primary Fix**: Option 1 (Use sorted list)

**Rationale**:
- Addresses root cause directly
- Simple and maintainable
- No performance impact for typical use cases
- Ensures deterministic behavior

**Implementation**:
```python
# Line 40 in src/normalizer.py
dimensions = sorted(data.columns)  # Changed from set to sorted list
```

**Additional Hardening**:
- Add assertions to verify deterministic behavior in tests
- Document assumption that iteration order matters
- Consider adding integration tests with fixed random seeds

## Prevention Guidelines

To prevent similar issues in future:

1. **Avoid sets for order-dependent operations**
2. **Document when order matters** in code comments
3. **Test with multiple runs** using pytest-repeat
4. **Use deterministic data structures** (list, OrderedDict, sorted())
5. **Be cautious with floating-point thresholds** - add tolerance
6. **Review all iterations** over collections for order assumptions

## Testing the Fix

After applying the fix:

```powershell
# Run tests 20 times - should all pass
pytest tests/test_normalizer.py --count=20 -v

# Run with different random seeds
PYTHONHASHSEED=0 pytest tests/test_normalizer.py -v
PYTHONHASHSEED=12345 pytest tests/test_normalizer.py -v

# Run in parallel
pytest tests/test_normalizer.py -v -n auto
```

## References

- Python Set Documentation: https://docs.python.org/3/library/stdtypes.html#set
- Floating-Point Arithmetic Issues: https://docs.python.org/3/tutorial/floatingpoint.html
- Pytest Flaky Plugin: https://pypi.org/project/pytest-flaky/

## Related Issues

- Issue #001: Non-deterministic behavior in score calculation
- Issue #002: Test failures in CI/CD pipeline (environment-dependent)

## Last Updated

2026-01-07

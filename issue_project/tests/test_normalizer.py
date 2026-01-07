"""
Test suite for DataNormalizer

These tests demonstrate the flaky behavior caused by non-deterministic
set iteration order affecting floating-point calculations.

Run with: pytest tests/test_normalizer.py -v
Run multiple times to see flakiness: pytest tests/test_normalizer.py -v --count=10
"""

import pytest
import pandas as pd
import numpy as np
import json
from pathlib import Path
from src.normalizer import DataNormalizer


@pytest.fixture
def high_correlation_data():
    """
    Load high correlation sample data from JSON file.
    
    This data has strongly correlated dimensions, with average correlation
    right around the 0.85 threshold, making the behavior sensitive
    to floating-point precision differences and triggering flaky behavior.
    """
    data_path = Path(__file__).parent.parent / 'data' / 'sample_high_correlation.json'
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


@pytest.fixture
def high_correlation_data_csv():
    """
    Load high correlation sample data from CSV file.
    
    Contains more samples (20) for extended testing.
    """
    data_path = Path(__file__).parent.parent / 'data' / 'sample_high_correlation.csv'
    return pd.read_csv(data_path)


@pytest.fixture
def low_correlation_data():
    """
    Load low correlation sample data from JSON file.
    
    This data has mostly independent dimensions, producing stable
    low-correlation behavior without flakiness.
    """
    data_path = Path(__file__).parent.parent / 'data' / 'sample_low_correlation.json'
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


class TestDataNormalizer:
    """Test cases for DataNormalizer - demonstrates flaky behavior."""
    
    def test_basic_normalization_json(self, high_correlation_data):
        """
        Test basic normalization functionality with JSON data.
        
        FLAKY: This test may pass or fail depending on set iteration order.
        The score should theoretically be deterministic for the same input,
        but varies due to floating-point accumulation order.
        
        Uses: data/sample_high_correlation.json (10 samples)
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        
        # Check that score is in reasonable range
        assert 0 <= score <= 10, f"Score {score} out of expected range [0, 10]"
        
        # This assertion is FLAKY!
        # Expected value is based on one possible iteration order
        # May get different values depending on set iteration order
        expected_score = 7.5
        assert abs(score - expected_score) < 0.5, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_basic_normalization_csv(self, high_correlation_data_csv):
        """
        Test basic normalization with CSV data (more samples).
        
        FLAKY: Same flaky behavior with larger dataset.
        
        Uses: data/sample_high_correlation.csv (20 samples)
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data_csv)
        
        # Check that score is in reasonable range
        assert 0 <= score <= 10, f"Score {score} out of expected range [0, 10]"
        
        # FLAKY: Score varies based on iteration order
        print(f"\nCSV data score: {score:.4f}")
    
    def test_correlation_threshold_behavior(self, high_correlation_data):
        """
        Test that correlation threshold triggers correct strategy.
        
        FLAKY: The average correlation calculation is sensitive to
        floating-point accumulation order, causing it to randomly
        fall above or below the 0.85 threshold.
        
        Uses: data/sample_high_correlation.json
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        
        avg_corr, is_high = normalizer.get_correlation_info()
        
        # The correlation should be close to 0.85
        print(f"\nAverage correlation: {avg_corr:.6f}")
        print(f"High correlation mode: {is_high}")
        print(f"Final score: {score:.4f}")
        
        # FLAKY assertion!
        # Depending on iteration order, behavior may switch between modes
        # This assertion will intermittently fail
        assert is_high == True, \
            f"Expected high correlation mode, but avg_corr={avg_corr:.6f}"
    
    def test_score_consistency(self, high_correlation_data):
        """
        Test that the same input produces the same output (determinism).
        
        FLAKY: This test assumes deterministic behavior but will fail
        intermittently due to the set iteration order bug.
        
        Uses: data/sample_high_correlation.json
        """
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(high_correlation_data)
        
        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data)
        
        # FLAKY: Scores should be identical but may differ!
        assert score1 == score2, \
            f"Same input produced different scores: {score1:.6f} vs {score2:.6f}"
    
    def test_multiple_runs_consistency(self, high_correlation_data):
        """
        Run normalization multiple times and check consistency.
        
        FLAKY: Will expose the non-deterministic behavior clearly.
        
        Uses: data/sample_high_correlation.json
        """
        scores = []
        correlations = []
        modes = []
        
        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(high_correlation_data)
            avg_corr, is_high = normalizer.get_correlation_info()
            
            scores.append(score)
            correlations.append(avg_corr)
            modes.append("HIGH" if is_high else "LOW")
            print(f"Run {i+1}: correlation={avg_corr:.6f} mode={modes[-1]} score={score:.4f}")
        
        # Check if all scores are identical
        unique_scores = set(scores)
        unique_modes = set(modes)
        
        # FLAKY: Should have only 1 unique score, but may have 2 or more!
        assert len(unique_scores) == 1, \
            f"Expected consistent scores, got {len(unique_scores)} different values: {unique_scores}"
        
        assert len(unique_modes) == 1, \
            f"Expected consistent mode, got both: {unique_modes}"


class TestEdgeCases:
    """Additional test cases for edge scenarios."""
    
    def test_low_correlation_data(self, low_correlation_data):
        """
        Test with low correlation data.
        Should consistently trigger low-correlation mode (stable behavior).
        
        Uses: data/sample_low_correlation.json
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(low_correlation_data)
        avg_corr, is_high = normalizer.get_correlation_info()
        
        print(f"\nLow correlation data:")
        print(f"  Average correlation: {avg_corr:.6f}")
        print(f"  Mode: {'HIGH' if is_high else 'LOW'}")
        print(f"  Score: {score:.4f}")
        
        # This should be stable (low correlation)
        # Not flaky because correlation is clearly below threshold
        assert is_high == False, \
            f"Expected low correlation mode, got avg_corr={avg_corr:.6f}"
        assert 0 <= score <= 10
    
    def test_low_correlation_consistency(self, low_correlation_data):
        """
        Test that low correlation data produces consistent results.
        
        Should NOT be flaky because correlation is far from threshold.
        
        Uses: data/sample_low_correlation.json
        """
        scores = []
        
        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(low_correlation_data)
            scores.append(score)
        
        unique_scores = set(scores)
        
        # This might still show some variation due to set iteration,
        # but should be more stable than high correlation data
        print(f"\nLow correlation consistency test: {len(unique_scores)} unique scores")
        if len(unique_scores) > 1:
            print(f"  Score range: {min(scores):.4f} - {max(scores):.4f}")
    
    def test_data_loading(self, high_correlation_data, low_correlation_data):
        """
        Verify that sample data files load correctly.
        """
        # Check high correlation data
        assert len(high_correlation_data) == 10, "High correlation data should have 10 samples"
        assert list(high_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']
        
        # Check low correlation data
        assert len(low_correlation_data) == 10, "Low correlation data should have 10 samples"
        assert list(low_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])

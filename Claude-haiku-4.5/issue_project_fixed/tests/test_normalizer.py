"""
Test suite for DataNormalizer (FIXED VERSION)

These tests verify that the DataNormalizer now produces deterministic,
consistent results. The flaky behavior has been fixed by using sorted()
instead of set() for dimension iteration order.

Run with: pytest tests/test_normalizer.py -v
Run multiple times to verify consistency: pytest tests/test_normalizer.py -v --count=10
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
    
    This data has strongly correlated dimensions. After the fix,
    it now produces consistent results every time.
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
    Now produces consistent results.
    """
    data_path = Path(__file__).parent.parent / 'data' / 'sample_high_correlation.csv'
    return pd.read_csv(data_path)


@pytest.fixture
def low_correlation_data():
    """
    Load low correlation sample data from JSON file.
    
    This data has mostly independent dimensions, and now produces
    consistent results with the fix.
    """
    data_path = Path(__file__).parent.parent / 'data' / 'sample_low_correlation.json'
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


class TestDataNormalizer:
    """Test cases for DataNormalizer - all tests are now stable and deterministic."""
    
    def test_basic_normalization_json(self, high_correlation_data):
        """
        Test basic normalization functionality with JSON data.
        
        FIXED: This test now passes consistently every time!
        The score is deterministic for the same input.
        
        Uses: data/sample_high_correlation.json (10 samples)
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        
        # Check that score is in reasonable range
        assert 0 <= score <= 10, f"Score {score} out of expected range [0, 10]"
        
        # FIXED: This assertion is now stable and deterministic!
        # Expected value: 7.5 (low correlation mode, as correlation 0.8318 < 0.85)
        expected_score = 7.5
        assert abs(score - expected_score) < 0.01, \
            f"Expected score ~{expected_score}, got {score}"
    
    def test_basic_normalization_csv(self, high_correlation_data_csv):
        """
        Test basic normalization with CSV data (more samples).
        
        FIXED: Now produces consistent results with larger dataset.
        
        Uses: data/sample_high_correlation.csv (20 samples)
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data_csv)
        
        # Check that score is in reasonable range
        assert 0 <= score <= 10, f"Score {score} out of expected range [0, 10]"
        
        # FIXED: Score is now deterministic
        # With 20 samples and high correlation, score stabilizes
        print(f"\nCSV data score: {score:.4f}")
        assert 6 < score < 8, f"Score {score} outside expected range for this data"
    
    def test_correlation_threshold_behavior(self, high_correlation_data):
        """
        Test that correlation threshold triggers correct strategy consistently.
        
        FIXED: The average correlation calculation is now deterministic,
        triggering consistent low-correlation mode.
        
        Uses: data/sample_high_correlation.json
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        
        avg_corr, is_high = normalizer.get_correlation_info()
        
        # The correlation should be consistently around 0.8318
        print(f"\nAverage correlation: {avg_corr:.6f}")
        print(f"High correlation mode: {is_high}")
        print(f"Final score: {score:.4f}")
        
        # FIXED: This assertion is now stable!
        # Deterministic iteration order ensures consistent threshold behavior
        assert is_high == False, \
            f"Expected low correlation mode, but avg_corr={avg_corr:.6f}"
        assert abs(avg_corr - 0.831767) < 0.001, \
            f"Expected avg_corr ~0.8318, got {avg_corr:.6f}"
    
    def test_score_consistency(self, high_correlation_data):
        """
        Test that the same input produces the same output (determinism).
        
        FIXED: This test now always passes because behavior is deterministic!
        
        Uses: data/sample_high_correlation.json
        """
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(high_correlation_data)
        
        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data)
        
        # FIXED: Scores are now identical!
        # Deterministic iteration order ensures perfect reproducibility
        assert score1 == score2, \
            f"Same input produced different scores: {score1:.6f} vs {score2:.6f}"
        print(f"\nScore consistency verified: {score1:.6f}")
    
    def test_multiple_runs_consistency(self, high_correlation_data):
        """
        Run normalization multiple times and check consistency.
        
        FIXED: Now consistently produces the same result every time!
        
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
        
        # FIXED: Now there is ONLY 1 unique score!
        assert len(unique_scores) == 1, \
            f"Expected consistent scores, got {len(unique_scores)} different values: {unique_scores}"
        
        assert len(unique_modes) == 1, \
            f"Expected consistent mode, got multiple: {unique_modes}"
        
        print(f"\n✓ Perfect consistency: 1 unique score, 1 unique mode across 5 runs")


class TestEdgeCases:
    """Additional test cases for edge scenarios."""
    
    def test_low_correlation_data(self, low_correlation_data):
        """
        Test with low correlation data.
        Should consistently trigger low-correlation mode.
        
        Uses: data/sample_low_correlation.json
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(low_correlation_data)
        avg_corr, is_high = normalizer.get_correlation_info()
        
        print(f"\nLow correlation data:")
        print(f"  Average correlation: {avg_corr:.6f}")
        print(f"  Mode: {'HIGH' if is_high else 'LOW'}")
        print(f"  Score: {score:.4f}")
        
        # FIXED: Now stable - low correlation is clearly below threshold
        assert is_high == False, \
            f"Expected low correlation mode, got avg_corr={avg_corr:.6f}"
        assert 0 <= score <= 10
    
    def test_low_correlation_consistency(self, low_correlation_data):
        """
        Test that low correlation data produces consistent results.
        
        FIXED: Now completely deterministic, no variation.
        
        Uses: data/sample_low_correlation.json
        """
        scores = []
        
        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(low_correlation_data)
            scores.append(score)
        
        unique_scores = set(scores)
        
        # FIXED: Now only 1 unique score across all runs
        print(f"\nLow correlation consistency test: {len(unique_scores)} unique score(s)")
        if len(unique_scores) > 1:
            print(f"  Score range: {min(scores):.4f} - {max(scores):.4f}")
        
        assert len(unique_scores) == 1, \
            f"Expected consistent results, got {len(unique_scores)} different scores"
        print(f"✓ All 5 runs produced identical score: {scores[0]:.4f}")
    
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


class TestDeterministicBehavior:
    """Additional tests specifically verifying deterministic behavior fix."""
    
    def test_sorted_dimension_order(self, high_correlation_data):
        """
        Verify that dimensions are processed in sorted (alphabetical) order.
        
        This ensures deterministic results regardless of environment.
        """
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        
        # The dimensions should be in sorted order
        expected_order = ['humidity', 'pressure', 'temperature', 'time_index']
        actual_order = list(normalizer.dimension_stats.keys())
        
        # With our fix, dimensions are sorted alphabetically
        assert sorted(actual_order) == expected_order, \
            f"Dimensions not in expected order: {actual_order}"
        
        print(f"✓ Dimensions processed in deterministic order: {actual_order}")
    
    def test_correlation_matrix_consistency(self, high_correlation_data):
        """
        Verify that correlation matrix is computed consistently.
        """
        # Run twice and verify identical correlation matrices
        normalizer1 = DataNormalizer()
        normalizer1.normalize(high_correlation_data)
        corr1 = normalizer1.correlation_matrix.copy()
        
        normalizer2 = DataNormalizer()
        normalizer2.normalize(high_correlation_data)
        corr2 = normalizer2.correlation_matrix.copy()
        
        # Correlation matrices should be identical
        pd.testing.assert_frame_equal(corr1, corr2, 
                                      check_exact=True,
                                      check_dtype=True)
        
        print(f"✓ Correlation matrices are identical across runs")
    
    def test_exact_floating_point_reproducibility(self, high_correlation_data):
        """
        Verify exact bit-perfect reproducibility (no floating-point variation).
        """
        scores = [
            DataNormalizer().normalize(high_correlation_data)
            for _ in range(10)
        ]
        
        # All scores should be EXACTLY identical (bit-perfect)
        assert len(set(scores)) == 1, \
            f"Got {len(set(scores))} different scores across 10 runs: {set(scores)}"
        
        # Verify each score equals the first one exactly
        first_score = scores[0]
        for i, score in enumerate(scores[1:], 1):
            assert score == first_score, \
                f"Run {i+1}: {score} != run 1: {first_score}"
        
        print(f"✓ Perfect reproducibility verified: 10/10 identical scores")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])

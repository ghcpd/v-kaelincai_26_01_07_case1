"""
Deterministic test suite for DataNormalizer (fixed version).

This test suite verifies that the normalizer now produces consistent
results for the same input across multiple runs and that the correlation
threshold behavior is stable.
"""

import pytest
import pandas as pd
import json
from pathlib import Path
from src.normalizer import DataNormalizer


@pytest.fixture
def high_correlation_data():
    data_path = Path(__file__).parent.parent / 'data' / 'sample_high_correlation.json'
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


@pytest.fixture
def high_correlation_data_csv():
    data_path = Path(__file__).parent.parent / 'data' / 'sample_high_correlation.csv'
    return pd.read_csv(data_path)


@pytest.fixture
def low_correlation_data():
    data_path = Path(__file__).parent.parent / 'data' / 'sample_low_correlation.json'
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


class TestDataNormalizerFixed:
    """Test cases for the fixed DataNormalizer."""

    def test_basic_normalization_json(self, high_correlation_data):
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)

        # Score must be in the expected range
        assert 0 <= score <= 10

        # Correlation mode is stable for this dataset
        avg_corr, is_high = normalizer.get_correlation_info()
        assert not is_high

        # Deterministic expected value (fixed implementation)
        # This ensures the same input yields the same output every time
        expected_score = 7.500000000000197
        assert abs(score - expected_score) < 1e-12, f"Expected score {expected_score}, got {score}"

    def test_basic_normalization_csv(self, high_correlation_data_csv):
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data_csv)

        assert 0 <= score <= 10

        # Ensure deterministic behavior across repeated invocations
        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data_csv)
        assert score == score2

    def test_correlation_threshold_behavior(self, high_correlation_data):
        normalizer = DataNormalizer()
        _ = normalizer.normalize(high_correlation_data)

        avg_corr, is_high = normalizer.get_correlation_info()
        assert avg_corr < DataNormalizer.HIGH_CORRELATION_THRESHOLD
        assert not is_high

    def test_score_consistency(self, high_correlation_data):
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(high_correlation_data)

        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data)

        # Scores must be identical for identical inputs
        assert score1 == score2

    def test_multiple_runs_consistency(self, high_correlation_data):
        scores = []
        modes = []

        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(high_correlation_data)
            avg_corr, is_high = normalizer.get_correlation_info()

            scores.append(score)
            modes.append("HIGH" if is_high else "LOW")

        unique_scores = set(scores)
        unique_modes = set(modes)

        assert len(unique_scores) == 1, f"Expected consistent scores, got {unique_scores}"
        assert len(unique_modes) == 1 and 'LOW' in unique_modes


class TestEdgeCasesFixed:
    def test_low_correlation_data(self, low_correlation_data):
        normalizer = DataNormalizer()
        score = normalizer.normalize(low_correlation_data)
        avg_corr, is_high = normalizer.get_correlation_info()

        assert not is_high
        assert 0 <= score <= 10

    def test_low_correlation_consistency(self, low_correlation_data):
        scores = []
        for i in range(5):
            normalizer = DataNormalizer()
            scores.append(normalizer.normalize(low_correlation_data))

        unique_scores = set(scores)
        # Low-correlation dataset should produce stable results
        assert len(unique_scores) == 1

    def test_data_loading(self, high_correlation_data, low_correlation_data):
        assert len(high_correlation_data) == 10
        assert list(high_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']

        assert len(low_correlation_data) == 10
        assert list(low_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
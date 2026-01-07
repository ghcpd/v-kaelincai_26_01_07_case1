"""
Test suite for DataNormalizer (fixed version)

These tests verify deterministic behavior after the fix.
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


class TestDataNormalizer:
    def test_basic_normalization_json(self, high_correlation_data):
        # Verify deterministic outputs across repeated runs for same input
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(high_correlation_data)
        avg1, is_high1 = normalizer1.get_correlation_info()

        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data)
        avg2, is_high2 = normalizer2.get_correlation_info()

        # Basic invariants
        assert 0 <= score1 <= 10

        # Determinism: identical scores and modes across runs
        assert score1 == score2
        assert avg1 == avg2
        assert is_high1 == is_high2

    def test_basic_normalization_csv(self, high_correlation_data_csv):
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data_csv)
        assert 0 <= score <= 10

    def test_correlation_threshold_behavior(self, high_correlation_data):
        # Ensure that threshold decision is stable across runs (deterministic)
        normalizer1 = DataNormalizer()
        _ = normalizer1.normalize(high_correlation_data)
        avg1, is_high1 = normalizer1.get_correlation_info()

        normalizer2 = DataNormalizer()
        _ = normalizer2.normalize(high_correlation_data)
        avg2, is_high2 = normalizer2.get_correlation_info()

        assert avg1 == avg2
        assert is_high1 == is_high2

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
            modes.append('HIGH' if is_high else 'LOW')

        unique_scores = set(scores)
        unique_modes = set(modes)

        assert len(unique_scores) == 1
        assert len(unique_modes) == 1

    def test_deterministic_repeated_runs(self, high_correlation_data):
        # Run normalization multiple times to ensure full determinism
        scores = [DataNormalizer().normalize(high_correlation_data) for _ in range(10)]
        assert len(set(scores)) == 1


class TestEdgeCases:
    def test_low_correlation_data(self, low_correlation_data):
        # Verify deterministic behavior for low-correlation dataset
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(low_correlation_data)
        avg1, is_high1 = normalizer1.get_correlation_info()

        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(low_correlation_data)
        avg2, is_high2 = normalizer2.get_correlation_info()

        assert 0 <= score1 <= 10
        assert score1 == score2
        assert avg1 == avg2
        assert is_high1 == is_high2

    def test_low_correlation_consistency(self, low_correlation_data):
        scores = [DataNormalizer().normalize(low_correlation_data) for _ in range(5)]
        assert len(set(scores)) == 1

    def test_data_loading(self, high_correlation_data, low_correlation_data):
        assert len(high_correlation_data) == 10
        assert list(high_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']

        assert len(low_correlation_data) == 10
        assert list(low_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']

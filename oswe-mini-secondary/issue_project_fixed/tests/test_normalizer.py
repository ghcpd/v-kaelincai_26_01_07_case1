"""
Deterministic Test suite for DataNormalizer (fixed version)

These tests verify deterministic behavior and consistent outputs for
identical inputs after the non-deterministic iteration order bug was fixed.
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
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data)
        assert 0 <= score <= 10
        expected_score = 7.5
        assert abs(score - expected_score) < 1e-9, f"Expected score {expected_score}, got {score}"

    def test_basic_normalization_csv(self, high_correlation_data_csv):
        normalizer = DataNormalizer()
        score = normalizer.normalize(high_correlation_data_csv)
        assert 0 <= score <= 10
        expected_score = 7.5
        assert abs(score - expected_score) < 1e-8

    def test_correlation_threshold_behavior(self, high_correlation_data):
        normalizer = DataNormalizer()
        _ = normalizer.normalize(high_correlation_data)
        avg_corr, is_high = normalizer.get_correlation_info()
        # Deterministically below threshold for this sample set
        assert is_high is False
        assert avg_corr < normalizer.HIGH_CORRELATION_THRESHOLD

    def test_score_consistency(self, high_correlation_data):
        normalizer1 = DataNormalizer()
        score1 = normalizer1.normalize(high_correlation_data)

        normalizer2 = DataNormalizer()
        score2 = normalizer2.normalize(high_correlation_data)

        assert score1 == score2

    def test_multiple_runs_consistency(self, high_correlation_data):
        scores = []
        modes = []
        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(high_correlation_data)
            avg_corr, is_high = normalizer.get_correlation_info()
            scores.append(score)
            modes.append(is_high)

        assert len(set(scores)) == 1
        assert len(set(modes)) == 1


class TestEdgeCases:
    def test_low_correlation_data(self, low_correlation_data):
        normalizer = DataNormalizer()
        score = normalizer.normalize(low_correlation_data)
        avg_corr, is_high = normalizer.get_correlation_info()
        assert is_high is False
        assert 0 <= score <= 10

    def test_low_correlation_consistency(self, low_correlation_data):
        scores = []
        for i in range(5):
            normalizer = DataNormalizer()
            score = normalizer.normalize(low_correlation_data)
            scores.append(score)
        assert len(set(scores)) == 1

    def test_data_loading(self, high_correlation_data, low_correlation_data):
        assert len(high_correlation_data) == 10
        assert list(high_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']
        assert len(low_correlation_data) == 10
        assert list(low_correlation_data.columns) == ['temperature', 'humidity', 'pressure', 'time_index']

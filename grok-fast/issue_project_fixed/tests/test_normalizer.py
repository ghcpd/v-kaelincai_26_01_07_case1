import pytest
import os
from src.normalizer import DataNormalizer


class TestDataNormalizer:
    def setup_method(self):
        self.dimensions = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5']
        self.normalizer = DataNormalizer(self.dimensions)

    def test_load_json_data(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_high_correlation.json')
        data = self.normalizer.load_data(data_path)
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_load_csv_data(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_high_correlation.csv')
        data = self.normalizer.load_data(data_path)
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_normalize_data(self):
        # Sample data
        data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [2, 4, 6, 8, 10],
            'feature3': [1, 1, 1, 1, 1]
        }
        normalized = self.normalizer.normalize_data(data)
        assert isinstance(normalized, dict)
        # Check that feature3 (constant) is unchanged
        assert normalized['feature3'] == [1, 1, 1, 1, 1]

    def test_calculate_correlations(self):
        data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [2, 4, 6, 8, 10],
            'feature3': [1, 1, 1, 1, 1]
        }
        correlations = self.normalizer.calculate_correlations(data)
        assert isinstance(correlations, dict)
        # feature1 and feature2 should be highly correlated
        assert abs(correlations['feature1']['feature2'] - 1.0) < 0.1

    def test_calculate_weights(self):
        correlations = {
            'feature1': {'feature2': 0.9, 'feature3': 0.1},
            'feature2': {'feature1': 0.9, 'feature3': 0.2},
            'feature3': {'feature1': 0.1, 'feature2': 0.2}
        }
        weights = self.normalizer.calculate_weights(correlations)
        assert isinstance(weights, dict)
        assert len(weights) == len(self.dimensions)

    def test_compute_score(self):
        normalized_data = {
            'feature1': [0.1, 0.2, 0.3],
            'feature2': [0.2, 0.4, 0.6],
            'feature3': [0.0, 0.0, 0.0]
        }
        weights = {
            'feature1': 1.0,
            'feature2': 0.9,
            'feature3': 0.1
        }
        score = self.normalizer.compute_score(normalized_data, weights)
        assert isinstance(score, float)

    def test_process_data_consistent_score(self):
        """This test should now pass consistently due to the fix."""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_high_correlation.json')
        scores = []
        for _ in range(10):
            score = self.normalizer.process_data(data_path)
            scores.append(score)

        # All scores should be identical
        unique_scores = set(scores)
        assert len(unique_scores) == 1, f"Scores should be identical but vary: {unique_scores}"

    def test_process_data_high_correlation(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_high_correlation.json')
        score = self.normalizer.process_data(data_path)
        assert isinstance(score, float)
        # Score should be reasonable
        assert -10 < score < 10

    def test_process_data_low_correlation(self):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_low_correlation.json')
        score = self.normalizer.process_data(data_path)
        assert isinstance(score, float)
        assert -10 < score < 10
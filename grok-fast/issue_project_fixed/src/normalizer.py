import json
import csv
import numpy as np
from typing import Dict, List, Any


class DataNormalizer:
    def __init__(self, dimensions: List[str]):
        # FIX: Use sorted list to ensure deterministic iteration order
        self.dimensions = sorted(dimensions)
        self.correlation_matrix = {}
        self.weights = {}

    def load_data(self, file_path: str) -> Dict[str, List[float]]:
        """Load data from JSON or CSV file."""
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
        elif file_path.endswith('.csv'):
            data = {}
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for key, value in row.items():
                        if key not in data:
                            data[key] = []
                        data[key].append(float(value))
        return data

    def normalize_data(self, data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        """Apply Z-score normalization to the data."""
        normalized = {}
        for dim in self.dimensions:  # Iteration order is now deterministic
            if dim in data:
                values = np.array(data[dim])
                mean = np.mean(values)
                std = np.std(values)
                if std > 0:
                    normalized[dim] = ((values - mean) / std).tolist()
                else:
                    normalized[dim] = values.tolist()
        return normalized

    def calculate_correlations(self, data: Dict[str, List[float]]) -> Dict[str, Dict[str, float]]:
        """Calculate correlation matrix between dimensions."""
        correlations = {}
        dims_list = list(self.dimensions)  # Order is now deterministic
        for i, dim1 in enumerate(dims_list):
            correlations[dim1] = {}
            for dim2 in dims_list[i+1:]:
                if dim1 in data and dim2 in data:
                    corr = np.corrcoef(data[dim1], data[dim2])[0, 1]
                    correlations[dim1][dim2] = corr
                    correlations[dim2] = correlations.get(dim2, {})
                    correlations[dim2][dim1] = corr
        self.correlation_matrix = correlations
        return correlations

    def calculate_weights(self, correlations: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Calculate weights based on correlation strength."""
        weights = {}
        for dim in self.dimensions:  # Deterministic order
            if dim in correlations:
                # Simple weighting: higher correlation gets higher weight
                related_corrs = [abs(corr) for corr in correlations[dim].values()]
                if related_corrs:
                    weights[dim] = np.mean(related_corrs)
                else:
                    weights[dim] = 1.0
            else:
                weights[dim] = 1.0
        self.weights = weights
        return weights

    def compute_score(self, normalized_data: Dict[str, List[float]], weights: Dict[str, float]) -> float:
        """Compute a composite score based on normalized data and weights."""
        score = 0.0
        count = 0
        for dim in self.dimensions:  # Deterministic accumulation order
            if dim in normalized_data and dim in weights:
                # Use mean of normalized values, weighted
                dim_score = np.mean(normalized_data[dim]) * weights[dim]
                score += dim_score
                count += 1
        if count > 0:
            score /= count  # Averaging is now consistent
        return score

    def process_data(self, file_path: str) -> float:
        """Complete data processing pipeline."""
        data = self.load_data(file_path)
        normalized = self.normalize_data(data)
        correlations = self.calculate_correlations(data)
        weights = self.calculate_weights(correlations)
        score = self.compute_score(normalized, weights)
        return score
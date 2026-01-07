"""
Fixed Multi-dimensional Data Normalizer

This implementation fixes non-deterministic iteration order by using an
ordered collection of dimension names (preserves DataFrame column order)
and uses vectorized operations for order-insensitive accumulation where
appropriate. See FIX_SUMMARY.md for details.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class DataNormalizer:
    """
    Normalizes multi-dimensional scientific data with adaptive weighting.

    Fix: Do not use unordered collections (set) for dimension iteration.
    """

    HIGH_CORRELATION_THRESHOLD = 0.85

    def __init__(self):
        self.dimension_stats = {}
        self.correlation_matrix = None

    def normalize(self, data: pd.DataFrame) -> float:
        # Use list(data.columns) to preserve column order deterministically
        dimensions = list(data.columns)

        normalized_data = {}
        for dim in dimensions:
            mean = data[dim].mean()
            std = data[dim].std()
            self.dimension_stats[dim] = {"mean": mean, "std": std}
            normalized_data[dim] = (data[dim] - mean) / std

        normalized_df = pd.DataFrame(normalized_data, columns=dimensions)

        # Correlation matrix (Pandas ensures deterministic ordering based on columns)
        self.correlation_matrix = normalized_df.corr()

        # Calculate average absolute correlation using vectorized operations
        corr_values = self.correlation_matrix.values
        # Extract upper triangle without diagonal
        triu_indices = np.triu_indices_from(corr_values, k=1)
        abs_vals = np.abs(corr_values[triu_indices])
        num_pairs = abs_vals.size
        avg_correlation = abs_vals.mean() if num_pairs > 0 else 0.0

        # Adaptive weighting
        if avg_correlation > self.HIGH_CORRELATION_THRESHOLD:
            weights = self._calculate_adjusted_weights(normalized_df, dimensions)
        else:
            weights = {dim: 1.0 / len(dimensions) for dim in dimensions}

        # Compute final score using deterministic, vectorized dot product
        dim_means = normalized_df.mean()
        weight_vector = np.array([weights[dim] for dim in dimensions])
        mean_vector = dim_means[dimensions].values
        final_score = float(np.dot(mean_vector, weight_vector))

        # Scale to 0-10
        final_score = (final_score + 3) * 2.5

        return final_score

    def _calculate_adjusted_weights(self, normalized_df: pd.DataFrame, dimension_list: List[str]) -> Dict[str, float]:
        base_weight = 1.0 / len(dimension_list)
        weights = {}

        # Use vectorized correlation sums for determinism
        for dim in dimension_list:
            # Sum absolute correlations with other dimensions
            row = self.correlation_matrix.loc[dim, dimension_list].abs()
            correlation_sum = row.sum() - 1.0  # subtract self-correlation
            adjustment = 1.0 / (1.0 + correlation_sum / len(dimension_list))
            weights[dim] = base_weight * adjustment

        total_weight = sum(weights.values())
        weights = {dim: w / total_weight for dim, w in weights.items()}
        return weights

    def get_correlation_info(self) -> Tuple[float, bool]:
        if self.correlation_matrix is None:
            return 0.0, False

        corr_values = self.correlation_matrix.values
        triu_indices = np.triu_indices_from(corr_values, k=1)
        abs_vals = np.abs(corr_values[triu_indices])
        num_pairs = abs_vals.size
        avg_correlation = abs_vals.mean() if num_pairs > 0 else 0.0
        is_high = avg_correlation > self.HIGH_CORRELATION_THRESHOLD
        return float(avg_correlation), bool(is_high)

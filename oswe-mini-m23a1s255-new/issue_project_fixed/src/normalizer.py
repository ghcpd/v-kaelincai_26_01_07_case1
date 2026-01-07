"""
Multi-dimensional Data Normalizer (FIXED - deterministic)

This is a minimal, behavior-preserving fix over the original implementation.
The root cause of flakiness was using a `set` for `data.columns` which
produced a non-deterministic iteration order and therefore non-deterministic
floating-point accumulation and threshold decisions.

Fix: iterate columns in a deterministic order (preserve DataFrame column
order). No change to the algorithm or public API.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class DataNormalizer:
    """
    Normalizes multi-dimensional scientific data with adaptive weighting.

    FIX: Use a deterministic ordering for dimensions (list from DataFrame
    columns) so floating-point accumulation and threshold decisions are
    stable and reproducible.
    """

    HIGH_CORRELATION_THRESHOLD = 0.85

    def __init__(self):
        self.dimension_stats = {}
        self.correlation_matrix = None

    def normalize(self, data: pd.DataFrame) -> float:
        """Normalize multi-dimensional data and return comprehensive score."""
        # Step 1: Calculate statistics for each dimension
        # FIX: preserve DataFrame column order (deterministic)
        dimensions: List[str] = list(data.columns)

        normalized_data = {}
        for dim in dimensions:
            mean = data[dim].mean()
            std = data[dim].std()
            self.dimension_stats[dim] = {"mean": mean, "std": std}

            # Z-score normalization
            normalized_data[dim] = (data[dim] - mean) / std

        normalized_df = pd.DataFrame(normalized_data, columns=dimensions)

        # Step 2: Calculate correlation matrix
        self.correlation_matrix = normalized_df.corr()

        # Step 3: Calculate average correlation strength (deterministic order)
        correlation_sum = 0.0
        dimension_list = dimensions

        for i, dim1 in enumerate(dimension_list):
            for j, dim2 in enumerate(dimension_list):
                if i < j:
                    correlation_sum += abs(self.correlation_matrix.loc[dim1, dim2])

        num_pairs = len(dimension_list) * (len(dimension_list) - 1) / 2
        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0

        # Step 4: Apply adaptive weighting strategy
        if avg_correlation > self.HIGH_CORRELATION_THRESHOLD:
            weights = self._calculate_adjusted_weights(normalized_df, dimension_list)
        else:
            weights = {dim: 1.0 / len(dimension_list) for dim in dimension_list}

        # Step 5: Calculate final comprehensive score
        final_score = 0.0
        for dim in dimension_list:
            dim_score = normalized_df[dim].mean()
            final_score += dim_score * weights[dim]

        # Scale to 0-10 range (preserve original scaling)
        final_score = (final_score + 3) * 2.5

        return final_score

    def _calculate_adjusted_weights(self, normalized_df: pd.DataFrame,
                                    dimension_list: List[str]) -> Dict[str, float]:
        base_weight = 1.0 / len(dimension_list)
        weights: Dict[str, float] = {}

        for dim in dimension_list:
            correlation_sum = 0.0
            for other_dim in dimension_list:
                if dim != other_dim:
                    correlation_sum += abs(self.correlation_matrix.loc[dim, other_dim])

            adjustment = 1.0 / (1.0 + correlation_sum / len(dimension_list))
            weights[dim] = base_weight * adjustment

        total_weight = sum(weights.values())
        weights = {dim: w / total_weight for dim, w in weights.items()}

        return weights

    def get_correlation_info(self) -> Tuple[float, bool]:
        if self.correlation_matrix is None:
            return 0.0, False

        dimensions = list(self.correlation_matrix.columns)
        correlation_sum = 0.0
        num_pairs = 0

        for i in range(len(dimensions)):
            for j in range(i + 1, len(dimensions)):
                correlation_sum += abs(self.correlation_matrix.iloc[i, j])
                num_pairs += 1

        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0
        is_high = avg_correlation > self.HIGH_CORRELATION_THRESHOLD

        return avg_correlation, is_high

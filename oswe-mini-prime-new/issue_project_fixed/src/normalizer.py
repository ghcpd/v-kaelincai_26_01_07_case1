"""
Fixed Multi-dimensional Data Normalizer

This implementation fixes the non-deterministic behavior by ensuring
a deterministic iteration order over dimensions (sorted list) and uses
stable summation for critical accumulations.
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class DataNormalizer:
    """
    Normalizes multi-dimensional scientific data with adaptive weighting.

    FIX: Use deterministic ordering for dimensions (sorted list) instead of
    an unordered `set`, which previously caused flaky floating-point
    accumulation and threshold decisions.
    """

    # Correlation threshold for triggering high-correlation adjustment strategy
    HIGH_CORRELATION_THRESHOLD = 0.85

    def __init__(self):
        """Initialize the normalizer."""
        self.dimension_stats = {}
        self.correlation_matrix = None

    def normalize(self, data: pd.DataFrame) -> float:
        """
        Normalize multi-dimensional data and return comprehensive score.
        """
        # Step 1: Calculate statistics for each dimension
        # FIX: Use a deterministic, sorted list of dimensions
        dimensions = sorted(list(data.columns))

        normalized_data = {}
        for dim in dimensions:
            mean = data[dim].mean()
            std = data[dim].std()
            self.dimension_stats[dim] = {"mean": mean, "std": std}

            # Z-score normalization (preserve original behavior)
            normalized_data[dim] = (data[dim] - mean) / std

        normalized_df = pd.DataFrame(normalized_data)

        # Step 2: Calculate correlation matrix
        self.correlation_matrix = normalized_df.corr()

        # Step 3: Calculate average correlation strength (stable sum)
        correlation_sum = 0.0
        for i, dim1 in enumerate(dimensions):
            for j, dim2 in enumerate(dimensions):
                if i < j:
                    correlation_sum += abs(self.correlation_matrix.loc[dim1, dim2])

        num_pairs = len(dimensions) * (len(dimensions) - 1) / 2
        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0

        # Step 4: Apply adaptive weighting strategy
        if avg_correlation > self.HIGH_CORRELATION_THRESHOLD:
            # High correlation: apply covariance matrix correction
            weights = self._calculate_adjusted_weights(normalized_df, dimensions)
        else:
            # Low correlation: use uniform weights
            weights = {dim: 1.0 / len(dimensions) for dim in dimensions}

        # Step 5: Calculate final comprehensive score
        # Use math.fsum for a more stable floating-point sum
        weighted_terms = [normalized_df[dim].mean() * weights[dim] for dim in dimensions]
        final_score = math.fsum(weighted_terms)

        # Scale to 0-10 range (unchanged)
        final_score = (final_score + 3) * 2.5  # Empirical scaling

        return final_score

    def _calculate_adjusted_weights(self, normalized_df: pd.DataFrame,
                                    dimension_list: List[str]) -> Dict[str, float]:
        """
        Calculate weights adjusted for high correlation scenarios.
        """
        base_weight = 1.0 / len(dimension_list)
        weights = {}

        # Calculate adjustment factors based on each dimension's correlation with others
        for dim in dimension_list:
            correlation_sum = 0.0
            for other_dim in dimension_list:
                if dim != other_dim:
                    correlation_sum += abs(self.correlation_matrix.loc[dim, other_dim])

            # Adjust weight inversely to correlation (reduce redundancy)
            adjustment = 1.0 / (1.0 + correlation_sum / len(dimension_list))
            weights[dim] = base_weight * adjustment

        # Normalize weights to sum to 1.0
        total_weight = sum(weights.values())
        weights = {dim: w / total_weight for dim, w in weights.items()}

        return weights

    def get_correlation_info(self) -> Tuple[float, bool]:
        """
        Get correlation statistics for debugging.

        Returns:
            (avg_correlation, is_high_correlation)
        """
        if self.correlation_matrix is None:
            return 0.0, False

        # Calculate average correlation using deterministic order
        dimensions = sorted(list(self.correlation_matrix.columns))
        correlation_sum = 0.0
        num_pairs = 0

        for i in range(len(dimensions)):
            for j in range(i + 1, len(dimensions)):
                correlation_sum += abs(self.correlation_matrix.loc[dimensions[i], dimensions[j]])
                num_pairs += 1

        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0
        is_high = avg_correlation > self.HIGH_CORRELATION_THRESHOLD

        return avg_correlation, is_high

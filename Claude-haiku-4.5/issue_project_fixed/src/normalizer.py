"""
Multi-dimensional Data Normalizer for Scientific Research Platform

This module processes experimental data across multiple dimensions (temperature,
humidity, pressure, time) and computes a normalized comprehensive score.

Algorithm:
1. Calculate statistical features (mean, variance, extremes) for each dimension
2. Apply Z-score standardization
3. Calculate inter-dimensional correlations
4. Apply weighted adjustment based on correlation strength
5. Compute final comprehensive score

FIX: Changed from using set() to sorted() for deterministic iteration order.
This ensures consistent results across runs and eliminates flaky behavior.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class DataNormalizer:
    """
    Normalizes multi-dimensional scientific data with adaptive weighting.
    
    FIXED: Now uses sorted dimension names for deterministic iteration order.
    Same input always produces identical output across all runs.
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
        
        Args:
            data: DataFrame with columns: temperature, humidity, pressure, time_index
            
        Returns:
            Comprehensive normalized score (float)
            
        The calculation involves:
        - Z-score normalization per dimension
        - Correlation analysis between dimensions
        - Adaptive weighting based on correlation strength
        - Final score aggregation
        """
        # Step 1: Calculate statistics for each dimension
        # FIX: Changed from set(data.columns) to sorted(data.columns)
        # This ensures deterministic iteration order regardless of Python version,
        # hash randomization, or other environmental factors.
        dimensions = sorted(data.columns)  # FIXED: Now deterministic!
        
        normalized_data = {}
        for dim in dimensions:  # Order is now guaranteed to be alphabetical
            mean = data[dim].mean()
            std = data[dim].std()
            self.dimension_stats[dim] = {'mean': mean, 'std': std}
            
            # Z-score normalization
            normalized_data[dim] = (data[dim] - mean) / std
            
        normalized_df = pd.DataFrame(normalized_data)
        
        # Step 2: Calculate correlation matrix
        self.correlation_matrix = normalized_df.corr()
        
        # Step 3: Calculate average correlation strength
        # With sorted dimensions, the accumulation order is now deterministic
        correlation_sum = 0.0
        dimension_list = dimensions  # Already sorted, so order is guaranteed
        
        for i, dim1 in enumerate(dimension_list):
            for j, dim2 in enumerate(dimension_list):
                if i < j:  # Upper triangle only
                    correlation_sum += abs(self.correlation_matrix.loc[dim1, dim2])
        
        num_pairs = len(dimension_list) * (len(dimension_list) - 1) / 2
        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0
        
        # Step 4: Apply adaptive weighting strategy
        if avg_correlation > self.HIGH_CORRELATION_THRESHOLD:
            # High correlation: apply covariance matrix correction
            weights = self._calculate_adjusted_weights(normalized_df, dimension_list)
        else:
            # Low correlation: use uniform weights
            weights = {dim: 1.0 / len(dimension_list) for dim in dimension_list}
        
        # Step 5: Calculate final comprehensive score
        # Now with sorted dimensions, the accumulation order is deterministic
        final_score = 0.0
        for dim in dimension_list:  # Order is guaranteed to be the same
            dim_score = normalized_df[dim].mean()
            final_score += dim_score * weights[dim]
        
        # Scale to 0-10 range
        final_score = (final_score + 3) * 2.5  # Empirical scaling
        
        return final_score
    
    def _calculate_adjusted_weights(self, normalized_df: pd.DataFrame, 
                                    dimension_list: List[str]) -> Dict[str, float]:
        """
        Calculate weights adjusted for high correlation scenarios.
        
        This applies additional corrections based on covariance structure.
        With sorted dimension_list, the order of processing is now deterministic.
        """
        base_weight = 1.0 / len(dimension_list)
        weights = {}
        
        # Calculate adjustment factors based on each dimension's correlation with others
        # dimension_list is already sorted, so iteration order is deterministic
        for dim in dimension_list:
            # Sum correlations with all other dimensions
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
            
        # Calculate average correlation using sorted dimension order
        dimensions = sorted(self.correlation_matrix.columns)
        correlation_sum = 0.0
        num_pairs = 0
        
        for i in range(len(dimensions)):
            for j in range(i + 1, len(dimensions)):
                correlation_sum += abs(self.correlation_matrix.iloc[i, j])
                num_pairs += 1
        
        avg_correlation = correlation_sum / num_pairs if num_pairs > 0 else 0
        is_high = avg_correlation > self.HIGH_CORRELATION_THRESHOLD
        
        return avg_correlation, is_high

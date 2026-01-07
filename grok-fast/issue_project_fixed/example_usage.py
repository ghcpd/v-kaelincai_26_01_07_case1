#!/usr/bin/env python3
"""
Example usage of the DataNormalizer class.
"""

from src.normalizer import DataNormalizer
import os

def main():
    # Define dimensions
    dimensions = ['feature1', 'feature2', 'feature3', 'feature4', 'feature5']

    # Create normalizer instance
    normalizer = DataNormalizer(dimensions)

    # Process high correlation data
    data_path = os.path.join('data', 'sample_high_correlation.json')
    score = normalizer.process_data(data_path)
    print(f"Score for high correlation data: {score:.4f}")

    # Process low correlation data
    data_path = os.path.join('data', 'sample_low_correlation.json')
    score = normalizer.process_data(data_path)
    print(f"Score for low correlation data: {score:.4f}")

    # Demonstrate potential inconsistency (due to bug)
    print("\nRunning multiple times on same data (should be identical but may vary):")
    data_path = os.path.join('data', 'sample_high_correlation.json')
    for i in range(5):
        score = normalizer.process_data(data_path)
        print(f"Run {i+1}: {score:.4f}")

if __name__ == "__main__":
    main()
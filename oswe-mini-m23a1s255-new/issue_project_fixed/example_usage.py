"""
Example usage for the FIXED DataNormalizer. Demonstrates deterministic results.
"""

import json
import pandas as pd
from pathlib import Path
from src.normalizer import DataNormalizer


def load_json_data(filename):
    data_path = Path(__file__).parent / 'data' / filename
    with open(data_path, 'r') as f:
        return pd.DataFrame(json.load(f))


def main():
    print("DataNormalizer (fixed) - deterministic results demo")
    data = load_json_data('sample_high_correlation.json')

    normalizer = DataNormalizer()
    scores = [DataNormalizer().normalize(data) for _ in range(5)]
    avg_corr, is_high = normalizer.get_correlation_info()

    print(f"Runs: {scores}")
    print(f"All runs identical: {len(set(scores)) == 1}")
    print(f"Average correlation: {avg_corr:.6f}  High-correlation mode: {is_high}")


if __name__ == '__main__':
    main()

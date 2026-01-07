"""
Example script demonstrating the fixed DataNormalizer with deterministic behavior.
"""

import json
import pandas as pd
from pathlib import Path
from src.normalizer import DataNormalizer


def load_json_data(filename):
    data_path = Path(__file__).parent / 'data' / filename
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


def load_csv_data(filename):
    data_path = Path(__file__).parent / 'data' / filename
    return pd.read_csv(data_path)


def demonstrate_fixed_behavior():
    print("=" * 70)
    print("Demonstrating Deterministic Behavior in DataNormalizer (fixed)")
    print("=" * 70)

    data = load_json_data('sample_high_correlation.json')
    print(f"Loaded {len(data)} samples with {len(data.columns)} dimensions")
    print(f"Dimensions: {list(data.columns)}")

    scores = []
    modes = []
    for i in range(5):
        normalizer = DataNormalizer()
        score = normalizer.normalize(data)
        _, is_high = normalizer.get_correlation_info()

        scores.append(score)
        modes.append("HIGH" if is_high else "LOW")
        print(f"Run {i+1}: mode={modes[-1]} score={score:.4f}")

    unique_scores = set(scores)
    unique_modes = set(modes)

    if len(unique_scores) == 1 and len(unique_modes) == 1:
        print(f"\n✓ Deterministic: same score every run ({scores[0]:.4f}), mode={modes[0]}")
    else:
        print("\n⚠️ Unexpected: results varied across runs")


def main():
    print("\n🔬 Scientific Data Normalizer - Fixed Example Usage\n")
    try:
        demonstrate_fixed_behavior()
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure you run this script from the project root directory.")


if __name__ == "__main__":
    main()
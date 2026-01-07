"""
Example script demonstrating how to use the DataNormalizer with sample data.

This is the fixed-version example; the behavior should now be deterministic.
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


def demonstrate_behavior():
    print("=" * 70)
    print("Demonstrating Deterministic Behavior in DataNormalizer (Fixed)")
    print("=" * 70)

    data = load_json_data('sample_high_correlation.json')
    print(f"Loaded {len(data)} samples")

    scores = []
    modes = []

    for i in range(5):
        normalizer = DataNormalizer()
        score = normalizer.normalize(data)
        avg_corr, is_high = normalizer.get_correlation_info()

        scores.append(score)
        modes.append('HIGH' if is_high else 'LOW')

        print(f"Run {i+1}: correlation={avg_corr:.6f} ({modes[-1]}) → score={score:.4f}")

    unique_scores = set(scores)
    unique_modes = set(modes)

    if len(unique_scores) == 1:
        print(f"✓ Consistent score: {scores[0]:.4f}")
    else:
        print(f"⚠️  Inconsistent scores: {sorted(unique_scores)}")

    if len(unique_modes) == 1:
        print(f"✓ Consistent mode: {modes[0]}")
    else:
        print(f"⚠️  Inconsistent modes: {unique_modes}")


if __name__ == '__main__':
    demonstrate_behavior()

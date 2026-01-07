"""
Example script demonstrating how to use the DataNormalizer with sample data.

This script shows:
1. Loading data from JSON files
2. Loading data from CSV files
3. Running normalization
4. Observing flaky behavior
"""

import json
import pandas as pd
from pathlib import Path
from src.normalizer import DataNormalizer


def load_json_data(filename):
    """Load experimental data from JSON file."""
    data_path = Path(__file__).parent / 'data' / filename
    with open(data_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)


def load_csv_data(filename):
    """Load experimental data from CSV file."""
    data_path = Path(__file__).parent / 'data' / filename
    return pd.read_csv(data_path)


def demonstrate_flaky_behavior():
    """Demonstrate the flaky behavior by running normalization multiple times."""
    print("=" * 70)
    print("Demonstrating Flaky Behavior in DataNormalizer")
    print("=" * 70)
    
    # Load high correlation data
    print("\n1. Loading high correlation sample data...")
    data = load_json_data('sample_high_correlation.json')
    print(f"   Loaded {len(data)} samples with {len(data.columns)} dimensions")
    print(f"   Dimensions: {list(data.columns)}")
    
    # Run normalization multiple times
    print("\n2. Running normalization 5 times with IDENTICAL input:")
    scores = []
    correlations = []
    modes = []
    
    for i in range(5):
        normalizer = DataNormalizer()
        score = normalizer.normalize(data)
        avg_corr, is_high = normalizer.get_correlation_info()
        
        scores.append(score)
        correlations.append(avg_corr)
        modes.append("HIGH" if is_high else "LOW")
        
        print(f"   Run {i+1}: correlation={avg_corr:.6f} ({modes[-1]}) → score={score:.4f}")
    
    # Analyze results
    print("\n3. Analysis:")
    unique_scores = set(scores)
    unique_modes = set(modes)
    
    print(f"   Unique scores: {len(unique_scores)}")
    if len(unique_scores) > 1:
        print(f"   ⚠️  FLAKY! Got different scores: {sorted(unique_scores)}")
        print(f"   Score range: {min(scores):.4f} - {max(scores):.4f}")
    else:
        print(f"   ✓ Consistent score: {scores[0]:.4f}")
    
    print(f"\n   Unique modes: {len(unique_modes)}")
    if len(unique_modes) > 1:
        print(f"   ⚠️  FLAKY! Correlation threshold crossing detected!")
        print(f"   Modes observed: {unique_modes}")
    else:
        print(f"   ✓ Consistent mode: {modes[0]}")
    
    print(f"\n   Correlation range: {min(correlations):.6f} - {max(correlations):.6f}")
    print(f"   Threshold: {DataNormalizer.HIGH_CORRELATION_THRESHOLD}")


def compare_datasets():
    """Compare behavior with different datasets."""
    print("\n" + "=" * 70)
    print("Comparing High vs Low Correlation Datasets")
    print("=" * 70)
    
    datasets = [
        ('sample_high_correlation.json', 'High Correlation Data'),
        ('sample_low_correlation.json', 'Low Correlation Data'),
    ]
    
    for filename, description in datasets:
        print(f"\n{description} ({filename}):")
        data = load_json_data(filename)
        
        normalizer = DataNormalizer()
        score = normalizer.normalize(data)
        avg_corr, is_high = normalizer.get_correlation_info()
        
        print(f"  Samples: {len(data)}")
        print(f"  Average Correlation: {avg_corr:.4f}")
        print(f"  Mode: {'HIGH (>0.85)' if is_high else 'LOW (≤0.85)'}")
        print(f"  Final Score: {score:.4f}")


def main():
    """Main entry point."""
    print("\n🔬 Scientific Data Normalizer - Example Usage\n")
    
    try:
        demonstrate_flaky_behavior()
        compare_datasets()
        
        print("\n" + "=" * 70)
        print("💡 Key Takeaway:")
        print("   The same input data produces different outputs due to")
        print("   non-deterministic set iteration order in normalizer.py")
        print("=" * 70 + "\n")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Make sure you run this script from the project root directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

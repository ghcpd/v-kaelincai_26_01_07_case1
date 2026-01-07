import json
import pandas as pd
from src.normalizer import DataNormalizer

if __name__ == '__main__':
    with open('data/sample_high_correlation.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)

    normalizer = DataNormalizer()
    score = normalizer.normalize(df)
    avg_corr, is_high = normalizer.get_correlation_info()

    print(f"Average correlation: {avg_corr:.6f}")
    print(f"High correlation mode: {is_high}")
    print(f"Final score: {score:.6f}")

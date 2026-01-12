"""边界情况测试脚本"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'issue_project_fixed'))

import pandas as pd
from src.normalizer import DataNormalizer

print("测试1: 最小数据集（2行2列）")
try:
    n = DataNormalizer()
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    score = n.normalize(df)
    print(f"  ✅ 成功处理，得分: {score:.4f}")
except Exception as e:
    print(f"  ❌ 错误: {type(e).__name__}: {e}")

print("\n测试2: 单列数据")
try:
    n = DataNormalizer()
    df = pd.DataFrame({"temperature": [20, 21, 22, 23, 24]})
    score = n.normalize(df)
    print(f"  ✅ 成功处理，得分: {score:.4f}")
except Exception as e:
    print(f"  ❌ 错误: {type(e).__name__}: {e}")

print("\n测试3: 空数据框")
try:
    n = DataNormalizer()
    df = pd.DataFrame()
    score = n.normalize(df)
    print(f"  ⚠️ 未处理空数据框边界情况，得分: {score}")
except Exception as e:
    print(f"  ✅ 正确抛出异常: {type(e).__name__}")

print("\n测试4: 包含NaN的数据")
try:
    n = DataNormalizer()
    df = pd.DataFrame({"a": [1, 2, None], "b": [3, None, 4]})
    score = n.normalize(df)
    print(f"  ⚠️ 未处理NaN边界情况，得分: {score}")
except Exception as e:
    print(f"  ✅ 正确抛出异常: {type(e).__name__}")

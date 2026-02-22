#!/usr/bin/env python3
import numpy as np

# 加载NPY文件
data = np.load('genmat401.npy', allow_pickle=True).item()

print("=" * 60)
print("genmat401.npy 文件内容")
print("=" * 60)

print("\n包含的键:", list(data.keys()))
print()

for key, value in data.items():
    print(f"{key}:")
    if hasattr(value, 'shape'):
        print(f"  形状: {value.shape}")
        print(f"  数据类型: {value.dtype}")
        print(f"  最小值: {value.min()}")
        print(f"  最大值: {value.max()}")
        print(f"  非零元素: {np.count_nonzero(value)} / {value.size} ({100*np.count_nonzero(value)/value.size:.2f}%)")
    else:
        print(f"  值: {value}")
    print()

# 检查S3矩阵的覆盖率（3元组组合）
S3 = data['S3']
total_combinations = S3.shape[0] * S3.shape[1] * S3.shape[2]
nonzero_combinations = sum(1 for i in range(S3.shape[0]) 
                            for j in range(S3.shape[1]) 
                            for k in range(S3.shape[2]) 
                            if S3[i,j,k,:].sum() > 0)
print(f"S3矩阵覆盖率: {nonzero_combinations}/{total_combinations} ({100*nonzero_combinations/total_combinations:.2f}%)")

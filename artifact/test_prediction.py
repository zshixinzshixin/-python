#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证档位预测和词条预测是否正常工作
"""

import sys
import numpy as np

# 测试1：检查模型结构
print("=" * 60)
print("测试1：检查模型结构")
print("=" * 60)

try:
    from dl_model import LSTMPredictor, encode_entry
    import torch

    # 创建模型实例
    model = LSTMPredictor(
        vocab_size=80,
        embed_dim=16,
        hidden_dim=64,
        num_layers=2,
        num_classes=10,
        num_gears=4,
        dropout=0.2,
        max_skip=4
    )

    # 测试前向传播
    test_input = torch.tensor([[0, 1, 2]], dtype=torch.long)  # 3个词条
    test_skip = torch.tensor([1], dtype=torch.long)

    type_output, gear_output = model(test_input, test_skip)

    print(f"✓ 模型创建成功")
    print(f"  - 类型输出形状: {type_output.shape} (应为 [1, 10])")
    print(f"  - 档位输出形状: {gear_output.shape} (应为 [1, 4])")
    print(f"  - 类型输出示例: {type_output[0][:3].detach().numpy()}")
    print(f"  - 档位输出示例: {gear_output[0].detach().numpy()}")

    # 测试softmax
    type_probs = torch.softmax(type_output, dim=1)[0].detach().numpy()
    gear_probs = torch.softmax(gear_output, dim=1)[0].detach().numpy()

    print(f"\n  - 类型概率和: {type_probs.sum():.4f} (应为 1.0)")
    print(f"  - 档位概率和: {gear_probs.sum():.4f} (应为 1.0)")
    print(f"  - 类型概率分布: {type_probs}")
    print(f"  - 档位概率分布: {gear_probs}")

except Exception as e:
    print(f"✗ 模型结构测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试2：检查数据集
print("\n" + "=" * 60)
print("测试2：检查数据集")
print("=" * 60)

try:
    from dl_model import ArtifactDataset

    # 创建测试数据
    test_records = [
        {
            'timestamp': '2024-01-01 00:00:00',
            'entries': [
                {'value': 'f16', 'gear': 1, 'star': '3星'},
                {'value': 's20', 'gear': 2, 'star': '3星'},
                {'value': 'g23', 'gear': 3, 'star': '3星'},
                {'value': 'b31', 'gear': 4, 'star': '5星'},
                {'value': 'B39', 'gear': 4, 'star': '5星'},
            ]
        }
    ]

    dataset = ArtifactDataset(test_records, use_sliding_window=True)

    print(f"✓ 数据集创建成功")
    print(f"  - 样本数量: {len(dataset)}")

    if len(dataset) > 0:
        sample = dataset[0]
        print(f"  - 样本格式: {len(sample)} 个元素")
        print(f"    - 输入序列形状: {sample[0].shape}")
        print(f"    - skip值: {sample[1].item()}")
        print(f"    - 目标类型: {sample[2].item()}")
        print(f"    - 目标档位: {sample[3].item()}")
        print(f"    - 权重: {sample[4].item()}")

except Exception as e:
    print(f"✗ 数据集测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试3：检查预测接口
print("\n" + "=" * 60)
print("测试3：检查预测接口（需要已训练的模型）")
print("=" * 60)

try:
    from dl_model import ModelTrainer
    from artifact_predictor import DataManager

    dm = DataManager()
    trainer = ModelTrainer(dm)

    # 测试数据
    test_entries = [
        {'value': 'f16', 'gear': 1, 'star': '3星'},
        {'value': 's20', 'gear': 2, 'star': '3星'},
        {'value': 'g23', 'gear': 3, 'star': '3星'},
    ]

    result = trainer.predict(test_entries, skip=1)

    if result is not None:
        type_probs, gear_probs = result
        print(f"✓ 预测接口调用成功")
        print(f"  - 类型概率形状: {type_probs.shape}")
        print(f"  - 档位概率形状: {gear_probs.shape}")
        print(f"  - 类型概率和: {type_probs.sum():.2f}%")
        print(f"  - 档位概率和: {gear_probs.sum():.2f}%")

        # 显示Top-3类型
        type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]
        top3_indices = np.argsort(type_probs)[-3:][::-1]
        print(f"\n  Top-3 类型预测:")
        for i, idx in enumerate(top3_indices, 1):
            print(f"    {i}. {type_names[idx]}: {type_probs[idx]:.1f}%")

        # 显示档位预测
        print(f"\n  档位预测:")
        for i in range(4):
            print(f"    {i+1}档: {gear_probs[i]:.1f}%")
    else:
        print(f"⚠ 模型未加载（需要训练后的模型文件）")

except Exception as e:
    print(f"✗ 预测接口测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试4：检查统计模式
print("\n" + "=" * 60)
print("测试4：检查统计模式")
print("=" * 60)

try:
    # 模拟统计模式预测
    script_dir = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
    model_path = __import__('os').path.join(script_dir, 'genmat401.npy')
    model_data = np.load(model_path, allow_pickle=True).item()

    print(f"✓ 统计模型加载成功")
    print(f"  - 可用键: {list(model_data.keys())}")
    print(f"  - S1矩阵形状: {model_data['S1'].shape}")

    # 模拟一次预测
    # 编码3个测试词条
    def encode_entry(value, gear, star):
        type_map = {'f': 0, 's': 1, 'g': 2, 'F': 3, 'S': 4, 'G': 5, 'j': 6, 'c': 7, 'b': 8, 'B': 9}
        type_char = value[0]
        type_idx = type_map[type_char]
        gear_idx = gear - 1
        star_idx = 0 if star == "3星" else 1
        return type_idx * 4 + gear_idx + star_idx * 40

    e1 = encode_entry('f16', 1, '3星')
    e2 = encode_entry('s20', 2, '3星')
    e3 = encode_entry('g23', 3, '3星')

    counts = model_data['S1'][e1, :].astype(float)
    total = counts.sum()

    if total > 0:
        probs = counts / total * 100
        print(f"\n  统计模式预测结果:")
        print(f"  - 总样本数: {int(total)}")

        # 解码并显示Top-5
        def decode_entry(entry_id):
            star_idx = entry_id // 40
            remainder = entry_id % 40
            type_idx = remainder // 4
            gear_idx = remainder % 4
            type_map_inv = {0: 'f', 1: 's', 2: 'g', 3: 'F', 4: 'S', 5: 'G', 6: 'j', 7: 'c', 8: 'b', 9: 'B'}
            return type_map_inv[type_idx], gear_idx + 1, "3星" if star_idx == 0 else "5星"

        top5_indices = np.argsort(probs)[-5:][::-1]
        for i, idx in enumerate(top5_indices, 1):
            t, g, s = decode_entry(idx)
            print(f"    {i}. {t}{g*4+12 if t in 'fsg' else g*5+15 if t in 'FSG' else g*15+15 if t == 'j' else g*4+5 if t == 'c' else g*2.5+5 if t == 'b' else g*5+10} ({s}): {probs[idx]:.1f}%")
    else:
        print(f"  - 该组合无历史数据")

except Exception as e:
    print(f"✗ 统计模式测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

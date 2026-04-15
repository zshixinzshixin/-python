#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试两个模型的预测效果"""

import sys
sys.path.insert(0, r"E:\@Python\artifact")

import torch
import json
import os
import numpy as np
from collections import Counter

DATA_DIR = r"E:\@Python\artifact\数据收集\个人数据（198094151）"
MODEL_DIR = r"E:\@Python\artifact\强化记录\models"

# 加载数据
def load_data():
    all_sequences = []
    all_labels = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for record in data.get('records', []):
                    entries = record.get('entries', [])
                    if len(entries) >= 4:
                        for i in range(len(entries) - 3):
                            seq = entries[i:i+3]
                            all_sequences.append(seq)
                            all_labels.append(entries[i+3])

    return all_sequences, all_labels

# 词条类型映射
TYPE_TO_ID = {
    'f': 0, 's': 1, 'g': 2, 'F': 3, 'S': 4,
    'G': 5, 'j': 6, 'c': 7, 'b': 8, 'B': 9
}
ID_TO_TYPE = {v: k for k, v in TYPE_TO_ID.items()}

# 五星数值映射
FIVE_STAR_VALUES = {
    'f': ['f16', 'f19', 'f21', 'f23'],
    's': ['s209', 's239', 's269', 's299'],
    'g': ['g14', 'g16', 'g18', 'g19'],
    'F': ['F51', 'F58', 'F66', 'F73'],
    'S': ['S41', 'S47', 'S53', 'S58'],
    'G': ['G41', 'G47', 'G53', 'G58'],
    'j': ['j16', 'j19', 'j21', 'j23'],
    'c': ['c45', 'c52', 'c58', 'c65'],
    'b': ['b27', 'b31', 'b35', 'b39'],
    'B': ['B54', 'B62', 'B7', 'B78']
}

# 三星数值映射
THREE_STAR_VALUES = {
    'f': ['f5', 'f6', 'f7', 'f8'],
    's': ['s100', 's110', 's120', 's130'],
    'g': ['g5', 'g6', 'g7', 'g8'],
    'c': ['c20', 'c23', 'c26', 'c30'],
    'j': ['j8', 'j9', 'j10', 'j12']
}

def get_value_id(value, star):
    if star == "5星":
        for type_char, values in FIVE_STAR_VALUES.items():
            if value in values:
                return values.index(value)
    else:
        for type_char, values in THREE_STAR_VALUES.items():
            if value in values:
                return values.index(value)
    return 0

def encode_entry(entry):
    type_char = entry['type']
    type_idx = TYPE_TO_ID.get(type_char, 0)
    gear_idx = entry['gear'] - 1
    star_idx = 0 if entry['star'] == "3星" else 1
    return type_idx * 4 + gear_idx + star_idx * 40

def test_model(model_path, sequences, labels, model_name):
    print(f"\n{'='*60}")
    print(f"测试模型: {model_name}")
    print(f"{'='*60}")

    # 加载模型
    from dl_model import LSTMPredictor

    import config
    model = LSTMPredictor(
        vocab_size=80,
        embed_dim=config.EMBED_DIM,
        hidden_dim=config.HIDDEN_DIM,
        num_layers=config.NUM_LAYERS,
        dropout=0.0
    )

    checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()

    correct = 0
    total = len(sequences)
    probs_list = []
    pred_types = []
    true_types = []

    with torch.no_grad():
        for seq, label in zip(sequences, labels):
            inputs = [encode_entry(e) for e in seq]
            input_tensor = torch.tensor([inputs], dtype=torch.long)
            output = model(input_tensor)
            probs = torch.softmax(output, dim=1).numpy()[0]

            pred_type_idx = np.argmax(probs)
            true_type_idx = TYPE_TO_ID.get(label['type'], 0)

            pred_type = ID_TO_TYPE.get(pred_type_idx, '?')
            true_type = label['type']

            pred_types.append(pred_type)
            true_types.append(true_type)

            if pred_type == true_type:
                correct += 1

            probs_list.append(probs)

    type_acc = correct / total * 100
    print(f"类型准确率: {type_acc:.2f}% ({correct}/{total})")

    pred_counter = Counter(pred_types)
    true_counter = Counter(true_types)

    print(f"\n预测类型分布:")
    for typ, count in pred_counter.most_common():
        pct = count / total * 100
        print(f"  {typ}: {count} ({pct:.1f}%)")

    print(f"\n真实类型分布:")
    for typ, count in true_counter.most_common():
        pct = count / total * 100
        print(f"  {typ}: {count} ({pct:.1f}%)")

    probs_array = np.array(probs_list)
    print(f"\n预测概率统计:")
    print(f"  最大值: {probs_array.max():.3f}")
    print(f"  平均值: {probs_array.mean():.3f}")
    print(f"  最小值: {probs_array.min():.3f}")
    print(f"  标准差: {probs_array.std():.3f}")

    return type_acc

def main():
    print("加载数据...")
    sequences, labels = load_data()
    print(f"共 {len(sequences)} 个测试样本")

    acc1 = test_model(
        os.path.join(MODEL_DIR, "model_20260404_040238 18.82.pt"),
        sequences, labels,
        "18.82% 模型"
    )

    acc2 = test_model(
        os.path.join(MODEL_DIR, "model_20260412_035424 19.14.pt"),
        sequences, labels,
        "19.14% 模型"
    )

    print(f"\n{'='*60}")
    print(f"总结")
    print(f"{'='*60}")
    print(f"18.82% 模型: {acc1:.2f}%")
    print(f"19.14% 模型: {acc2:.2f}%")
    print(f"推荐: {'19.14% 模型' if acc2 > acc1 else '18.82% 模型'}")

if __name__ == "__main__":
    main()

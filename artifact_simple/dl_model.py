#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度学习预测模型 - S版
只保留预测功能，删除训练相关代码
"""

import torch
import torch.nn as nn
import numpy as np
import os

# 导入配置
import config

# 词条类型映射
type_map = {
    'f': 0, 's': 1, 'g': 2, 'F': 3, 'S': 4,
    'G': 5, 'j': 6, 'c': 7, 'b': 8, 'B': 9
}


def encode_entry(value, gear, star):
    """
    将词条编码为组合ID
    value: 词条值（如f16）
    gear: 档位（1-4）
    star: 星级（"3星"或"5星"）
    返回: 组合ID（0-79）
    """
    type_char = value[0]
    type_idx = type_map[type_char]
    gear_idx = gear - 1  # 转为0-3
    star_idx = 0 if star == "3星" else 1
    # 组合ID = 类型×4 + 档位 + 星级×40
    return type_idx * 4 + gear_idx + star_idx * 40


def decode_entry(entry_id):
    """
    将组合ID解码为词条信息
    返回: (type_char, gear, star)
    """
    star_idx = entry_id // 40
    remainder = entry_id % 40
    type_idx = remainder // 4
    gear_idx = remainder % 4

    # 反向查找类型字符
    for char, idx in type_map.items():
        if idx == type_idx:
            type_char = char
            break

    gear = gear_idx + 1
    star = "3星" if star_idx == 0 else "5星"

    return type_char, gear, star


class LSTMPredictor(nn.Module):
    """LSTM预测模型 - 支持skip参数"""

    def __init__(self, vocab_size=80, embed_dim=None, hidden_dim=None, num_layers=None, num_classes=None, dropout=None, max_skip=None):
        # 使用配置文件中的参数
        if embed_dim is None:
            embed_dim = config.EMBED_DIM
        if hidden_dim is None:
            hidden_dim = config.HIDDEN_DIM
        if num_layers is None:
            num_layers = config.NUM_LAYERS
        if num_classes is None:
            num_classes = config.NUM_CLASSES
        if dropout is None:
            dropout = config.DROPOUT
        if max_skip is None:
            max_skip = config.MAX_SKIP

        super(LSTMPredictor, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers,
                           batch_first=True, dropout=dropout)
        
        # skip嵌入层 (skip范围1-4，嵌入维度4)
        self.skip_embedding = nn.Embedding(max_skip + 1, 4)
        
        # 全连接层，输入维度 = hidden_dim + 4 (skip嵌入)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim + 4, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim // 2, num_classes)
        )

    def forward(self, x, skip=None):
        # x: (batch_size, seq_len=3)
        # skip: (batch_size,) 跳过步数，1=预测下一个，2=跳过1个预测，3=跳过2个预测，4=跳过3个预测
        embedded = self.embedding(x)  # (batch_size, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # 使用最后一个时间步的输出
        last_output = lstm_out[:, -1, :]  # (batch_size, hidden_dim)
        
        # 如果提供了skip参数，拼接skip嵌入
        if skip is not None:
            skip_embed = self.skip_embedding(skip)  # (batch_size, 4)
            last_output = torch.cat([last_output, skip_embed], dim=1)  # (batch_size, hidden_dim + 4)
        else:
            # 默认skip=1，用0填充（skip=0的嵌入）
            batch_size = last_output.size(0)
            skip_embed = self.skip_embedding(torch.zeros(batch_size, dtype=torch.long, device=last_output.device))
            last_output = torch.cat([last_output, skip_embed], dim=1)
        
        output = self.fc(last_output)  # (batch_size, num_classes)
        return output


class ModelPredictor:
    """模型预测器 - 只保留预测功能"""

    def __init__(self, models_dir, device=None):
        self.models_dir = models_dir
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None

    def load_model(self):
        """加载模型"""
        model_path = os.path.join(self.models_dir, 'best_model.pt')
        if not os.path.exists(model_path):
            return False

        checkpoint = torch.load(model_path, map_location=self.device)
        self.model = LSTMPredictor(
            vocab_size=checkpoint['vocab_size'],
            embed_dim=checkpoint['embed_dim'],
            hidden_dim=checkpoint['hidden_dim'],
            num_layers=checkpoint['num_layers'],
            num_classes=checkpoint['num_classes'],
            max_skip=checkpoint.get('max_skip', 3)  # 兼容旧模型，默认3
        ).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        return True

    def predict(self, entries, skip=1):
        """
        预测下一个词条 - 支持skip参数
        entries: list of dict, 包含value, gear, star
        skip: 跳过步数，1=预测下一个，2=跳过1个预测，3=跳过2个预测，4=跳过3个预测
        返回: 10种词条类型的概率分布
        """
        if self.model is None:
            if not self.load_model():
                return None

        # 编码输入
        encoded = []
        for entry in entries:
            entry_id = encode_entry(entry['value'], entry['gear'], entry['star'])
            encoded.append(entry_id)

        # 取最后3个
        input_seq = encoded[-3:]
        input_tensor = torch.tensor([input_seq], dtype=torch.long).to(self.device)
        skip_tensor = torch.tensor([skip], dtype=torch.long).to(self.device)

        with torch.no_grad():
            output = self.model(input_tensor, skip_tensor)
            probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]

        return probabilities * 100  # 转为百分比

    def predict_dl_smart(self, all_entries):
        """
        智能预测：根据词条数量选择不同的skip策略
        动态支持 config.MAX_SKIP 配置
        all_entries: 所有已录入的词条列表
        返回: 加权后的概率分布
        """
        import numpy as np

        n = len(all_entries)
        
        # 确保模型已加载
        if self.model is None:
            if not self.load_model():
                return None
        
        # 获取模型实际支持的max_skip（兼容旧模型）
        # 从skip_embedding层的大小推断: embedding.num_embeddings = max_skip + 1
        model_max_skip = self.model.skip_embedding.num_embeddings - 1
        
        # 使用配置和模型支持的最小值
        max_skip = min(config.MAX_SKIP, model_max_skip)

        # 最少3个词条：只用 skip=1
        if n < 4:
            return self.predict(all_entries[-3:], skip=1)

        # 计算可用多少个skip（受限于词条数量、配置和模型支持）
        # n个词条最多可用 skip = min(max_skip, (n-2))
        # 因为：3词条→skip=1, 4词条→skip=2, 5词条→skip=3, 6词条→skip=4
        available_skips = min(max_skip, n - 2)

        predictions = []
        weights = []

        for skip in range(1, available_skips + 1):
            # 获取输入序列：从后往前取3个，再往前skip-1个位置
            # skip=1: 取最后3个 [-3:]
            # skip=2: 往前移1位 [-4:-1]
            # skip=3: 往前移2位 [-5:-2]
            # skip=4: 往前移3位 [-6:-3]
            start_idx = -(3 + skip - 1)
            end_idx = start_idx + 3 if start_idx + 3 < 0 else None

            if abs(start_idx) <= n:
                input_seq = all_entries[start_idx:end_idx]
                if len(input_seq) == 3:
                    pred = self.predict(input_seq, skip=skip)
                    if pred is not None:
                        predictions.append(pred)
                        # 根据skip获取权重
                        if skip == 1:
                            # 5-6词条用 SKIP_1_WEIGHT_5TO6，7+用 SKIP_1_WEIGHT_7PLUS
                            weight = config.SKIP_1_WEIGHT_5TO6 if n < 7 else config.SKIP_1_WEIGHT_7PLUS
                        elif skip == 2:
                            weight = config.SKIP_2_WEIGHT
                        elif skip == 3:
                            weight = config.SKIP_3_WEIGHT
                        elif skip == 4:
                            weight = config.SKIP_4_WEIGHT
                        else:
                            # skip > 4 时，权重递减
                            weight = config.SKIP_4_WEIGHT * (0.5 ** (skip - 4))
                        weights.append(weight)

        if not predictions:
            return self.predict(all_entries[-3:], skip=1)

        # 加权平均
        weights = np.array(weights)
        weights = weights / weights.sum()

        final_probs = np.zeros(10)
        for pred, w in zip(predictions, weights):
            final_probs += pred * w

        return final_probs

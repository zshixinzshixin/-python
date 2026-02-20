#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import os
from datetime import datetime

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


class ArtifactDataset(Dataset):
    """圣遗物强化数据集"""

    def __init__(self, records, use_sliding_window=True, star_transition_weight=2.0):
        """
        records: list of dict, 每个dict包含timestamp和entries
        use_sliding_window: 是否使用滑动窗口生成多个样本
        star_transition_weight: 跨星级样本的权重倍数（3星→5星转换样本权重更高）
        """
        self.samples = []
        self.weights = []

        if use_sliding_window and len(records) >= 2:
            # 将所有记录合并成一个长序列
            all_entries = []
            for record in records:
                all_entries.extend(record['entries'])

            # 滑动窗口生成样本
            for i in range(len(all_entries) - 3):
                # 编码3个输入词条
                input_seq = []
                stars = []
                for j in range(3):
                    entry = all_entries[i + j]
                    entry_id = encode_entry(entry['value'], entry['gear'], entry['star'])
                    input_seq.append(entry_id)
                    stars.append(entry['star'])

                # 目标：第4个词条的类型
                target_type = type_map[all_entries[i + 3]['value'][0]]
                target_star = all_entries[i + 3]['star']

                self.samples.append((input_seq, target_type))

                # 计算权重：跨星级样本权重更高
                # 如果输入包含3星和5星，或者目标与输入星级不同
                has_3_star = '3星' in stars
                has_5_star = '5星' in stars
                is_transition = (has_3_star and has_5_star) or \
                               (has_3_star and target_star == '5星') or \
                               (has_5_star and target_star == '3星')

                if is_transition:
                    self.weights.append(star_transition_weight)
                else:
                    self.weights.append(1.0)
        else:
            # 原始方案：每条记录独立生成样本
            for record in records:
                entries = record['entries']
                if len(entries) < 4:
                    continue

                for i in range(len(entries) - 3):
                    input_seq = []
                    stars = []
                    for j in range(3):
                        entry = entries[i + j]
                        entry_id = encode_entry(entry['value'], entry['gear'], entry['star'])
                        input_seq.append(entry_id)
                        stars.append(entry['star'])

                    target_type = type_map[entries[i + 3]['value'][0]]
                    target_star = entries[i + 3]['star']

                    self.samples.append((input_seq, target_type))

                    # 计算权重
                    has_3_star = '3星' in stars
                    has_5_star = '5星' in stars
                    is_transition = (has_3_star and has_5_star) or \
                                   (has_3_star and target_star == '5星') or \
                                   (has_5_star and target_star == '3星')

                    if is_transition:
                        self.weights.append(star_transition_weight)
                    else:
                        self.weights.append(1.0)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        input_seq, target = self.samples[idx]
        weight = self.weights[idx]
        return torch.tensor(input_seq, dtype=torch.long), torch.tensor(target, dtype=torch.long), torch.tensor(weight, dtype=torch.float)


class LSTMPredictor(nn.Module):
    """LSTM预测模型"""

    def __init__(self, vocab_size=80, embed_dim=16, hidden_dim=64, num_layers=2, num_classes=10, dropout=0.2):
        super(LSTMPredictor, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers,
                           batch_first=True, dropout=dropout)
        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        # x: (batch_size, seq_len=3)
        embedded = self.embedding(x)  # (batch_size, seq_len, embed_dim)
        lstm_out, (hidden, cell) = self.lstm(embedded)
        # 使用最后一个时间步的输出
        last_output = lstm_out[:, -1, :]  # (batch_size, hidden_dim)
        output = self.fc(last_output)  # (batch_size, num_classes)
        return output


class ModelTrainer:
    """模型训练器"""

    def __init__(self, data_manager, device=None):
        self.data_manager = data_manager
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.training_log = []

    def prepare_data(self, test_ratio=0.2, batch_size=32):
        """准备训练数据"""
        data = self.data_manager.load_records()
        records = data['records']

        if len(records) < 10:
            return None, None, "数据不足，需要至少10条记录"

        # 创建数据集
        dataset = ArtifactDataset(records)

        if len(dataset) == 0:
            return None, None, "没有有效的训练样本"

        # 划分训练集和测试集
        test_size = int(len(dataset) * test_ratio)
        train_size = len(dataset) - test_size

        train_dataset, test_dataset = torch.utils.data.random_split(
            dataset, [train_size, test_size]
        )

        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        return train_loader, test_loader, None

    def train(self, epochs=100, learning_rate=0.001, patience=10):
        """训练模型"""
        train_loader, test_loader, error = self.prepare_data()
        if error:
            return False, error

        # 初始化模型
        self.model = LSTMPredictor().to(self.device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5)

        best_accuracy = 0
        best_model_state = None
        patience_counter = 0

        self.training_log = []

        for epoch in range(epochs):
            # 训练阶段
            self.model.train()
            train_loss = 0
            train_correct = 0
            train_total = 0

            for inputs, targets, weights in train_loader:
                inputs, targets, weights = inputs.to(self.device), targets.to(self.device), weights.to(self.device)

                optimizer.zero_grad()
                outputs = self.model(inputs)

                # 使用加权损失函数
                loss = criterion(outputs, targets)
                # 应用样本权重
                weighted_loss = (loss * weights).mean()
                weighted_loss.backward()
                optimizer.step()

                train_loss += weighted_loss.item()
                _, predicted = torch.max(outputs, 1)
                train_total += targets.size(0)
                train_correct += (predicted == targets).sum().item()

            train_accuracy = 100 * train_correct / train_total

            # 测试阶段
            self.model.eval()
            test_loss = 0
            test_correct = 0
            test_total = 0

            with torch.no_grad():
                for inputs, targets, _ in test_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    outputs = self.model(inputs)
                    loss = criterion(outputs, targets)

                    test_loss += loss.item()
                    _, predicted = torch.max(outputs, 1)
                    test_total += targets.size(0)
                    test_correct += (predicted == targets).sum().item()

            test_accuracy = 100 * test_correct / test_total

            # 记录日志
            log_entry = {
                'epoch': epoch + 1,
                'train_loss': train_loss / len(train_loader),
                'train_acc': train_accuracy,
                'test_loss': test_loss / len(test_loader),
                'test_acc': test_accuracy
            }
            self.training_log.append(log_entry)

            # 学习率调整
            scheduler.step(test_loss)

            # 早停检查
            if test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                best_model_state = self.model.state_dict().copy()
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                print(f"早停于epoch {epoch + 1}")
                break

            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch+1}/{epochs}, Train Acc: {train_accuracy:.2f}%, Test Acc: {test_accuracy:.2f}%")

        # 加载最佳模型
        if best_model_state:
            self.model.load_state_dict(best_model_state)

        # 保存模型（传入准确率）
        self.save_model(accuracy=best_accuracy)

        # 保存训练日志
        self.save_training_log()

        return True, f"训练完成！最佳测试准确率: {best_accuracy:.2f}%"

    def save_model(self, accuracy=0):
        """保存模型 - 版本管理
        同时保存带时间戳的版本和best_model.pt
        """
        if self.model is None:
            return

        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 保存带时间戳的版本
        versioned_path = os.path.join(
            self.data_manager.models_dir,
            f'model_{timestamp}.pt'
        )

        # 保存best_model.pt（最新模型）
        best_model_path = os.path.join(
            self.data_manager.models_dir,
            'best_model.pt'
        )

        model_data = {
            'model_state_dict': self.model.state_dict(),
            'vocab_size': 80,
            'embed_dim': 16,
            'hidden_dim': 64,
            'num_layers': 2,
            'num_classes': 10,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'accuracy': accuracy
        }

        # 保存版本化模型
        torch.save(model_data, versioned_path)
        print(f"模型版本已保存: {versioned_path}")

        # 保存/覆盖best_model.pt
        torch.save(model_data, best_model_path)
        print(f"最佳模型已更新: {best_model_path}")

    def list_models(self):
        """列出所有可用的模型版本"""
        models = []
        for filename in os.listdir(self.data_manager.models_dir):
            if filename.startswith('model_') and filename.endswith('.pt'):
                filepath = os.path.join(self.data_manager.models_dir, filename)
                try:
                    checkpoint = torch.load(filepath, map_location='cpu')
                    models.append({
                        'filename': filename,
                        'timestamp': checkpoint.get('timestamp', '未知'),
                        'accuracy': checkpoint.get('accuracy', 0),
                        'is_best': filename == 'best_model.pt'
                    })
                except:
                    pass
        # 按时间倒序排列
        models.sort(key=lambda x: x['timestamp'], reverse=True)
        return models

    def load_model_by_path(self, model_path):
        """从指定路径加载模型"""
        if not os.path.exists(model_path):
            return False

        checkpoint = torch.load(model_path, map_location=self.device)
        self.model = LSTMPredictor(
            vocab_size=checkpoint['vocab_size'],
            embed_dim=checkpoint['embed_dim'],
            hidden_dim=checkpoint['hidden_dim'],
            num_layers=checkpoint['num_layers'],
            num_classes=checkpoint['num_classes']
        ).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        return True

    def save_training_log(self):
        """保存训练日志"""
        log_path = os.path.join(self.data_manager.models_dir, 'training_log.txt')
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("Epoch,Train Loss,Train Acc,Test Loss,Test Acc\n")
            for entry in self.training_log:
                f.write(f"{entry['epoch']},{entry['train_loss']:.4f},{entry['train_acc']:.2f}%,"
                       f"{entry['test_loss']:.4f},{entry['test_acc']:.2f}%\n")

    def load_model(self):
        """加载模型"""
        model_path = os.path.join(self.data_manager.models_dir, 'best_model.pt')
        if not os.path.exists(model_path):
            return False

        checkpoint = torch.load(model_path, map_location=self.device)
        self.model = LSTMPredictor(
            vocab_size=checkpoint['vocab_size'],
            embed_dim=checkpoint['embed_dim'],
            hidden_dim=checkpoint['hidden_dim'],
            num_layers=checkpoint['num_layers'],
            num_classes=checkpoint['num_classes']
        ).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model.eval()

        return True

    def predict(self, entries):
        """
        预测下一个词条
        entries: list of dict, 包含value, gear, star
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

        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = torch.softmax(output, dim=1).cpu().numpy()[0]

        return probabilities * 100  # 转为百分比


if __name__ == "__main__":
    # 测试代码
    from artifact_predictor import DataManager

    dm = DataManager()
    trainer = ModelTrainer(dm)

    # 检查是否有足够数据
    count = dm.get_record_count()
    print(f"当前记录数: {count}")

    if count >= 100:
        print("开始训练...")
        success, message = trainer.train(epochs=50)
        print(message)
    else:
        print(f"数据不足，需要至少10条记录，当前{count}条")

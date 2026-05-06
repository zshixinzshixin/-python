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


class ArtifactDataset(Dataset):
    """圣遗物强化数据集 - 支持skip参数"""

    def __init__(self, records, use_sliding_window=True, star_transition_weight=None, max_skip=None):
        # 使用配置文件中的权重
        if star_transition_weight is None:
            star_transition_weight = config.STAR_TRANSITION_WEIGHT
        # 使用配置文件中的max_skip
        if max_skip is None:
            max_skip = config.MAX_SKIP
        """
        records: list of dict, 每个dict包含timestamp和entries
        use_sliding_window: 是否使用滑动窗口生成多个样本
        star_transition_weight: 跨星级样本的权重倍数（3星→5星转换样本权重更高）
        max_skip: 最大跳过步数（1=预测下一个，2=跳过1个，3=跳过2个，4=跳过3个）
        """
        self.samples = []
        self.weights = []

        if use_sliding_window and len(records) >= 2:
            # 滑动窗口方案：合并所有记录生成样本
            all_entries = []
            for record in records:
                all_entries.extend(record['entries'])

            # 滑动窗口生成样本，支持多种skip
            for i in range(len(all_entries) - 3):
                # 编码3个输入词条
                input_seq = []
                stars = []
                for j in range(3):
                    entry = all_entries[i + j]
                    entry_id = encode_entry(entry['value'], entry['gear'], entry['star'])
                    input_seq.append(entry_id)
                    stars.append(entry['star'])

                # 生成多种skip的样本
                for skip in range(1, min(max_skip + 1, len(all_entries) - i - 2)):
                    target_idx = i + 3 + skip - 1  # skip=1时预测第4个(i+3)
                    if target_idx < len(all_entries):
                        target_type = type_map[all_entries[target_idx]['value'][0]]
                        target_star = all_entries[target_idx]['star']

                        # 样本格式：(input_seq, skip, target_type)
                        self.samples.append((input_seq, skip, target_type))

                        # 计算权重：跨星级样本权重更高，skip大的样本权重略低
                        has_3_star = '3星' in stars
                        has_5_star = '5星' in stars
                        is_transition = (has_3_star and has_5_star) or \
                                       (has_3_star and target_star == '5星') or \
                                       (has_5_star and target_star == '3星')

                        base_weight = star_transition_weight if is_transition else 1.0
                        # skip越大权重略低（近期预测更可靠）
                        skip_discount = 1.0 - (skip - 1) * 0.1  # skip=1:1.0, skip=2:0.9, skip=3:0.8
                        self.weights.append(base_weight * skip_discount)
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

                    # 生成多种skip的样本
                    for skip in range(1, min(max_skip + 1, len(entries) - i - 2)):
                        target_idx = i + 3 + skip - 1
                        if target_idx < len(entries):
                            target_type = type_map[entries[target_idx]['value'][0]]
                            target_star = entries[target_idx]['star']

                            self.samples.append((input_seq, skip, target_type))

                            # 计算权重
                            has_3_star = '3星' in stars
                            has_5_star = '5星' in stars
                            is_transition = (has_3_star and has_5_star) or \
                                           (has_3_star and target_star == '5星') or \
                                           (has_5_star and target_star == '3星')

                            base_weight = star_transition_weight if is_transition else 1.0
                            skip_discount = 1.0 - (skip - 1) * 0.1
                            self.weights.append(base_weight * skip_discount)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        input_seq, skip, target_type = self.samples[idx]
        weight = self.weights[idx]
        return (torch.tensor(input_seq, dtype=torch.long),
                torch.tensor(skip, dtype=torch.long),
                torch.tensor(target_type, dtype=torch.long),
                torch.tensor(weight, dtype=torch.float))


class LSTMPredictor(nn.Module):
    """LSTM预测模型 - 支持skip参数，只预测词条类型"""

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

        self.num_classes = num_classes

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers,
                           batch_first=True, dropout=dropout)

        # skip嵌入层 (skip范围1-4，嵌入维度4)
        self.skip_embedding = nn.Embedding(max_skip + 1, 4)

        # 全连接层
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

        # 类型预测
        output = self.fc(last_output)  # (batch_size, num_classes)

        return output


class ModelTrainer:
    """模型训练器"""

    def __init__(self, data_manager, device=None):
        self.data_manager = data_manager
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.training_log = []

    def prepare_data(self, test_ratio=None, batch_size=None):
        """准备训练数据"""
        # 使用配置文件中的参数
        if test_ratio is None:
            test_ratio = config.TEST_RATIO
        if batch_size is None:
            batch_size = config.BATCH_SIZE

        data = self.data_manager.load_records()
        records = data['records']

        if len(records) < config.MIN_RECORDS_FOR_TRAINING:
            return None, None, f"数据不足，需要至少{config.MIN_RECORDS_FOR_TRAINING}条记录"

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

    def train(self, epochs=None, learning_rate=None, patience=None):
        """训练模型"""
        # 使用配置文件中的参数
        if epochs is None:
            epochs = config.EPOCHS
        if learning_rate is None:
            learning_rate = config.LEARNING_RATE
        if patience is None:
            patience = config.PATIENCE

        train_loader, test_loader, error = self.prepare_data()
        if error:
            return False, error

        # 初始化模型
        self.model = LSTMPredictor().to(self.device)
        criterion = nn.CrossEntropyLoss(reduction='none')
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=max(5, patience//2), factor=0.5)

        best_accuracy = 0
        best_top3_accuracy = 0
        best_model_state = None
        patience_counter = 0

        self.training_log = []
        
        # 记录数据集大小
        train_size = len(train_loader.dataset)
        test_size = len(test_loader.dataset)

        for epoch in range(epochs):
            # 训练阶段
            self.model.train()
            train_loss = 0
            train_correct = 0
            train_top3_correct = 0
            train_total = 0

            for inputs, skips, targets, weights in train_loader:
                inputs, skips = inputs.to(self.device), skips.to(self.device)
                targets = targets.to(self.device)
                weights = weights.to(self.device)

                optimizer.zero_grad()
                outputs = self.model(inputs, skips)

                loss = criterion(outputs, targets)
                weighted_loss = (loss * weights).mean()
                weighted_loss.backward()
                optimizer.step()

                train_loss += weighted_loss.item()

                # Top-1准确率
                _, predicted = torch.max(outputs, 1)
                train_correct += (predicted == targets).sum().item()
                
                # Top-3准确率
                _, top3_pred = torch.topk(outputs, 3, dim=1)
                for i in range(targets.size(0)):
                    if targets[i] in top3_pred[i]:
                        train_top3_correct += 1
                
                train_total += targets.size(0)

            train_accuracy = 100 * train_correct / train_total
            train_top3_accuracy = 100 * train_top3_correct / train_total

            # 测试阶段
            self.model.eval()
            test_loss = 0
            test_correct = 0
            test_top3_correct = 0
            test_total = 0

            with torch.no_grad():
                for inputs, skips, targets, _ in test_loader:
                    inputs, skips = inputs.to(self.device), skips.to(self.device)
                    targets = targets.to(self.device)

                    outputs = self.model(inputs, skips)
                    loss = criterion(outputs, targets).mean()

                    test_loss += loss.item()

                    # Top-1准确率
                    _, predicted = torch.max(outputs, 1)
                    test_correct += (predicted == targets).sum().item()
                    
                    # Top-3准确率
                    _, top3_pred = torch.topk(outputs, 3, dim=1)
                    for i in range(targets.size(0)):
                        if targets[i] in top3_pred[i]:
                            test_top3_correct += 1
                    
                    test_total += targets.size(0)

            test_accuracy = 100 * test_correct / test_total
            test_top3_accuracy = 100 * test_top3_correct / test_total

            # 记录日志
            log_entry = {
                'epoch': epoch + 1,
                'train_loss': train_loss / len(train_loader),
                'train_acc': train_accuracy,
                'train_top3_acc': train_top3_accuracy,
                'test_loss': test_loss / len(test_loader),
                'test_acc': test_accuracy,
                'test_top3_acc': test_top3_accuracy
            }
            self.training_log.append(log_entry)

            # 学习率调整
            scheduler.step(test_loss / len(test_loader))

            # 早停检查（以Top-1测试准确率为准）
            if test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                best_top3_accuracy = test_top3_accuracy
                best_model_state = self.model.state_dict().copy()
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                print(f"早停触发，最佳测试准确率: {best_accuracy:.2f}%, Top-3准确率: {best_top3_accuracy:.2f}%")
                stopped_by_early = True
                break
        else:
            stopped_by_early = False

        # 加载最佳模型
        if best_model_state is not None:
            self.model.load_state_dict(best_model_state)

        # 生成训练结果报告
        final_log = self.training_log[-1] if self.training_log else None
        if final_log:
            # 计算收敛能力（分析最佳准确率时刻的状态）
            import numpy as np
            
            # 找到最佳准确率所在的轮次
            best_epoch_idx = max(range(len(self.training_log)), 
                                key=lambda i: self.training_log[i]['test_acc'])
            best_epoch = self.training_log[best_epoch_idx]
            best_epoch_num = best_epoch['epoch']
            total_epochs = len(self.training_log)
            
            # 分析最佳点附近的趋势（最佳点前3轮到后2轮）
            start_idx = max(0, best_epoch_idx - 2)
            end_idx = min(len(self.training_log), best_epoch_idx + 3)
            nearby_logs = self.training_log[start_idx:end_idx]
            nearby_accs = [log['test_acc'] for log in nearby_logs]
            
            # 最佳点附近是否稳定
            if len(nearby_accs) >= 3:
                if max(nearby_accs) - min(nearby_accs) < 1.5:
                    stability = f"已平稳（第{best_epoch_num}轮）"
                elif nearby_accs[-1] > nearby_accs[0]:
                    stability = f"上升中（第{best_epoch_num}轮）"
                else:
                    stability = f"波动中（第{best_epoch_num}轮）"
            else:
                stability = f"数据不足（第{best_epoch_num}轮）"
            
            # 最佳点时的损失趋势（对比之前）
            if best_epoch_idx > 0:
                prev_loss = self.training_log[best_epoch_idx - 1]['test_loss']
                curr_loss = best_epoch['test_loss']
                if curr_loss < prev_loss * 0.98:
                    loss_status = "损失下降"
                elif curr_loss > prev_loss * 1.02:
                    loss_status = "损失上升"
                else:
                    loss_status = "损失平稳"
            else:
                loss_status = "初始轮次"
            
            # 平稳能力评级
            if "已平稳" in stability:
                stability_level = "S"
            elif "上升中" in stability:
                stability_level = "A"
            else:
                stability_level = "B"
            
            # 损失状态评级
            if "下降" in loss_status:
                loss_level = "S"
            elif "平稳" in loss_status:
                loss_level = "A"
            else:
                loss_level = "B"
            
            # 泛化能力评级
            generalization_gap = best_epoch['train_acc'] - best_epoch['test_acc']
            if generalization_gap < 5.0:
                generalization_level = "S"
                generalization_desc = "差距<5%"
            elif generalization_gap < 15.0:
                generalization_level = "A"
                generalization_desc = "差距5-15%"
            else:
                generalization_level = "B"
                generalization_desc = "差距>15%"
            
            # 计算模型质量等级（综合准确率和稳定性）
            # 准确率评分
            if best_accuracy >= 20 or best_top3_accuracy >= 50:
                acc_score = 3
            elif best_accuracy >= 15 or best_top3_accuracy >= 40:
                acc_score = 2
            elif best_accuracy >= 12 or best_top3_accuracy >= 30:
                acc_score = 1
            else:
                acc_score = 0
            
            # 稳定性评分（每个S级+1分）
            stab_score = 0
            if stability_level == "S": stab_score += 1
            if loss_level == "S": stab_score += 1
            if generalization_level == "S": stab_score += 1
            
            # 综合评级
            total_score = acc_score + stab_score
            if total_score >= 5:
                quality_level = "S"
            elif total_score >= 3:
                quality_level = "A"
            else:
                quality_level = "B"
            quality_desc = f"准确率{acc_score}分+稳定性{stab_score}分=总分{total_score}分"
            
            # 相比随机的提升
            improvement = best_accuracy - 10.0  # 10类随机基准
            
            message = (
                f"训练完成！\n"
                f"【训练质量】{quality_level}（{quality_desc}）\n\n"
                f"【准确率】\n"
                f"Top-1准确率: {best_accuracy:.2f}%  (比随机好 +{improvement:.2f}%)\n"
                f"Top-3准确率: {best_top3_accuracy:.2f}%  (前3个包含正确答案)\n\n"
                f"【数据】{train_size}条训练 / {test_size}条测试\n\n"
                f"【稳定性】\n"
                f"平稳能力：{stability_level}（{stability}）\n"
                f"损失状态：{loss_level}（{loss_status}）\n"
                f"泛化能力：{generalization_level}（{generalization_desc}）"
            )
        else:
            message = f"训练完成！最佳测试准确率: {best_accuracy:.2f}%"
        # 保存最佳准确率到实例变量，供后续保存模型时使用
        self.best_accuracy = best_accuracy
        self.best_top3_accuracy = best_top3_accuracy
        
        return True, message

    def save_training_log(self, path=None):
        """保存训练日志到文本文件"""
        if path is None:
            path = '强化记录/models/training_log.txt'
        
        if not self.training_log:
            return
        
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("训练日志\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"{'轮次':<6}{'训练损失':<12}{'训练准确率':<12}{'测试损失':<12}{'测试准确率':<12}\n")
            f.write("-" * 60 + "\n")
            
            for log in self.training_log:
                f.write(f"{log['epoch']:<6}{log['train_loss']:<12.4f}{log['train_acc']:<12.2f}{log['test_loss']:<12.4f}{log['test_acc']:<12.2f}\n")
            
            f.write("=" * 60 + "\n")

    def save_model(self, path=None):
        """保存模型"""
        if path is None:
            path = '强化记录/models/best_model.pt'

        if self.model is not None:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            torch.save(self.model.state_dict(), path)
            # 同时保存训练日志
            self.save_training_log()
            
            # 保存带时间戳的历史版本
            if hasattr(self, 'best_accuracy'):
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                history_path = f'强化记录/models/model_{timestamp}_{self.best_accuracy:.2f}.pt'
                torch.save(self.model.state_dict(), history_path)

    def load_model(self, path=None):
        """加载模型"""
        if path is None:
            path = '强化记录/models/best_model.pt'

        self.model = LSTMPredictor().to(self.device)
        try:
            self.model.load_state_dict(torch.load(path, map_location=self.device, weights_only=True))
            self.model.eval()
        except FileNotFoundError:
            self.model = None

    def predict(self, entries, skip=1):
        """预测接口 - 只预测词条类型"""
        if len(entries) < 3:
            return None

        # 加载模型
        if self.model is None:
            self.load_model()

        if self.model is None:
            return None

        # 准备输入
        input_seq = []
        for entry in reversed(entries[-3:]):
            entry_id = encode_entry(entry['value'], entry['gear'], entry['star'])
            input_seq.append(entry_id)

        input_tensor = torch.tensor([input_seq], dtype=torch.long).to(self.device)
        skip_tensor = torch.tensor([skip], dtype=torch.long).to(self.device)

        # 预测
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_tensor, skip_tensor)
            probs = torch.softmax(output, dim=1).cpu().numpy()[0] * 100

        return probs

    def predict_dl_smart(self, all_entries):
        """智能预测 - 根据词条数量选择skip策略
        all_entries: 所有已录入的词条（从最旧到最新）
        返回: 类型概率数组 或 None
        """
        if len(all_entries) < 3:
            return None

        # 根据已录入词条数量选择skip策略
        # 已录入3个 → skip=1（预测第4个）
        # 已录入4个 → skip=2（预测第5个）
        # 已录入5个 → skip=3（预测第6个）
        # 已录入6个及以上 → skip=4（预测第7个）
        num_entries = len(all_entries)
        if num_entries <= 3:
            skip = 1
        elif num_entries == 4:
            skip = 2
        elif num_entries == 5:
            skip = 3
        else:
            skip = 4

        return self.predict(all_entries, skip=skip)

    def get_training_log(self):
        """获取训练日志"""
        return self.training_log

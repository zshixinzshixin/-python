#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从genmat401.npy生成基础预训练模型
解决冷启动问题：0条记录也能使用深度学习模式
"""

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import os

# 设置随机种子保证可复现
torch.manual_seed(42)
np.random.seed(42)

class ArtifactDataset(Dataset):
    """从NPY采样的数据集"""
    def __init__(self, sequences):
        self.sequences = sequences
    
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        input_seq, target = self.sequences[idx]
        return torch.tensor(input_seq, dtype=torch.long), torch.tensor(target, dtype=torch.long)

class ArtifactLSTM(nn.Module):
    """LSTM模型（与dl_model.py一致）"""
    def __init__(self, vocab_size=80, embedding_dim=16, hidden_dim=64, num_layers=2, num_classes=10):
        super(ArtifactLSTM, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, num_layers, 
                           batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        output = self.fc(lstm_out[:, -1, :])
        return output

def generate_sequences_from_npy(npy_path, num_samples=10000):
    """
    从NPY文件采样生成训练序列
    
    NPY结构：字典格式，包含S3, W3等统计矩阵
    S3[i,j,k,t] = 次数 (三星数据)
    - i,j,k: 前3个词条的索引(0-39)
    - t: 目标词条类型(0-9)
    """
    print(f"加载NPY文件: {npy_path}")
    data = np.load(npy_path, allow_pickle=True).item()
    
    # 使用S3（三星）和W3（五星）混合
    S3 = data['S3']  # 三星统计 (40, 40, 40, 10)
    W3 = data.get('W3', S3)  # 五星统计，如果没有就用S3
    
    print(f"S3形状: {S3.shape}")
    print(f"W3形状: {W3.shape}")
    
    sequences = []
    total_valid = 0
    
    # 合并S3和W3
    combined = S3.astype(np.float32) + W3.astype(np.float32)
    
    # 遍历所有可能的3元组
    for i in range(40):
        for j in range(40):
            for k in range(40):
                counts = combined[i, j, k]
                total = counts.sum()
                
                if total > 10:  # 至少出现10次才使用
                    total_valid += 1
                    # 根据频率采样
                    sample_count = min(int(total / 10), 30)  # 限制样本数
                    
                    for _ in range(sample_count):
                        # 根据概率分布选择下一个词条
                        probs = counts / total
                        next_type = np.random.choice(10, p=probs)
                        
                        # 输入是3个词条的索引（已包含档位信息）
                        input_ids = [i, j, k]
                        sequences.append((input_ids, next_type))
    
    print(f"有效3元组数量: {total_valid}")
    print(f"生成序列总数: {len(sequences)}")
    
    # 随机采样指定数量
    if len(sequences) > num_samples:
        indices = np.random.choice(len(sequences), num_samples, replace=False)
        sequences = [sequences[i] for i in indices]
    elif len(sequences) < num_samples:
        # 如果不够，重复采样
        extra = num_samples - len(sequences)
        extra_indices = np.random.choice(len(sequences), extra, replace=True)
        sequences.extend([sequences[i] for i in extra_indices])
    
    print(f"最终训练样本: {len(sequences)}")
    return sequences

def train_base_model(sequences, epochs=30, batch_size=64):
    """训练基础模型"""
    
    # 创建数据集
    dataset = ArtifactDataset(sequences)
    # 划分训练集和测试集 (80/20)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # 创建模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    model = ArtifactLSTM().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.5)
    
    # 训练
    best_test_acc = 0
    
    for epoch in range(epochs):
        # 训练
        model.train()
        train_loss = 0
        train_correct = 0
        train_total = 0
        
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += targets.size(0)
            train_correct += predicted.eq(targets).sum().item()
        
        scheduler.step()
        
        # 测试
        model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                test_total += targets.size(0)
                test_correct += predicted.eq(targets).sum().item()
        
        train_acc = 100. * train_correct / train_total
        test_acc = 100. * test_correct / test_total
        
        if (epoch + 1) % 5 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Train Acc: {train_acc:.2f}%, Test Acc: {test_acc:.2f}%')
        
        if test_acc > best_test_acc:
            best_test_acc = test_acc
    
    return model, best_test_acc

def save_model(model, accuracy, save_path='强化记录/models/best_model.pt'):
    """保存模型"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    torch.save({
        'model_state_dict': model.state_dict(),
        'accuracy': accuracy,
        'source': 'genmat401.npy (base model)',
        'description': '基于历史数据统计的预训练模型'
    }, save_path)
    
    print(f"\n模型已保存: {save_path}")
    print(f"测试准确率: {accuracy:.2f}%")
    print("\n说明：这是基于通用统计数据的预训练模型")
    print("随着您保存更多强化记录并重新训练，模型会越来越个性化")

def main():
    print("=" * 50)
    print("生成基础预训练模型")
    print("=" * 50)
    
    # 1. 从NPY生成训练数据
    npy_path = 'genmat401.npy'
    if not os.path.exists(npy_path):
        print(f"错误：找不到 {npy_path}")
        return
    
    sequences = generate_sequences_from_npy(npy_path, num_samples=10000)
    
    if len(sequences) < 100:
        print("错误：生成的训练样本太少，无法训练")
        return
    
    # 2. 训练模型
    print("\n开始训练...")
    model, accuracy = train_base_model(sequences, epochs=30)
    
    # 3. 保存模型
    save_model(model, accuracy)
    
    print("\n" + "=" * 50)
    print("完成！现在可以直接使用深度学习模式了")
    print("=" * 50)

if __name__ == '__main__':
    main()

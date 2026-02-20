"""
测试预测功能
验证滑动窗口预测是否正常工作
"""
import sys
sys.path.append('..')

import numpy as np
from artifact_predictor import ArtifactPredictor, DataManager
from dl_model import ModelTrainer

def test_prediction():
    print("=" * 60)
    print("测试预测功能")
    print("=" * 60)
    
    # 创建数据管理器
    dm = DataManager()
    
    # 检查是否有模型
    import os
    model_path = os.path.join(dm.models_dir, 'best_model.pt')
    if not os.path.exists(model_path):
        print("❌ 没有找到训练好的模型")
        print(f"   请先运行 test_training.py 训练模型")
        return False
    
    print("✅ 找到模型文件")
    
    # 创建训练器并加载模型
    trainer = ModelTrainer(dm)
    if not trainer.load_model():
        print("❌ 加载模型失败")
        return False
    
    print("✅ 模型加载成功")
    
    # 模拟录入一些词条
    test_entries = [
        {'value': 'f16', 'gear': 1, 'star': '3星'},
        {'value': 's239', 'gear': 2, 'star': '3星'},
        {'value': 'g18', 'gear': 3, 'star': '3星'},
        {'value': 'F73', 'gear': 4, 'star': '5星'},
        {'value': 'c52', 'gear': 2, 'star': '5星'},
    ]
    
    print("\n测试数据（模拟录入）:")
    for i, entry in enumerate(test_entries, 1):
        print(f"  {i}. {entry['value']} ({entry['star']}, {entry['gear']}档)")
    
    # 测试预测
    print("\n进行预测...")
    probs = trainer.predict(test_entries)
    
    if probs is None:
        print("❌ 预测失败")
        return False
    
    print("✅ 预测成功！")
    
    # 显示结果
    type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]
    
    print("\n预测结果（概率%）:")
    print("-" * 40)
    
    # 排序显示
    sorted_indices = np.argsort(probs)[::-1]
    for i, idx in enumerate(sorted_indices[:5], 1):
        name = type_names[idx]
        prob = probs[idx]
        bar = "█" * int(prob / 2)
        print(f"  {i}. {name:6s}: {prob:5.1f}% {bar}")
    
    # Top-3推荐
    top3_indices = sorted_indices[:3]
    print("\nTop-3推荐:")
    for i, idx in enumerate(top3_indices, 1):
        print(f"  {i}. {type_names[idx]} ({probs[idx]:.1f}%)")
    
    # 置信度
    max_prob = np.max(probs)
    std_prob = np.std(probs)
    confidence = max_prob * (1 + std_prob / 10)
    confidence = min(100, confidence)
    
    if confidence >= 40:
        level = "高"
    elif confidence >= 25:
        level = "中"
    else:
        level = "低"
    
    print(f"\n置信度: {level} ({confidence:.1f})")
    
    return True

if __name__ == "__main__":
    success = test_prediction()
    print("\n" + "=" * 60)
    if success:
        print("预测功能验证通过！")
    else:
        print("预测功能验证失败！")
    print("=" * 60)

"""
测试训练功能
验证模型是否能正常训练
"""
import sys
sys.path.append('..')

from dl_model import ModelTrainer
from artifact_predictor import DataManager

def test_training():
    print("=" * 60)
    print("测试训练功能")
    print("=" * 60)
    
    # 创建数据管理器
    dm = DataManager()
    count = dm.get_record_count()
    print(f"\n当前记录数: {count}")
    
    if count < 10:
        print(f"❌ 记录不足，需要至少10条，当前{count}条")
        print("\n建议：运行 generate_data.py 生成模拟数据")
        return False
    
    print(f"✅ 记录数足够，开始训练...")
    print(f"   训练数据: {count} 条记录")
    
    # 创建训练器
    trainer = ModelTrainer(dm)
    
    # 开始训练（只训练10个epoch用于测试）
    print("\n开始训练（最多10 epochs）...")
    success, message = trainer.train(epochs=10, patience=3)
    
    if success:
        print(f"✅ 训练成功！")
        print(f"   {message}")
        return True
    else:
        print(f"❌ 训练失败: {message}")
        return False

if __name__ == "__main__":
    success = test_training()
    print("\n" + "=" * 60)
    if success:
        print("训练功能验证通过！")
    else:
        print("训练功能验证失败！")
    print("=" * 60)

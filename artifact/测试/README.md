# 验证工具

这个文件夹包含用于验证程序功能的测试脚本。

## 文件说明

| 文件 | 功能 | 使用场景 |
|------|------|---------|
| `generate_data.py` | 生成模拟训练数据 | 快速生成测试数据 |
| `test_training.py` | 测试训练功能 | 验证模型能否正常训练 |
| `test_prediction.py` | 测试预测功能 | 验证预测是否正常 |

## 使用步骤

### 1. 生成模拟数据

```bash
cd 验证
python generate_data.py --num 50
```

- 在 `../强化记录/` 目录生成50条模拟数据
- 每条记录包含3星垫刀+5星强化词条

### 2. 测试训练功能

```bash
python test_training.py
```

- 检查记录数是否≥10条
- 训练模型（最多10 epochs）
- 保存模型到 `../强化记录/models/best_model.pt`

### 3. 测试预测功能

```bash
python test_prediction.py
```

- 加载训练好的模型
- 用模拟数据进行预测
- 显示预测结果和置信度

## 完整验证流程

```bash
# 1. 生成数据
python generate_data.py --num 100

# 2. 训练模型
python test_training.py

# 3. 测试预测
python test_prediction.py
```

## 注意事项

- 模拟数据是随机生成的，没有真实规律
- 训练准确率可能接近随机（10%左右）
- 真实数据训练效果会更好

import numpy as np

# 加载NPY数据
data = np.load('genmat401.npy', allow_pickle=True).item()
S3 = data['S3']

# 计算整体概率分布
# S3[i,j,k,t] 表示词条i→j→k后，出现类型t的次数
total_counts = np.sum(S3, axis=(0,1,2))  # 对所有输入组合求和
print("各类型总出现次数:")
type_names = ["小防", "小生", "小攻", "大防", "大生", "大攻", "精通", "充能", "暴击", "暴伤"]
for i, (name, count) in enumerate(zip(type_names, total_counts)):
    print(f"  {name}: {int(count)}")

# 计算概率
total = np.sum(total_counts)
probs = total_counts / total * 100
print(f"\n总记录数: {int(total)}")
print("\n各类型概率分布:")
for name, prob in zip(type_names, probs):
    print(f"  {name}: {prob:.2f}%")

# 统计信息
print(f"\n最高概率: {np.max(probs):.2f}% ({type_names[np.argmax(probs)]})")
print(f"最低概率: {np.min(probs):.2f}% ({type_names[np.argmin(probs)]})")
print(f"标准差: {np.std(probs):.2f}")

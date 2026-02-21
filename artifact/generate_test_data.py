# -*- coding: utf-8 -*-
"""
生成测试数据 - 用于测试训练模块
格式与预测器保存的数据完全一致
文件名带_test后缀，便于区分
"""

import json
import random
import os
from datetime import datetime

# 词条类型映射（与预测器一致）
ENTRY_TYPES = {
    'g': '小攻', 'G': '大攻',
    'f': '小防', 'F': '大防',
    's': '小生', 'S': '大生',
    'j': '精通',
    'c': '充能',
    'b': '暴率', 'B': '暴伤'
}

# 星级映射
STAR_MAP = {3: '3星', 4: '4星', 5: '5星'}

# 圣遗物类型
ARTIFACT_TYPES = ["flower", "feather", "sand", "cup", "head"]


def generate_value(entry_type, gear):
    """生成词条值（模拟数值）"""
    base_values = {
        'g': (14, 20), 'G': (40, 50),
        'f': (14, 20), 'F': (40, 50),
        's': (150, 250), 'S': (400, 500),
        'j': (16, 23),
        'c': (4, 6),
        'b': (2, 4), 'B': (5, 8),
    }
    
    min_val, max_val = base_values.get(entry_type, (10, 20))
    value = random.randint(min_val, max_val)
    return f"{entry_type}{value}"


def generate_entry(order, star=None):
    """生成单个词条条目"""
    entry_type = random.choice(list(ENTRY_TYPES.keys()))
    
    if star is None:
        star = random.choice([3, 4, 5])
    
    gear = random.randint(1, 4)
    value = generate_value(entry_type, gear)
    
    return {
        "value": value,
        "gear": gear,
        "star": STAR_MAP[star],
        "type": entry_type,
        "order": order
    }


def generate_session_entries(num_entries=20, pattern="random"):
    """生成一次强化会话的词条列表"""
    entries = []
    
    for i in range(1, num_entries + 1):
        if pattern == "random":
            star = random.choice([3, 4, 5])
        elif pattern == "only_3star":
            star = 3
        elif pattern == "only_5star":
            star = 5
        elif pattern == "mixed_3_to_5":
            star = 3 if i <= num_entries * 0.75 else 5
        elif pattern == "rising":
            if i <= num_entries * 0.33:
                star = 3
            elif i <= num_entries * 0.66:
                star = 4
            else:
                star = 5
        else:
            star = random.choice([3, 4, 5])
        
        entries.append(generate_entry(i, star))
    
    return entries


def generate_test_record_file(num_sessions=12, entries_per_session=15, output_dir="强化记录"):
    """
    生成测试记录文件
    
    Args:
        num_sessions: 生成多少个会话（默认12个，超过10个训练门槛）
        entries_per_session: 每个会话多少词条
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 文件名带_test后缀，便于区分测试数据
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"record_test_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    # 生成数据
    records = []
    patterns = ["random", "only_3star", "only_5star", "mixed_3_to_5", "rising"]
    
    for i in range(num_sessions):
        pattern = patterns[i % len(patterns)]
        
        session = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "entries": generate_session_entries(entries_per_session, pattern),
            "artifact_type": random.choice(ARTIFACT_TYPES)
        }
        records.append(session)
    
    # 正确的完整格式
    data = {
        "records": records,
        "metadata": {
            "total_records": num_sessions,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_type": "test"  # 标记为测试数据
        }
    }
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 统计
    total_entries = sum(len(r["entries"]) for r in records)
    star_count = {"3星": 0, "4星": 0, "5星": 0}
    for record in records:
        for entry in record["entries"]:
            star_count[entry["star"]] += 1
    
    print(f"✓ 已生成测试数据: {filepath}")
    print(f"  - 会话数: {num_sessions} (满足≥10的训练要求)")
    print(f"  - 总词条: {total_entries}")
    print(f"  - 星级分布: {star_count}")
    print(f"  - 文件名标记: _test (便于区分真实数据)")
    
    return filepath


if __name__ == "__main__":
    print("=" * 60)
    print("生成测试数据（用于测试训练模块）")
    print("=" * 60)
    print("\n说明:")
    print("- 生成的文件名带 '_test' 后缀")
    print("- 便于与你自己录入的真实数据区分")
    print("- 默认生成12条记录，满足训练要求(≥10)")
    print("=" * 60)
    
    print("\n生成测试数据...")
    filepath = generate_test_record_file(
        num_sessions=12,      # 12条记录，超过10条的训练门槛
        entries_per_session=15  # 每个会话15个词条
    )
    
    print("\n" + "=" * 60)
    print("✓ 测试数据生成完成！")
    print("=" * 60)
    print(f"\n文件路径: {filepath}")
    print("\n文件命名规则:")
    print("  - record_test_*.json = 程序生成的测试数据")
    print("  - record_*.json = 你自己录入的真实数据")
    print("\n现在可以在预测器中：")
    print("1. 点击'导入数据'选择此文件")
    print("2. 点击'训练模型'测试训练功能")
    
    input("\n按回车键退出...")

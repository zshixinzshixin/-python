"""
生成模拟训练数据
用于快速生成测试数据
"""
import sys
sys.path.append('..')

import json
import random
import os
from datetime import datetime, timedelta

# 词条类型
TYPES = ['f', 's', 'g', 'F', 'S', 'G', 'j', 'c', 'b', 'B']
TYPE_NAMES = ['小防', '小生', '小攻', '大防', '大生', '大攻', '精通', '充能', '暴击', '暴伤']

# 3星数值
THREE_STAR_VALUES = {
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

def generate_entry(star_type):
    """生成一个词条"""
    type_char = random.choice(TYPES)
    gear = random.randint(1, 4)
    value = THREE_STAR_VALUES[type_char][gear - 1]
    
    return {
        'value': value,
        'gear': gear,
        'star': star_type,
        'type': type_char
    }

def generate_record():
    """生成一条强化记录"""
    entries = []
    
    # 3星垫刀（3-6个）
    num_3star = random.randint(3, 6)
    for _ in range(num_3star):
        entries.append(generate_entry('3星'))
    
    # 5星强化（4-8个）
    num_5star = random.randint(4, 8)
    for _ in range(num_5star):
        entries.append(generate_entry('5星'))
    
    return entries

def main(num_records=50):
    output_dir = '../强化记录'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"生成{num_records}条模拟数据...")
    
    for i in range(num_records):
        entries = generate_record()
        timestamp = (datetime.now() - timedelta(minutes=i*5)).strftime("%Y-%m-%d %H:%M:%S")
        
        record = {
            'timestamp': timestamp,
            'entries': entries,
            'artifact_type': random.choice(['flower', 'feather', 'sands', 'goblet', 'circlet'])
        }
        
        data = {
            'records': [record],
            'metadata': {
                'total_records': 1,
                'last_updated': timestamp
            }
        }
        
        filename = f'record_simulated_{i+1:04d}.json'
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if (i + 1) % 10 == 0:
            print(f"  已生成 {i+1}/{num_records}")
    
    print(f"\n✅ 完成！保存在 {output_dir}/")
    print(f"\n现在可以运行 test_training.py 进行训练测试了")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='生成模拟训练数据')
    parser.add_argument('--num', type=int, default=50, help='生成记录数量（默认50）')
    args = parser.parse_args()
    
    main(args.num)

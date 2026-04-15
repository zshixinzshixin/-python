#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据分析脚本 - 分析个人数据"""

import json
import os
from collections import Counter, defaultdict

DATA_DIR = r"E:\@Python\artifact\数据收集\个人数据（198094151）"

# 词条类型名称
TYPE_NAMES = {
    'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
    'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'
}

def load_data():
    """加载所有JSON文件"""
    all_entries = []
    total_records = 0
    total_files = 0

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                records = data.get('records', [])
                total_records += len(records)
                total_files += 1

                for record in records:
                    entries = record.get('entries', [])
                    all_entries.extend(entries)

    return all_entries, total_records, total_files

def analyze_entries(entries):
    """分析词条数据"""
    # 1. 基本统计
    print(f"\n{'='*50}")
    print(f"基本统计")
    print(f"{'='*50}")
    print(f"总词条数: {len(entries)}")

    # 2. 星级分布
    print(f"\n{'='*50}")
    print(f"星级分布")
    print(f"{'='*50}")
    star_counter = Counter(e['star'] for e in entries)
    for star, count in star_counter.most_common():
        pct = count / len(entries) * 100
        print(f"  {star}: {count} ({pct:.1f}%)")

    # 3. 档位分布
    print(f"\n{'='*50}")
    print(f"档位分布 (五星)")
    print(f"{'='*50}")
    five_star_gears = [e['gear'] for e in entries if e['star'] == '5星']
    gear_counter = Counter(five_star_gears)
    for gear, count in sorted(gear_counter.items()):
        pct = count / len(five_star_gears) * 100 if five_star_gears else 0
        print(f"  档位{gear}: {count} ({pct:.1f}%)")

    # 4. 词条类型分布 (五星)
    print(f"\n{'='*50}")
    print(f"词条类型分布 (五星)")
    print(f"{'='*50}")
    five_star_types = [e['type'] for e in entries if e['star'] == '5星']
    type_counter = Counter(five_star_types)
    for typ, count in type_counter.most_common():
        name = TYPE_NAMES.get(typ, typ)
        pct = count / len(five_star_types) * 100 if five_star_types else 0
        print(f"  {typ}({name}): {count} ({pct:.1f}%)")

    # 5. 词条类型分布 (三星)
    print(f"\n{'='*50}")
    print(f"词条类型分布 (三星)")
    print(f"{'='*50}")
    three_star_types = [e['type'] for e in entries if e['star'] == '3星']
    type_counter = Counter(three_star_types)
    for typ, count in type_counter.most_common():
        name = TYPE_NAMES.get(typ, typ)
        pct = count / len(three_star_types) * 100 if three_star_types else 0
        print(f"  {typ}({name}): {count} ({pct:.1f}%)")

    # 6. 每个record的长度分布
    print(f"\n{'='*50}")
    print(f"检查数据完整性")
    print(f"{'='*50}")
    # 按文件分组计算record长度
    file_lengths = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for record in data.get('records', []):
                    entries_count = len(record.get('entries', []))
                    file_lengths.append(entries_count)

    length_counter = Counter(file_lengths)
    print(f"Record长度分布:")
    for length, count in sorted(length_counter.items()):
        print(f"  {length}个词条: {count}条记录")

    # 7. 检查星级与数值的匹配
    print(f"\n{'='*50}")
    print(f"检查数值与星级匹配 (可能的数据问题)")
    print(f"{'='*50}")

    # 五星数值范围
    FIVE_STAR_VALUES = {
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

    errors = []
    for e in entries:
        typ = e['type']
        value = e['value']
        star = e['star']

        if star == '5星' and typ in FIVE_STAR_VALUES:
            if value not in FIVE_STAR_VALUES[typ]:
                errors.append(f"  错误: {value} 被标记为{star}但不在五星数值列表中 (类型{typ})")

    if errors:
        print(f"发现 {len(errors)} 个潜在问题:")
        for err in errors[:10]:  # 只显示前10个
            print(err)
        if len(errors) > 10:
            print(f"  ... 还有 {len(errors)-10} 个问题")
    else:
        print(f"未发现明显的星级/数值不匹配问题")

def main():
    print(f"数据分析: {DATA_DIR}")
    entries, total_records, total_files = load_data()
    print(f"共 {total_files} 个文件, {total_records} 条记录, {len(entries)} 个词条")
    analyze_entries(entries)

if __name__ == "__main__":
    main()

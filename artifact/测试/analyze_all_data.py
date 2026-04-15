#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数据分析脚本 - 分析所有数据"""

import json
import os
from collections import Counter

# 词条类型名称
TYPE_NAMES = {
    'f': '小防', 's': '小生', 'g': '小攻', 'F': '大防', 'S': '大生',
    'G': '大攻', 'j': '精通', 'c': '充能', 'b': '暴击', 'B': '暴伤'
}

def analyze_folder(name, path):
    """分析一个数据文件夹"""
    all_entries = []
    files = 0
    records = 0

    for filename in os.listdir(path):
        if filename.endswith('.json'):
            filepath = os.path.join(path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                files += 1
                for record in data.get('records', []):
                    records += 1
                    entries = record.get('entries', [])
                    all_entries.extend(entries)

    # 统计五星词条类型分布
    five_star = [e for e in all_entries if e['star'] == '5星']
    type_counter = Counter(e['type'] for e in five_star)

    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    print(f"文件: {files}, 记录: {records}, 词条: {len(all_entries)}")
    print(f"五星词条: {len(five_star)}")

    if five_star:
        print(f"\n五星词条类型分布:")
        for typ, count in type_counter.most_common():
            pct = count / len(five_star) * 100
            print(f"  {typ}({TYPE_NAMES.get(typ, typ)}): {count} ({pct:.1f}%)")

    return len(five_star)

def main():
    base = r"E:\@Python\artifact\数据收集"

    results = []
    results.append(("个人数据(198094151)", analyze_folder("个人数据(198094151)", os.path.join(base, "个人数据（198094151）"))))
    results.append(("个人数据(127469003)", analyze_folder("个人数据(127469003)", os.path.join(base, "个人数据（127469003）"))))
    results.append(("混合数据", analyze_folder("混合数据", os.path.join(base, "混合数据"))))

    print(f"\n{'='*60}")
    print(f"总结")
    print(f"{'='*60}")
    total_five = sum(r[1] for r in results)
    for name, count in results:
        print(f"{name}: {count} 五星词条")
    print(f"\n总计五星词条: {total_five}")
    print(f"估计可生成训练样本(3-序列): ~{total_five - 3}")

if __name__ == "__main__":
    main()

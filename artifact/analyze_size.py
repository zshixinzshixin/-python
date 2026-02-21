# -*- coding: utf-8 -*-
"""
分析打包目录大小，找出占用空间的大文件
"""

import os
from pathlib import Path
from collections import defaultdict


def get_size(path):
    """获取文件或目录大小"""
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_size(entry.path)
    return total


def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def analyze_directory(target_dir):
    """分析目录大小"""
    print(f"分析目录: {target_dir}")
    print("=" * 70)
    
    if not os.path.exists(target_dir):
        print(f"错误: 目录不存在 {target_dir}")
        return
    
    # 统计各子目录大小
    dir_sizes = []
    for entry in os.scandir(target_dir):
        if entry.is_dir():
            size = get_size(entry.path)
            dir_sizes.append((entry.name, size))
    
    # 按大小排序
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    
    print("\n子目录大小排名:")
    print("-" * 70)
    for name, size in dir_sizes[:20]:  # 显示前20
        print(f"  {format_size(size):>12}  {name}")
    
    # 统计总大小
    total_size = get_size(target_dir)
    print(f"\n总大小: {format_size(total_size)}")
    
    # 查找大文件（超过10MB）
    print("\n\n大文件列表（超过10MB）:")
    print("-" * 70)
    large_files = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size > 10 * 1024 * 1024:  # 10MB
                    large_files.append((file_path, size))
            except:
                pass
    
    # 按大小排序
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    for file_path, size in large_files[:30]:  # 显示前30
        rel_path = os.path.relpath(file_path, target_dir)
        print(f"  {format_size(size):>12}  {rel_path}")
    
    # 按文件类型统计
    print("\n\n按文件类型统计:")
    print("-" * 70)
    type_sizes = defaultdict(int)
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if not ext:
                ext = '(无扩展名)'
            file_path = os.path.join(root, file)
            try:
                type_sizes[ext] += os.path.getsize(file_path)
            except:
                pass
    
    # 按大小排序
    sorted_types = sorted(type_sizes.items(), key=lambda x: x[1], reverse=True)
    for ext, size in sorted_types[:15]:
        print(f"  {format_size(size):>12}  {ext}")


def main():
    target_dir = r"C:\DDDATE\@Python\artifact\dist\圣遗物预测器"
    analyze_directory(target_dir)


if __name__ == '__main__':
    main()

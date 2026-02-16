# check_environment.py
import os
import sys

print("=" * 60)
print("环境检查")
print("=" * 60)

print(f"Python 版本: {sys.version}")
print(f"Python 解释器: {sys.executable}")

# 检查可能的 Qt 插件路径
possible_paths = [
    r'D:\MiniConda\Library\plugins',
    r'D:\MiniConda\Lib\site-packages\PyQt5\Qt5\plugins',
    r'D:\MiniConda\pkgs\qt-main-5.15.15-h9151539_4\Library\plugins',
]

print("\n检查 Qt 插件路径:")
for path in possible_paths:
    exists = os.path.exists(path)
    print(f"  {path}: {'✅ 存在' if exists else '❌ 不存在'}")
    if exists:
        # 列出插件目录内容
        try:
            files = os.listdir(path)
            platform_dir = os.path.join(path, 'platforms')
            if os.path.exists(platform_dir):
                platforms = os.listdir(platform_dir)
                print(f"    找到平台插件: {platforms}")
        except:
            pass

print("\nPATH 环境变量中的 Qt 相关路径:")
for p in os.environ['PATH'].split(';'):
    if 'qt' in p.lower() or 'conda' in p.lower():
        print(f"  {p}")

print("\n" + "=" * 60)
print("测试 PyQt5 导入")
print("=" * 60)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖库检查工具
检查微信定时消息发送工具所需的所有依赖库是否已安装
"""

import sys

# 定义需要检查的依赖库
REQUIRED_PACKAGES = {
    'PyQt5': {
        'import_name': 'PyQt5',
        'description': 'GUI界面库，用于创建应用程序窗口'
    },
    'pyautogui': {
        'import_name': 'pyautogui',
        'description': '模拟键盘鼠标操作，用于控制键盘输入消息'
    },
    'pyperclip': {
        'import_name': 'pyperclip',
        'description': '剪贴板操作，用于长消息快速粘贴'
    },
    'pywinauto': {
        'import_name': 'pywinauto',
        'description': 'Windows窗口自动化，用于激活微信窗口'
    },
    'ntplib': {
        'import_name': 'ntplib',
        'description': 'NTP时间同步，用于获取网络标准时间'
    }
}


def check_package(package_name, import_name):
    """检查单个包是否已安装"""
    try:
        __import__(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)


def get_python_info():
    """获取当前 Python 环境信息"""
    executable = sys.executable
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    return executable, version


def check_all_dependencies():
    """检查所有依赖库"""
    python_path, python_version = get_python_info()

    print("=" * 60)
    print("微信定时消息发送工具 - 依赖库检查")
    print("=" * 60)
    print()
    print(f"🐍 Python 版本: {python_version}")
    print(f"📁 Python 路径: {python_path}")
    print()

    missing_packages = []
    installed_packages = []

    for package_name, info in REQUIRED_PACKAGES.items():
        is_installed, error = check_package(package_name, info['import_name'])

        if is_installed:
            installed_packages.append(package_name)
            print(f"✅ {package_name:<15} - 已安装")
            print(f"   用途: {info['description']}")
        else:
            missing_packages.append(package_name)
            print(f"❌ {package_name:<15} - 未安装")
            print(f"   用途: {info['description']}")
        print()

    print("=" * 60)

    if missing_packages:
        print(f"\n⚠️  缺少 {len(missing_packages)} 个依赖库:")
        for pkg in missing_packages:
            print(f"   - {pkg}")

        print("\n📦 请运行以下命令安装:")
        print(f"   pip install {' '.join(missing_packages)}")

        print("\n📦 或者一次性安装所有依赖:")
        print(f"   pip install {' '.join(REQUIRED_PACKAGES.keys())}")

        return False
    else:
        print(f"\n✅ 所有 {len(installed_packages)} 个依赖库均已安装！")
        print("\n🚀 可以运行 wechat_timer.py 了")
        return True


def main():
    """主函数"""
    check_all_dependencies()
    print()
    input("按回车键退出...")


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
打包后清理脚本 - 删除不必要的文件减小体积

使用方法: python clean_dll.py [打包目录路径] [--dry-run]
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# 可删除文件分类

# 1. 测试相关（运行时不需要）
TEST_PATTERNS = ['*test*.dll', '*tests*.dll', '*_test*.pyd', '*_tests*.pyd']

# 2. 调试符号（发布版本不需要）
DEBUG_PATTERNS = ['*.pdb', '*.sym']

# 3. 文档和静态库（运行时不需要）
# 注意：不删除.txt文件，避免误删setuptools需要的文件
DOC_PATTERNS = ['*.html', '*.md', '*.rst', '*.qch', '*.qhc']

# 4. 静态库文件（运行时不需要，只编译时需要）
STATIC_LIB_PATTERNS = ['*.lib']  # .lib文件是静态库，运行时不需要

# 4. 未使用的Qt组件（更完整列表）
UNUSED_QT = [
    'Qt5Network.dll', 'Qt5Qml.dll', 'Qt5Quick.dll', 'Qt5WebSockets.dll',
    'Qt5Xml.dll', 'Qt5Sql.dll', 'Qt5Multimedia.dll', 'Qt5MultimediaWidgets.dll',
    'Qt5OpenGL.dll', 'Qt5PrintSupport.dll', 'Qt5Sensors.dll', 'Qt5SerialPort.dll',
    'Qt5Positioning.dll', 'Qt5Location.dll', 'Qt5Nfc.dll', 'Qt5Bluetooth.dll',
    'Qt5WebChannel.dll', 'Qt5WebEngineCore.dll', 'Qt5WebEngine.dll',
]

# 5. 未使用的Python标准库（扩展列表）
UNUSED_PYTHON_DIRS = [
    'pydoc_data', 'idlelib', 'tkinter', 'turtledemo',
    'lib2to3', 'ensurepip', 'venv', 'wsgiref', 'curses',
    'dbm', 'email', 'http', 'urllib', 'xml', 'xmlrpc',
    'multiprocessing', 'concurrent', 'asyncio', 'unittest',
    'logging', 'lzma', 'zipfile', 'tarfile', 'gzip',
]

# 6. 国际化文件（只保留中英文）
UNUSED_TRANSLATIONS = [
    'qtbase_ar.qm', 'qtbase_bg.qm', 'qtbase_ca.qm', 'qtbase_cs.qm',
    'qtbase_da.qm', 'qtbase_de.qm', 'qtbase_es.qm', 'qtbase_fi.qm',
    'qtbase_fr.qm', 'qtbase_gd.qm', 'qtbase_he.qm', 'qtbase_hu.qm',
    'qtbase_it.qm', 'qtbase_ja.qm', 'qtbase_ko.qm', 'qtbase_lv.qm',
    'qtbase_pl.qm', 'qtbase_pt.qm', 'qtbase_ru.qm', 'qtbase_sk.qm',
    'qtbase_tr.qm', 'qtbase_uk.qm'
]

# 7. 可删除的目录
REMOVABLE_DIR_PATTERNS = ['tcl', 'tk', 'test', 'tests', 'testing', '__pycache__']

# 8. PyTorch大型不必要文件/目录
PYTORCH_UNUSED = [
    'torch/lib/cudnn*',           # CUDA深度学习库（如果用CPU版本）
    'torch/lib/nvrtc*',           # CUDA运行时编译器
    'torch/lib/cuda*',            # CUDA库
    'torch/lib/libtorch_python.dll',  # 可能重复
    'torch/include',              # C++头文件
    'torch/share',                # 共享文件
    'torch/cuda',                 # CUDA支持（如果用CPU版本）
    'torch/distributed',          # 分布式训练
    'torch/fx',                   # FX转换
    'torch/package',              # 包管理
    'torch/_appdirs.py',
    'torch/_dynamo',              # Dynamo编译器
    'torch/_functorch',           # functorch
    'torch/_inductor',            # Inductor编译器
    'torch/_lazy',                # 懒加载
    'torch/_numpy',               # NumPy兼容层
    'torch/_prims',               # 原始操作
    'torch/_refs',                # 引用实现
    'torch/_subclasses',          # 子类
    'torch/ao',                   # AO量化
    'torch/backends',             # 后端（保留必要的）
    'torch/contrib',              # 贡献代码
    'torch/csrc',                 # C++源码
    'torch/datapipe',             # 数据管道
    'torch/export',               # 导出
    'torch/fft',                  # FFT（如果用不到）
    'torch/func',                 # 函数式API
    'torch/futures',              # 异步
    'torch/hub',                  # Hub模型
    'torch/jit',                  # JIT编译（如果用不到）
    'torch/linalg',               # 线性代数（如果用不到）
    'torch/masked',               # Masked张量
    'torch/monitor',              # 监控
    'torch/mtia',                 # MTIA
    'torch/nested',               # 嵌套张量
    'torch/onnx',                 # ONNX导出（如果用不到）
    'torch/profiler',             # 性能分析
    'torch/quantization',         # 量化（如果用不到）
    'torch/sparse',               # 稀疏张量（如果用不到）
    'torch/special',              # 特殊函数
    'torch/testing',              # 测试
    'torch/utils/benchmark',      # 基准测试
    'torch/utils/checkpoint.py',  # 检查点
    'torch/utils/cpp_extension.py',  # C++扩展
    'torch/utils/data',           # 数据加载（保留必要的）
    'torch/utils/dlpack.py',
    'torch/utils/mobile_optimizer.py',
    'torch/utils/model_dump.py',
    'torch/utils/model_zoo.py',
    'torch/utils/tensorboard',    # TensorBoard
    'torch/xpu',                  # XPU
]

# 9. NumPy不必要文件
NUMPY_UNUSED = [
    'numpy/core/tests',
    'numpy/lib/tests',
    'numpy/ma/tests',
    'numpy/matrixlib/tests',
    'numpy/polynomial/tests',
    'numpy/random/tests',
    'numpy/testing',
    'numpy/f2py',                 # Fortran接口
    'numpy/distutils',            # 构建工具
    'numpy/typing',               # 类型提示
    'numpy/_typing',              # 内部类型
]

# 10. Pandas不必要文件
PANDAS_UNUSED = [
    'pandas/tests',
    'pandas/_testing',
    'pandas/plotting',            # 绘图（如果用不到）
    'pandas/io/sas',              # SAS格式
    'pandas/io/sql.py',           # SQL（如果用不到）
    'pandas/io/html.py',          # HTML
    'pandas/io/xml.py',           # XML
    'pandas/io/json',             # JSON（如果用pandas的JSON）
    'pandas/io/clipboard',        # 剪贴板
    'pandas/io/gbq.py',           # BigQuery
    'pandas/io/stata.py',         # Stata
    'pandas/io/feather_format.py', # Feather
    'pandas/io/parquet.py',       # Parquet
    'pandas/io/orc.py',           # ORC
]

# 需要保护的目录（即使匹配也不删除）
PROTECTED_DIRS = ['setuptools', 'pkg_resources', 'jaraco']

# 核心库目录（允许清理.lib文件，但不删除其他文件）
CORE_LIBS = ['numpy', 'torch', 'pandas']

# CUDA相关文件（如果只用CPU版本PyTorch，可以删除）
# 注意：只删除NVIDIA CUDA库，不删除PyTorch核心文件
CUDA_FILES = [
    'magma.dll',                  # MAGMA库
    'cublasLt64_12.dll',          # cuBLAS Lt
    'cublas64_12.dll',            # cuBLAS
    'cusparse64_12.dll',          # cuSPARSE
    'cufft64_11.dll',             # cuFFT
    'cusolver64_11.dll',          # cuSOLVER
    'nvJitLink_120_0.dll',        # NVJitLink
    'nvrtc64_120_0.dll',          # NVRTC
    'nvrtc-builtins64_120.dll',   # NVRTC内置
    'cudart64_12.dll',            # CUDA Runtime
    'cudnn64_8.dll',              # cuDNN
    'cudnn_ops_infer64_8.dll',    # cuDNN操作
    'cudnn_cnn_infer64_8.dll',    # cuDNN CNN
    'cudnn_adv_infer64_8.dll',    # cuDNN高级
    # 注意：不删除 torch_cuda.dll 和 torch_python.dll，这是PyTorch核心
]


def get_directory_size(path):
    """获取目录大小"""
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_directory_size(entry.path)
    return total


def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def is_protected_path(path):
    """检查路径是否在保护列表中"""
    path_str = str(path).lower()
    for protected in PROTECTED_DIRS:
        if protected.lower() in path_str:
            return True
    return False


def find_removable_files(target_dir):
    """查找所有可删除的文件"""
    files_to_remove = []
    dirs_to_remove = []
    
    # 查找测试文件
    for pattern in TEST_PATTERNS:
        for file_path in Path(target_dir).rglob(pattern):
            if file_path.is_file() and not is_protected_path(file_path):
                files_to_remove.append(file_path)
    
    # 查找调试符号
    for pattern in DEBUG_PATTERNS:
        for file_path in Path(target_dir).rglob(pattern):
            if file_path.is_file() and not is_protected_path(file_path):
                files_to_remove.append(file_path)
    
    # 查找文档文件
    for pattern in DOC_PATTERNS:
        for file_path in Path(target_dir).rglob(pattern):
            if file_path.is_file() and not is_protected_path(file_path):
                files_to_remove.append(file_path)
    
    # 查找静态库文件（.lib）
    # 注意：.lib文件是静态库，运行时不需要，可以安全删除
    for pattern in STATIC_LIB_PATTERNS:
        for file_path in Path(target_dir).rglob(pattern):
            if file_path.is_file():
                # 允许删除核心库中的.lib文件
                files_to_remove.append(file_path)
    
    # 查找未使用的Qt组件
    for qt_file in UNUSED_QT:
        for file_path in Path(target_dir).rglob(qt_file):
            if file_path.is_file():
                files_to_remove.append(file_path)
    
    # 查找未使用的国际化文件
    for trans_file in UNUSED_TRANSLATIONS:
        for file_path in Path(target_dir).rglob(trans_file):
            if file_path.is_file():
                files_to_remove.append(file_path)
    
    # 查找未使用的Python目录
    for dir_name in UNUSED_PYTHON_DIRS:
        for dir_path in Path(target_dir).rglob(dir_name):
            if dir_path.is_dir() and not is_protected_path(dir_path):
                dirs_to_remove.append(dir_path)
    
    # 查找其他可删除目录
    for pattern in REMOVABLE_DIR_PATTERNS:
        for dir_path in Path(target_dir).rglob(pattern):
            if dir_path.is_dir() and not is_protected_path(dir_path):
                dirs_to_remove.append(dir_path)
    
    # 查找PyTorch不必要文件/目录
    for pattern in PYTORCH_UNUSED:
        for path in Path(target_dir).rglob(pattern):
            if not is_protected_path(path):
                if path.is_file():
                    files_to_remove.append(path)
                elif path.is_dir():
                    dirs_to_remove.append(path)
    
    # 查找NumPy不必要文件/目录
    for pattern in NUMPY_UNUSED:
        for path in Path(target_dir).rglob(pattern):
            if not is_protected_path(path):
                if path.is_file():
                    files_to_remove.append(path)
                elif path.is_dir():
                    dirs_to_remove.append(path)
    
    # 查找Pandas不必要文件/目录
    for pattern in PANDAS_UNUSED:
        for path in Path(target_dir).rglob(pattern):
            if not is_protected_path(path):
                if path.is_file():
                    files_to_remove.append(path)
                elif path.is_dir():
                    dirs_to_remove.append(path)
    
    # 去重
    files_to_remove = list(set(files_to_remove))
    dirs_to_remove = list(set(dirs_to_remove))
    
    return files_to_remove, dirs_to_remove


def backup_directory(src_dir):
    """备份目录"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"{src_dir}_backup_{timestamp}"
    
    print(f"\n创建备份: {backup_dir}")
    shutil.copytree(src_dir, backup_dir)
    print(f"✓ 备份完成")
    
    return backup_dir


def clean_directory(target_dir, dry_run=False):
    """清理目录"""
    if not os.path.exists(target_dir):
        print(f"错误: 目录不存在 {target_dir}")
        return False
    
    print(f"\n{'[预览模式] ' if dry_run else ''}目标目录: {target_dir}")
    print("=" * 70)
    
    # 记录大小
    size_before = get_directory_size(target_dir)
    print(f"当前大小: {format_size(size_before)}")
    
    # 查找可删除项
    files_to_remove, dirs_to_remove = find_removable_files(target_dir)
    
    if not files_to_remove and not dirs_to_remove:
        print("\n✓ 没有发现可删除的文件")
        return True
    
    # 分类统计
    test_files = [f for f in files_to_remove if any(p in str(f) for p in TEST_PATTERNS)]
    debug_files = [f for f in files_to_remove if any(p in str(f) for p in DEBUG_PATTERNS)]
    doc_files = [f for f in files_to_remove if any(p in str(f) for p in DOC_PATTERNS)]
    lib_files = [f for f in files_to_remove if f.suffix == '.lib']
    qt_files = [f for f in files_to_remove if f.name in UNUSED_QT]
    trans_files = [f for f in files_to_remove if f.name in UNUSED_TRANSLATIONS]
    pytorch_files = [f for f in files_to_remove if 'torch' in str(f).lower()]
    numpy_files = [f for f in files_to_remove if 'numpy' in str(f).lower()]
    pandas_files = [f for f in files_to_remove if 'pandas' in str(f).lower()]
    
    # 计算静态库文件总大小
    lib_size = sum(f.stat().st_size for f in lib_files)
    
    print(f"\n可删除文件统计:")
    print(f"  测试文件: {len(test_files)} 个")
    print(f"  静态库文件(.lib): {len(lib_files)} 个 ({format_size(lib_size)})")
    print(f"  PyTorch相关: {len(pytorch_files)} 个")
    print(f"  NumPy相关: {len(numpy_files)} 个")
    print(f"  Pandas相关: {len(pandas_files)} 个")
    print(f"  调试符号: {len(debug_files)} 个")
    print(f"  文档文件: {len(doc_files)} 个")
    print(f"  Qt组件: {len(qt_files)} 个")
    print(f"  翻译文件: {len(trans_files)} 个")
    print(f"  目录: {len(dirs_to_remove)} 个")
    print(f"  总计: {len(files_to_remove)} 个文件, {len(dirs_to_remove)} 个目录")
    
    if dry_run:
        print("\n[预览模式] 未执行删除")
        return True
    
    # 确认删除
    confirm = input("\n确认删除以上文件? (y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return False
    
    # 创建备份
    backup_dir = backup_directory(target_dir)
    
    # 执行删除
    removed_count = 0
    removed_size = 0
    
    print("\n删除文件...")
    for file_path in files_to_remove:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            removed_count += 1
            removed_size += file_size
            print(f"  ✓ {file_path.name}")
        except Exception as e:
            print(f"  ✗ {file_path.name}: {e}")
    
    print("\n删除目录...")
    for dir_path in dirs_to_remove:
        try:
            dir_size = get_directory_size(dir_path)
            shutil.rmtree(dir_path)
            removed_count += 1
            removed_size += dir_size
            print(f"  ✓ {dir_path.name}")
        except Exception as e:
            print(f"  ✗ {dir_path.name}: {e}")
    
    # 显示结果
    size_after = get_directory_size(target_dir)
    print(f"\n{'=' * 70}")
    print(f"清理完成!")
    print(f"  删除项目: {removed_count} 个")
    print(f"  释放空间: {format_size(removed_size)}")
    print(f"  清理前: {format_size(size_before)}")
    print(f"  清理后: {format_size(size_after)}")
    print(f"  备份位置: {backup_dir}")
    print(f"\n提示: 如果程序运行异常，可以从备份恢复")
    
    return True


def restore_backup(target_dir):
    """从备份恢复"""
    dist_dir = os.path.dirname(target_dir) if os.path.isfile(target_dir) else target_dir
    
    # 查找备份目录
    backup_dirs = []
    for item in os.listdir(dist_dir):
        if 'backup' in item and os.path.isdir(os.path.join(dist_dir, item)):
            backup_dirs.append(item)
    
    if not backup_dirs:
        print("错误: 没有找到备份目录")
        return False
    
    # 显示备份列表
    print("\n找到以下备份:")
    for i, backup in enumerate(backup_dirs, 1):
        print(f"  {i}. {backup}")
    
    # 选择备份
    try:
        choice = int(input("\n选择要恢复的备份 (输入序号): "))
        if choice < 1 or choice > len(backup_dirs):
            print("无效的选择")
            return False
    except ValueError:
        print("无效的输入")
        return False
    
    selected_backup = backup_dirs[choice - 1]
    backup_path = os.path.join(dist_dir, selected_backup)
    
    # 确认恢复
    confirm = input(f"\n确认从 '{selected_backup}' 恢复? (y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return False
    
    # 执行恢复
    print(f"\n正在恢复...")
    
    # 删除当前目录
    if os.path.exists(target_dir):
        print(f"  删除当前目录: {target_dir}")
        shutil.rmtree(target_dir)
    
    # 从备份恢复
    print(f"  从备份恢复: {backup_path}")
    shutil.copytree(backup_path, target_dir)
    
    print(f"\n✓ 恢复完成!")
    print(f"  恢复来源: {backup_path}")
    
    # 询问是否删除备份
    delete_backup = input(f"\n是否删除备份 '{selected_backup}'? (y/n): ")
    if delete_backup.lower() == 'y':
        shutil.rmtree(backup_path)
        print(f"  ✓ 已删除备份")
    
    return True


def remove_cuda_files(target_dir, dry_run=False):
    """删除CUDA相关文件（如果只用CPU版本）"""
    print(f"\n{'[预览模式] ' if dry_run else ''}删除CUDA文件")
    print("=" * 70)
    
    if not os.path.exists(target_dir):
        print(f"错误: 目录不存在 {target_dir}")
        return False
    
    # 查找CUDA文件
    cuda_files_found = []
    for cuda_file in CUDA_FILES:
        for file_path in Path(target_dir).rglob(cuda_file):
            if file_path.is_file():
                cuda_files_found.append(file_path)
    
    if not cuda_files_found:
        print("没有找到CUDA文件")
        return True
    
    # 计算大小
    total_size = sum(f.stat().st_size for f in cuda_files_found)
    print(f"找到 {len(cuda_files_found)} 个CUDA文件")
    print(f"预计释放空间: {format_size(total_size)}")
    print("\n文件列表:")
    for f in cuda_files_found[:10]:
        print(f"  {format_size(f.stat().st_size):>12}  {f.name}")
    if len(cuda_files_found) > 10:
        print(f"  ... 还有 {len(cuda_files_found) - 10} 个文件")
    
    if dry_run:
        print("\n[预览模式] 未执行删除")
        return True
    
    # 警告
    print("\n⚠️ 警告: 删除CUDA文件后，程序将无法使用GPU加速!")
    print("   如果程序需要GPU支持，请不要删除这些文件。")
    
    confirm = input("\n确认删除CUDA文件? (y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return False
    
    # 创建备份
    backup_dir = backup_directory(target_dir)
    
    # 删除文件
    removed_count = 0
    removed_size = 0
    
    print("\n删除CUDA文件...")
    for file_path in cuda_files_found:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            removed_count += 1
            removed_size += file_size
            print(f"  ✓ {file_path.name}")
        except Exception as e:
            print(f"  ✗ {file_path.name}: {e}")
    
    print(f"\n{'=' * 70}")
    print(f"CUDA文件清理完成!")
    print(f"  删除文件: {removed_count} 个")
    print(f"  释放空间: {format_size(removed_size)}")
    print(f"  备份位置: {backup_dir}")
    
    return True


def main():
    """主函数"""
    # 解析参数
    target_dir = None
    dry_run = False
    restore_mode = False
    cuda_mode = False
    
    for arg in sys.argv[1:]:
        if arg == '--dry-run':
            dry_run = True
        elif arg == '--restore':
            restore_mode = True
        elif arg == '--cuda':
            cuda_mode = True
        elif os.path.exists(arg):
            target_dir = arg
    
    # 默认目录
    if not target_dir:
        target_dir = os.path.join(os.path.dirname(__file__), 'dist', '圣遗物预测器')
    
    # 执行相应操作
    if restore_mode:
        restore_backup(target_dir)
    elif cuda_mode:
        remove_cuda_files(target_dir, dry_run)
    else:
        clean_directory(target_dir, dry_run)


if __name__ == '__main__':
    main()

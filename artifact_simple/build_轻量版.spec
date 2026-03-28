# -*- mode: python ; coding: utf-8 -*-
# 轻量版打包配置 - 圣遗物预测器轻量版

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, Tree
from PyInstaller.utils.hooks import collect_dynamic_libs
import pandas
import numpy
import torch

block_cipher = None

# 获取库路径
def get_pandas_path():
    return pandas.__path__[0]

def get_numpy_path():
    return numpy.__path__[0]

def get_torch_path():
    return torch.__path__[0]

# 基础数据文件
datas = [
    ('config.py', '.'),
    ('dl_model.py', '.'),
    ('icon', 'icon'),  # 图标文件夹
]

a = Analysis(
    ['artifact_predictor.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # PyTorch C扩展
        'torch._C',
        'torch._C._nn',
        'torch._C._jit',
        'torch._C._autograd',
        'torch._C._sparse',
        # Pandas
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.hashtable',
        'pandas._libs.index',
        'pandas._libs.lib',
        'pandas._libs.parsers',
        'pandas.core',
        # NumPy
        'numpy.core._dtype_ctypes',
        'numpy.core._multiarray_umath',
        'numpy.core.multiarray',
        'numpy.core.umath',
        'numpy.random',
        'numpy.linalg',
        # PyTorch
        'torch.nn',
        'torch.optim',
        'torch.utils.data',
        # 其他
        'openpyxl',
        'openpyxl.cell._writer',
        'PyQt5',
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'sklearn',
        'seaborn',
        'plotly',
        'PIL',
        'Pillow',
        'imageio',
        'tqdm',
        'jupyter',
        'IPython',
        'notebook',
        'pytest',
        'requests',
        'urllib3',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 使用Tree确保关键目录完整
numpy_tree = Tree(get_numpy_path(), prefix='numpy', excludes=["*.pyc", "__pycache__", "*.lib"])
pandas_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc", "__pycache__", "*.lib"])

a.datas += numpy_tree
a.datas += pandas_tree

# torch 的 Python 文件用 Tree 添加到 datas
torch_tree = Tree(get_torch_path(), prefix='torch', excludes=["*.pyc", "__pycache__", "test", "testing", "*.lib", "*.dll", "*.pyd"])
a.datas += torch_tree

# 收集动态库到 a.binaries（collect_dynamic_libs 返回二元组，转为三元组）
for name, path in collect_dynamic_libs('numpy'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('pandas'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('torch'):
    a.binaries.append((name, path, 'BINARY'))

# torch 的 DLLs 需要显式添加到 binaries
torch_path = get_torch_path()
import os
for dll_file in ['torch_python.dll', 'torch.dll', 'torch_cpu.dll', 'torch_global_deps.dll']:
    dll_full_path = os.path.join(torch_path, 'lib', dll_file)
    if os.path.exists(dll_full_path):
        a.binaries.append((dll_file, dll_full_path, 'BINARY'))

# OpenMP DLL
for dll_file in ['libiomp5md.dll', 'libiompstubs5md.dll']:
    dll_full_path = os.path.join(torch_path, 'lib', dll_file)
    if os.path.exists(dll_full_path):
        a.binaries.append((dll_file, dll_full_path, 'BINARY'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='圣遗物预测器_轻量版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon\\icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='圣遗物预测器_轻量版',
)

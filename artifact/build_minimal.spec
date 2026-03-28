# -*- mode: python ; coding: utf-8 -*-
# 精简版 - 依赖 PyInstaller 自动分析，不使用 Tree

from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_dynamic_libs
import torch

block_cipher = None

# 基础数据文件
datas = [
    ('config.py', '.'),
    ('genmat401.npy', '.'),
    ('dl_model.py', '.'),
    ('icon', 'icon'),
]

a = Analysis(
    ['artifact_predictor.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # PyTorch
        'torch._C',
        'torch._C._nn',
        'torch._C._jit',
        'torch._C._autograd',
        'torch._C._sparse',
        'torch.nn',
        'torch.optim',
        'torch.utils.data',
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

# 收集动态库（二元组转三元组）
for name, path in collect_dynamic_libs('numpy'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('pandas'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('torch'):
    a.binaries.append((name, path, 'BINARY'))

# torch 核心 DLLs
torch_path = torch.__path__[0]
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
    name='圣遗物预测器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False, # 关闭控制台窗口查看错误和调试信息
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
    name='圣遗物预测器',
)

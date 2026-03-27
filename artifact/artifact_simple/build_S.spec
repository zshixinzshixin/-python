# -*- mode: python ; coding: utf-8 -*-
# S版打包配置 - 圣遗物预测器S版

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

# 收集动态库
binaries = []
binaries.extend(collect_dynamic_libs('numpy'))
binaries.extend(collect_dynamic_libs('pandas'))
binaries.extend(collect_dynamic_libs('torch'))

# 基础数据文件
datas = [
    ('config.py', '.'),
    ('dl_model.py', '.'),
    ('icon', 'icon'),  # 图标文件夹
    ('强化记录/models/best_model.pt', '强化记录/models'),  # 预训练模型
]

a = Analysis(
    ['artifact_predictor.py'],
    pathex=['.'],
    binaries=binaries,
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
# 排除静态库文件(.lib)以减小体积，这些文件编译时需要但运行时不需要
numpy_tree = Tree(get_numpy_path(), prefix='numpy', excludes=["*.pyc", "__pycache__", "*.lib"])
pandas_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc", "__pycache__", "*.lib"])
torch_tree = Tree(get_torch_path(), prefix='torch', excludes=["*.pyc", "__pycache__", "test", "testing", "*.lib"])

a.datas += numpy_tree
a.datas += pandas_tree
a.datas += torch_tree

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='圣遗物预测器S版',
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
    icon='icon\\icon.ico',  # exe文件图标
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='圣遗物预测器S版',
)

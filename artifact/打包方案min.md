# 圣遗物预测器 - 精简打包方案

## 方案概述

本方案使用 `build_minimal.spec` 进行打包，相比完整版 `build_working.spec` 具有以下特点：

- **体积更小**：约 735MB（完整版约 797MB）
- **启动更快**：不使用 Tree 强制收集库文件
- **依赖自动分析**：让 PyInstaller 自动处理依赖关系

## 核心差异

| 特性 | build_minimal.spec (精简版) | build_working.spec (完整版) |
|------|---------------------------|---------------------------|
| Tree 收集 | ❌ 不使用 | ✅ 使用 |
| 文件收集方式 | PyInstaller 自动分析 | 强制完整收集 |
| 体积 | ~735MB | ~797MB |
| 启动速度 | 更快 | 较慢 |
| 兼容性 | 依赖自动分析准确性 | 更完整 |

## 打包步骤

### 1. 环境准备

```bash
# 确保使用正确的 Python 版本 (3.12)
python --version

# 同步依赖
uv sync
```

### 2. 执行打包

```bash
# 使用精简版 spec
uv run pyinstaller --clean build_minimal.spec
```

### 3. 输出目录

打包完成后，程序位于：
```
dist/圣遗物预测器/
├── 圣遗物预测器.exe      # 主程序
├── _internal/            # 依赖库
│   ├── python312.dll
│   ├── torch/
│   ├── numpy/
│   ├── pandas/
│   └── ...
└── 强化记录/             # 数据目录（运行时创建）
    ├── models/
    └── records/
```

## 关键配置说明

### 动态库收集

```python
# 自动收集 numpy/pandas/torch 的 DLLs
for name, path in collect_dynamic_libs('numpy'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('pandas'):
    a.binaries.append((name, path, 'BINARY'))
for name, path in collect_dynamic_libs('torch'):
    a.binaries.append((name, path, 'BINARY'))
```

### 核心 DLL 显式添加

```python
# torch 核心 DLLs
torch_path = torch.__path__[0]
for dll_file in ['torch_python.dll', 'torch.dll', 'torch_cpu.dll', 'torch_global_deps.dll']:
    dll_full_path = os.path.join(torch_path, 'lib', dll_file)
    if os.path.exists(dll_full_path):
        a.binaries.append((dll_file, dll_full_path, 'BINARY'))

# OpenMP DLL（并行计算必需）
for dll_file in ['libiomp5md.dll', 'libiompstubs5md.dll']:
    dll_full_path = os.path.join(torch_path, 'lib', dll_file)
    if os.path.exists(dll_full_path):
        a.binaries.append((dll_file, dll_full_path, 'BINARY'))
```

### 隐藏导入

```python
hiddenimports=[
    # PyTorch C扩展
    'torch._C',
    'torch._C._nn',
    'torch._C._jit',
    'torch._C._autograd',
    'torch._C._sparse',
    # Pandas/NumPy 内部模块
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime',
    'numpy.core._dtype_ctypes',
    'numpy.core._multiarray_umath',
    # ...
]
```

## 性能优化

### 训练线程优化

训练功能已移至子线程执行，避免阻塞 GUI：

```python
class TrainingThread(QThread):
    """训练线程，避免阻塞 GUI"""
    finished = pyqtSignal(bool, str)
    
    def run(self):
        # 在子线程中执行训练
        trainer = ModelTrainer(self.data_manager)
        success, message = trainer.train(epochs=self.epochs)
        self.finished.emit(success, message)
```

### 排除不必要模块

```python
excludes=[
    'matplotlib',
    'scipy',
    'sklearn',
    'seaborn',
    'plotly',
    'PIL',
    'Pillow',
    # ...
]
```

## 常见问题

### Q: 打包后程序找不到模型文件？

A: 确保 `genmat401.npy` 在打包目录中，程序使用相对路径加载：
```python
base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
model_path = os.path.join(base_path, 'genmat401.npy')
```

### Q: 训练时界面卡顿？

A: 训练已在子线程中执行，界面不会卡死。如果感觉慢，是因为数据量不同导致的正常差异。

### Q: 如何减小体积？

A: 当前 735MB 主要包含：
- torch_cpu.dll: ~250MB
- Python 运行时: ~100MB
- 其他依赖: ~385MB

如需进一步减小，可考虑使用 UPX 压缩（会增加启动时间）。

### Q: 打包后启动慢？

A: 首次启动需要解压 `_internal` 中的文件，后续启动会快一些。

## 版本信息

- Python: 3.12
- PyTorch: 2.5.1
- PyInstaller: 6.19.0
- 打包日期: 2026-03-28

## 相关文件

- `build_minimal.spec` - 精简版打包配置
- `build_working.spec` - 完整版打包配置（备用）
- `artifact_predictor.py` - 主程序
- `dl_model.py` - 深度学习模型

# GameAuto 开发者指南

## 项目改造说明

本项目已成功改造为支持pip开发模式安装。主要更改包括：

### 1. 更新了 `pyproject.toml` 配置

- 添加了项目脚本入口点: `gameauto = "gameauto.__main__:main"`
- 配置了可选的开发依赖
- 使用自动包发现机制
- 配置了包数据（游戏资源文件）

### 2. 更新了 `MANIFEST.in`

- 明确指定要包含的文件类型
- 排除不必要的文件
- 包含游戏资源文件

### 3. 添加了版本信息

- 在 `gameauto/__init__.py` 中添加了 `__version__` 属性

### 4. 更新了 `README.md`

- 添加了详细的安装说明
- 包含开发模式安装指南
- 添加了使用示例

## 安装方式

### 开发模式安装

```bash
# 克隆仓库
git clone https://github.com/imbatony/gameauto.git
cd gameauto

# 创建虚拟环境（推荐）
python -m venv .venv
.venv\Scripts\activate  # Windows

# 安装为开发模式
pip install -e .

# 安装开发依赖
pip install -e .[dev]
```

### 生产环境安装

```bash
pip install gameauto
```

## 使用方式

### 命令行使用

安装后可以直接使用 `gameauto` 命令：

```bash
gameauto --game octopath farming
gameauto --game octopath myscript.txt --config myconfig.json
```

### Python模块使用

```python
from gameauto import GameAuto

gameauto = GameAuto("octopath", "config.json")
gameauto.run("farming")
```

## 开发工作流

### 1. 设置开发环境

```bash
git clone <repo-url>
cd gameauto
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

### 2. 代码修改

- 直接修改 `gameauto/` 目录下的源代码
- 由于使用了 `-e` 标志安装，修改会立即生效

### 3. 测试

```bash
# 运行测试
pytest

# 测试命令行工具
gameauto --help

# 测试Python导入
python -c "import gameauto; print(gameauto.__version__)"
```

### 4. 代码格式化

```bash
black gameauto/
```

### 5. 构建包

```bash
python -m build
```

## 项目结构

```
gameauto/
├── pyproject.toml          # 项目配置
├── MANIFEST.in            # 包文件清单
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
├── gameauto/              # 主包
│   ├── __init__.py        # 包初始化（包含版本信息）
│   ├── __main__.py        # 命令行入口
│   ├── octopath/          # 游戏特定模块
│   └── base/              # 基础功能模块
└── test/                  # 测试文件
```

## 发布流程

1. 更新版本号（在 `gameauto/__init__.py` 和 `pyproject.toml` 中）
2. 构建包：`python -m build`
3. 测试安装：`pip install dist/gameauto-*.whl`
4. 发布到PyPI：`twine upload dist/*`

## 注意事项

- 确保所有游戏资源文件都在 `gameauto/octopath/assets/` 目录下
- 命令行工具入口点配置在 `pyproject.toml` 的 `[project.scripts]` 部分
- 开发模式安装允许实时修改代码而无需重新安装
- 使用虚拟环境可以避免依赖冲突

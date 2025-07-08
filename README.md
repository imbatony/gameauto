# gameauto [![gameauto](https://github.com/imbatony/gameauto/actions/workflows/python-app.yml/badge.svg)](https://github.com/imbatony/gameauto/actions/workflows/python-app.yml)

一个简单的游戏自动化库

## 安装

### 从源码安装（开发模式）

```bash
# 克隆仓库
git clone https://github.com/imbatony/gameauto.git
cd gameauto

# 安装为开发模式（可编辑安装）
pip install -e .

# 或者安装开发依赖
pip install -e .[dev]
```

### 从PyPI安装

```bash
pip install gameauto
```

## 使用方法

安装后，你可以通过命令行使用gameauto：

```bash
# 运行内建任务
gameauto --game octopath farming

# 运行自定义脚本
gameauto --game octopath myscript.txt

# 指定配置文件
gameauto --game octopath farming --config myconfig.json
```

或者在Python代码中使用：

```python
from gameauto import GameAuto

# 初始化游戏自动化
gameauto = GameAuto("octopath", "config.json")

# 运行任务
gameauto.run("farming")

# 运行自定义脚本
gameauto.run_script("myscript.txt")
```

## 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/imbatony/gameauto.git
cd gameauto

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 安装开发依赖
pip install -e .[dev]
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black gameauto/
```

## 支持的游戏

- Octopath Traveler（歧路旅人）

## 系统要求

- Windows系统
- Python 3.7+
import os

# 游戏窗口标题
APP_NAME = os.getenv("GAMEAUTO_APP_NAME", "MuMu模拟器12")

# 默认应用窗口偏移, 用于调整游戏窗口的坐标,去除窗口边框
DEFAULT_APP_X_OFFSET = int(os.getenv("GAMEAUTO_APP_X_OFFSET", 0))
DEFAULT_APP_Y_OFFSET = int(os.getenv("GAMEAUTO_APP_Y_OFFSET", 50))

# 默认行动间隔延迟(ms)
DEFAULT_ACTION_DELAY = 500

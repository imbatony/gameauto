import os

# 游戏窗口标题
APP_NAME = os.getenv("GAMEAUTO_APP_NAME", "MuMu模拟器12")

# 默认应用窗口偏移, 用于调整游戏窗口的坐标,去除窗口边框
DEFAULT_APP_X_OFFSET = int(os.getenv("GAMEAUTO_APP_X_OFFSET", 0))
DEFAULT_APP_Y_OFFSET = int(os.getenv("GAMEAUTO_APP_Y_OFFSET", 50))

# 默认行动间隔延迟(ms)
DEFAULT_ACTION_DELAY = 250

# 默认ADB主机地址
ADB_HOST = os.getenv("GAMEAUTO_ADB_HOST", os.environ.get("ANDROID_ADB_SERVER_HOST", "127.0.0.1"))

# 默认ADB端口 5037
ADB_PORT = int(os.getenv("GAMEAUTO_ADB_PORT", int(os.environ.get("ANDROID_ADB_SERVER_PORT", 5037))))

# 歧路旅人的包名
_OCTOPATH_APP_PACKAGE_NAME = "com.netease.ma167"

_OCTOPATH_BILIBI_APP_PACKAGE_NAME = "com.netease.ma167.bilibili"


_OCTOPATH_APP_ACTIVITY_NAME = "com.epicgames.ue4.GameActivity"

# 默认的游戏包名

ANDRIOD_GAME_PACKAGE_NAME = os.getenv("GAMEAUTO_ANDRIOD_GAME_PACKAGE_NAME", _OCTOPATH_APP_PACKAGE_NAME)

# 默认的游戏Activity名
ANDRIOD_GAME_ACTIVITY_NAME = os.getenv("GAMEAUTO_ANDRIOD_GAME_ACTIVITY_NAME", _OCTOPATH_APP_ACTIVITY_NAME)

# 默认的Device Serial
DEFAULT_ANDROID_SERIAL = os.getenv("GAMEAUTO_ANDROID_SERIAL", os.environ.get("ANDROID_SERIAL", None))

from enum import Enum
from .base import BaseGUI
from .pyautogui import RealGUI


class GUIType(Enum):
    DEFAULT = "pyautogui"
    MOCK = "mock"


def getGUI(config: dict) -> BaseGUI:
    """
    获取GUI实例
    """
    gui_type = config.get("game", {}).get("gui", GUIType.DEFAULT.value)
    if gui_type == GUIType.DEFAULT.value:
        return RealGUI(config)
    else:
        raise ValueError(f"不支持的GUI类型:{gui_type}")

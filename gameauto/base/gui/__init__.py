from enum import Enum
from .base import BaseGUI, BaseApp
from .pyautogui import PYAutoGUI
from .adb import ADBGUI


class GUIType(Enum):
    DEFAULT = "pyautogui"
    PYAUTOGUI = "pyautogui"
    ADB = "adb"
    MOCK = "mock"


def getGUI(config: dict) -> BaseGUI:
    """
    获取GUI实例
    """
    gui_type = config.get("game", {}).get("gui", GUIType.DEFAULT.value)
    if gui_type == GUIType.DEFAULT.value or gui_type == GUIType.PYAUTOGUI.value:
        return PYAutoGUI(config)
    elif gui_type == GUIType.ADB.value:
        return ADBGUI(config)
    else:
        raise ValueError(f"不支持的GUI类型:{gui_type}")

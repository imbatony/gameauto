from .base import BaseGUI, BaseApp
import pyautogui
from ..tuples import Point, Box
from ...gameconstants import APP_NAME
from PIL import Image
from pygetwindow import (
    Win32Window,
    getWindowsWithTitle,
)


class Window32App(BaseApp):
    """
    Windows应用类
    """

    def __init__(self, win: Win32Window):
        super().__init__()
        self.win = win

    def app_position(self) -> Box:
        return Box(self.win.left, self.win.top, self.win.width, self.win.height)


class PYAutoGUI(BaseGUI):
    """
    通过pyautogui实现点击、拖拽、截图等操作
    """

    def __init__(self, config: dict):
        super().__init__(config=config)

    def screenshot(self, filename: str = None, region: Box = None) -> Image.Image:
        """
        截图
        """
        self.logger.debug(f"截图: {filename}, {region}")
        return pyautogui.screenshot(filename, region)

    def touch(self, p: Point, duration: float = 0.2):
        """
        触摸, 与click的区别在于不需要指定button,并且按键有持续时间
        """
        self.logger.debug(f"触摸: {p}")
        # 先移动到目标位置
        pyautogui.moveTo(x=p.x, y=p.y, duration=duration)
        # 再按下
        pyautogui.mouseDown(duration=duration)
        # 再抬起
        pyautogui.mouseUp()

    def dragLeftRight(
        self,
        start: Point,
        left: Point,
        right: Point,
        duration: float = 0.8,
        single_duration=0.2,
    ):
        """
        来回拖拽
        """
        pyautogui.moveTo(start)
        pyautogui.mouseDown()
        d_sum = 0
        while d_sum < duration:
            d_sum += single_duration * 4
            pyautogui.moveTo(left, duration=single_duration)
            pyautogui.moveTo(start, duration=single_duration)
            pyautogui.moveTo(right, duration=single_duration)
            pyautogui.moveTo(start, duration=single_duration)
        pyautogui.mouseUp()

    def active_app(self) -> Window32App | None:
        appname = self.config.get("game", {}).get("app_name", APP_NAME)
        if not appname:
            self.logger.error("未配置app_name")
            return None
        self.logger.debug(f"激活应用:{appname}")
        wins: list[Win32Window] = getWindowsWithTitle(appname)
        if not wins or len(wins) == 0:
            self.logger.error(f"未找到应用:{appname}")
            return None

        if len(wins) > 1:
            self.logger.warning(f"找到多个应用:{appname}, 取第一个")
        win = wins[0]
        win.show()
        win.activate()
        return Window32App(win)

    def drag(self, start: Point, end: Point, duration: float = 0.8):
        """
        拖拽
        """
        self.logger.debug(f"拖拽: {start} -> {end}")
        pyautogui.moveTo(start)
        pyautogui.dragTo(end, duration=duration)

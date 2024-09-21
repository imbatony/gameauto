import os
from ..utils import get_logger
from ..gameconstants import APP_NAME, DEFAULT_APP_X_OFFSET, DEFAULT_APP_Y_OFFSET
from .tuples import TxtBox
from .gui import BaseGUI, RealGUI
from .tuples import TxtBox, Point, Box
from pygetwindow import (
    Window,
    Win32Window,
    getWindowsWithTitle,
)


class BaseTaskCtx(object):
    """
    任务上下文
    任务执行过程中的上下文信息
    """

    # 最大历史状态记录长度
    max_status_len = 10
    # 最大历史截图记录长度
    max_screenshots_len = 10
    # 最大历史ocr结果记录长度
    max_ocr_results_len = 10

    def __init__(self, config: dict, gui: BaseGUI = None):
        self.app: Window = None
        # 截图
        self.his_screenshots: list[str] = []
        self.cur_screenshot: str | None = None
        self.his_status: list[int] = []
        self.cur_status = -1
        self.cur_ocr_result: list[TxtBox] = []
        self.his_ocr_results: list[list[TxtBox]] = []
        self.logger = get_logger(self.__class__.__name__, config)
        self.config = config
        # 偏移量, 用于调整窗口坐标, 排除窗口边框等
        self.x_offset = int(
            config.get("game", {}).get("x_offset", DEFAULT_APP_X_OFFSET)
        )
        self.y_offset = int(
            config.get("game", {}).get("y_offset", DEFAULT_APP_Y_OFFSET)
        )
        self.gui = gui or RealGUI(config)

    def active_app(self) -> bool:
        appname = self.config.get("game", {}).get("app_name", APP_NAME)
        self.logger.debug(f"激活应用:{appname}")
        apps: list[Win32Window] = getWindowsWithTitle(appname)
        if not apps or len(apps) == 0:
            self.logger.error(f"未找到应用:{appname}")
            return False

        if len(apps) > 1:
            self.logger.warning(f"找到多个应用:{appname}, 取第一个")
        app = apps[0]
        self.update_app(app)
        app.show()
        app.activate()
        return True

    @property
    def left(self) -> int:
        if not self.app:
            return self.x_offset
        return self.app.left + self.x_offset

    @property
    def top(self) -> int:
        if not self.app:
            return self.y_offset
        return self.app.top + self.y_offset

    @property
    def width(self) -> int:
        if not self.app:
            return 0
        return self.app.width - self.x_offset

    @property
    def height(self) -> int:
        if not self.app:
            return 0
        return self.app.height - self.y_offset

    @property
    def center(self) -> Point:
        return Point(self.left + self.width // 2, self.top + self.height // 2)

    @property
    def region(self) -> Box:
        return Box(self.left, self.top, self.width, self.height)

    def update_app(self, app):
        self.app = app
        return self

    def update_screenshot(self, screenshot, delete_old=True):
        if len(self.his_screenshots) >= self.max_screenshots_len:
            path = self.his_screenshots.pop(0)
            # 删除文件
            if delete_old and os.path.exists(path):
                os.remove(path)

        self.his_screenshots.append(screenshot)
        self.cur_screenshot = screenshot
        return self

    def update_status(self, status: int):
        if len(self.his_status) >= self.max_status_len:
            self.his_status.pop(0)
        self.his_status.append(status)
        self.cur_status = status
        return self

    def get_last_status(self):
        return self.cur_status

    def get_history_status(self, last: int):
        # 获取倒数第last个状态
        # last=0表示最后一个状态 即当前状态
        index = len(self.his_status) - last - 1
        if index < 0:
            index = 0
        return self.his_status[index]

    def update_ocr_result(self, ocr_result):
        if len(self.his_ocr_results) >= self.max_ocr_results_len:
            self.his_ocr_results.pop(0)
        self.cur_ocr_result = ocr_result
        self.his_ocr_results.append(ocr_result)
        return self

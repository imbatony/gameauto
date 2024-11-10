from abc import abstractmethod
import os
from typing import Optional
from ..utils import get_logger
from ..gameconstants import DEFAULT_APP_X_OFFSET, DEFAULT_APP_Y_OFFSET
from .tuples import TxtBox
from .gui import BaseGUI, getGUI, BaseApp
from .tuples import Point, Box


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

    def __init__(self, config: dict, gui: Optional[BaseGUI] = None):
        self.app: BaseApp = None
        # 截图
        self.his_screenshots: list[str] = []
        self.cur_screenshot: str | None = None
        self.his_status: list[int] = []
        self.cur_status = 0
        self.cur_ocr_result: list[TxtBox] = []
        self.his_ocr_results: list[list[TxtBox]] = []
        self.logger = get_logger(self.__class__.__name__, config)
        self.config = config
        # 偏移量, 用于调整窗口坐标, 排除窗口边框等
        self.x_offset = int(config.get("game", {}).get("x_offset", DEFAULT_APP_X_OFFSET))
        self.y_offset = int(config.get("game", {}).get("y_offset", DEFAULT_APP_Y_OFFSET))

        # 游戏窗口大小, 如果设置了, 则使用设置实际的大小，而不是app的大小
        # 用于适配不同分辨率的游戏窗口
        self.game_width = int(config.get("game", {}).get("width", -1))
        self.game_height = int(config.get("game", {}).get("height", -1))

        self.logger.debug(f"游戏窗口偏移量: ({self.x_offset}, {self.y_offset})")
        self.logger.debug(f"游戏窗口大小: ({self.width}, {self.height})")

        self.gui = gui or getGUI(config)
        self.debug = config.get("debug", False)

    def active_app(self):
        app = self.gui.active_app()
        if app is None:
            raise Exception("激活应用失败")
        else:
            self.update_app(app)

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
        if self.game_width > 0:
            return self.game_width
        if not self.app:
            return 0
        return self.app.width - self.x_offset

    @property
    def height(self) -> int:
        if self.game_height > 0:
            return self.game_height
        if not self.app:
            return 0
        return self.app.height - self.y_offset

    @property
    def center(self) -> Point:
        return Point(self.left + self.width // 2, self.top + self.height // 2)

    @property
    def region(self) -> Box:
        return Box(self.left, self.top, self.width, self.height)

    def get_absolute_pos(self, x, y) -> Point:
        return Point(x + self.left, y + self.top)

    def update_app(self, app):
        self.app = app
        return self

    def update_screenshot(self, screenshot, delete_old=None):

        if delete_old is None:
            # 默认删除旧截图, 除非是调试模式
            delete_old = not self.debug

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

    @abstractmethod
    def detect_status(self, ocr_result: list[TxtBox] = None) -> int:
        pass

    def __del__(self):
        if hasattr(self, "debug") and self.debug:
            # 测试状态不删除历史截图
            return
        self.logger.info("清理历史截图")
        if self.his_screenshots:
            for path in self.his_screenshots:
                if os.path.exists(path):
                    os.remove(path)

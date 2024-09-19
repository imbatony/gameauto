from abc import abstractmethod
import os
import time
from ..utils import get_logger
from .constants import ANDRIOD_EMULATOR_NAME
from .gui import RealGUI, BaseGUI
from .ctx import BaseTaskCtx
from .position import TextPosition


class BaseGameAction(object):
    """
    游戏动作基类
    动作的执行逻辑在run方法中实现, 通常由多个命令以及一些逻辑组成
    游戏动作通常有实际的游戏含义,如进行一次游戏战斗,进行一次游戏抽卡等
    游戏动作需要关心当前的游戏状态, 来决定执行哪些命令, 以及命令的执行逻辑和顺序
    多个动作可以组合成一个任务
    自定义脚本中一行通常对应一个动作
    """

    def __init__(self, config: dict, ctx: BaseTaskCtx, gui: BaseGUI = None, *args):
        self.config = config
        self.args = args
        self.gui = gui or RealGUI(config)
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name, config)
        self.ctx = ctx

    def run(self):
        raise NotImplementedError

    def active_app(self):
        self.logger.debug(f"激活应用")
        appname = self.config.get("appname", ANDRIOD_EMULATOR_NAME)
        app = self.gui.active_app(appname)
        self.ctx.update_app(app)

    def get_app_screen_shot(self) -> str:
        self.logger.debug(f"截取app窗口的屏幕截图")
        path = os.path.join(os.environ.get("TEMP"), f"{int(time.time())}.png")
        app_x, app_y, app_width, app_height = (
            self.ctx.x,
            self.ctx.y,
            self.ctx.width,
            self.ctx.height,
        )
        region = (app_x, app_y, app_width, app_height)
        self.gui.screenshot(path, region=region)
        self.ctx.cur_screenshot = path
        return path

    def renew_status(self, ocr=True) -> int:
        self.logger.debug(f"刷新当前状态")
        path = self.get_app_screen_shot()
        self.ctx.update_screenshot(path)
        if ocr:
            ocr_result = self.ocr(path)
            self.ctx.update_ocr_result(ocr_result)
        status = self.detect_status()
        self.ctx.update_status(status)
        return self.ctx.cur_status

    @abstractmethod
    def detect_status(self) -> int:
        """
        检测当前状态
        需要根据当前状态的特征，比如界面元素，文本等，判断当前状态
        状态值由具体的游戏决定
        """
        raise NotImplementedError

    def ocr(self, image_path) -> list[TextPosition]:
        list = self.gui.ocr(image_path)
        for idx in range(len(list)):
            line = list[idx]
            # 需要增加实际的应用的偏移量
            line.x += self.ctx.x
            line.y += self.ctx.y
        return list

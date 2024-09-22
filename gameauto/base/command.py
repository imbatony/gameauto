from abc import abstractmethod
from enum import Enum
import os
import time
from .ctx import BaseTaskCtx
from .tuples import TxtBox


class CommandReturnCode(Enum):
    SUCCESS = 0
    FAILED = 1
    TIMEOUT = 2
    CANCEL = 3
    UNKNOWN = 4


class BaseCommand:
    """
    游戏命令基类
    命令的执行逻辑在run方法中实现, 通常由多个动作以及一些逻辑组成
    游戏命令通常有实际的游戏含义,如进行一次游戏战斗,进行一次游戏抽卡等
    游戏命令需要关心当前的游戏状态, 来决定执行哪些命令, 以及命令的执行逻辑和顺序
    多个命令可以组合成一个任务
    自定义脚本中一行通常对应一个命令
    为了支持自定义脚本, 命令的参数必须是字符串, 需要在命令中解析
    """

    @classmethod
    @abstractmethod
    def run(cls, ctx: BaseTaskCtx, *args) -> CommandReturnCode:
        raise NotImplementedError

    @classmethod
    def get_app_screen_shot(cls, ctx: BaseTaskCtx) -> str:
        ctx.logger.debug(f"截取app窗口的屏幕截图")
        path = os.path.join(os.environ.get("TEMP"), f"{int(time.time())}.png")
        ctx.gui.screenshot(path, region=ctx.region)
        ctx.cur_screenshot = path
        return path

    @classmethod
    def renew_status(cls, ctx: BaseTaskCtx, ocr=True) -> int:
        ctx.logger.debug(f"刷新当前状态")
        path = cls.get_app_screen_shot(ctx)
        ctx.logger.debug(f"截图保存到:{path}")
        ctx.update_screenshot(path)
        if ocr:
            ocr_result = cls.ocr(ctx, path)
            ctx.update_ocr_result(ocr_result)
        status = cls.detect_status(ctx)
        ctx.update_status(status)
        return ctx.cur_status

    @classmethod
    @abstractmethod
    def detect_status(cls, ctx: BaseTaskCtx, ocr_result: list[TxtBox] = None) -> int:
        """
        检测当前状态
        需要根据当前状态的特征，比如界面元素，文本等，判断当前状态
        状态值由具体的游戏决定
        """
        raise NotImplementedError

    @classmethod
    def ocr(cls, ctx: BaseTaskCtx, image_path) -> list[TxtBox]:
        list = ctx.gui.ocr(image_path)
        list_with_offset = []
        for idx in range(len(list)):
            line = list[idx]
            # 需要增加实际的应用的偏移量
            line_with_offset = TxtBox(
                text=line.text,
                left=line.left + ctx.left,
                top=line.top + ctx.top,
                width=line.width,
                height=line.height,
            )
            list_with_offset.append(line_with_offset)
        return list_with_offset

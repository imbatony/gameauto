from abc import abstractmethod
from enum import Enum
from typing import Any
from ..utils import get_logger
from .ctx import BaseTaskCtx
from .gui import RealGUI, BaseGUI


class CommandRetStatus(Enum):
    SUCCESS = "SUCCESS"
    NOT_RUN = "NOT_RUN"
    TIMEOUT = "TIMEOUT"
    EXCEPTION = "EXCEPTION"


class CommandRet(object):
    def __init__(
        self,
        success: bool,
        status: CommandRetStatus,
        exp: Exception,
        ellipsis: int,
        obj: Any = None,
    ):
        self.status: CommandRetStatus = status
        self.success: bool = success
        self.exp: Exception = exp
        self.ellipsis: int = ellipsis
        self.obj: Any = obj

    def __str__(self):
        return f"CommandRet<status={self.status}, success={self.success}, ellipsis={self.ellipsis}, obj={self.obj}>"


class BaseCommand(object):
    """
    命令基类
    命令需要执行一系列操作，比如点击战斗按钮，滑动屏幕等
    命令通常不关心当前的游戏状态, 也没有复杂的逻辑, 只是需要根据游戏状态计算坐标, 例如点击需要根据当前的游戏状态来判断点击的位置
    一个命令的执行结果是一个CommandRet对象
    命令是游戏自动化的最小执行单元
    """

    def __init__(self, config: dict, gui: BaseGUI = None, *args, **kwargs):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name, config)
        self.config = config
        self.gui = gui or RealGUI(config)
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def run(self, ctx: BaseTaskCtx) -> CommandRet:
        """
        执行命令
        """
        raise NotImplementedError

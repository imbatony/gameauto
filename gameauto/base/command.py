from abc import abstractmethod
from enum import Enum
from .ctx import BaseTaskCtx


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
    def run(cls, ctx: BaseTaskCtx, *args: str) -> CommandReturnCode:
        raise NotImplementedError

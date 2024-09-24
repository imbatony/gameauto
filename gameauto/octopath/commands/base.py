from abc import abstractmethod
from ...base import BaseCommand, BaseTaskCtx, TxtBox, CommandReturnCode
from ..status import OctopathStatus
from ..actions import ACTION, runActionChain
from ..ctx import OctopathTaskCtx


class BaseOctopathCommand(BaseCommand):

    __alternate_names__ = []

    @classmethod
    def get_alternate_names(cls) -> list[str]:
        return cls.__alternate_names__

    @classmethod
    @abstractmethod
    def run(cls, ctx: BaseTaskCtx, *args) -> CommandReturnCode:
        raise NotImplementedError

    @classmethod
    def _runActions(cls, ctx: OctopathTaskCtx, actions: list[ACTION]) -> CommandReturnCode:
        command_name = cls.__alternate_names__[0]
        ret = runActionChain(ctx, actions)
        if not ret.success:
            ctx.logger.error(f"{command_name}失败")
            return CommandReturnCode.FAILED
        return CommandReturnCode.SUCCESS

    @classmethod
    def runAction(cls, ctx: OctopathTaskCtx, action: ACTION) -> CommandReturnCode:
        command_name = cls.__alternate_names__[0]
        ret = runActionChain(ctx, [action])
        if not ret.success:
            ctx.logger.error(f"{command_name}失败")
            return CommandReturnCode.FAILED
        return CommandReturnCode.SUCCESS

    @classmethod
    def runActionChain(cls, ctx: OctopathTaskCtx, *actions: ACTION) -> CommandReturnCode:
        action_list = list(actions)
        return cls._runActions(ctx, action_list)


class ChainedOctopathCommand(BaseOctopathCommand):
    """
    链式命令
    """

    @classmethod
    @abstractmethod
    def get_alternate_names(cls) -> list[str]:
        return []

    @classmethod
    @abstractmethod
    def commands(cls) -> list[type[BaseCommand]]:
        return []

    @classmethod
    def run(cls, ctx: BaseTaskCtx, *args) -> CommandReturnCode:
        for command in cls.commands():
            ret = command.run(ctx, *args)
            if ret != CommandReturnCode.SUCCESS:
                ctx.logger.error(f"命令执行失败:{command}")
                return ret
        return CommandReturnCode.SUCCESS

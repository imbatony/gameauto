from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx


class ForceExitToMenuCommand(BaseOctopathCommand):
    @classmethod
    def get_alternate_names(cls) -> list[str]:
        return ["强制返回主菜单", "ForceExitToMenu"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx) -> CommandReturnCode:
        """
        强制返回主菜单

        :return: 执行结果
        """
        ctx.logger.info("强制返回主菜单")
        return CommandReturnCode.SUCCESS

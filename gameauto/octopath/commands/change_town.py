from ..constants import TOWN, get_town_by_name
from .base import BaseOctopathCommand, CommandReturnCode, ChainedOctopathCommand
from ..ctx import OctopathTaskCtx
from ..status import OctopathStatus
from .force import ForceExitToMenuCommand
from ..actions import *


class ChangeTownCommand(BaseOctopathCommand):
    @classmethod
    def get_alternate_names(cls) -> list[str]:
        return ["切换城镇", "ChangeTown"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, town_name: str) -> CommandReturnCode:
        """
        切换城镇

        :param town_name: 城镇名称
        :return: 执行结果
        """
        ctx.logger.info("切换城镇 %s", town_name)
        town: TOWN = get_town_by_name(town_name)
        if town is None:
            ctx.logger.error(f"未找到城镇: {town_name}")
            return CommandReturnCode.FAILED

        status = cls.renew_status(ctx)
        if not OctopathStatus.is_menu(status):
            ctx.logger.error("当前不在主菜单, 请先返回主菜单")
            return CommandReturnCode.FAILED

        # 点击地图菜单
        ClickMenuAction.run(ctx, "大陆地图")

        return CommandReturnCode.SUCCESS


class ForceChangeTownCommand(ChainedOctopathCommand):

    @classmethod
    def get_alternate_names(cls) -> list[str]:
        return ["强制切换城镇", "ForceChangeTown"]

    @classmethod
    def get_chained_commands(cls):
        return [ForceExitToMenuCommand, ChangeTownCommand]

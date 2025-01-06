from time import sleep

from ..status import OctopathStatus
from ..constants import IconName, TOWN, getTownByName
from ...base import Point, CommandReturnCode
from .base import BaseOctopathCommand, CommandReturnCode
from ..actions import (
    ClickIconAction,
    ACTION,
    ClickAction,
)
from ..ctx import OctopathTaskCtx

class DevSetCurTownCommand(BaseOctopathCommand):
    __alternate_names__ = ["开发专用强制设置当前城镇", "DevOnlyForceSetCurTown"]
    @classmethod
    def run(cls, ctx: OctopathTaskCtx, town_name: str) -> CommandReturnCode:
        """
        开发专用强制设置当前城镇
        :param town_name: 城镇名称
        :return: 执行结果
        """
        ctx.logger.info("开发专用强制设置当前城镇 %s", town_name)
        town: TOWN = getTownByName(town_name)
        if town is None:
            ctx.logger.error(f"未找到城镇: {town_name}")
            return CommandReturnCode.FAILED

        # 如果当前已经在目标城镇, 则直接返回成功
        if ctx.cur_town == town:
            ctx.logger.info("当前已经在目标城镇")
            return CommandReturnCode.SUCCESS

        # 强制设置当前城镇
        ctx.cur_town = town
        return CommandReturnCode.SUCCESS
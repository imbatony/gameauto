from time import sleep
from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..actions import (
    ClickIconAction,
    ACTION,
    ClickAction,
    ClickCenterIconAction,
    DragLeftRightAction,
)
from ..constants import getIconNameByName
from ...base.tuples import Point


class ClickIconCommand(BaseOctopathCommand):
    __alternate_names__ = ["点击图标", "ClickIcon"]

    @classmethod
    def run(
        cls,
        ctx: OctopathTaskCtx,
        icon_name_str: str,
        wait_str: str = "1",
        is_center_str: str = "False",
    ) -> CommandReturnCode:
        """
        点击图标

        :param icon_name: 图标名称
        :param wait: 点击后等待时间
        :param is_center: 默认为False, 如果为True, 则当有多个图标时, 会点击中心位置

        :return: 执行结果
        """
        ctx.logger.info("点击图标 %s", icon_name_str)
        icon_name = getIconNameByName(icon_name_str)
        if icon_name is None:
            ctx.logger.error(f"未找到图标: {icon_name_str}")
            return CommandReturnCode.FAILED

        wait = float(wait_str)
        is_center = is_center_str.lower() == "true"

        if not is_center:
            code = cls.runAction(ctx, ACTION("点击图标", ClickIconAction, [icon_name], wait))
        else:
            code = cls.runAction(ctx, ACTION("点击图标", ClickCenterIconAction, [icon_name], wait))
        return code


class ClickPosCommand(BaseOctopathCommand):
    __alternate_names__ = ["点击坐标", "ClickPos"]

    @classmethod
    def run(
        cls,
        ctx: OctopathTaskCtx,
        x: str = None,
        y: str = None,
        wait_str: str = "1",
        is_relative_str: str = "False",
        relative_width_str: str = "1280",
        relative_height_str: str = "720",
    ) -> CommandReturnCode:
        """
        点击坐标

        :param x: x坐标
        :param y: y坐标
        :param wait_str: 点击后等待时间
        :param is_relative: 是否相对坐标, 默认为False, 如果为True, 则x, y为相对坐标, 需要传入相对宽高针对游戏窗口的宽高进行换算
        :param relative_width: 相对宽度
        :param relative_height: 相对高度

        :return: 执行结果
        """
        if x is None or y is None:
            # 如果没有传入坐标, 则点击中心
            x = ctx.width // 2
            y = ctx.height // 2

        x = int(x)
        y = int(y)

        is_relative = is_relative_str.lower() == "true"
        wait = float(wait_str)

        if is_relative:
            x = int(x * ctx.width / int(relative_width_str))
            y = int(y * ctx.height / int(relative_height_str))

        if x < 0 or x > ctx.width or y < 0 or y > ctx.height:
            ctx.logger.error(f"坐标超出范围: {x}, {y}")
            return CommandReturnCode.FAILED

        ctx.logger.info("点击坐标 %s, %s", x, y)
        return cls.runAction(
            ctx,
            ACTION("点击坐标", ClickAction, [Point(x, y), 0.4, False], wait),
        )


class WalkAroundCommand(BaseOctopathCommand):
    __alternate_names__ = ["原地走动", "WalkAround"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, duration_str: str = "8") -> CommandReturnCode:
        """
        原地走动, 用于触怪

        :param duration: 持续时间
        :return: 执行结果
        """

        ctx.logger.info("原地走动")
        duration = float(duration_str)
        start_time = ctx.getCurTime()
        while ctx.getCurTime() - start_time < duration:
            code = cls.runAction(ctx, ACTION("左右移动", DragLeftRightAction, [1 / 8, 2], 0))
            if code != CommandReturnCode.SUCCESS:
                return code

        return CommandReturnCode.SUCCESS

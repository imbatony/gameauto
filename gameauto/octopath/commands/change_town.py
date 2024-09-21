from time import sleep
from ..constants import TOWN, get_town_by_name, IconName
from ...base.tuples import Point, Box, TxtBox
from .base import (
    BaseOctopathCommand,
    CommandReturnCode,
    ChainedOctopathCommand,
)

from ..ctx import OctopathTaskCtx
from ..status import OctopathStatus
from .force import ForceExitToMenuCommand
from ..actions import ClickIconAction, EXE_ACTION, ClickAction


class ChangeTownCommand(BaseOctopathCommand):
    __alternate_names__ = ["切换城镇", "ChangeTown"]

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

        code = cls.run_actions(
            ctx,
            [
                EXE_ACTION("点击地图菜单", ClickIconAction, [IconName.MAP], 1),
                EXE_ACTION(
                    "点击缩小地图", ClickIconAction, [IconName.ZOOM_OUT_MAP], 0
                ),  # 因为下一步需要OCR, 所以不需要等待
            ],
        )
        if code != CommandReturnCode.SUCCESS:
            ctx.logger.error("切换城镇失败")
            return code

        # 等待地图加载
        sleep(1)
        # 获取当前屏幕截图
        path = cls.get_app_screen_shot(ctx)
        # 识别地图
        ocr_result = cls.ocr(ctx, path)
        # 如果城市位置在当前屏幕上,则直接点击
        for pos in ocr_result:
            if town.name in pos.text:
                ctx.logger.debug(f"找到城镇: {pos.text}")
                # 需要为点击位置添加偏移量, 图标在文字上方
                city_icon_pos = Point(
                    pos.center.x, pos.center.y - (30 / 720) * ctx.height
                )
                ret = cls.run_actions(
                    ctx,
                    [
                        EXE_ACTION("点击城镇", ClickAction, [city_icon_pos, 0.5], 0.5),
                        EXE_ACTION(
                            "点击前往这里",
                            ClickIconAction,
                            [IconName.CONFORM_GOTO],
                            0.8,
                        ),
                        EXE_ACTION(
                            "点击确认", ClickIconAction, [IconName.DIALOG_YES], 8
                        ),  # 等待8秒, 等待地图加载
                    ],
                )
                if code != CommandReturnCode.SUCCESS:
                    ctx.logger.error("切换城镇失败")
                    return CommandReturnCode.FAILED
                else:
                    ctx.logger.info(f"切换城镇{town_name}成功")
                    return CommandReturnCode.SUCCESS
        # 如果城市位置不在当前屏幕上,则计算滑动位置
        # 找到最接近中心位置的文字, 确定当前所在城镇
        center_pos: Point = ctx.region.center

        def distance(p1: Point, text_box: TxtBox) -> float:
            p2 = text_box.center
            return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2

        min_distance = 999999
        min_pos = None
        for pos in ocr_result:
            d = distance(center_pos, pos)
            if d < min_distance:
                min_distance = d
                min_pos = pos

        if min_pos is None:
            ctx.logger.error("未找到当前城镇")
            return CommandReturnCode.FAILED

        ctx.logger.debug(f"当前城镇: {min_pos.text}")

        return ret


class ForceChangeTownCommand(ChainedOctopathCommand):
    __alternate_names__ = ["强制切换城镇", "ForceChangeTown"]

    @classmethod
    def get_chained_commands(cls):
        return [ForceExitToMenuCommand, ChangeTownCommand]

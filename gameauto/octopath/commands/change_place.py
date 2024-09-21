from time import sleep
from ..constants import (
    TOWN,
    getTownByName,
    IconName,
    getWorldIconNameByTown,
    getWildByName,
    WILD,
)
from ...base.tuples import Point, TxtBox
from .base import (
    BaseOctopathCommand,
    CommandReturnCode,
    ChainedOctopathCommand,
)

from ..ctx import OctopathTaskCtx
from ..status import OctopathStatus
from .force import ForceExitToMenuCommand
from ..actions import ClickIconAction, EXE_ACTION, ClickAction, ClickCenterIconAction


class ChangeTownCommand(BaseOctopathCommand):
    __alternate_names__ = ["切换城镇", "ChangeTown"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, town_name: str) -> CommandReturnCode:
        """
        切换城镇

        :param town_name: 城镇名称
        :return: 执行结果
        """
        code = CommandReturnCode.UNKNOWN
        ctx.logger.info("切换城镇 %s", town_name)
        town: TOWN = getTownByName(town_name)
        if town is None:
            ctx.logger.error(f"未找到城镇: {town_name}")
            return CommandReturnCode.FAILED

        # 如果当前已经在目标城镇, 则直接返回成功
        if ctx.cur_town == town:
            ctx.logger.info("当前已经在目标城镇")
            return CommandReturnCode.SUCCESS

        status = cls.renew_status(ctx)
        if not OctopathStatus.is_menu(status):
            ctx.logger.error("当前不在主菜单, 请先返回主菜单")
            return CommandReturnCode.FAILED

        world_icon_name = getWorldIconNameByTown(town)

        code = cls.run_actions(
            ctx,
            [
                EXE_ACTION("点击地图菜单", ClickIconAction, [IconName.MAP], 1),
                EXE_ACTION("切换世界", ClickIconAction, [world_icon_name], 1),
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
        ctx.logger.debug("获取当前屏幕截图")
        path = cls.get_app_screen_shot(ctx)
        # 识别地图
        ocr_result = cls.ocr(ctx, path)
        # 如果城市位置在当前屏幕上,则直接点击
        code = cls.click_town_if_in_screen(ctx, town)
        if code == CommandReturnCode.SUCCESS:
            ctx.logger.info(f"切换城镇{town.name}成功")
            ctx.cur_town = town
            ctx.cur_wild = None
            return CommandReturnCode.SUCCESS
        if code != CommandReturnCode.UNKNOWN:
            return code

        # 如果城市位置不在当前屏幕上,则计算滑动位置
        # 找到最接近中心位置的文字, 确定当前所在城镇
        min_pos = cls.get_close_town(ctx, ocr_result)
        if min_pos is None:
            return CommandReturnCode.FAILED

        ctx.logger.debug(f"当前城镇: {min_pos.text}")
        return code

    @classmethod
    def click_town_if_in_screen(cls, ctx: OctopathTaskCtx, town: TOWN):
        path = cls.get_app_screen_shot(ctx)
        ocr_result = cls.ocr(ctx, path)
        for pos in ocr_result:
            if town.keyword in pos.text:
                city_icon_pos = Point(
                    pos.center.x, pos.center.y - (30 / 720) * ctx.height
                )
                code = cls.click_city_pos(ctx, city_icon_pos)
                if code != CommandReturnCode.SUCCESS:
                    ctx.logger.error("切换城镇失败")
                    return CommandReturnCode.FAILED
                else:
                    ctx.logger.info(f"切换城镇{town.name}成功")
                    return CommandReturnCode.SUCCESS
        return CommandReturnCode.UNKNOWN

    @classmethod
    def get_close_town(cls, ctx: OctopathTaskCtx, ocr_result) -> Point | None:
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
            return None

        return min_pos

    @classmethod
    def click_city_pos(cls, ctx: OctopathTaskCtx, pos: Point):
        code = cls.run_actions(
            ctx,
            [
                EXE_ACTION("点击城镇", ClickAction, [pos, 0.5], 0.5),
                EXE_ACTION(
                    "点击前往这里", ClickIconAction, [IconName.CONFORM_GOTO], 0.8
                ),
                EXE_ACTION("点击确认", ClickIconAction, [IconName.DIALOG_YES], 10),
            ],
        )
        return code


class ForceChangeTownCommand(ChainedOctopathCommand):
    __alternate_names__ = ["强制切换城镇", "ForceChangeTown"]

    @classmethod
    def get_chained_commands(cls):
        return [ForceExitToMenuCommand, ChangeTownCommand]


class ChangeToWildCommand(BaseOctopathCommand):
    __alternate_names__ = ["切换到野外", "ChangeToWild"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, wild_name) -> CommandReturnCode:
        """
        切换到野外

        :param wild_name: 野外名称
        :return: 执行结果
        """
        code = CommandReturnCode.UNKNOWN
        ctx.logger.info("切换到野外 %s", wild_name)
        wild: WILD = getWildByName(wild_name)
        if wild is None:
            ctx.logger.error(f"未找到野外: {wild_name}")
            return CommandReturnCode.FAILED

        # 如果当前已经在野外, 则无需切换
        if ctx.cur_wild == wild:
            ctx.logger.info(f"当前已经在{wild_name}")
            return CommandReturnCode.SUCCESS

        in_nearby_city = False

        # 如果当前已经在附近城市中, 则无需切换城市
        if ctx.cur_town is not None:
            if ctx.cur_town.name == wild.town_name_near_by:
                ctx.logger.info(f"当前已经在{ctx.cur_town.name}")
                in_nearby_city = True

        if not in_nearby_city:
            code = ChangeTownCommand.run(ctx, wild.town_name_near_by)
            if code != CommandReturnCode.SUCCESS:
                ctx.logger.error("切换城市失败")
                return code

        code = cls.run_actions(
            ctx,
            [
                EXE_ACTION("点击地图菜单", ClickIconAction, [IconName.MAP], 1),
                EXE_ACTION(
                    "点击野外图标", ClickCenterIconAction, [wild.icon_name], 1
                ),  # 点击野外图标
                EXE_ACTION(
                    "点击前往这里", ClickIconAction, [IconName.CONFORM_GOTO], 0.8
                ),
                EXE_ACTION("点击确认", ClickIconAction, [IconName.DIALOG_YES], 8),
            ],
        )
        if code != CommandReturnCode.SUCCESS:
            ctx.logger.error("切换野外失败")
            return code

        ctx.cur_wild = wild
        ctx.cur_town = None
        ctx.logger.info(f"切换到野外{wild_name}成功")
        return CommandReturnCode.SUCCESS

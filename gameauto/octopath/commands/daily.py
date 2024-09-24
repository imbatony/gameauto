from time import sleep

from ..status import OctopathStatus
from ..constants import IconName, TOWN, getTownByName
from ...base import Point, CommandReturnCode
from .move.change_place import ChangeTownCommand
from ..actions import (
    ClickIconAction,
    ACTION,
    ClickAction,
)
from ..ctx import OctopathTaskCtx


class GetItemsInNamelessTown(ChangeTownCommand):

    __alternate_names__ = ["无名小镇回收道具", "日常回收", "GetItemsInNamelessTown"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx) -> CommandReturnCode:
        """
        日常任务:
        无名小镇回收道具
        :return: 执行结果
        """
        town: TOWN = getTownByName("无名小镇")
        status = cls.renew_status(ctx)
        if not OctopathStatus.is_menu(status):
            ctx.logger.error("当前不在主菜单, 请先返回主菜单")
            return CommandReturnCode.FAILED
        # 切换到世界地图, 并缩小地图，以方便查找城镇
        code = cls.click_map_and_zoom_out(ctx, IconName.WORLD_NORMAL)

        if code != CommandReturnCode.SUCCESS:
            ctx.logger.error("切换城镇失败")
            return code

        # 等待地图加载
        sleep(1)
        # 获取当前屏幕截图
        ctx.logger.debug("获取当前屏幕截图")
        path = cls.get_app_screen_shot(ctx)
        # 识别地图
        ocr_result = ctx.ocr(path)
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
    def click_city_pos(cls, ctx: OctopathTaskCtx, pos: Point):
        """
        无名小镇回收道具

        """
        code = cls.runActionChain(
            ctx,
            ACTION("点击城镇", ClickAction, [pos, 0.5], 0.5),
            ACTION("点击回收道具", ClickIconAction, [IconName.MAPICON_SELECTED_BTN_GET_ITEM], 0.8),
            ACTION("点击是", ClickIconAction, [IconName.DIALOG_GET_ITEM_YES], 3),
            ACTION("点击确认", ClickIconAction, [IconName.DIALOG_GET_ITEM_CONFIRM], 1),
            ACTION("点击关闭", ClickIconAction, [IconName.EXIT], 1),
        )
        return code

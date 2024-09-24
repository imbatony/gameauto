from ...constants import IconName, getAssetPath, getIconByIconName, ICON
from ..base import (
    BaseOctopathCommand,
    CommandReturnCode,
)

from ...ctx import OctopathTaskCtx
from ...actions import ClickIconAction, ACTION, ClickAction
from ....base import Point, Box


class EnterHotelAndSleepCommand(BaseOctopathCommand):
    __alternate_names__ = ["进入旅馆休息", "EnterHotelAndSleep"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx) -> CommandReturnCode:
        """
        进入旅馆

        :return: 执行结果
        """
        ctx.logger.info("进入旅馆")

        icon_hotel = getIconByIconName(IconName.HOTEL)
        icon_hotel_path = getAssetPath(icon_hotel.asset)
        box: Box = ctx.gui.locateCenterOnScreen(icon_hotel_path, confidence=0.8, grayscale=True, region=ctx.region)

        if box:
            # 如果当前能找到旅馆图标, 则直接点击进入, 一般3秒内就能找到,这时无法通过小地图进入，因为图标会被遮挡
            ctx.logger.debug("找到旅馆图标, 直接点击进入")
            code = cls.runAction(ctx, ACTION("点击旅馆", ClickAction, [box.center], 3))
        else:
            # 如果当前不能找到旅馆图标, 则通过小地图进入
            code = cls.runActionChain(
                ctx,
                ACTION("点击小地图", ClickIconAction, [IconName.MINI_MAP], 1),
                # 一般旅馆离城镇较近, 所以一般10秒内就能找到
                # 0.98是为了避免误点到其他图标, 关闭灰度检测避免检测到地图上的图标
                ACTION("点击进入旅馆", ClickIconAction, [IconName.HOTEL_MINI_MAP, 0.2, False, 0.98], 10),
            )

        code = cls.runActionChain(
            ctx,
            ACTION("点击床的图标,触发NPC对话", ClickIconAction, [IconName.BED, 0.2, True, 0.7], 1.5),  # 一般1.5秒内就能找到
            ACTION("点击跳过对话", ClickAction, [], 1),
            ACTION("点击跳过对话", ClickAction, [], 2),
            ACTION("点击是", ClickIconAction, [IconName.DIALOG_YES], 6),  # 一般休息需要等待6秒
            ACTION("点击确定", ClickIconAction, [IconName.DIALOG_CONFIRM], 1),
        )

        if code != CommandReturnCode.SUCCESS:
            ctx.logger.error("进入旅馆失败")
            return code

        # TODO:针对特殊情况, 需要添加一些特殊处理逻辑,通过识别床的图标判断是否进入旅馆

        # 休息后重置战斗次数
        ctx.battle_count_after_sleep = 0
        return CommandReturnCode.SUCCESS

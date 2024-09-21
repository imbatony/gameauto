from ..constants import IconName
from .base import (
    BaseOctopathCommand,
    CommandReturnCode,
)

from ..ctx import OctopathTaskCtx
from ..actions import ClickIconAction, EXE_ACTION, ClickAction


class EnterHotelAndSleepCommand(BaseOctopathCommand):
    __alternate_names__ = ["进入旅馆休息", "EnterHotelAndSleep"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx) -> CommandReturnCode:
        """
        进入旅馆

        :return: 执行结果
        """
        ctx.logger.info("进入旅馆")

        code = cls.run_actions(
            ctx,
            [
                EXE_ACTION("点击小地图", ClickIconAction, [IconName.MINI_MAP], 1),
                EXE_ACTION(
                    "点击进入旅馆",
                    ClickIconAction,
                    [
                        IconName.HOTEL_IN_MINI_MAP,
                        0.2,
                        False,
                        0.98,
                    ],  # 0.98是为了避免误点到其他图标, 关闭灰度检测避免检测到地图上的图标
                    10,
                ),
                # 一般旅馆离城镇较近, 所以一般10秒内就能找到
                EXE_ACTION("点击休息", ClickIconAction, [IconName.BED], 1.5),
                EXE_ACTION("点击跳过对话", ClickAction, [], 2),
                EXE_ACTION(
                    "点击是", ClickIconAction, [IconName.DIALOG_YES], 8
                ),  # 一般需要等待8秒
                EXE_ACTION("点击确定", ClickIconAction, [IconName.DIALOG_CONFIRM], 1),
            ],
        )

        if code != CommandReturnCode.SUCCESS:
            ctx.logger.error("进入旅馆失败")
            return code

        # TODO:针对特殊情况, 需要添加一些特殊处理逻辑,通过识别床的图标判断是否进入旅馆

        # 休息后重置战斗次数
        ctx.battle_count_after_sleep = 0
        return CommandReturnCode.SUCCESS

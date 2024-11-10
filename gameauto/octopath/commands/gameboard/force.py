from ..base import BaseOctopathCommand, CommandReturnCode
from ...ctx import OctopathTaskCtx
from ...actions import ClickIconAction, ACTION, ClickAction, KACTION
from ...constants import IconName
from ....base import Point
from ...status import OctopathStatus
from .status import detectGameboardStatus


class RestRoadCommand(BaseOctopathCommand):

    __alternate_names__ = ["重置路线", "RestRoad"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        ctx.chosse_road = 0


class ForceExitGameBoardCommand(BaseOctopathCommand):
    """
    强制退出游戏盘
    """

    __alternate_names__ = ["强制退出游戏盘", "ForceExitGameBoard"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        """
        强制退出游戏盘

        :return: 执行结果
        """
        ctx.logger.info("强制退出游戏盘")
        end = False
        finished = False
        while not end:
            path = ctx.renew_current_screen()
            status, box, boost = detectGameboardStatus(ctx, path)
            center = Point(0, 0)
            if box is not None:
                center = box.center
            ctx.logger.info(f"当前状态：{status}")
            if status == OctopathStatus.Gameboard_Start.value:
                ctx.logger.info("退出游戏盘成功")
                return CommandReturnCode.SUCCESS
            if status & OctopathStatus.CanQuit.value == OctopathStatus.CanQuit.value:
                cls.runActionChain(
                    ctx,
                    KACTION("点击选项", ClickIconAction, {"icon_name": IconName.GAME_BOARD_OPTION, "screen": path}, 1),
                    ACTION("点击退出", ClickIconAction, [IconName.GAME_BOARD_END], 1),
                    ACTION("点击是", ClickIconAction, [IconName.DIALOG_YES], 5),
                    ACTION("点击确认", ClickIconAction, [IconName.GAME_BOARD_CONFIRM], 3),
                )

            elif status == OctopathStatus.Gameboard_ChooseRoad.value:
                cls.runActionChain(
                    ctx,
                    # 防止异常情况，点击两次
                    KACTION("点击确认", ClickAction, {"duration": 0.05}, 0.1),
                    KACTION(
                        "选择最短的路",
                        ClickAction,
                        {
                            "pos": center,
                        },
                    ),
                )
            elif status == OctopathStatus.Gameboard_CONFIRM.value:
                cls.runAction(
                    ctx,
                    KACTION(
                        "点击确认",
                        ClickIconAction,
                        {"icon_name": IconName.GAME_BOARD_CONFIRM, "screen": path},
                    ),
                )
            elif status == OctopathStatus.Combat.value:
                cls.runActionChain(
                    ctx, ACTION("强制退出战斗", ClickIconAction, [IconName.BATTLE_FORCE_END], 2), ACTION("点击确认", ClickIconAction, [IconName.DIALOG_YES], 2)
                )
            else:
                cls.runAction(ctx, KACTION("点击确认", ClickAction, {"duration": 0.05}, 0.1))

        ctx.chosse_road = 0
        return CommandReturnCode.SUCCESS

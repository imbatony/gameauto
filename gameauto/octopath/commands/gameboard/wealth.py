from time import sleep
from ..base import BaseOctopathCommand, CommandReturnCode
from ...ctx import OctopathTaskCtx
from ...actions import ClickIconAction, ACTION, ClickAction, KACTION
from ...constants import IconName
from ....base import Point, Box
from PIL import Image
from typing import NamedTuple, Optional, Tuple, Union
from ...status import OctopathStatus
from pathlib import Path
from ....base import Box
from PIL import Image
from .status import GameboardStatus, detectGameboardStatus


class WealthGameBoardStage1Command(BaseOctopathCommand):
    """
    财富游戏板
    """

    __alternate_names__ = ["财富游戏盘阶段1", "GameBoardWealthStage1"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        """
        财富游戏盘

        :return: 执行结果
        """
        ctx.logger.info("财富游戏盘开始")
        # 将消耗的游戏券设为为0，并将敌人强度设为5
        cls.runActionChain(
            ctx,
            # 点击开始游戏
            ACTION("点击游玩", ClickIconAction, [IconName.GAME_BOARD_PLAY], 1),
            ACTION("游戏券设为为0", ClickAction, [Point(320, 293)], 1),
            ACTION("敌人强度+1", ClickAction, [Point(954, 293)]),
            ACTION("敌人强度+1", ClickAction, [Point(954, 293)]),
            ACTION("敌人强度+1", ClickAction, [Point(954, 293)]),
            ACTION("敌人强度+1", ClickAction, [Point(954, 293)]),
            ACTION("敌人强度+1", ClickAction, [Point(954, 293)], 1),
            ACTION("点击游玩", ClickIconAction, [IconName.GAME_BOARD_PLAY]),
        )
        # 遇到岔路，选择上面的路，需要点击三下
        # 遇到
        end = False
        dead = False
        round_start = ctx.getCurTime()
        while not end:
            path = ctx.renew_current_screen()
            status, box, boost = detectGameboardStatus(ctx, path)
            ctx.logger.debug(f"当前状态: {status}, {box}")
            center = Point(0, 0)
            if box is not None:
                center = box.center
            if status == OctopathStatus.Gameboard_ChooseRoad.value:
                cls.runActionChain(
                    ctx,
                    # 防止异常情况，点击两次
                    ACTION("点击确认", ClickAction, [], 0.2),
                    KACTION(
                        "选择最短的路",
                        ClickAction,
                        {
                            "pos": center,
                        },
                    ),
                )

            elif status == OctopathStatus.Gameboard_ChooseStrongOrWeeker.value:
                cls.runAction(
                    ctx,
                    KACTION(
                        "选择强敌",
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
                        ClickAction,
                        {
                            "pos": center,
                        },
                    ),
                )

            elif status & OctopathStatus.Gameboard_FREE.value == OctopathStatus.Gameboard_FREE.value:
                cls.runActionChain(
                    ctx,
                    KACTION(
                        "点击骰子",
                        ClickAction,
                        {
                            "pos": center,
                        },
                    ),
                    ACTION("点击确认", ClickAction, [], 0.2),
                )

            elif status == OctopathStatus.Gameboard_FINISH.value:
                end = True

            elif status == OctopathStatus.Combat.value:
                ctx.logger.info("进入战斗")
                return CommandReturnCode.SUCCESS
            else:
                cls.runAction(ctx, ACTION("点击确认", ClickAction, [], 0.2))

            if ctx.getCurTime() - round_start > 100:
                dead = True
                end = True

        if dead:
            cls.runAction(ctx, ACTION("点击确认", ClickAction, [], 0.2))

        return CommandReturnCode.SUCCESS

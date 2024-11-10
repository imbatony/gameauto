from enum import Enum
from ..base import BaseOctopathCommand, CommandReturnCode
from ...ctx import OctopathTaskCtx
from ...actions import ClickIconAction, ACTION, ClickAction, KACTION, ClickDiceAction
from ...constants import IconName
from ....base import Point
from ...status import OctopathStatus
from .status import GameboardStatus, detectGameboardStatus


class PowerGameBoardStartCommand(BaseOctopathCommand):
    """
    权威游戏盘
    """

    __alternate_names__ = ["权威游戏盘开始", "PowerGameBoardStart"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        """
        权威游戏盘

        :return: 执行结果
        """
        ctx.logger.info("权威游戏盘开始")
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
        return CommandReturnCode.SUCCESS


class ROAD_CHOICE(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


road_chooses = [
    Point(640 - 100, 320),  # left
    Point(640 + 100, 320),  # right
    Point(640, 320 - 100),  # up
    Point(320, 320 + 100),  # down
]

power_chooses = [
    ROAD_CHOICE.LEFT,  # left
    ROAD_CHOICE.RIGHT,  # right
    ROAD_CHOICE.UP,  # up
    ROAD_CHOICE.LEFT,  # left
]


class PowerGameBoardCommand(BaseOctopathCommand):
    """
    权威游戏盘
    """

    __alternate_names__ = ["权威游戏盘", "PowerGameBoard"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        """
        权威游戏盘

        :return: 执行结果
        """
        # 遇到岔路，选择上面的路，需要点击三下
        # 遇到
        end = False
        dead = False
        round_start = ctx.getCurTime()
        while not end:
            path = ctx.renew_current_screen()
            status, box, boost = detectGameboardStatus(ctx, path)
            ctx.logger.debug(f"当前状态: {status}, {box}, {boost}")
            center = Point(0, 0)
            if box is not None:
                center = box.center
            if status == OctopathStatus.Gameboard_ChooseRoad.value:
                road = ctx.updateChooseRoad(4)  # 一共四个岔路
                choose = power_chooses[road]
                ctx.logger.info(f"当前第{road + 1}条岔路, 选择{choose}")
                pos = road_chooses[choose.value]
                cls.runActionChain(
                    ctx,
                    # 防止异常情况，点击两次
                    KACTION("点击确认", ClickAction, {"duration": 0.15}, 0.1),
                    KACTION(
                        "选择最短的路",
                        ClickAction,
                        {
                            "pos": pos,
                            "duration": 0.15,
                        },
                        1,
                    ),
                )

            elif status == OctopathStatus.Gameboard_ChooseStrongOrWeeker.value:
                cls.runActionChain(
                    ctx,
                    KACTION(
                        "选择强敌",
                        ClickAction,
                        {
                            "pos": center,
                            "duration": 0.05,
                        },
                        0,
                    ),
                )

            elif status == OctopathStatus.Gameboard_CONFIRM.value:
                cls.runActionChain(
                    ctx,
                    KACTION(
                        "点击确认",
                        ClickAction,
                        {
                            "pos": center,
                            "duration": 0.05,
                        },
                        0.5,
                    ),
                    KACTION(
                        "点击确认",
                        ClickAction,
                        {
                            "pos": center,
                            "duration": 0.05,
                        },
                        0.5,
                    ),
                    KACTION(
                        "点击确认",
                        ClickAction,
                        {
                            "pos": center,
                            "duration": 0.05,
                        },
                        0.5,
                    ),
                )

            elif status & OctopathStatus.Gameboard_FREE.value == OctopathStatus.Gameboard_FREE.value:
                cls.runActionChain(
                    ctx,
                    KACTION(
                        "点击骰子",
                        ClickDiceAction,
                        {
                            "center": center,
                            "boost": boost,
                        },
                        0.4,
                    ),
                    KACTION("点击确认", ClickAction, {"duration": 0.05}, 0),
                )

            elif status == OctopathStatus.Gameboard_FINISH.value:
                end = True

            elif status == OctopathStatus.Combat.value:
                ctx.logger.info("进入战斗")
                return CommandReturnCode.SUCCESS
            else:
                cls.runActionChain(ctx, KACTION("点击确认", ClickAction, {"duration": 0.15}, 0.05), KACTION("点击确认", ClickAction, {"duration": 0.15}, 0.05))

            if ctx.getCurTime() - round_start > 300:
                dead = True
                end = True

        if dead:
            cls.runAction(ctx, KACTION("点击确认", ClickAction, {"duration": 0.15}, 0.1))

        return CommandReturnCode.SUCCESS

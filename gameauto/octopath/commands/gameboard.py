from time import sleep
from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..actions import ClickIconAction, ACTION, ClickAction, KACTION
from ..constants import IconName
from ...base import Point
from PIL import Image
from typing import Optional, Tuple, Union
from ..status import OctopathStatus
from pathlib import Path
from ...base import Box


def _detect_status_with_screen_shot(ctx: OctopathTaskCtx, screenshot: Union[str, Image.Image, Path]) -> Tuple[int, Optional[Box]]:
    # 检测当前状态, 根据屏幕截图判断当前状态
    status = OctopathStatus.Unknown.value
    box = None
    box = ctx.findImageInScreen(IconName.GAME_BOARD_PLAY, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_Start.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_CONFIRM, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_NEED, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_NONEED, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_IGNORE, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_LOVER, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_DICE, screenshot, confidence=0.93, region=ctx.dice_region)
    if box is not None:
        status = OctopathStatus.Gameboard_FREE.value | OctopathStatus.CanQuit.value
        return status, box

    box = ctx.findImageInScreen(IconName.TRAITS_IN_BATTLE, screenshot, confidence=0.9, region=ctx.battle_region)
    if box is not None:
        status = OctopathStatus.Combat.value
        return status, box

    box = ctx.findImageInScreen(IconName.ATTACK, screenshot, confidence=0.9, region=ctx.attack_region)
    if box is not None:
        status = OctopathStatus.CanAttack.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_UP, screenshot, confidence=0.9, grayscale=True)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_RIGHT, screenshot, confidence=0.9, grayscale=True)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        box = Box(box.left + box.width / 2, box.top, box.width, box.height)
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_LEFT, screenshot, confidence=0.9, grayscale=True)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return status, box

    # box = ctx.findImageInScreen(IconName.GAME_BOARD_DICE2, screenshot, confidence=0.9, grayscale=True)
    # if box is not None:
    #     status = OctopathStatus.Gameboard_FREE.value | OctopathStatus.CanQuit.value
    #     return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_STORNGER, screenshot, confidence=0.9, grayscale=True)
    if box is not None:
        ctx.logger.info("检测到强敌，选择强敌路线")
        status = OctopathStatus.Gameboard_ChooseStrongOrWeeker.value
        return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_UP, screenshot, confidence=0.9, grayscale=True)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return status, box

    return status, None


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
            status, box = _detect_status_with_screen_shot(ctx, path)
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


class PowerGameBoardStage1Command(BaseOctopathCommand):
    """
    权威游戏盘
    """

    __alternate_names__ = ["权威游戏盘阶段1", "PowerGameBoardStage1"]

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
        # 遇到岔路，选择上面的路，需要点击三下
        # 遇到
        end = False
        dead = False
        round_start = ctx.getCurTime()
        while not end:
            path = ctx.renew_current_screen()
            status, box = _detect_status_with_screen_shot(ctx, path)
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

            if ctx.getCurTime() - round_start > 160:
                dead = True
                end = True

        if dead:
            cls.runAction(ctx, ACTION("点击确认", ClickAction, [], 0.2))

        return CommandReturnCode.SUCCESS


class FameGameBoardStage1Command(BaseOctopathCommand):
    """
    名声游戏盘
    """

    __alternate_names__ = ["名声游戏盘阶段1", "FameGameBoardStage1"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> CommandReturnCode:
        """
        名声游戏盘

        :return: 执行结果
        """
        ctx.logger.info("名声游戏盘开始")
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
            status, box = _detect_status_with_screen_shot(ctx, path)
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

            if ctx.getCurTime() - round_start > 200:
                dead = True
                end = True

        if dead:
            cls.runAction(ctx, ACTION("点击确认", ClickAction, [], 0.2))

        return CommandReturnCode.SUCCESS


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
            status, box = _detect_status_with_screen_shot(ctx, path)
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
                    ACTION("点击确认", ClickAction, [], 0.2),
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
                cls.runAction(ctx, ACTION("点击确认", ClickAction, []))

        return CommandReturnCode.SUCCESS

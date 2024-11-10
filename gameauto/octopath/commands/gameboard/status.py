from ...ctx import OctopathTaskCtx
from ...constants import IconName, RGBRelPoint, rgbPointFrom720P
from ....base import Point, Box, RGB
from PIL import Image
from typing import NamedTuple, Optional
from ...status import OctopathStatus
from PIL import Image
from ....base import BaseGUI


class GameboardStatus(NamedTuple):
    status: int
    box: Optional[Box]
    boost: int


def getRgbFromImage(image: Image.Image, pos: Point) -> RGB:
    rgb = image.getpixel(xy=pos)
    return RGB(rgb[0], rgb[1], rgb[2])


def compareRgb(rgbPoint: RGBRelPoint, ctx: OctopathTaskCtx, image: Image.Image, threshold: int) -> bool:
    point: Point = ctx.get_absolute_pos_from_rel_radio(rgbPoint.relPoint)
    rgb: RGB = getRgbFromImage(image, point)
    return rgb.isSimilar(rgbPoint.rgb, threshold)


p1 = rgbPointFrom720P(RGB(255, 255, 116), Point(1114, 607))
p2 = rgbPointFrom720P(RGB(255, 255, 116), Point(1136, 607))
p3 = rgbPointFrom720P(RGB(255, 255, 116), Point(1158, 607))


def detectGameboardStatus(ctx: OctopathTaskCtx, screenshot: str) -> GameboardStatus:
    # 检测当前状态, 根据屏幕截图判断当前状态
    status = OctopathStatus.Unknown.value

    screenshotImage = Image.open(screenshot)
    screenshot = BaseGUI.PreProcess_Images(screenshot)
    box = None
    box = ctx.findImageInScreen(IconName.GAME_BOARD_PLAY, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_Start.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_CONFIRM, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_NEED, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_NONEED, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_IGNORE, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_QUESTION_LOVER, screenshot, confidence=0.95)
    if box is not None:
        status = OctopathStatus.Gameboard_CONFIRM.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_DICE, screenshot, confidence=0.93, region=ctx.dice_region)
    if box is not None:
        status = OctopathStatus.Gameboard_FREE.value | OctopathStatus.CanQuit.value
        boost = 0
        if compareRgb(p1, ctx, screenshotImage, 50):
            boost += 1
        if compareRgb(p2, ctx, screenshotImage, 50):
            boost += 1
        if compareRgb(p3, ctx, screenshotImage, 50):
            boost += 1
        return GameboardStatus(status, box, boost)

    box = ctx.findImageInScreen(IconName.TRAITS_IN_BATTLE, screenshot, confidence=0.9, region=ctx.battle_region)
    if box is not None:
        status = OctopathStatus.Combat.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.ATTACK, screenshot, confidence=0.9, region=ctx.attack_region)
    if box is not None:
        status = OctopathStatus.CanAttack.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_UP, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_RIGHT, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        box = Box(box.left + box.width / 2, box.top, box.width, box.height)
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_LEFT, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return GameboardStatus(status, box, 0)

    # box = ctx.findImageInScreen(IconName.GAME_BOARD_DICE2, screenshot, confidence=0.9, grayscale=True)
    # if box is not None:
    #     status = OctopathStatus.Gameboard_FREE.value | OctopathStatus.CanQuit.value
    #     return status, box

    box = ctx.findImageInScreen(IconName.GAME_BOARD_STORNGER, screenshot, confidence=0.9)
    if box is not None:
        ctx.logger.info("检测到强敌，选择强敌路线")
        status = OctopathStatus.Gameboard_ChooseStrongOrWeeker.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_UP, screenshot, confidence=0.9)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return GameboardStatus(status, box, 0)

    box = ctx.findImageInScreen(IconName.GAME_BOARD_CHOOSE_ROAD_POWER, screenshot, confidence=0.92)
    if box is not None:
        status = OctopathStatus.Gameboard_ChooseRoad.value
        return GameboardStatus(status, box, 0)

    return GameboardStatus(status, None, 0)

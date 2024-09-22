from enum import Enum
from ...base import Box, Point, RGB, RGBPoint
from .assets import DETACTABLE, rbFrom720P, ASSET


class ENEMY(DETACTABLE):
    pass


class EnemyName(Enum):
    FallenCait = "亡者凯特琳"


Enemies = {
    EnemyName.FallenCait: ENEMY(
        "亡者凯特琳",
        ASSET("fallen_cait.png", "enemy"),
        rbFrom720P(60, 300, 450, 250),
        None,
    )
}


def getEnemy(name: EnemyName) -> ENEMY:
    return Enemies[name]


def getIconPath(name: EnemyName) -> str:
    enemy = getEnemy(name)
    if enemy and enemy.icon_asset:
        return enemy.icon_asset.path
    return None

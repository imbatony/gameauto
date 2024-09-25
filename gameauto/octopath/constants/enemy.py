from enum import Enum
from .assets import rbFrom720P, ASSET, DETACTABLE, RELATIVE_POS


class ENEMY(DETACTABLE):
    __slots__ = ()

    def __new__(cls, name, icon_asset: ASSET, detectable_box: RELATIVE_POS = None):
        detectable_box = rbFrom720P(60, 300, 450, 250) if detectable_box is None else detectable_box
        return super().__new__(cls, name, icon_asset, detectable_box)


class EnemyName(Enum):
    FallenCait = "亡者凯特琳"


Enemies = {EnemyName.FallenCait: ENEMY("亡者凯特琳", ASSET("fallen_cait.png", "enemy"))}


def getEnemy(name: EnemyName) -> ENEMY:
    return Enemies[name]


def getIconPath(name: EnemyName) -> str:
    enemy = getEnemy(name)
    if enemy and enemy.icon_asset:
        return enemy.icon_asset.path
    return None

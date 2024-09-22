import collections
from .towns import getTownByName
from .assets import ASSET
from .icons import IconName

WILD = collections.namedtuple("WILD", ["town_name_near_by", "icon_name"])

wild_names: dict[str, WILD] = {
    "边狱-盖斯特峡谷": WILD("边狱-克拉古斯比亚", IconName.MAP_WILD_GORGE_HELL),
}


def getNearByTownByWild(wild: WILD) -> str:
    town = getTownByName(wild.town_name_near_by)
    return town


def getWildByName(name: str) -> WILD:
    if name in wild_names:
        return wild_names[name]
    return None
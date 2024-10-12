import collections
from .towns import getTownByName
from .icons import IconName

WILD = collections.namedtuple("WILD", ["town_name_near_by", "icon_name"])

wild_names: dict[str, WILD] = {
    "边狱-盖斯特峡谷": WILD("边狱-克拉古斯比亚", IconName.MAP_WILD_GORGE_HELL),
    "边狱-瓦洛雷后森": WILD("边狱-瓦洛雷", IconName.MAP_WILD_FOREST_HELL),
    "恐怖山谷": WILD("牧羊岩", IconName.MAP_WILD_GORGE),
    "静湖的地下遗址": WILD("库利亚布鲁克", IconName.MAP_WILD_RUINS),
    "原初洞穴": WILD("恩波格洛", IconName.MAP_WILD_CAVE),
}


def getNearByTownByWild(wild: WILD) -> str:
    town = getTownByName(wild.town_name_near_by)
    return town


def getWildByName(name: str) -> WILD:
    if name in wild_names:
        return wild_names[name]
    return None

import collections
from .towns import getTownByName
from .icons import IconName
from .assets import rpFrom720P

WILD = collections.namedtuple("WILD", ["town_name_near_by", "icon_name", "need_zoom", "addtional_option"])

wild_names: dict[str, WILD] = {
    "边狱-盖斯特峡谷": WILD("边狱-克拉古斯比亚", IconName.MAP_WILD_GORGE_HELL, False, None),
    "边狱-盖斯特峡谷2": WILD("边狱-克拉古斯比亚", IconName.MAP_WILD_GORGE_HELL, False, rpFrom720P(640, 280)),
    "边狱-艾德拉斯城": WILD("边狱-克拉古斯比亚", IconName.MAP_WILD_PALACE, False, None),
    "边狱-瓦洛雷后森": WILD("边狱-瓦洛雷", IconName.MAP_WILD_FOREST_HELL, False, None),
    "边狱-荷鲁布尔古城": WILD("边狱-荷鲁布尔古", IconName.MAP_WILD_PALACE, False, None),
    "悔恨之间": WILD("边狱-荷鲁布尔古", IconName.MAP_WILD_GATE_HELL, False, None),
    "恐怖山谷": WILD("牧羊岩", IconName.MAP_WILD_GORGE, False, None),
    "静湖的地下遗址": WILD("库利亚布鲁克", IconName.MAP_WILD_RUINS, False, None),
    "原初洞穴": WILD("恩波格洛", IconName.MAP_WILD_CAVE, False, None),
    "热腾的泉窟": WILD("贝尔肯", IconName.MAP_WILD_CAVE, False, None),
    "圣火神祠堂": WILD("圣域瓦洛雷", IconName.MAP_WILD_TEMPLE, True, rpFrom720P(640, 280)),
}


def getNearByTownByWild(wild: WILD) -> str:
    town = getTownByName(wild.town_name_near_by)
    return town


def getWildByName(name: str) -> WILD:
    if name in wild_names:
        return wild_names[name]
    return None

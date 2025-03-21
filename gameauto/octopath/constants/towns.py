import collections
from enum import Enum
from .icons import IconName


TOWN = collections.namedtuple("TOWN", ["name", "world", "directly", "keywords", "asset"])


class World(Enum):
    NORMAL = 0  # 现世
    HELL = 1  # 边狱
    HAVEN = 2  # 圣域


town_names: dict[str, TOWN] = {
    "瓦洛雷": TOWN("瓦洛雷", World.NORMAL, True, ["瓦洛雷"], None),
    "格兰波特": TOWN("格兰波特", World.NORMAL, True, ["格兰波特"], None),
    "牧羊岩": TOWN("牧羊岩", World.NORMAL, True, ["牧羊岩"], None),
    "无名小镇": TOWN("无名小镇", World.NORMAL, True, ["无名小镇"], None),
    "恩波格洛": TOWN("恩波格洛", World.NORMAL, True, ["恩波"], None),
    "贝尔肯": TOWN("贝尔肯", World.NORMAL, True, ["贝尔"], None),
    "克拉古斯比亚": TOWN("克拉古斯比亚", World.NORMAL, True, ["克拉古斯"], None),
    "库利亚布鲁克": TOWN("库利亚布鲁克", World.NORMAL, True, ["库利亚"], None),
    "边狱-克拉古斯比亚": TOWN("边狱-克拉古斯比亚", World.HELL, True, ["克拉古斯"], None),
    "边狱-瓦洛雷": TOWN("边狱-瓦洛雷", World.HELL, True, ["瓦洛雷"], None),
    "边狱-荷鲁布尔古": TOWN("边狱-荷鲁布尔古", World.HELL, True, ["贝尔"], None),
    "圣域瓦洛雷": TOWN("圣域瓦洛雷", World.HAVEN, True, ["瓦洛雷"], None),
}


def getWorldIconNameByTown(town: TOWN) -> IconName:
    if town.world == World.NORMAL:
        return IconName.WORLD_NORMAL
    elif town.world == World.HAVEN:
        return IconName.WORLD_HAVEN
    return IconName.WORLD_HELL


def getWorldNameByTown(town: TOWN) -> str:
    if town.world == World.NORMAL:
        return "现世"
    return "边狱"


def getTownByName(name: str) -> TOWN:
    if name in town_names:
        return town_names[name]
    return None

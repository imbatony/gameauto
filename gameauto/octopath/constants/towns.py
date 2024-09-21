import collections
from enum import Enum
from .assets import ASSET


TOWN = collections.namedtuple("TOWN", ["name", "world", "directly", "keyword", "asset"])


class World(Enum):
    NORMAL = 0  # 现世
    HELL = 1  # 边狱


town_names: dict[str, TOWN] = {
    "瓦洛雷": TOWN("瓦洛雷", World.NORMAL, True, "瓦洛雷", None),
    "格兰波特": TOWN("格兰波特", World.NORMAL, True, "格兰波特", None),
    "边狱-克拉古斯比亚": TOWN(
        "边狱-克拉古斯比亚", World.HELL, True, "克拉古斯比亚", None
    ),
}


def get_town_by_name(name: str) -> TOWN:

    if name in town_names:
        return town_names[name]
    return None

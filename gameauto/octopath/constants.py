import collections
from enum import Enum


TOWN = collections.namedtuple("TOWN", ["name", "world", "directly", "keyword", "icon"])


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


ItemRelativePostion = collections.namedtuple(
    "ItemRelativePostion", ["name", "x_order", "y_ratio"]
)

default_menu_item_radio = 29 / 32

item_relative_postions: dict[str, ItemRelativePostion] = {
    "菜单": ItemRelativePostion("菜单", 0, default_menu_item_radio),
    "队伍": ItemRelativePostion("队伍", 1, default_menu_item_radio),
    "探索": ItemRelativePostion("探索", 2, default_menu_item_radio),
    "试炼之塔": ItemRelativePostion("试炼之塔", 3, default_menu_item_radio),
    "游戏盘": ItemRelativePostion("游戏盘", 4, default_menu_item_radio),
    "追忆之书": ItemRelativePostion("追忆之书", 5, default_menu_item_radio),
    "大陆地图": ItemRelativePostion("大陆地图", 6, default_menu_item_radio),
    "商店": ItemRelativePostion("商店", 7, default_menu_item_radio),
    "指引": ItemRelativePostion("指引", 8, default_menu_item_radio),
    "精灵": ItemRelativePostion("精灵", 9, default_menu_item_radio),
}


def get_item_relative_postion_by_name(name: str) -> ItemRelativePostion:

    if name in item_relative_postions:
        return item_relative_postions[name]
    return None

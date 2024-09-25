from enum import Enum
from .assets import ASSET, RELATIVE_POS, ICON, rpFrom720P, getAssetPath


class IconName(Enum):
    ZOOM_OUT_MAP = "地图缩小"
    MENU = "菜单"
    TEAM = "队伍"
    EXPLORE = "探索"
    TOWER = "试炼之塔"
    GAME_BOARD = "游戏盘"
    MEMORY_BOOK = "追忆之书"
    MAP = "大陆地图"
    SHOP = "商店"
    GUIDE = "指引"
    ELF = "精灵"

    BACK = "返回"
    EXIT = "退出"

    MAPICON_SELECTED_BTN_GOTO = "前往这里"  # 用于确认地图点击
    MAPICON_SELECTED_BTN_GET_ITEM = "道具回收"  # 用于点击确认回收道具
    MAPICON_SELECTED_BTN_GOTO_2 = "前往这里"  # 用于确认地图点击, 只适用于无名小镇

    DIALOG_YES = "对话-是"
    DIALOG_NO = "对话-否"
    DIALOG_CONFIRM = "对话-确定"

    DIALOG_GET_ITEM_YES = "对话-道具回收-是"
    DIALOG_GET_ITEM_NO = "对话-道具回收-否"
    DIALOG_GET_ITEM_CONFIRM = "对话-道具回收-确定"

    MINI_MAP = "小地图"

    WORLD_NORMAL = "现世"
    WORLD_HELL = "边狱"

    HOTEL_MINI_MAP = "旅馆-小地图"
    BED = "床"
    HOTEL = "旅馆"

    MAP_WILD_GORGE = "野外-峡谷"
    MAP_WILD_PALACE = "野外-宫殿"
    MAP_WILD_CAVE = "野外-洞窟"
    MAP_WILD_FOREST = "野外-森林"
    MAP_WILD_SITE = "野外-遗迹"
    MAP_WILD_RUINS = "野外-废墟"

    MAP_WILD_GORGE_HELL = "野外-峡谷-边狱"

    # traits
    TRAITS_IN_BATTLE = "特征-战斗"


TOP_BUTTON_Y_RATIO = 20 / 720
MENU_BUTTON_Y_RATIO = 625 / 720


def get_x_ratio(total, index) -> float:
    return (index + 0.5) / total


icons: dict[IconName, ICON] = {
    IconName.ZOOM_OUT_MAP: ICON(ASSET("zoom_out.png", "icon"), RELATIVE_POS(1206 / 1280, 647 / 720)),
    IconName.MENU: ICON(None, RELATIVE_POS(get_x_ratio(10, 0), MENU_BUTTON_Y_RATIO)),
    IconName.TEAM: ICON(None, RELATIVE_POS(get_x_ratio(10, 1), MENU_BUTTON_Y_RATIO)),
    IconName.EXPLORE: ICON(None, RELATIVE_POS(get_x_ratio(10, 2), MENU_BUTTON_Y_RATIO)),
    IconName.TOWER: ICON(None, RELATIVE_POS(get_x_ratio(10, 3), MENU_BUTTON_Y_RATIO)),
    IconName.GAME_BOARD: ICON(None, RELATIVE_POS(get_x_ratio(10, 4), MENU_BUTTON_Y_RATIO)),
    IconName.MEMORY_BOOK: ICON(None, RELATIVE_POS(get_x_ratio(10, 5), MENU_BUTTON_Y_RATIO)),
    IconName.MAP: ICON(None, RELATIVE_POS(get_x_ratio(10, 6), MENU_BUTTON_Y_RATIO)),
    IconName.SHOP: ICON(None, RELATIVE_POS(get_x_ratio(10, 7), MENU_BUTTON_Y_RATIO)),
    IconName.GUIDE: ICON(None, RELATIVE_POS(get_x_ratio(10, 8), MENU_BUTTON_Y_RATIO)),
    IconName.ELF: ICON(None, RELATIVE_POS(get_x_ratio(10, 9), MENU_BUTTON_Y_RATIO)),
    IconName.BACK: ICON(None, RELATIVE_POS(50 / 1280, TOP_BUTTON_Y_RATIO)),
    IconName.EXIT: ICON(None, RELATIVE_POS(1230 / 1280, TOP_BUTTON_Y_RATIO)),
    IconName.MAPICON_SELECTED_BTN_GOTO: ICON(None, rpFrom720P(1040, 630)),
    IconName.MAPICON_SELECTED_BTN_GET_ITEM: ICON(None, rpFrom720P(950, 630)),
    IconName.MAPICON_SELECTED_BTN_GOTO_2: ICON(None, rpFrom720P(1150, 630)),
    IconName.DIALOG_NO: ICON(None, rpFrom720P(480, 480)),
    IconName.DIALOG_YES: ICON(None, rpFrom720P(800, 480)),
    IconName.DIALOG_CONFIRM: ICON(None, rpFrom720P(640, 480)),
    IconName.DIALOG_GET_ITEM_YES: ICON(None, rpFrom720P(800, 600)),
    IconName.DIALOG_GET_ITEM_NO: ICON(None, rpFrom720P(480, 600)),
    IconName.DIALOG_GET_ITEM_CONFIRM: ICON(None, rpFrom720P(640, 530)),
    IconName.MINI_MAP: ICON(None, rpFrom720P(1000, 100)),
    IconName.WORLD_NORMAL: ICON(None, rpFrom720P(180, 160)),
    IconName.WORLD_HELL: ICON(None, rpFrom720P(180, 260)),
    IconName.HOTEL_MINI_MAP: ICON(ASSET("hotel_mini_map.png", "icon"), None),
    IconName.BED: ICON(ASSET("bed.png", "icon"), None),
    IconName.HOTEL: ICON(ASSET("hotel.png", "icon"), None),
    # map
    IconName.MAP_WILD_GORGE: ICON(ASSET("wild_gorge.png", "map"), None),
    IconName.MAP_WILD_PALACE: ICON(ASSET("wild_palace.png", "map"), None),
    IconName.MAP_WILD_CAVE: ICON(ASSET("wild_cave.png", "map"), None),
    IconName.MAP_WILD_FOREST: ICON(ASSET("wild_forest.png", "map"), None),
    IconName.MAP_WILD_SITE: ICON(ASSET("wild_site.png", "map"), None),
    IconName.MAP_WILD_RUINS: ICON(ASSET("wild_ruins.png", "map"), None),
    IconName.MAP_WILD_GORGE_HELL: ICON(ASSET("wild_gorge_hell.png", "map"), None),
    # traits
    IconName.TRAITS_IN_BATTLE: ICON(ASSET("battle.png", "traits"), None),
}


def getIconByIconName(name: IconName) -> ICON:
    if name in icons:
        return icons[name]
    return None


def getIconNameByName(name: str) -> IconName:
    for k, v in icons.items():
        if v.name == name:
            return k
    return None


def getIconPathByIconName(name: IconName) -> str:
    icon = getIconByIconName(name)
    return getAssetPath(icon.asset)

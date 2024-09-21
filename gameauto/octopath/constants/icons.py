from enum import Enum
from .assets import ASSET, RELATIVE_POS, ICON


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

    CONFORM_GOTO = "前往这里"  # 用于确认地图点击

    DIALOG_YES = "对话-是"
    DIALOG_NO = "对话-否"
    DIALOG_CONFIRM = "对话-确定"

    MINI_MAP = "小地图"

    WORLD_NORMAL = "现世"
    WORLD_HELL = "边狱"

    HOTEL_IN_MINI_MAP = "旅馆"
    BED = "床"

    MAP_WILD_GORGE = "野外-峡谷"
    MAP_WILD_PALACE = "野外-宫殿"
    MAP_WILD_CAVE = "野外-洞窟"
    MAP_WILD_FOREST = "野外-森林"
    MAP_WILD_SITE = "野外-遗迹"
    MAP_WILD_RUINS = "野外-废墟"

    MAP_WILD_GORGE_HELL = "野外-峡谷-边狱"


TOP_BUTTON_Y_RATIO = 20 / 720
MENU_BUTTON_Y_RATIO = 625 / 720


def get_x_ratio(total, index) -> float:
    return (index + 0.5) / total


icons: dict[IconName, ICON] = {
    IconName.ZOOM_OUT_MAP: ICON(
        ASSET("zoom_out.png", "icon"), RELATIVE_POS(1206 / 1280, 647 / 720)
    ),
    IconName.MENU: ICON(None, RELATIVE_POS(get_x_ratio(10, 0), MENU_BUTTON_Y_RATIO)),
    IconName.TEAM: ICON(None, RELATIVE_POS(get_x_ratio(10, 1), MENU_BUTTON_Y_RATIO)),
    IconName.EXPLORE: ICON(None, RELATIVE_POS(get_x_ratio(10, 2), MENU_BUTTON_Y_RATIO)),
    IconName.TOWER: ICON(None, RELATIVE_POS(get_x_ratio(10, 3), MENU_BUTTON_Y_RATIO)),
    IconName.GAME_BOARD: ICON(
        None, RELATIVE_POS(get_x_ratio(10, 4), MENU_BUTTON_Y_RATIO)
    ),
    IconName.MEMORY_BOOK: ICON(
        None, RELATIVE_POS(get_x_ratio(10, 5), MENU_BUTTON_Y_RATIO)
    ),
    IconName.MAP: ICON(None, RELATIVE_POS(get_x_ratio(10, 6), MENU_BUTTON_Y_RATIO)),
    IconName.SHOP: ICON(None, RELATIVE_POS(get_x_ratio(10, 7), MENU_BUTTON_Y_RATIO)),
    IconName.GUIDE: ICON(None, RELATIVE_POS(get_x_ratio(10, 8), MENU_BUTTON_Y_RATIO)),
    IconName.ELF: ICON(None, RELATIVE_POS(get_x_ratio(10, 9), MENU_BUTTON_Y_RATIO)),
    IconName.BACK: ICON(None, RELATIVE_POS(50 / 1280, TOP_BUTTON_Y_RATIO)),
    IconName.EXIT: ICON(None, RELATIVE_POS(1230 / 1280, TOP_BUTTON_Y_RATIO)),
    IconName.CONFORM_GOTO: ICON(None, RELATIVE_POS(1040 / 1280, 630 / 720)),
    IconName.DIALOG_NO: ICON(None, RELATIVE_POS(480 / 1280, 480 / 720)),
    IconName.DIALOG_YES: ICON(None, RELATIVE_POS(800 / 1280, 480 / 720)),
    IconName.DIALOG_CONFIRM: ICON(None, RELATIVE_POS(640 / 1280, 480 / 720)),
    IconName.MINI_MAP: ICON(None, RELATIVE_POS(1000 / 1280, 100 / 720)),
    IconName.WORLD_NORMAL: ICON(None, RELATIVE_POS(90 / 1280, 160 / 720)),
    IconName.WORLD_HELL: ICON(None, RELATIVE_POS(90 / 1280, 260 / 720)),
    IconName.HOTEL_IN_MINI_MAP: ICON(ASSET("hotel_in_mini_map.png", "icon"), None),
    IconName.BED: ICON(ASSET("bed.png", "icon"), None),
    IconName.MAP_WILD_GORGE: ICON(ASSET("wild_gorge.png", "map"), None),
    IconName.MAP_WILD_PALACE: ICON(ASSET("wild_palace.png", "map"), None),
    IconName.MAP_WILD_CAVE: ICON(ASSET("wild_cave.png", "map"), None),
    IconName.MAP_WILD_FOREST: ICON(ASSET("wild_forest.png", "map"), None),
    IconName.MAP_WILD_SITE: ICON(ASSET("wild_site.png", "map"), None),
    IconName.MAP_WILD_RUINS: ICON(ASSET("wild_ruins.png", "map"), None),
    IconName.MAP_WILD_GORGE_HELL: ICON(ASSET("wild_gorge_hell.png", "map"), None),
}


def getIconByIconName(name: IconName) -> ICON:
    if name in icons:
        return icons[name]
    return None

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
    ATTACK = "攻击"
    EXCHANGE = "交换"
    YES = "是"

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
    MAP_WILD_FOREST_HELL = "野外-森林-边狱"

    # traits
    TRAITS_IN_BATTLE = "特征-战斗"
    TRAITS_ENEMY = "特征-敌人"

    # fighter
    FIGHTER_ICON_1 = "战斗者图标1"
    FIGHTER_ICON_2 = "战斗者图标2"
    FIGHTER_ICON_3 = "战斗者图标3"
    FIGHTER_ICON_4 = "战斗者图标4"
    # skills
    SKILL_ICON_0 = "技能图标0"
    SKILL_ICON_1 = "技能图标1"
    SKILL_ICON_2 = "技能图标2"
    SKILL_ICON_3 = "技能图标3"
    SKILL_ICON_4 = "技能图标4"
    SKILL_ICON_5 = "技能图标5"
    SKILL_ENABLE = "发动大招"

    # memery book
    MEMORY_BOOK_ICON_1 = "大陆的记录"
    MEMORY_BOOK_ICON_2 = "旅行者的记忆"
    MEMORY_BOOK_ICON_3 = "故事的写记"

    # left tabs
    LEFT_TAB_1 = "左侧标签1"
    LEFT_TAB_2 = "左侧标签2"
    LEFT_TAB_3 = "左侧标签3"
    LEFT_TAB_4 = "左侧标签4"
    LEFT_TAB_5 = "左侧标签5"
    LEFT_TAB_6 = "左侧标签6"

    # filter
    FILTER = "筛选"
    FILTER_CONFIRM = "筛选确认"

    # 竞技场
    ARENA_EXIT_CONFIRM = "竞技场-退出-确认"
    ARENA_EXIT_CLOSE = "竞技场-退出-关闭"
    ARENA_EXIT_RETURN = "竞技场-退出-返回"

    # 游戏盘
    GAME_BOARD_PLAY = "游戏盘-开始"
    GAME_BOARD_DICE = "游戏盘-骰子"
    GAME_BOARD_DICE2 = "游戏盘-骰子"
    GAME_BOARD_CONFIRM = "游戏盘-确认"
    GAME_BOARD_FINISH = "游戏盘-关闭"
    GAME_BOARD_QUESTION_NEED = "游戏盘-问题-需要"
    GAME_BOARD_QUESTION_NONEED = "游戏盘-问题-不需要"
    GAME_BOARD_QUESTION_IGNORE = "游戏盘-问题-忽略"
    GAME_BOARD_QUESTION_LOVER = "游戏盘-问题-情人"
    GAME_BOARD_UP = "游戏盘-向上岔路"
    GAME_BOARD_LEFT = "游戏盘-向左岔路"
    GAME_BOARD_RIGHT = "游戏盘-向右岔路"
    GAME_BOARD_STORNGER = "游戏盘-敌人强化"
    GAME_BOARD_WEEKER = "游戏盘-敌人弱化"
    GAME_BOARD_OPTION = "游戏盘-选项"
    GAME_BOARD_END = "游戏盘-结束"
    GAME_BOARD_CHOOSE_ROAD_POWER = "游戏盘-选择路-霸者"

    # 战斗
    BATTLE_ALL_MAX = "战斗-全体最大"
    BATTLE_FORCE_END = "战斗-强制结束"
    BATTLE_DELEGATE = "战斗-委托"


TOP_BUTTON_Y_RATIO = 20 / 720
MENU_BUTTON_Y_RATIO = 625 / 720


def get_x_ratio(total, index) -> float:
    return (index + 0.5) / total


fighter_icons: list[IconName] = [IconName.FIGHTER_ICON_1, IconName.FIGHTER_ICON_2, IconName.FIGHTER_ICON_3, IconName.FIGHTER_ICON_4]

skill_icons: list[IconName] = [
    IconName.SKILL_ICON_0,  # 大招
    IconName.SKILL_ICON_1,  # 攻击
    IconName.SKILL_ICON_2,  # 技能1
    IconName.SKILL_ICON_3,  # 技能2
    IconName.SKILL_ICON_4,  # 技能3
    IconName.SKILL_ICON_5,  # 技能4
]

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
    IconName.YES: ICON(ASSET("yes.png", "icon"), None),
    IconName.ATTACK: ICON(ASSET("attack.png", "icon"), rpFrom720P(1100, 640)),
    IconName.EXCHANGE: ICON(ASSET("exchange.png", "icon"), rpFrom720P(1105, 640)),
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
    IconName.MAP_WILD_FOREST_HELL: ICON(ASSET("wild_forest_hell.png", "map"), None),
    # traits
    IconName.TRAITS_IN_BATTLE: ICON(ASSET("battle.png", "traits"), None),
    IconName.TRAITS_ENEMY: ICON(ASSET("enemy.png", "traits"), None),
    # person
    IconName.FIGHTER_ICON_1: ICON(None, rpFrom720P(1100, 90)),
    IconName.FIGHTER_ICON_2: ICON(None, rpFrom720P(1100, 230)),
    IconName.FIGHTER_ICON_3: ICON(None, rpFrom720P(1100, 370)),
    IconName.FIGHTER_ICON_4: ICON(None, rpFrom720P(1100, 510)),
    # skills
    IconName.SKILL_ICON_0: ICON(None, rpFrom720P(700, 100)),
    IconName.SKILL_ICON_1: ICON(None, rpFrom720P(841, 200)),
    IconName.SKILL_ICON_2: ICON(None, rpFrom720P(841, 300)),
    IconName.SKILL_ICON_3: ICON(None, rpFrom720P(841, 400)),
    IconName.SKILL_ICON_4: ICON(None, rpFrom720P(841, 500)),
    IconName.SKILL_ICON_5: ICON(None, rpFrom720P(841, 600)),
    IconName.SKILL_ENABLE: ICON(None, rpFrom720P(841, 460)),
    # memory book
    IconName.MEMORY_BOOK_ICON_1: ICON(None, rpFrom720P(230, 600)),
    IconName.MEMORY_BOOK_ICON_2: ICON(None, rpFrom720P(635, 600)),
    IconName.MEMORY_BOOK_ICON_3: ICON(None, rpFrom720P(1050, 600)),
    # left tabs
    IconName.LEFT_TAB_1: ICON(None, rpFrom720P(90, 165)),
    IconName.LEFT_TAB_2: ICON(None, rpFrom720P(90, 165 + 88)),
    IconName.LEFT_TAB_3: ICON(None, rpFrom720P(90, 165 + 88 * 2)),
    IconName.LEFT_TAB_4: ICON(None, rpFrom720P(90, 165 + 88 * 3)),
    IconName.LEFT_TAB_5: ICON(None, rpFrom720P(90, 165 + 88 * 4)),
    IconName.LEFT_TAB_6: ICON(None, rpFrom720P(90, 165 + 88 * 5)),
    # filter
    IconName.FILTER: ICON(None, rpFrom720P(972, 85)),
    IconName.FILTER_CONFIRM: ICON(None, rpFrom720P(800, 645)),
    # 竞技场
    IconName.ARENA_EXIT_CONFIRM: ICON(ASSET("arena_exit_confirm.png", "icon"), None),
    IconName.ARENA_EXIT_CLOSE: ICON(ASSET("arena_exit_close.png", "icon"), None),
    IconName.ARENA_EXIT_RETURN: ICON(None, rpFrom720P(586, 638)),
    # 游戏盘
    IconName.GAME_BOARD_PLAY: ICON(ASSET("play.png", "icon"), None),
    IconName.GAME_BOARD_DICE: ICON(ASSET("dice.png", "icon"), None),
    IconName.GAME_BOARD_DICE2: ICON(ASSET("dice2.png", "icon"), None),
    IconName.GAME_BOARD_CONFIRM: ICON(ASSET("confirm.png", "icon"), None),
    IconName.GAME_BOARD_QUESTION_IGNORE: ICON(ASSET("question_ignore.png", "icon"), None),
    IconName.GAME_BOARD_QUESTION_LOVER: ICON(ASSET("question_lover.png", "icon"), None),
    IconName.GAME_BOARD_FINISH: ICON(ASSET("game_board_finish.png", "icon"), None),
    IconName.GAME_BOARD_UP: ICON(ASSET("game_board_up.png", "icon"), None),
    IconName.GAME_BOARD_LEFT: ICON(ASSET("game_board_left.png", "icon"), None),
    IconName.GAME_BOARD_RIGHT: ICON(ASSET("game_board_right.png", "icon"), None),
    IconName.GAME_BOARD_STORNGER: ICON(ASSET("game_board_stronger.png", "icon"), None),
    IconName.GAME_BOARD_OPTION: ICON(ASSET("game_board_option.png", "icon"), None),
    IconName.GAME_BOARD_END: ICON(ASSET("game_board_end.png", "icon"), None),
    IconName.GAME_BOARD_QUESTION_NEED: ICON(ASSET("question_need.png", "icon"), None),
    IconName.GAME_BOARD_QUESTION_NONEED: ICON(ASSET("question_no_need.png", "icon"), None),
    IconName.GAME_BOARD_CHOOSE_ROAD_POWER: ICON(ASSET("choose_road_power.png", "icon"), None),
    # battle
    IconName.BATTLE_ALL_MAX: ICON(None, rpFrom720P(862, 642)),
    IconName.BATTLE_FORCE_END: ICON(None, rpFrom720P(584, 644)),
    IconName.BATTLE_DELEGATE: ICON(None, rpFrom720P(480, 644)),
}


def getIconByIconName(name: IconName) -> ICON:
    if name in icons:
        return icons[name]
    return None


def getIconNameByName(name: str) -> IconName:
    for k, v in icons.items():
        if k.value == name:
            return k
    return None


def getIconPathByIconName(name: IconName) -> str:
    icon = getIconByIconName(name)
    return getAssetPath(icon.asset)


def getFighterIconNameByNumber(num: int) -> ICON:
    index = (num - 1) // 2
    return fighter_icons[index]


def getSkillIconByNumber(num: int) -> ICON:
    index = num
    iconName = skill_icons[index]
    return getIconByIconName(iconName)


def getTeammateIconNameByNumber(num: int) -> IconName:
    index = -num - 1
    iconName = fighter_icons[index]
    return iconName

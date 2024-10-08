from enum import Enum


class OctopathStatus(Enum):
    Unknown = 0  # 未知状态
    Free = 1 << 0  # 自由状态,可以进行任意操作
    Combat = 1 << 1  # 战斗中
    Dialog = 1 << 2  # 对话中，可以选择对话选项
    Menu = 1 << 3  # 主菜单中
    Other = 1 << 4  # 其他菜单中
    Gameboard = 1 << 5  # 游戏棋盘中
    Conclusion = 1 << 6  # 结算中，可以点击退出
    Conclusion2 = 1 << 7  # 结算中,需要长按退出
    CanAttack = 1 << 8  # 可以攻击
    Finish = 1 << 9  # 结束状态
    ChooseRoad = 1 << 10  # 选择道路
    ChooseWeekerOrStronger = 1 << 11  # 选择强弱
    Start = 1 << 12  # 开始
    CanQuit = 1 << 13  # 可以退出
    Gameboard_Start = Gameboard | Start  # 游戏棋盘开始
    Gameboard_FREE = Gameboard | Free  # 游戏棋盘中，可以投掷骰子
    Gameboard_CONFIRM = Gameboard | Dialog  # 游戏棋盘中，需要确认
    Gameboard_FINISH = Gameboard | Finish  # 游戏棋盘中，其他菜单
    Gameboard_ChooseRoad = Gameboard | ChooseRoad  # 游戏棋盘中，需要选择道路
    Gameboard_Combat = Gameboard | Combat  # 游戏棋盘中，战斗中
    Gameboard_ChooseStrongOrWeeker = Gameboard | ChooseWeekerOrStronger  # 游戏棋盘中，需要选择强弱
    Gameboard_CanQuit = Gameboard | CanQuit  # 游戏棋盘中，可以退出

    def is_free(int) -> bool:
        return int & OctopathStatus.Free.value == OctopathStatus.Free.value

    def is_combat(int) -> bool:
        return int & OctopathStatus.Combat.value == OctopathStatus.Combat.value

    def is_dialog(int) -> bool:
        return int & OctopathStatus.Dialog.value == OctopathStatus.Dialog.value

    def is_menu(int) -> bool:
        return int & OctopathStatus.Menu.value == OctopathStatus.Menu.value

    def is_other(int) -> bool:
        return int & OctopathStatus.Other.value == OctopathStatus.Other.value

    def is_gameboard(int) -> bool:
        return int & OctopathStatus.Gameboard.value == OctopathStatus.Gameboard.value

    def is_conclusion(int) -> bool:
        return int & OctopathStatus.Conclusion.value == OctopathStatus.Conclusion.value

    def is_conclusion2(int) -> bool:
        return int & OctopathStatus.Conclusion2.value == OctopathStatus.Conclusion2.value

    def is_unknown(int) -> bool:
        return int == OctopathStatus.Unknown.value

    def is_can_attack(int) -> bool:
        return int & OctopathStatus.CanAttack.value == OctopathStatus.CanAttack.value

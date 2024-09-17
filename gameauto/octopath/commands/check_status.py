import os
from .base import BaseOctCommand
from enum import Enum
import cv2


class OctopathStatus(Enum):
    Free = 1 << 0  # 自由状态,可以进行任意操作
    Combat = 1 << 1  # 战斗中
    Dialog = 1 << 2  # 对话中，可以选择对话选项
    Menu = 1 << 3  # 主菜单中
    Other = 1 << 4  # 其他菜单中
    Unknown = 1 << 10  # 未知状态

    def is_free(int) -> bool:
        return int & OctopathStatus.Free.value == OctopathStatus.Free.value

    def is_combat(int) -> bool:
        return int & OctopathStatus.Combat.value == OctopathStatus.Combat.value

    def is_dialog(int) -> bool:
        return int & OctopathStatus.Dialog.value == OctopathStatus.Dialog.value

    def is_menu(int) -> bool:
        return int & OctopathStatus.Menu.value == OctopathStatus.Menu.value

    def is_unknown(int) -> bool:
        return int & OctopathStatus.Unknown.value == OctopathStatus.Unknown.value


class StrPosition:
    def __init__(self, str, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.str = str

    def get_center(self, offset_x=0, offset_y=0):
        return (self.x1 + self.x2) // 2 + offset_x, (self.y1 + self.y2) // 2 + offset_y

    def __str__(self):
        return f"StrPosition<str={self.str}, x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2}>"


class OctopathCheckStatusRet(object):
    def __init__(self, status: int, positions: list[StrPosition]):
        self.status = status
        self.positions = positions

    def __str__(self):
        positions_str = "\n\t".join([str(pos) for pos in self.positions])
        return f"OctopathCheckStatusRet<status={self.status}, positions=\n\t{positions_str}>"


class OctopathCheckStatusCommand(BaseOctCommand):
    def __init__(self, config, image_path):
        super().__init__(config=config, image_path=image_path)
        self.image_path = image_path

    def run_impl(self) -> OctopathCheckStatusRet:
        # if the image is None or not found, get the screenshot
        if not os.path.exists(self.image_path):
            self.image_path = self.app_screenshot(self.image_path)
        # check the status of the game

        self.logger.debug(f"检查游戏状态: {self.image_path}")
        # 识别图片中的文字
        # result = self.recognize_text(self.image_path)
        # self.logger.debug(f": {result}")
        # positions = []
        # for line in result["data"]:
        #     positions.append(
        #         StrPosition(
        #             line["text"],
        #             line["text_box_position"][0][0], # 左上角坐标
        #             line["text_box_position"][0][1],
        #             line["text_box_position"][1][0], # 右下角坐标
        #             line["text_box_position"][1][1],
        #         )
        #     )

        result = self.ocr(self.image_path)
        positions = []
        for line in result:
            for ele in line:
                txt = ele[1][0]
                confidence = ele[1][1]
                left_top = ele[0][0]
                right_bottom = ele[0][1]
                positions.append(
                    StrPosition(
                        txt, left_top[0], left_top[1], right_bottom[0], right_bottom[1]
                    )
                )

        # check the status by the text
        # the status is 0 by default
        status = 0

        # check the status by the text
        for pos in positions:
            if "菜单" in pos.str:
                status |= OctopathStatus.Menu.value | OctopathStatus.Free.value
                break
            if "其他" in pos.str:
                status |= OctopathStatus.Other.value | OctopathStatus.Free.value
                break
            if "回合" in pos.str:
                status |= OctopathStatus.Combat.value
                if "攻击" in pos.str:
                    status |= OctopathStatus.Free.value

        return OctopathCheckStatusRet(status, positions)

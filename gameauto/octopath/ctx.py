import time
import uuid
from ..base import BaseTaskCtx
from ..gameconstants import DEFAULT_ACTION_DELAY
from .constants import TOWN, WILD, getIconPathByIconName, IconName
from PIL import Image
from typing import Optional, Union
from ..base.tuples import Point, TxtBox, Box
from .status import OctopathStatus
import os
from pathlib import Path


class OctopathTaskCtx(BaseTaskCtx):
    def __init__(self, config: dict):
        super().__init__(config)
        self.action_default_interval = int(config.get("game", {}).get("action_interval", DEFAULT_ACTION_DELAY)) / 1000.0

        self.battle_count_after_sleep = 0
        self.total_battle_count = 0
        self.cur_town: TOWN = None
        self.cur_wild: WILD = None
        self.battle_exchange = [False, False, False, False]
        self.enemy_positions = []
        self.enemy_total = 0

    def getCurTime(self):
        return time.time()

    def findImageInScreen(self, image: Union[str, Image.Image, Path, IconName], screenshot: Union[str, Image.Image, Path] = None, **kargs) -> Box | None:

        if image is None:
            self.logger.debug(f"查找图片失败: 图片为空")
            return None

        if screenshot is None:
            screenshot = self.renew_current_screen()

        if isinstance(image, IconName):
            image = getIconPathByIconName(image)
        try:
            self.logger.debug(f"查找图片: {image} in {screenshot}")
            return self.gui.locate(image, screenshot, **kargs)
        except Exception:
            self.logger.exception(f"查找图片失败")
            return None

    def locateCenterOnScreen(
        self,
        needleImage: Union[str, Image.Image, Path],
        region: Box,
        screen_image: Union[str, Image.Image, Path] = None,
        center: bool = False,
        confidence=None,
        grayscale: bool | None = None,
    ) -> Optional[Box]:
        """
        识别图片位置
        """
        self.logger.debug("识别图片位置")

        if screen_image is None:
            screen_image = self.renew_current_screen()

        if isinstance(screen_image, Path):
            screen_image = str(screen_image)

        try:
            box = None
            if not center:
                box = self.gui.locate(needleImage, screen_image, region=region, confidence=confidence, grayscale=grayscale)
            else:
                # 找到所有位置
                pos_generator = self.gui.locateAll(needleImage, screen_image, region=region, confidence=confidence, grayscale=grayscale)
                # 选择最靠近中心的位置
                center_pos = Point(region[0] + region[2] / 2, region[1] + region[3] / 2)
                min_distance = 999999
                for p in pos_generator:
                    # 计算距离
                    distance = (p[0] - center_pos.x) ** 2 + (p[1] - center_pos.y) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        box = p
            if box is None:
                self.logger.debug("找不到图片")
                return None
            else:
                self.logger.debug(f"找到图片位置: {box}")
                return box
        except Exception:
            self.logger.exception("识别图片位置异常")
            return None

    def detect_status(self, ocr_result: list[TxtBox] = None) -> int:
        # 检测当前状态, 根据OCR结果判断当前状态
        # TODO: 优化状态检测逻辑, 由于OCR识别结果不稳定, 而且耗时较长, 可以考虑使用其他方式检测状态，比如关键像素点颜色检测，或者使用opencv模板匹配等
        if ocr_result is None:
            screen_shot = self.cur_screenshot
            if screen_shot is None:
                screen_shot = self.renew_current_screen()
            return self._detect_status_with_screen_shot(screen_shot)

        return self._detect_status_with_ocr(ocr_result)

    def _detect_status_with_ocr(self, ocr_result: list[TxtBox]) -> int:
        status = OctopathStatus.Unknown.value
        for pos in ocr_result:
            if "菜单" in pos.text or "商店" in pos.text or "地图" in pos.text:
                self.logger.debug(f"主菜单: {pos.text}")
                status |= OctopathStatus.Menu.value | OctopathStatus.Free.value
            if "其他" in pos.text or "道具" in pos.text or "通知" in pos.text:
                self.logger.debug(f"其他菜单: {pos.text}")
                status |= OctopathStatus.Other.value | OctopathStatus.Free.value
            if "回合" in pos.text or "战斗" in pos.text:
                self.logger.debug(f"战斗中: {pos.text}")
                status |= OctopathStatus.Combat.value
            if "结算" in pos.text:
                self.logger.debug(f"结算: {pos.text}")
                status |= OctopathStatus.Conclusion.value | OctopathStatus.Free.value | OctopathStatus.Combat.value

        for pos in ocr_result:
            if "攻击" in pos.text and OctopathStatus.is_combat(status):
                self.logger.debug(f"战斗待命: {pos.text}")
                status |= OctopathStatus.Free.value

        return status

    @property
    def battle_region(self) -> Box:
        return Box(100, 0, 100 // 2, 40)

    @property
    def attack_region(self) -> Box:
        return Box(1000, 620, 150, 50)

    @property
    def dice_region(self) -> Box:
        return Box(1000, 520, 300, 130)

    def _detect_status_with_screen_shot(self, screenshot: Union[str, Image.Image, Path]) -> int:
        # 检测当前状态, 根据屏幕截图判断当前状态
        status = OctopathStatus.Unknown.value

        if self.findImageInScreen(IconName.TRAITS_IN_BATTLE, screenshot, confidence=0.9, grayscale=True, region=self.battle_region) is not None:
            status |= OctopathStatus.Combat.value

        if self.findImageInScreen(IconName.ATTACK, screenshot, confidence=0.9, grayscale=True, region=self.attack_region) is not None:
            status |= OctopathStatus.CanAttack.value

        return status

    def ocr(self, image: Union[str, Path, Image.Image]) -> list[TxtBox]:
        list = self.gui.ocr(image)
        list_with_offset = []
        for idx in range(len(list)):
            line = list[idx]
            # 需要增加实际的应用的偏移量
            line_with_offset = TxtBox(
                text=line.text,
                left=line.left + self.left,
                top=line.top + self.top,
                width=line.width,
                height=line.height,
            )
            list_with_offset.append(line_with_offset)
        return list_with_offset

    def renew_current_screen(self) -> str:
        dir = os.path.join(os.environ.get("TEMP"), "octopath")
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name = uuid.uuid1().__str__() + ".png"
        path = os.path.join(os.environ.get("TEMP"), "octopath", file_name)
        self.gui.screenshot(path, region=self.region)
        self.logger.debug(f"截取app窗口的屏幕截图,区域范围为{self.region}, 保存到:{path}")
        self.update_screenshot(path)
        return path

    def renew_status(self, ocr=True) -> int:
        self.logger.debug("刷新当前状态")
        path = self.renew_current_screen()
        ocr_result = None
        if ocr:
            ocr_result = self.ocr(path)
            self.update_ocr_result(ocr_result)
        status = self.detect_status(ocr_result)
        pre_status = self.cur_status
        self.dealWithStatusChange(status, pre_status)
        self.update_status(status)
        return self.cur_status

    def dealWithStatusChange(self, status: int, pre_status: int):
        if OctopathStatus.is_combat(status) and not OctopathStatus.is_combat(pre_status):
            self.logger.debug("进入战斗")
            self.battle_count_after_sleep += 1
            self.total_battle_count += 1
            self.regconize_enemy(self.cur_screenshot)
            self.logger.debug(f"敌人数量: {len(self.enemy_positions)}")
            self.enemy_total += len(self.enemy_positions)

        if OctopathStatus.is_combat(pre_status) and not OctopathStatus.is_combat(status):
            self.logger.debug("战斗结束")
            self.reset_battle_exchange()
            self.reset_enemy()

    def isInCombat(self, renew: bool = False, ocr=False) -> bool:
        if renew:
            self.renew_status(ocr=ocr)
        return OctopathStatus.is_combat(self.cur_status)

    def reset_battle_exchange(self):
        self.battle_exchange = [False, False, False, False]

    def toggle_battle_exchange(self, number: int, exchange: bool | None = None):
        index = (number - 1) // 2
        if exchange is None:
            self.battle_exchange[index] = not self.battle_exchange[index]
        else:
            self.battle_exchange[index] = exchange

    def need_exchange(self, number: int) -> bool:
        index = (number - 1) // 2
        front = number % 2 == 1
        return front and self.battle_exchange[index] or not front and not self.battle_exchange[index]

    def reset_enemy(self):
        self.enemy_positions = []

    def add_enemy_pos(self, pos: Point):
        self.enemy_positions.append(pos)

    def get_enemy_pos(self, num) -> Point:
        index = num - 1
        return self.enemy_positions[index]

    @property
    def enemy_region(self) -> Box:
        return Box(self.left, self.top + self.height // 2, self.width // 2, self.height // 2 - 50)

    def regconize_enemy(self, screenshot: str):
        # 通过敌人的血条位置识别敌人位置
        self.reset_enemy()
        path = getIconPathByIconName(IconName.TRAITS_ENEMY)
        try:
            poses = []
            boxes = self.gui.locateAll(path, screenshot, confidence=0.905, region=self.enemy_region)
            for box in boxes:
                # 需要增加pos的偏移量
                shield_pos = box.center
                pos = Point(shield_pos.x + 50, shield_pos.y - 50)
                poses.append(pos)
            # 按照x坐标排序
            self.enemy_positions = sorted(poses, key=lambda x: x.x)
            self.logger.debug(f"识别敌人位置: {self.enemy_positions}")
        except Exception as e:
            self.logger.error(f"识别敌人位置失败: {e}")

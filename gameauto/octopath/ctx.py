import time
from ..base import BaseTaskCtx
from ..gameconstants import DEFAULT_ACTION_DELAY
from .constants import TOWN, WILD, getIconPathByIconName, IconName
from PIL import Image
from typing import Union
from ..base.tuples import TxtBox
from .status import OctopathStatus
import torch
import numpy as np
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

    def getCurTime(self):
        return time.time()

    def findImageInScreen(self, image: Union[str, Image.Image, Path, IconName], screenshot: Union[str, Image.Image, Path] = None, **kargs) -> bool:

        if image is None:
            return False

        if screenshot is None:
            screenshot = self.gui.screenshot()

        if isinstance(image, IconName):
            image = getIconPathByIconName(image)
        try:
            return self.gui.locate(image, screenshot, **kargs) is not None
        except Exception:
            self.logger.debug(f"查找图片失败")
            return False

    def detect_status(self, ocr_result: list[TxtBox] = None) -> int:
        # 检测当前状态, 根据OCR结果判断当前状态
        # TODO: 优化状态检测逻辑, 由于OCR识别结果不稳定, 而且耗时较长, 可以考虑使用其他方式检测状态，比如关键像素点颜色检测，或者使用opencv模板匹配等
        status = OctopathStatus.Unknown.value

        if ocr_result is None:
            screen_shot = self.cur_screenshot
            if screen_shot is None:
                screen_shot = self.renew_current_screen()
            return self._detect_status_with_screen_shot(screen_shot)

        return status

    def _detect_status_with_ocr(self, ocr_result: list[TxtBox]) -> int:
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

    def _detect_status_with_screen_shot(self, screenshot: Union[str, Image.Image, Path]) -> int:
        # 检测当前状态, 根据屏幕截图判断当前状态
        status = OctopathStatus.Unknown.value

        if self.findImageInScreen(IconName.TRAITS_IN_BATTLE, screenshot):
            status |= OctopathStatus.Combat.value

        return status

    def ocr(self, image: Union[str, Path, Image.Image, torch.Tensor, np.ndarray]) -> list[TxtBox]:
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

    def renew_current_screen(self):
        path = os.path.join(os.environ.get("TEMP"), f"{int(time.time())}.png")
        self.gui.screenshot(path, region=self.region)
        self.logger.debug(f"截取app窗口的屏幕截图,区域范围为{self.region}, 保存到:{path}")
        path = self.update_screenshot(path)

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

        if OctopathStatus.is_combat(pre_status) and not OctopathStatus.is_combat(status):
            self.logger.debug("战斗结束")

    def isInCombat(self, renew: bool = False, ocr=False) -> bool:
        if renew:
            self.renew_status(ocr=ocr)
        return OctopathStatus.is_combat(self.cur_status)

    async def isInCombatAsync(self, renew: bool = False, ocr=False) -> bool:
        if renew:
            await self.renew_statusAsync(ocr=ocr)
        return OctopathStatus.is_combat(self.cur_status)

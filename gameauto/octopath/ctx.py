import time
from ..base import BaseTaskCtx
from ..gameconstants import DEFAULT_ACTION_DELAY
from .constants import TOWN, WILD, IconName, getIconPathByIconName
from PIL import Image
from typing import Union, Optional, Generator
from ..base.tuples import TxtBox
from .status import OctopathStatus


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

    def findIconInScreen(self, icon_name: IconName, screenshot: Optional[Image.Image] = None, **kargs) -> bool:
        image = getIconPathByIconName(icon_name)
        if screenshot is None:
            screenshot = self.gui.screenshot()
            try:
                return self.gui.locate(image, screenshot, **kargs) is not None
            except Exception:
                return False

    def detect_status(self, ocr_result: list[TxtBox] = None) -> int:
        # 检测当前状态, 根据OCR结果判断当前状态
        # TODO: 优化状态检测逻辑, 由于OCR识别结果不稳定, 而且耗时较长, 可以考虑使用其他方式检测状态，比如关键像素点颜色检测，或者使用opencv模板匹配等
        status = OctopathStatus.Unknown.value
        ocr_result: list[TxtBox] = ocr_result or self.cur_ocr_result
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

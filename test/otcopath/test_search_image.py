import importlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock
import pyautogui as pg
import time

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

SRC_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEST_DATA_DIR = Path(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testdata"
)
ENERMY_IMAGE_DIR = Path(SRC_DIR, "gameauto", "octopath", "assets", "images", "enemy")
sys.path.append(str(TEST_DATA_DIR))
importlib.invalidate_caches()

from gameauto.base.gui import getGUI, BaseGUI
from gameauto.octopath.constants.enemy import EnemyName, getIconPath
from gameauto.octopath.ctx import OctopathTaskCtx


class TestSearchImage(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        config = json.load(open(config_path))
        self.gui = getGUI(config)
        self.ctx = OctopathTaskCtx(config)

    def test_locate(self):
        image_path = getIconPath(EnemyName.FallenCait)
        image_path_2 = Path(
            TEST_DATA_DIR, "image", "octopath", "combating_cait.png"
        ).__str__()
        start_time = time.time()
        pos = pg.locate(
            needleImage=image_path, haystackImage=image_path_2, confidence=0.9
        )
        self.ctx.logger.info(f"耗时: {time.time() - start_time}")
        self.assertIsNotNone(pos)

    def test_locate_performace(self):
        image_path = getIconPath(EnemyName.FallenCait)
        image_path_2 = Path(
            TEST_DATA_DIR, "image", "octopath", "combating_cait.png"
        ).__str__()
        start_time = time.time()
        for i in range(100):
            pos = pg.locate(
                needleImage=image_path, haystackImage=image_path_2, confidence=0.9
            )
        end_time = time.time()
        self.ctx.logger.info(
            f"耗时: {end_time - start_time}, 平均耗时: {(end_time - start_time) / 100}"
        )
        self.assertIsNotNone(pos)

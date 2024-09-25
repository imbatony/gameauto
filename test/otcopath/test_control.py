import importlib
import json
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TEST_DATA_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testdata")
sys.path.append(str(TEST_DATA_DIR))
importlib.invalidate_caches()

from gameauto.octopath.commands import get_command_type_by_name, OctopathTaskCtx
from gameauto.octopath.commands.wait import WaitUntilIconFoundCommand
from gameauto.octopath.constants import IconName


class TestControlCommnad(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        self.config = json.load(open(config_path, encoding="utf-8"))
        self.ctx = OctopathTaskCtx(self.config)

    def test_wait_unil_icon_found_command(self, mock=None):
        cmdType = get_command_type_by_name("等待图标出现")
        self.assertIsNotNone(cmdType)
        self.assertEqual(cmdType, WaitUntilIconFoundCommand)
        screen_shot = Path(TEST_DATA_DIR, "image", "octopath", "combating.png")
        find = self.ctx.findImageInScreen(IconName.TRAITS_IN_BATTLE, screen_shot)
        self.assertTrue(find)

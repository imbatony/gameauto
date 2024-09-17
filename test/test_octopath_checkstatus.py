import importlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEST_DATA_DIR = Path(os.path.dirname(os.path.abspath(__file__)), "testdata")
sys.path.append(str(TEST_DATA_DIR))
importlib.invalidate_caches()

from gameauto.octopath.commands.check_status import *


class TestOctopathCheckStatus(unittest.TestCase):
    def test_check_status(self, mock=None):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "main.png")
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        config = json.load(open(config_path))
        command = OctopathCheckStatusCommand(config, image_path)
        command.recognize_text = MagicMock(return_value={"data":[{"text": "菜单", "text_box_position": [[1448, 1813], [2797, 1824], [2797, 1933], [1448, 1922]]}]})
        ret = command.run()
        self.assertTrue(ret.success)
        self.assertEqual(ret.status, "success")
        self.assertIsNotNone(ret.obj)
        obj:OctopathCheckStatusRet = ret.obj
        self.assertTrue(OctopathStatus.is_menu(obj.status))
        self.assertTrue(OctopathStatus.is_free(obj.status))
        self.assertFalse(OctopathStatus.is_combat(obj.status))

    def test_status_enum(self):
        self.assertEqual(OctopathStatus.Free.value, 1 << 0)
        self.assertEqual(OctopathStatus.Combat.value, 1 << 1)
        self.assertEqual(OctopathStatus.Dialog.value, 1 << 2)
        self.assertEqual(OctopathStatus.Menu.value, 1 << 3)
        self.assertEqual(OctopathStatus.Other.value, 1 << 4)
        self.assertEqual(OctopathStatus.Unknown.value, 1 << 10)

    def test_check_status_720p(self):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "main_720p.png")
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        config = json.load(open(config_path))
        command = OctopathCheckStatusCommand(config, image_path)
        ret = command.run()
        self.assertTrue(ret.success)
        self.assertEqual(ret.status, "success")
        self.assertIsNotNone(ret.obj)
        obj:OctopathCheckStatusRet = ret.obj
        self.assertTrue(OctopathStatus.is_menu(obj.status))
        self.assertTrue(OctopathStatus.is_free(obj.status))
        self.assertFalse(OctopathStatus.is_combat(obj.status))
import importlib
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
TEST_DATA_DIR = Path(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testdata"
)
sys.path.append(str(TEST_DATA_DIR))
importlib.invalidate_caches()

from gameauto.octopath.commands import *
from gameauto.octopath.status import OctopathStatus
from gameauto.octopath.ctx import OctopathTaskCtx


class TestOctopathCheckStatus(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        config = json.load(open(config_path))
        self.ctx = OctopathTaskCtx(config)
        self.cmd = BaseOctopathCommand

    def test_check_status(self, mock=None):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "main.png")
        ret = self.cmd.ocr(self.ctx, image_path)
        status = self.cmd.detect_status(self.ctx, ret)
        self.assertTrue(OctopathStatus.is_menu(status))
        self.assertTrue(OctopathStatus.is_free(status))
        self.assertFalse(OctopathStatus.is_combat(status))

    def test_status_enum(self):
        self.assertEqual(OctopathStatus.Free.value, 1 << 0)
        self.assertEqual(OctopathStatus.Combat.value, 1 << 1)
        self.assertEqual(OctopathStatus.Dialog.value, 1 << 2)
        self.assertEqual(OctopathStatus.Menu.value, 1 << 3)
        self.assertEqual(OctopathStatus.Other.value, 1 << 4)
        self.assertEqual(OctopathStatus.Unknown.value, 0)

    def test_check_status_720p(self):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "main_720p.png")
        ret = self.cmd.ocr(self.ctx, image_path)
        status = self.cmd.detect_status(self.ctx, ret)
        self.assertTrue(OctopathStatus.is_menu(status))
        self.assertTrue(OctopathStatus.is_free(status))
        self.assertFalse(OctopathStatus.is_combat(status))

    def test_check_combat(self):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "combat.png")
        ret = self.cmd.ocr(self.ctx, image_path)
        status = self.cmd.detect_status(self.ctx, ret)
        self.assertTrue(OctopathStatus.is_combat(status))
        self.assertFalse(OctopathStatus.is_menu(status))
        self.assertTrue(OctopathStatus.is_free(status))

    def test_check_combating(self):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "combating.png")
        ret = self.cmd.ocr(self.ctx, image_path)
        status = self.cmd.detect_status(self.ctx, ret)
        self.assertTrue(OctopathStatus.is_combat(status))
        self.assertFalse(OctopathStatus.is_menu(status))
        self.assertFalse(OctopathStatus.is_free(status))

    def test_check_end_of_combat(self):
        image_path = Path(TEST_DATA_DIR, "image", "octopath", "end_of_combat.png")
        ret = self.cmd.ocr(self.ctx, image_path)
        status = self.cmd.detect_status(self.ctx, ret)
        self.assertTrue(OctopathStatus.is_free(status))
        self.assertTrue(OctopathStatus.is_combat(status))
        self.assertFalse(OctopathStatus.is_menu(status))
        self.assertFalse(OctopathStatus.is_dialog(status))
        self.assertFalse(OctopathStatus.is_other(status))
        self.assertFalse(OctopathStatus.is_unknown(status))
        self.assertEqual(
            status,
            OctopathStatus.Free.value
            | OctopathStatus.Combat.value
            | OctopathStatus.Conclusion.value,
        )

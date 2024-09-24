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


class TestGetCommnad(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
        self.config = json.load(open(config_path))
        self.ctx = OctopathTaskCtx(self.config)

    def test_get_command(self, mock=None):
        cmd = get_command_type_by_name("强制返回主菜单")
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd.get_alternate_names(), ["强制返回主菜单", "ForceExitToMenu"])

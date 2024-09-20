import importlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
TEST_DATA_DIR = Path(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testdata"
)
sys.path.append(str(TEST_DATA_DIR))
importlib.invalidate_caches()

from gameauto.octopath.commands import *

config_path = Path(TEST_DATA_DIR, "config", "octopath.json")
config = json.load(open(config_path))
print(config)
ctx = OctopathTaskCtx(config)
ctx.active_app()

cmd = get_command_type_by_name("切换城镇")
cmd.run(ctx, "瓦洛雷")

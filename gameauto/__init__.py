from __future__ import absolute_import

__version__ = "0.0.1"

from .octopath import OctoPathGameAuto
import os
from .utils import get_logger


class GameAuto(object):
    def __init__(self, game, config):
        self.game = game
        # 读取配置文件
        self.config = self.read_config(config)
        self.logger = get_logger(self.game, self.config)

        if self.game == "octopath":
            self.gameauto = OctoPathGameAuto(self.config)
        else:
            print(f"不存在的游戏名: {self.game}")
            raise ModuleNotFoundError(f"不存在的游戏名: {self.game}")

    def run(self, action):
        self.logger.debug(f"game: {self.game}, action: {action}, config: {self.config}")
        self.gameauto.run(action)

    def run_script(self, script):
        self.logger.debug(f"game: {self.game}, script: {script}, config: {self.config}")
        # 逐行读取脚本文件
        # 当行首为#时，跳过该行
        content = ""

        try:
            with open(script, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("#"):
                        continue
                    content += line
        except UnicodeDecodeError:
            self.logger.error(f"读取脚本文件失败,请将文件保存为UTF-8格式: {script}")
            return
        except Exception:
            self.logger.error(f"读取脚本文件失败: {script}")
            return

        self.gameauto.run_script(content)

    def support_task(self, task):
        return self.gameauto.support_task(task)

    def read_config(self, config):
        import json

        # If the config file is not provided, use the default config
        default_config = {}
        if not config:
            config = "gameauto.json"

        if not os.path.exists(config):
            return default_config
        with open(config, "r", encoding="utf-8") as f:
            config = json.load(f)
            # merge the default config with the provided config
            # the provided config will overwrite the default config
            # if there is a conflict
            default_config.update(config)
            return default_config

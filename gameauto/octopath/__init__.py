from ..base import GameAutoBase
import importlib

# 提前导入所有的任务模块
from .tasks import *


class OctoPathGameAuto(GameAutoBase):
    # TODO: 需要支持中文任务名, 可以将中文任务名和英文任务名进行映射
    name_mapping: dict[str, str] = {}
    # TODO: 需要支持任务描述, 可以将任务名和任务描述进行映射
    description_mapping: dict[str, str] = {}

    def __init__(self, config):
        super().__init__(config=config)
        self._name = "OctoPath"

    def run(self, task):
        task = self.get_real_task_name(task)
        self.logger.debug(f"game: {self._name}, task: {task}, config: {self.config}")
        # import the module dynamically
        try:
            module = importlib.import_module("gameauto.octopath.tasks." + task)
            # create an instance of the class dynamically
            action_class = getattr(module, task)
            action_instance = action_class()
            action_instance.run()
        except ModuleNotFoundError as e:
            print(f"不存在的游戏自动化任务: {task}")

    def support_task(self, task):
        task = self.get_real_task_name(task)
        try:
            importlib.import_module("gameauto.octopath.tasks." + task)
            return True
        except ModuleNotFoundError as e:
            return False

    def get_real_task_name(self, task):
        return self.name_mapping.get(task, task)

    def get_task_list(self):
        return [
            (task, self.description_mapping.get(task, task))
            for task in self.name_mapping
        ]

    def run_script(self, script_content: str):
        ScriptOctopathTask(self.config, script_content).run()

from ..base import GameAutoBase
import importlib


class OctoPathGameAuto(GameAutoBase):
    def __init__(self, config):
        super().__init__(config=config)
        self._name = 'OctoPath'

    def run(self, action):
        self.logger.debug(
            f'game: {self._name}, action: {action}, config: {self.config}')
        # import the module dynamically
        try:
            module = importlib.import_module(
                'gameauto.octopath.actions.' + action)
            # create an instance of the class dynamically
            action_class = getattr(module, action)
            action_instance = action_class()
            action_instance.run()
        except ModuleNotFoundError as e:
            print(f'不存在的游戏自动化行动: {action}')

    def support_action(self, action):
        try:
            importlib.import_module('gameauto.octopath.actions.' + action)
            return True
        except ModuleNotFoundError as e:
            return False

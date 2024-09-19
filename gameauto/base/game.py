from abc import abstractmethod
from ..utils import get_logger


class GameAutoBase(object):
    """
    游戏自动化基类
    用于执行游戏自动化任务
    """

    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__
        self.logger = get_logger(self.__class__.__name__, config)

    @abstractmethod
    def run(self, task):
        """
        执行任务
        """
        raise NotImplementedError

    @abstractmethod
    def support_task(self, task) -> bool:
        """
        是否支持任务
        """
        raise NotImplementedError

    @abstractmethod
    def get_real_task_name(self, task) -> str:
        """
        获取真实任务名, 用于支持中文任务名
        """
        raise NotImplementedError

    @abstractmethod
    def get_task_list(self) -> list[(str, str)]:
        """
        获取支持的任务列表, 返回任务名和任务描述
        """
        raise NotImplementedError

    @abstractmethod
    def run_script(self, script_content: str):
        """
        执行自定义脚本
        """
        raise NotImplementedError

from ..utils import get_logger


class BaseTask(object):
    """
    任务基类
    任务是通过游戏行动组合而成的一个操作序列
    任务是游戏自动化的最大执行单元
    """

    def __init__(self, config, *args, **kwargs):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.name, config)
        self.config = config
        self.args = args
        self.kwargs = kwargs
        self.app = None

    def run(self) -> None:
        raise NotImplementedError

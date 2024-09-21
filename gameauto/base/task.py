from ..utils import get_logger


class BaseTask(object):

    @staticmethod
    def run(self) -> None:
        raise NotImplementedError

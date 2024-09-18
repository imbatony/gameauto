from ..utils import get_logger

class GameAutoBase(object):
    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__
        self.logger = get_logger(self.__class__.__name__, config)

    def run(self, action):
        raise NotImplementedError
    
    def support_action(self, action)-> bool:
        raise NotImplementedError
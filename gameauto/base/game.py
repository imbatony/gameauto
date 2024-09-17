import logging

class GameAutoBase(object):
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        if self.config.get('debug', False):
            self.logger.setLevel(logging.DEBUG)

    def run(self, action):
        raise NotImplementedError
    
    def support_action(self, action)-> bool:
        raise NotImplementedError
import logging
class BaseGameAction(object):
    def __init__(self, config, *args):
        self.config = config
        self.args = args
        self.logger = logging.getLogger(__name__)
        if self.config.get('debug', False):
            self.logger.setLevel(logging.DEBUG)
        
    def run(self):
        raise NotImplementedError
import logging
import time
from gameauto.base.command import BaseAutoGuiCommand, CommandRet
class BaseGameAction(object):
    def __init__(self, config, *args):
        self.config = config
        self.args = args
        self.logger = logging.getLogger(__name__)
        if self.config.get('debug', False):
            self.logger.setLevel(logging.DEBUG)
        self.commands: list[BaseAutoGuiCommand] = []
        
    def run(self):
        # get the start time
        start_time = time.time()
        success = True
        # run all the commands
        for command in self.commands:
            ret = command.run()
            if not ret.success:
                self.logger.error(f"命令 {command.__class__.__name__}执行失败: {ret.status} {ret.exp}")
                success = False
                break
        # get the end time
        end_time = time.time()
        # print the time
        self.logger.debug(f"Action:{self.__class__.__name__}执行完成: {end_time - start_time}, 成功: {success}")
    
    def add_command(self, command):
        self.commands.append(command)
    
    def clear_commands(self):
        self.commands.clear()
    
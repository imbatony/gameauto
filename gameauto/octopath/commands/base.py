from abc import abstractmethod
import pyautogui as pyautogui
from ...base import BaseCommand, CommandRet, CommandRetStatus
import time
import timeout_decorator
from ...base import BaseGUI


class BaseOctCommand(BaseCommand):
    def __init__(self, config, gui: BaseGUI = None, *args, **kwargs):
        super().__init__(config, gui, *args, **kwargs)

    @abstractmethod
    def run_impl(self) -> object:
        raise NotImplementedError

    def run(self) -> CommandRet:
        ret: CommandRet = CommandRet(False, CommandRetStatus.NOT_RUN, 0)
        # 记录开始时间
        start_time = time.time()
        # 执行具体的操作
        # 如果超时且break_if_timeout为True，则退出
        try:
            ret.obj = self.run_impl()
            ret.success = True
            ret.status = CommandRetStatus.SUCCESS
        except timeout_decorator.timeout_decorator.TimeoutError as e:
            ret.success = False
            ret.status = CommandRetStatus.TIMEOUT
            ret.exp = e
            self.logger.exception(f"{self.name}执行超时")
        except Exception as e:
            ret.success = False
            ret.status = CommandRetStatus.EXCEPTION
            ret.exp = e
            self.logger.exception(f"{self.name}执行异常")
        finally:
            ellipsis = time.time() - start_time
            ret.ellipsis = ellipsis
            self.logger.debug(f"{self.name}执行完成: {time.time() - start_time}")
        return ret

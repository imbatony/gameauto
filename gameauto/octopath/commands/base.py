import pyautogui as pyautogui
from ...base import BaseAutoGuiCommand, CommandRet
import time
import timeout_decorator


class BaseOctCommand(BaseAutoGuiCommand):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)

    def run_impl(self) -> object:
        raise NotImplementedError

    def run(self) -> CommandRet:
        ret: CommandRet = CommandRet(False, "not_run", None, 0)
        # 记录开始时间
        start_time = time.time()
        # 执行具体的操作
        # 如果超时且break_if_timeout为True，则退出
        try:
            ret.obj = self.run_impl()
            ret.success = True
            ret.status = "success"
        except timeout_decorator.timeout_decorator.TimeoutError as e:
            ret.success = False
            ret.status = "timeout"
            ret.exp = e
            self.logger.exception(f"{self.name}执行超时")
        except Exception as e:
            ret.success = False
            ret.status = "exception"
            ret.exp = e
            self.logger.exception(f"{self.name}执行异常")
        finally:
            ellipsis = time.time() - start_time
            ret.ellipsis = ellipsis
            self.logger.debug(f"{self.name}执行完成: {time.time() - start_time}")
        return ret
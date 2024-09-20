from abc import abstractmethod
import pyautogui as pyautogui
from ...base import BaseAction, ActionRet, ActionRetStatus
from ..ctx import OctopathTaskCtx
import time
import timeout_decorator


class BaseOctAction(BaseAction):

    @classmethod
    @abstractmethod
    def run_impl(cls, ctx: OctopathTaskCtx, *args, **kargs) -> object:
        pass

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args, **kargs) -> ActionRet:
        ret: ActionRet = ActionRet(False, ActionRetStatus.NOT_RUN, None, 0)
        # 记录开始时间
        start_time = time.time()
        # 执行具体的操作
        # 如果超时且break_if_timeout为True，则退出
        try:
            ret.obj = cls.run_impl(ctx, *args, **kargs)
            ret.success = True
            ret.status = ActionRetStatus.SUCCESS
        except timeout_decorator.timeout_decorator.TimeoutError as e:
            ret.success = False
            ret.status = ActionRetStatus.TIMEOUT
            ret.exp = e
            ctx.logger.exception(f"{cls.__name__}执行超时")
        except Exception as e:
            ret.success = False
            ret.status = ActionRetStatus.EXCEPTION
            ret.exp = e
            ctx.logger.exception(f"{cls.__name__}执行异常")
        finally:
            ellipsis = time.time() - start_time
            ret.ellipsis = ellipsis
            ctx.logger.debug(f"{cls.__name__}执行完成: {time.time() - start_time}")
        return ret

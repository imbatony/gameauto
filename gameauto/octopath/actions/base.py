from abc import abstractmethod
import collections
import pyautogui as pyautogui
from ...base import BaseAction, ActionRet, ActionRetStatus
from ..ctx import OctopathTaskCtx
import time
import timeout_decorator


class ActionRunError(Exception):
    pass


class BaseOctAction(BaseAction):

    @classmethod
    def get_desc(cls) -> str:
        return cls.__desc__

    @classmethod
    @abstractmethod
    def run_impl(cls, ctx: OctopathTaskCtx, *args) -> object:
        pass

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, *args) -> ActionRet:
        ret: ActionRet = ActionRet(False, ActionRetStatus.NOT_RUN, None, 0)
        # 记录开始时间
        start_time = time.time()
        # 执行具体的操作
        # 如果超时且break_if_timeout为True，则退出
        try:
            ret.obj = cls.run_impl(ctx, *args)
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


EXE_ACTION = collections.namedtuple(
    "EXE_ACTION", ["desc", "action_cls", "args", "interval"]
)


def runActionChain(ctx: OctopathTaskCtx, actions: list[EXE_ACTION]) -> ActionRet:
    ret: ActionRet = ActionRet(False, ActionRetStatus.NOT_RUN, None, 0)
    for action in actions:
        action_cls: type[BaseOctAction] = action.action_cls
        ctx.logger.debug(f"执行操作: {action.desc}")
        ret: ActionRet = action_cls.run(ctx, *action.args)
        if ret.status != ActionRetStatus.SUCCESS:
            ctx.logger.error(f"操作停止: {action.desc}")
            return ret
        if action.interval:
            ctx.logger.debug(f"等待: {action.interval}秒")
            time.sleep(action.interval)
        else:
            time.sleep(ctx.action_interval)
    return ret

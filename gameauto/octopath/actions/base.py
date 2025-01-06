from abc import abstractmethod
import collections
from ...base import BaseAction, ActionRet, ActionRetStatus
from ..ctx import OctopathTaskCtx
import time
import timeout_decorator
from typing import NamedTuple, Union


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


class ACTION(NamedTuple):
    desc: str
    action_cls: type[BaseOctAction]
    args: tuple = ()
    interval: int = 0


class KACTION(NamedTuple):
    desc: str
    action_cls: type[BaseOctAction]
    kargs: dict
    interval: int = 0


def runActionChain(ctx: OctopathTaskCtx, actions: list[Union[ACTION, KACTION]]) -> ActionRet:
    ret: ActionRet = ActionRet(False, ActionRetStatus.NOT_RUN, None, 0)
    for action in actions:
        # 如果action为None，则跳过
        if action is None:
            continue
        if not isinstance(action, KACTION) and not isinstance(action, ACTION):
            raise ActionRunError("action必须为ACTION或KACTION类型")

        action_cls: type[BaseOctAction] = action.action_cls
        ctx.logger.debug(f"执行操作: {action.desc}")

        if isinstance(action, KACTION):
            ret: ActionRet = action_cls.run(ctx, **action.kargs)
        else:
            ret: ActionRet = action_cls.run(ctx, *action.args)
        if ret.status != ActionRetStatus.SUCCESS:
            ctx.logger.error(f"操作停止: {action.desc}")
            return ret
        if action.interval:
            ctx.logger.debug(f"等待: {action.interval}秒")
            time.sleep(action.interval)
        elif action.interval == 0:
            pass
        else:
            time.sleep(ctx.action_default_interval)
    return ret


class DummyOctpathAction(BaseOctAction):
    __desc__ = "空操作"
    @classmethod
    def run_impl(cls, ctx: OctopathTaskCtx, *args) -> object:
        return None
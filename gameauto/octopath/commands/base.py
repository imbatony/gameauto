from abc import abstractmethod
import collections
from ...base import BaseCommand, BaseTaskCtx, TxtBox, CommandReturnCode
from ..status import OctopathStatus
from ..actions import EXE_ACTION, runActionChain
from ..ctx import OctopathTaskCtx


class BaseOctopathCommand(BaseCommand):

    __alternate_names__ = []

    @classmethod
    def get_alternate_names(cls) -> list[str]:
        return cls.__alternate_names__

    @classmethod
    @abstractmethod
    def run(cls, ctx: BaseTaskCtx, *args) -> CommandReturnCode:
        raise NotImplementedError

    @classmethod
    def detect_status(cls, ctx: BaseTaskCtx, ocr_result: list[TxtBox] = None) -> int:
        # check the status by the text
        status = OctopathStatus.Unknown.value
        ocr_result: list[TxtBox] = ocr_result or ctx.cur_ocr_result
        for pos in ocr_result:
            if "菜单" in pos.text or "商店" in pos.text or "地图" in pos.text:
                ctx.logger.debug(f"主菜单: {pos.text}")
                status |= OctopathStatus.Menu.value | OctopathStatus.Free.value
                break
            if "其他" in pos.text or "道具" in pos.text or "通知" in pos.text:
                ctx.logger.debug(f"其他菜单: {pos.text}")
                status |= OctopathStatus.Other.value | OctopathStatus.Free.value
                break
            if "回合" in pos.text:
                ctx.logger.debug(f"战斗中: {pos.text}")
                status |= OctopathStatus.Combat.value
                break
            if "战斗结算" in pos.text:
                ctx.logger.debug(f"结算: {pos.text}")
                status |= (
                    OctopathStatus.Conclusion.value
                    | OctopathStatus.Free.value
                    | OctopathStatus.Combat.value
                )
                break

        for pos in ocr_result:
            if "攻击" in pos.text and OctopathStatus.is_combat(status):
                ctx.logger.debug(f"战斗待命: {pos.text}")
                status |= OctopathStatus.Free.value

        return status

    @classmethod
    def run_actions(
        cls, ctx: OctopathTaskCtx, actions: list[EXE_ACTION]
    ) -> CommandReturnCode:
        command_name = cls.__alternate_names__[0]
        ret = runActionChain(ctx, actions)
        if not ret.success:
            ctx.logger.error(f"{command_name}失败")
            return CommandReturnCode.FAILED
        return CommandReturnCode.SUCCESS


class ChainedOctopathCommand(BaseOctopathCommand):
    """
    链式命令
    """

    @classmethod
    @abstractmethod
    def get_alternate_names(cls) -> list[str]:
        return []

    @classmethod
    @abstractmethod
    def commands(cls) -> list[type[BaseCommand]]:
        return []

    @classmethod
    def run(cls, ctx: BaseTaskCtx, *args) -> CommandReturnCode:
        for command in cls.commands():
            ret = command.run(ctx, *args)
            if ret != CommandReturnCode.SUCCESS:
                ctx.logger.error(f"命令执行失败:{command}")
                return ret
        return CommandReturnCode.SUCCESS

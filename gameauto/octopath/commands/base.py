from ...base import BaseCommand, BaseTaskCtx, TextPosition
from ..status import OctopathStatus
from ...base.gui import BaseGUI


class BaseOctopathCommand(BaseCommand):
    def __init__(self, config: dict, ctx: BaseTaskCtx, gui: BaseGUI = None):
        super().__init__(config=config, ctx=ctx, gui=gui)

    def run(self):
        raise NotImplementedError

    def detect_status(self, ocr_result: list[TextPosition]):
        # check the status by the text
        status = OctopathStatus.Unknown.value
        ocr_result: list[TextPosition] = ocr_result or self.ctx.cur_ocr_result
        for pos in ocr_result:
            if "菜单" in pos.text:
                self.logger.debug(f"主菜单: {pos.text}")
                status |= OctopathStatus.Menu.value | OctopathStatus.Free.value
            if "其他" in pos.text:
                self.logger.debug(f"其他菜单: {pos.text}")
                status |= OctopathStatus.Other.value | OctopathStatus.Free.value
            if "回合" in pos.text:
                self.logger.debug(f"战斗中: {pos.text}")
                status |= OctopathStatus.Combat.value
            if "战斗结算" in pos.text:
                self.logger.debug(f"结算: {pos.text}")
                status |= (
                    OctopathStatus.Conclusion.value
                    | OctopathStatus.Free.value
                    | OctopathStatus.Combat.value
                )

        for pos in ocr_result:
            if "攻击" in pos.text and OctopathStatus.is_combat(status):
                self.logger.debug(f"战斗待命: {pos.text}")
                status |= OctopathStatus.Free.value

        return status

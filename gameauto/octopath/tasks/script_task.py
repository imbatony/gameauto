import time
from ...base import BaseTask, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..commands import get_command_type_by_name


class ScriptOctopathTask(BaseTask):
    def __init__(self, config, script: str):
        self.ctx = OctopathTaskCtx(config)
        self.script = script

    def run(self) -> None:
        self.ctx.logger.debug(f"开始执行自定义脚本")
        self.ctx.active_app()
        for line in self.script.split("\n"):
            command, *args = line.split()
            # TODO: 需要多个空格的情况
            # TODO: 需要处理循环情况
            start_time = time.time()
            code = self.executeCommand(command, *args)
            end_time = time.time()
            self.ctx.logger.debug(f"执行命令:{command}, 耗时:{end_time - start_time}")
            if code != CommandReturnCode.SUCCESS:
                self.ctx.logger.error(f"命令执行失败:{command}")
                break

    def executeCommand(self, command: str, *args) -> CommandReturnCode:
        command_type = get_command_type_by_name(command)
        if command_type is None:
            self.ctx.logger.error(f"未找到命令:{command}")
            return
        return command_type.run(self.ctx, *args)

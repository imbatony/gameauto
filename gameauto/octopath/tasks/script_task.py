import time
from ...base import BaseTask, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..commands import get_command_type_by_name


# TODO: 考虑替换为Jinja2模板的脚本
class ScriptOctopathTask(BaseTask):
    def __init__(
        self,
        config,
        script: str,
        ctx: OctopathTaskCtx = None,
        origin_script_line: int = 0,
        is_sub_task: bool = False,
    ):
        self.ctx = ctx or OctopathTaskCtx(config)
        self.script = script
        self.origin_script_line = origin_script_line
        self.is_sub_task = is_sub_task

    def run(self) -> None:
        if not self.is_sub_task:
            self.ctx.logger.debug(f"开始执行自定义脚本")
        else:
            self.ctx.logger.debug(f"开始执行子任务脚本")

        try:
            if not self.is_sub_task:
                self.ctx.active_app()
        except Exception:
            self.ctx.logger.exception(f"激活应用失败")
            return

        lines = self.script.split("\n")
        line_index = 0
        while line_index < len(lines):
            line = lines[line_index].strip()
            # 如果是空行, 则跳过
            if not line:
                line_index += 1
                continue
            # 如果是注释, 则跳过
            if line.startswith("#"):
                line_index += 1
                continue
            command, *args = line.split()
            # 如果命令为循环或者loop, 则执行循环
            if command == "loop" or command == "循环":
                # 记录循环开始行号
                loop_start_line_index = line_index
                # 设置循环嵌套层数
                loop_nest_count = 1
                # 获取循环次数
                loop_count = int(args[0])
                # 获取循环内容
                # 循环内容为下一行到下一个endloop之间的内容
                loop_content = []
                line_index += 1
                while line_index < len(lines):
                    line = lines[line_index].strip()
                    command, *args = line.split()
                    if command == "loop" or command == "循环":
                        loop_nest_count += 1
                    if command == "endloop" or command == "循环结束":
                        loop_nest_count -= 1
                        if loop_nest_count == 0:
                            break
                    loop_content.append(line)
                    line_index += 1
                # 如果循环内容为空, 则提示错误
                if len(loop_content) == 0:
                    self.ctx.logger.error(
                        f"自定义脚本解析失败, 循环内容为空, 行号:{loop_start_line_index+1 + self.origin_script_line}"
                    )
                    return
                # 如果到达文件末尾, 则提示错误
                if line_index == len(lines):
                    self.ctx.logger.error(
                        f"自定义脚本解析失败, 未找到对应的endloop或者循环结束标识, 行号:{loop_start_line_index+1 + self.origin_script_line}"
                    )
                    return
                # 执行循环
                # 将循环内容拼接成一个字符串
                # 递归调用ScriptOctopathTask执行循环内容
                loop_content_str = "\n".join(loop_content)
                for i in range(loop_count):
                    sub_task = ScriptOctopathTask(
                        self.ctx.config,
                        loop_content_str,
                        self.ctx,
                        loop_start_line_index + 1 + self.origin_script_line,
                        is_sub_task=True,
                    )
                    sub_task.run()

                line_index += 1
                continue

            start_time = time.time()
            code = self.executeCommand(command, *args)
            end_time = time.time()
            self.ctx.logger.debug(f"执行命令:{line}, 耗时:{end_time - start_time}")
            if code != CommandReturnCode.SUCCESS:
                self.ctx.logger.error(f"命令执行失败:{command}")
                break
            line_index += 1

        # 执行完毕后, 退出应用
        # 如果

    def executeCommand(self, command: str, *args) -> CommandReturnCode:
        command_type = get_command_type_by_name(command)
        if command_type is None:
            self.ctx.logger.error(f"未找到命令:{command}")
            return
        return command_type.run(self.ctx, *args)

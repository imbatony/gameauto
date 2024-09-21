from .base import (
    BaseOctopathCommand,
    CommandReturnCode,
)

from ..ctx import OctopathTaskCtx


class TestCommand(BaseOctopathCommand):
    """
    测试
    用于测试循环脚本
    """

    __alternate_names__ = ["测试", "Test"]

    @classmethod
    def run(cls, ctx: OctopathTaskCtx, content: str) -> CommandReturnCode:
        """
        测试

        :return: 执行结果
        """
        ctx.logger.info("测试 %s", content)
        return CommandReturnCode.SUCCESS

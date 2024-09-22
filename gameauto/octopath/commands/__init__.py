from __future__ import absolute_import
from typing import Type

from .base import *
from .combat import *
from .control import *
from .move import *
from .force import *
from .test import *
from .daily import *
import inspect


command_name_type_cahce: dict[str, type[BaseOctopathCommand]] = {}


def get_command_type_by_name(
    name: str, cls: type[BaseOctopathCommand] = BaseOctopathCommand
) -> Type[BaseOctopathCommand] | None:
    """
    根据命令名获取命令类型, 用于解析自定义脚本

    :param name: 命令名
    :return: 命令类型

    """
    if name in command_name_type_cahce:
        return command_name_type_cahce[name]
    for command in cls.__subclasses__():
        # 深度优先,递归查找子类
        cmd = get_command_type_by_name(name, command)
        if cmd:
            command_name_type_cahce[name] = cmd
            return cmd
        if inspect.isabstract(command):
            continue
        if name in command.get_alternate_names():
            command_name_type_cahce[name] = command
            return command
    return None

from __future__ import absolute_import
from typing import Type

from .base import *
from .change_place import *
from .force import *
from .enter_hotel_sleep import *
from .test import *
import inspect


def get_command_type_by_name(name: str) -> Type[BaseOctopathCommand] | None:
    """
    根据命令名获取命令类型, 用于解析自定义脚本

    :param name: 命令名
    :return: 命令类型

    """

    for command in BaseOctopathCommand.__subclasses__():
        if inspect.isabstract(command):
            continue
        if name in command.get_alternate_names():
            return command
    return None

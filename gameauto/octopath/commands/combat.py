from time import sleep
from .base import BaseOctopathCommand, CommandReturnCode
from ..ctx import OctopathTaskCtx
from ..actions import (
    ClickIconAction,
    ACTION,
    ClickAction,
    ClickCenterIconAction,
    DragLeftRightAction,
)
from ..constants import getIconNameByName
from ...base.tuples import Point

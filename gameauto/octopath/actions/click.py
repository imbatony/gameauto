from .base import BaseOctAction
from ...base import Point
from ..ctx import OctopathTaskCtx
from ..constants import get_item_relative_postion_by_name, ItemRelativePostion


def _caculate_click_pos(pos: ItemRelativePostion, ctx: OctopathTaskCtx) -> Point:
    """
    计算点击位置
    """
    x = ctx.left
    y = ctx.top
    w = ctx.width
    h = ctx.height
    y_offset = int(h * pos.y_ratio)
    x_offset = int(w * (pos.x_order + 0.5) / 10)
    return Point(x + x_offset, y + y_offset)


class ClickMenuAction(BaseOctAction):
    @classmethod
    def run_impl(cls, ctx: OctopathTaskCtx, item_name: str):
        rel: ItemRelativePostion = get_item_relative_postion_by_name(item_name)
        if rel is None:
            ctx.error(f"找不到菜单项{item_name}")
            return False
        pos = _caculate_click_pos(rel, ctx)
        ctx.gui.click(pos)
        return None

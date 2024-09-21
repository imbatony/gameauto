from .base import BaseOctAction, ActionRunError
from ...base import Point
from ..ctx import OctopathTaskCtx
from ..constants import (
    ICON,
    get_icon_by_name,
    IconName,
    get_asset_path,
    RELATIVE_POS,
)


def _caculate_click_pos(pos: RELATIVE_POS, ctx: OctopathTaskCtx) -> Point:
    """
    计算点击位置
    """
    x = ctx.left
    y = ctx.top
    w = ctx.width
    h = ctx.height
    y_offset = int(h * pos.y_ratio)
    x_offset = int(w * pos.x_ratio)
    return Point(x + x_offset, y + y_offset)


class ClickAction(BaseOctAction):
    @classmethod
    def run_impl(cls, ctx: OctopathTaskCtx, pos: Point, duration: float = 0.1):
        ctx.gui.touch(pos, duration=duration)
        return None


class ClickIconAction(BaseOctAction):
    @classmethod
    def run_impl(cls, ctx: OctopathTaskCtx, icon_name: IconName, duration: float = 0.1):
        icon: ICON = get_icon_by_name(icon_name)
        if icon is None:
            raise ActionRunError(f"找不到图标{icon_name.value}")

        # 如果有相对位置，意味着图标位置是固定的, 这时候可以计算出点击位置, 直接点击
        if icon.relative_pos:
            pos = _caculate_click_pos(icon.relative_pos, ctx)
            ctx.gui.touch(pos, duration=duration)
            return None

        # 如果没有相对位置, 通过图片定位找到图标位置,然后点击
        pic_path = get_asset_path(icon.asset)
        pos = ctx.gui.locateCenterOnScreen(
            pic_path, confidence=0.8, grayscale=True, region=ctx.region
        )
        if pos is None:
            raise ActionRunError(f"找不到图标{icon_name.value}")
        ctx.gui.touch(pos)
        return None

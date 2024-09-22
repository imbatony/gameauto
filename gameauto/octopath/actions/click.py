from time import sleep
from .base import BaseOctAction, ActionRunError
from ...base import Point
from ..ctx import OctopathTaskCtx
from ..constants import (
    ICON,
    getIconByIconName,
    IconName,
    getAssetPath,
    RELATIVE_POS,
)


def _toAbsoluteForRelPos(pos: RELATIVE_POS, ctx: OctopathTaskCtx) -> Point:
    """
    根据相对位置计算绝对位置
    """
    x = ctx.left
    y = ctx.top
    w = ctx.width
    h = ctx.height
    y_offset = int(h * pos.y_ratio)
    x_offset = int(w * pos.x_ratio)
    return Point(x + x_offset, y + y_offset)


def _toAbsolutePos(pos: Point, ctx: OctopathTaskCtx) -> Point:
    """
    根据游戏内位置计算屏幕绝对位置
    """
    return Point(pos.x + ctx.left, pos.y + ctx.top)


class ClickAction(BaseOctAction):
    @classmethod
    def run_impl(
        cls,
        ctx: OctopathTaskCtx,
        pos: Point = None,
        duration: float = 0.4,
        is_absolute=True,  # 是否是绝对坐标
    ):
        if pos is None:
            # 如果没有指定位置, 默认点击屏幕中心, 用于跳过对话等操作
            pos = Point(ctx.left + ctx.width // 2, ctx.top + ctx.height // 2)
        if not is_absolute:
            # 如果是相对坐标, 需要计算绝对坐标
            pos = _toAbsolutePos(pos, ctx)
        ctx.gui.touch(pos, duration=duration)
        return None


class ClickIconAction(BaseOctAction):
    @classmethod
    def run_impl(
        cls,
        ctx: OctopathTaskCtx,
        icon_name: IconName,
        duration: float = 0.1,
        grayscale=True,
        confidence=0.8,
        center=False,
    ):
        icon: ICON = getIconByIconName(icon_name)
        if icon is None:
            raise ActionRunError(f"找不到图标{icon_name.value}")

        # 如果有相对位置，意味着图标位置是固定的, 这时候可以计算出点击位置, 直接点击
        if icon.relative_pos:
            pos = _toAbsoluteForRelPos(icon.relative_pos, ctx)
            ctx.gui.touch(pos, duration=duration)
            return None

        # 如果没有相对位置, 通过图片定位找到图标位置,然后点击
        pic_path = getAssetPath(icon.asset)
        pos = None
        pos = ctx.gui.locateCenterOnScreen(
            pic_path,
            confidence=confidence,
            grayscale=grayscale,
            region=ctx.region,
            center=center,
        )

        if pos is None:
            raise ActionRunError(f"找不到图标{icon_name.value}")
        ctx.gui.touch(pos)
        return None


class ClickCenterIconAction(BaseOctAction):
    @classmethod
    def run_impl(
        cls,
        ctx: OctopathTaskCtx,
        icon_name: IconName,
        duration: float = 0.1,
        grayscale=True,
        confidence=0.8,
    ):
        """
        点击最靠近屏幕中心的图标
        """
        return ClickIconAction.run_impl(
            ctx=ctx,
            icon_name=icon_name,
            duration=duration,
            grayscale=grayscale,
            confidence=confidence,
            center=True,
        )


class DragLeftRightAction(BaseOctAction):
    @classmethod
    def run_impl(
        cls,
        ctx: OctopathTaskCtx,
        single_duration=0.2,
        duration: float = 0.8,
        width_ratio: float = 0.0625,
        start_pos: Point = None,
    ):
        """
        来回拖动

        Args:
            duration: 单次拖动时间
            in
            width_ratio: 拖动的宽度占屏幕宽度的比例

        """
        if start_pos is None:
            # 如果没有指定起始位置, 默认从屏幕中心开始
            start_pos = Point(ctx.left + ctx.width // 2, ctx.top + ctx.height // 2)

        left = Point(start_pos.x - int(ctx.width * width_ratio), start_pos.y)
        right = Point(start_pos.x + int(ctx.width * width_ratio), start_pos.y)

        ctx.gui.dragLeftRight(
            start_pos,
            left=left,
            right=right,
            duration=duration,
            single_duration=single_duration,
        )
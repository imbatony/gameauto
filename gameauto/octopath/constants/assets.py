from abc import ABCMeta, abstractmethod
import os
from pathlib import Path
from ...base.tuples import Box, Point, RGB
from typing import NamedTuple


ASSET_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
IMAGE_DIR = Path(ASSET_DIR, "images")
MAP_IMAGE_DIR = Path(IMAGE_DIR, "maps")
ICON_IMAGE_DIR = Path(IMAGE_DIR, "icons")


class ASSET(NamedTuple):
    name: str
    type: str

    @property
    def path(self):
        return getAssetPath(self)


def getAssetPath(asset: ASSET) -> str:
    if asset.type == "map":
        return str(Path(MAP_IMAGE_DIR, asset.name))
    elif asset.type == "icon":
        return str(Path(ICON_IMAGE_DIR, asset.name))
    elif asset.type == "enemy":
        return str(Path(IMAGE_DIR, "enemy", asset.name))
    elif asset.type == "traits":
        return str(Path(IMAGE_DIR, "traits", asset.name))

    return None


class RELATIVE_POS(NamedTuple):
    x_ratio: float
    y_ratio: float


class ICON(NamedTuple):
    asset: ASSET
    relative_pos: RELATIVE_POS

    @property
    def path(self):
        return getAssetPath(self.asset)


def rpFrom720P(x: int, y: int) -> RELATIVE_POS:
    return RELATIVE_POS(x / 1280, y / 720)


# 保存了截图中的矩形区域，以及原始截图的宽高, 可以用来在不同分辨率下计算对应的矩形区域
class RelBox(NamedTuple):
    left: int
    top: int
    width: int
    height: int
    original_width: int
    original_height: int


def rbFrom720P(left: int, top: int, width: int, height: int) -> RelBox:
    return RelBox(left, top, width, height, 1280, 720)


# 计算当前分辨率下的矩形区域
def toAbsBox(rel_box: RelBox, width: int, height: int) -> Box:
    return Box(
        int(rel_box.left * width / rel_box.original_width),
        int(rel_box.top * height / rel_box.original_height),
        int(rel_box.width * width / rel_box.original_width),
        int(rel_box.height * height / rel_box.original_height),
    )


class RGBRelPoint(NamedTuple):
    rgb: RGB
    relPoint: RELATIVE_POS


def rgbPointFrom720P(rgb: RGB, point: Point) -> RGBRelPoint:
    return RGBRelPoint(rgb, RELATIVE_POS(point.x / 1280, point.y / 720))


class DETACTABLE(NamedTuple):
    name: str
    icon_asset: ASSET
    detect_box: RelBox

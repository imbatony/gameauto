import collections
from typing import NamedTuple


Point = collections.namedtuple("Point", "x y")
RGBPoint = collections.namedtuple("RGBPoint", "rgb point")
RGB = collections.namedtuple("RGB", "red green blue")


class RGB(NamedTuple):
    red: int
    green: int
    blue: int

    def __eq__(self, other: RGB) -> bool:
        return self.red == other.red and self.green == other.green and self.blue == other.blue

    def isSimilar(self, other: RGB, threshold=10) -> bool:
        return abs(self.red - other.red) < threshold and abs(self.green - other.green) < threshold and abs(self.blue - other.blue) < threshold


class TxtBox(NamedTuple):
    left: int
    top: int
    width: int
    height: int
    text: str

    @property
    def center(self):
        return Point(self.left + self.width // 2, self.top + self.height // 2)


class Box(NamedTuple):
    left: int
    top: int
    width: int
    height: int

    @property
    def center(self):
        return Point(self.left + self.width // 2, self.top + self.height // 2)

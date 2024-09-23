import collections
from typing import NamedTuple


Point = collections.namedtuple("Point", "x y")
RGB = collections.namedtuple("RGB", "red green blue")
RGBPoint = collections.namedtuple("RGBPoint", "rgb point")


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

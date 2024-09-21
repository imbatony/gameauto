import collections


Box = collections.namedtuple("Box", "left top width height")
Point = collections.namedtuple("Point", "x y")
RGB = collections.namedtuple("RGB", "red green blue")
TxtBox = collections.namedtuple("TxtBox", "left top width height text")

Box.center = property(
    lambda self: Point(self.left + self.width // 2, self.top + self.height // 2)
)

TxtBox.center = property(
    lambda self: Point(self.left + self.width // 2, self.top + self.height // 2)
)

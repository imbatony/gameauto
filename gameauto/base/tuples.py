import collections


Box = collections.namedtuple("Box", "left top width height")
Point = collections.namedtuple("Point", "x y")
RGB = collections.namedtuple("RGB", "red green blue")
TxtBox = collections.namedtuple("TxtBox", "left top width height text")


def center(box: Box):
    return Point(box.left + box.width // 2, box.top + box.height // 2)


def center(txtBox: TxtBox):
    return Point(txtBox.left + txtBox.width // 2, txtBox.top + txtBox.height // 2)

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Position<x={self.x}, y={self.y}>"


class TextPosition(Position):
    def __init__(self, text: str, x: int, y: int):
        super().__init__(x, y)
        self.text: str = text

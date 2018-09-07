import math


class Color:

    def __init__(self, r, g ,b):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        if isinstance(other, Color):
            return (Color(self.r + other.r, self.g + other.g, self.b + other.b))

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Color(self.r * other, self.g * other, self.b * other)
        elif isinstance(other, Color):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return (Color(self.r * other, self.g * other, self.b * other))
        elif isinstance(other, Color):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def __truediv__(self, other):
        return Color(self.r / other, self.g / other, self.b / other)

    def __floordiv__(self, other):
        return Color(self.r / other, self.g / other, self.b / other)

    def clamp(self):
        return Color(min(1, max(0, self.r)), min(1, max(0, self.g)), min(1, max(0, self.b)))

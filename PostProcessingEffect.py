from Color import Color


class ToneMapping:

    # max-to-one
    def post_process(self, color):
        m = max(color.r, color.g, color.b)
        if m > 1:
            return color / m
        else:
            return color


class GammaCorrection:
    def __init__(self, gamma=1.6):
        self.gamma = gamma

    def post_process(self, color):
        color = color
        return Color(color.r**self.gamma, color.g**self.gamma, color.b**self.gamma)

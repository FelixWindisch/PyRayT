import pygame
import math
from Color import Color


class Texture:
    path = 0
    texture = 0

    def __init__(self, path):
        self.path = path
        self.texture = pygame.image.load(path)

    def sample(self, u, v):
        try:
            sample = self.texture.get_at((math.floor(v * self.texture.get_height()), math.floor(u * self.texture.get_width())))
        except:
            return Color(0, 0, 0)

        return Color(sample[0] / 255, sample[1] / 255, sample[2] / 255)

    def get_size(self):
        return self.texture.get_size()

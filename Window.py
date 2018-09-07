import pygame


class Window:

    def __init__(self, resolution_x, resolution_y):
        self.screen = pygame.display.set_mode((resolution_x, resolution_y))
        pygame.display.set_caption('PyRayT v1.0')

    def set_pixel(self, x, y, color):
        pygame.draw.rect(self.screen, (color.r * 255, color.g * 255, color.b * 255), (x, y, 1, 1))

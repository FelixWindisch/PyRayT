import pygame
import Texture
import math


def mip_map(texture, mips):
    for i in range(0, mips):
        surf = texture.texture
        a = int(surf.get_width()/2.0)
        b = int(surf.get_height()/2.0)
        surf.unlock()
        surf = pygame.transform.smoothscale(surf, (a, b))
        texture.texture = surf
    return texture

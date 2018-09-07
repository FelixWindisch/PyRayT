from Color import Color
from Vector import Vec3


class Light:
    def __init__(self, direction, color, intensity, position):
        # negate for NdotL
        self.direction = -direction
        self.color = color
        self.intensity = intensity
        self.position = position

    def get_attenuation(self, distance):
        return 1


class DirectionalLight(Light):

    def __init__(self, direction, color, intensity):
        # negate for NdotL
        self.direction = -direction
        self.color = color
        self.intensity = intensity
        self.position = Vec3(0, 0, 0)

    def get_attenuation(self, distance):
        return 1


class OmniLight(Light):

    def __init__(self, position, color, intensity):
        self.position = position
        self.color = color
        self.intensity = intensity
        self.direction = None

    def get_attenuation(self, distance):
        return self.intensity / distance ** 2


class AreaLight(Light):

    def __init__(self, color, intensity, surface):
        self.color = color
        self.intensity = intensity
        self.surface = surface
        self.direction = None
        self.position = Vec3(0, 0, 0)

    def get_attenuation(self, distance):
        return self.intensity / distance ** 2

import random
import math
from Vector import*


def sample_hemisphere(n):
    s = sample_unit_square()
    phi = 2 * math.pi * s.x
    theta = 2 * math.pi * s.y
    # orthonormal base
    j = n.cross(Vec3(1, 1, 1))
    k = n.cross(j)
    return n * math.sin(phi) + j * math.sin(theta) + k * math.cos(phi)


def sample_unit_square():
    return Vec3(random.random(), random.random(), 0)


def sample_disc():
    while True:
        sample = sample_unit_square()
        if sample.length() <= 1:
            return sample

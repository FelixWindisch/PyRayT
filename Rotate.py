from Vector import Vec3
import math


def rotate_point_x(p, degrees):
    p.y = p.y * math.cos(degrees) - p.z * math.sin(degrees)
    p.z = p.y * math.sin(degrees) + p.z * math.cos(degrees)
    return p


def rotate_point_y(p, degrees):
    p.z = p.z * math.cos(degrees) - p.x * math.sin(degrees)
    p.x = p.z * math.sin(degrees) + p.x * math.cos(degrees)
    return p


def rotate_point_z(p, degrees):
    p.x = p.x*math.cos(degrees) - p.y * math.sin(degrees)
    p.y = p.x * math.sin(degrees) + p.y * math.cos(degrees)
    return p


def rotate_point(p, eulerangles):
    p = rotate_point_x(p, eulerangles.x)
    p = rotate_point_y(p, eulerangles.y)
    p = rotate_point_z(p, eulerangles.z)
    return p
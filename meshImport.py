import pywavefront
import os
import Objects
import Color
from Vector import*


def import_mesh(path):
    scene = pywavefront.Wavefront(path, strict=True)
    triangles = []
    for name, material in scene.materials.items():
        for i in range(0, int(len(material.vertices) / 24)):
            y = i * 24
            triangles.append(Objects.SmoothTriangle(
                Vec3(material.vertices[5 + y], material.vertices[6 + y], material.vertices[7 + y]),
                Vec3(material.vertices[2+ y], material.vertices[3 + y], material.vertices[4 + y]),
                Vec2(material.vertices[0+ y], material.vertices[1 + y]),
                Vec3(material.vertices[13 + y], material.vertices[14 + y], material.vertices[15 + y]),
                Vec3(material.vertices[10 + y], material.vertices[11 + y], material.vertices[12 + y]),
                Vec2(material.vertices[8 + y], material.vertices[9 + y]),
                Vec3(material.vertices[21 + y], material.vertices[22 + y], material.vertices[23 + y]),
                Vec3(material.vertices[18 + y], material.vertices[19 + y], material.vertices[20 + y]),
                Vec2(material.vertices[16 + y], material.vertices[17 + y])
            ))
    return triangles


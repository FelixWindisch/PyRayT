import pywavefront
import os

scene = pywavefront.Wavefront('C:\Users\Felix\PycharmProjects\PyPathTracer\PyPath-master\PyPath-master'+'/Pyramid.obj', strict=True)
for name, material in scene.materials.items():
    print(material.vertices)

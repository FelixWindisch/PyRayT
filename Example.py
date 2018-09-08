import os
from Material import*
from Light import*
from Objects import*
import meshImport
from Cubemap import Cubemap
from Scene import Scene
from Camera import Camera
from Vector import*
from Raytracing import Trace
from Material import LambertianMaterial

# Textures
UVDebug = Texture(os.getcwd()+"/Assets/Example/UvDebug.jpg")
# Cubemaps
skyBox = Cubemap("/Assets/Example/Skybox_Sky")
# Materials
# Lambert
lambert_white = LambertianMaterial(Color(1, 1, 1))
lambert_red = LambertianMaterial(Color(1, 0, 0))
lambert_green = LambertianMaterial(Color(0, 1, 0))
lambert_blue = LambertianMaterial(Color(0, 0, 1))
uv_debug = LambertianMaterial(Color(1, 1, 1), UVDebug)
# Phong
phong_white_rough = PhongMaterial(Color(1, 1, 1), Color(1, 1, 1), 1)
phong_white_glossy = PhongMaterial(Color(1, 1, 1), Color(1, 1, 1), 4)
# PBR
roughMetal = PBRMaterial(Color(0, 0, 1), 1, 1)
roughMetal = PBRMaterial(Color(0, 0, 1), 1, 1)
smoothDielectric = PBRMaterial(Color(0, 0, 1), 1, 0)
smoothDielectric = PBRMaterial(Color(0, 0, 1), 0, 0)
# Transparent
tinted = TransparentMaterial(1, 0.8, False, False)
cubemapRefraction = TransparentMaterial(1.6, 1, True, True)
raytracedRefraction = TransparentMaterial(1.6, 1, False, True)
# Mirror
mirror = ReflectiveMaterial(Color(1, 1, 1), 1)
cubemapReflection = ReflectiveMaterial(Color(1, 1, 1), 1, skyBox)
# Checkerboard
checkerBoard = CheckerboardMaterial()
reflectiveCheckerBoarb = ReflectiveCheckerboardMaterial()
# Lights
frontal_directional_light = [DirectionalLight(Vec3(0.1, -0.6, 1), Color(1, 1, 1), 1)]
omniLight = [OmniLight(Vec3(0, 7, 6), Color(1, 0.8, 0.8), 2)]
disc_light = [AreaLight(Color(1, 1, 1), 3, Disc(Vec3(0, 2, 10), Vec3(0, 1, 0), 3, EmissiveMaterial(Color(1, 1, 1), 5)))]
sphere_light = [AreaLight(Color(1, 1, 1), 1, Sphere(Vec3(0, 0, 6), 1, EmissiveMaterial(Color(1, 1, 1), 1)))]

# Objects
groundPlane = Plane(Vec3(0, -4, 0), Vec3(0, -1, 0), LambertianMaterial(Color(1, 1, 1)))
monkey = Mesh(meshImport.import_mesh(os.getcwd()+'/Assets/Example/Monkey.obj'), Vec3(0, 0, 20), Vec3(math.radians(180), math.radians(0), math.radians(180)), 8, lambert_white)
icosahedron = Mesh(meshImport.import_mesh(os.getcwd()+'/Assets/Example/Icosahedron.obj'), Vec3(0, 0, 1000), Vec3(math.radians(180), math.radians(0), 0), 8, lambert_white)
pyramid = Mesh(meshImport.import_mesh(os.getcwd()+'/Assets/Example/Pyramid.obj'), Vec3(0, 0, 1000), Vec3(math.radians(180), math.radians(0), 0), 8, lambert_white)

# TraceStacks
whitted = [Trace(0, True, 0, 8)]
area_lights = [Trace(0, True, 100, 8)]
pseudo_pathtracing = [Trace(20, True, 0, 3), Trace(0, False, 0, 3)]
pathtracing = [Trace(25, True, 0, 3), Trace(25, True, 0, 3)]
# Camera Angles
frontCamera = Camera(Vec3(0, 0, 0), Vec3(0, 0, 0), Vec2(100, 100), True, pseudo_pathtracing, None)


# Scenes
sphere = Scene([monkey], frontal_directional_light, frontCamera, skyBox, Color(0, 0, 0))
caustics = Scene([disc_light[0].surface, groundPlane, Sphere(Vec3(0, 1, 10), 2, lambert_white)], disc_light, frontCamera, skyBox, Color(0, 0, 0))
Implicit_Geometry = Scene([groundPlane, Sphere(Vec3(0, 1, 10), 1, LambertianMaterial(Color(1, 0, 1))), Sphere(Vec3(2, 1, 8), 1, LambertianMaterial (Color(1, 1, 1))), Sphere(Vec3(-2, 1, 8), 1, LambertianMaterial (Color(1, 1, 1)))], omniLight, frontCamera, skyBox, Color(1, 1, 1))
pathTracingDemo = Scene([Plane(Vec3(0, -4, 0), Vec3(0, -1, 0), LambertianMaterial(Color(1, 1, 0))),
                         Plane(Vec3(-4, 0, 0), Vec3(-1, 0, 0), LambertianMaterial(Color(0, 1, 1))),
                         Plane(Vec3(4, 0, 0), Vec3(1, 0, 0), LambertianMaterial(Color(1, 1, 1))),
                         Plane(Vec3(0, 0, 13), Vec3(0, 0, 1), LambertianMaterial(Color(0.5, 1, 0.5))),
                         Sphere(Vec3(0, -1.6, 10), 2, LambertianMaterial(Color(1, 0.5, 1)))],
                        disc_light, frontCamera, skyBox, Color(0, 0, 0))
caustics = Scene([groundPlane, Sphere(Vec3(0, 0, 10), 2, raytracedRefraction)], disc_light, frontCamera, skyBox, Color(0, 0, 0))


def generate_material_sphere_scene(material):
    scene = Scene([Sphere(Vec3(0, 0, 10), 4, material)], frontal_directional_light, frontCamera, skyBox, Color(0, 0, 0))
    return scene
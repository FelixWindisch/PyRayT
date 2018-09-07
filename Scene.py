import Light


class Scene:
    objects = []
    lights = []
    camera = 0
    ambient = 0

    def __init__(self, objects, lights, camera, skyBox, ambientlight):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.skyBox = skyBox
        self.ambient = ambientlight

        for l in lights:
            if isinstance(l, Light.AreaLight):
                objects.append(l.surface)

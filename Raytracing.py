import Rotate
from Ray import Ray
import math
from Light import*
import Sample
import lighting

scene = None


def trace(ray, trace_stack, recursion, eta=1):
    hit, hit_n, hit_object, hit_distance, uv = trace_nearest(ray)
    if hit is not None and trace_stack[0].global_illumination_samples < 1:
        affected_lights = list()
        for l in scene.lights:
            if isinstance(l, DirectionalLight):
                shadow_ray = Ray(hit, l.direction)
                s_hit, p1, p2, p3, p4 = trace_nearest(shadow_ray)
            elif isinstance(l, OmniLight):
                shadow_ray = Ray(hit, l.position - hit)
                s_hit, p1, p2, p3, p4 = trace_nearest(shadow_ray)
                if s_hit is not None and (s_hit-hit).length() > (l.position-hit).length():
                    s_hit = None
                l.direction = l.position - hit
            elif isinstance(l, AreaLight):
                if trace_stack[0].area_light_samples <= 1:
                    sample_ray = Ray(hit, (l.surface.get_center() - hit))
                    l_hit, l_hit_n, l_hit_object, l_hit_distance, l_uv = trace_nearest(sample_ray)
                    s_hit = 5
                    if l_hit_object == l.surface:
                        # approximate as Point Light
                        l = OmniLight(l.surface.get_center(), l.color, l.intensity)
                        l.direction = l.position - hit
                        affected_lights.append(l)
                else:
                    for i in range(0, trace_stack[0].area_light_samples):
                        sample = l.surface.get_sample()
                        sample_ray = Ray(hit + 0.05 * hit_n, (sample-hit).normalize())
                        l_hit, l_hit_n, l_hit_object, l_hit_distance, l_uv = trace_nearest(sample_ray)
                        if l_hit_object == l.surface:
                            affected_lights.append(Light(-(l_hit-sample).normalize(), l.color, l.intensity / trace_stack[0].area_light_samples))
                        s_hit = 5
            if s_hit is None:
                affected_lights.append(l)
        material_color = hit_object.material.shade(ray.direction, hit_n, affected_lights, hit, recursion, uv, eta)
        return material_color
    elif len(trace_stack) != 0 and trace_stack[0].global_illumination_samples > 0 and hit is not None:
        material_color = Color(0, 0, 0)
        gi_samples = trace_stack[0].global_illumination_samples
        popped_trace_stack = trace_stack.copy()
        popped_trace_stack.pop(0)
        for i in range(0, gi_samples):
            sample = Sample.sample_hemisphere(hit_n)
            sample_ray = Ray(hit, sample)
            sample_color = trace(sample_ray, popped_trace_stack, recursion)
            material_color += hit_object.material.shade(ray.direction, hit_n, [Light(-sample, sample_color, 1 / gi_samples, Vec3(0, 0, 0))], hit, recursion, uv)
        return material_color
    if trace_stack[0].render_skybox:
        v = ray.direction.normalize()
        return scene.skyBox.sample(v)
    else:
        return scene.ambient


def generate_prime_ray(x, y, camera):
    if camera.perspective:
        fov = math.pi * 20
        aspect_ratio = camera.resolution.x / camera.resolution.y
        px = (2 * ((x + 0.5) / camera.resolution.x) - 1) * math.tan(fov / 2 * math.pi / 180) * aspect_ratio
        py = (2 * ((y + 0.5) / camera.resolution.y) - 1) * math.tan(fov / 2 * math.pi / 180)
        direction = Vec3(px, -py, 1).normalize()
        direction = Rotate.rotate_point(direction, camera.rotation)
        return Ray(camera.position, direction)
    else:
        return Ray(scene.camera.position + Vec3(x - (scene.camera.resolution.x/2), -(y - (scene.camera.resolution.y/2)), 0) / 40, Rotate.rotate_point(Vec3(0, 0, 1), scene.camera.rotation))


def trace_nearest(ray):
    hit_object = None
    min_dist = math.inf
    nearest_hit = None
    n_nearest_hit = None
    for o in scene.objects:
        b_hit, hit, n_hit, uv = o.intersects(ray)
        if b_hit:
            distance = (ray.origin - hit).length()
            if distance < min_dist:
                nearest_hit = hit
                n_nearest_hit = n_hit
                hit_object = o
                min_dist = distance
    if nearest_hit is not None:
        return nearest_hit, n_nearest_hit, hit_object, min_dist, uv
    else:
        return None, None, None, None, None


class Trace:
    def __init__(self, global_illumination_samples, render_skybox, area_light_samples, max_recursion):
        self.global_illumination_samples = global_illumination_samples  # int
        self.render_skybox = render_skybox                              # bool
        self.area_light_samples = area_light_samples                    # int
        self.max_recursion = max_recursion                              # int

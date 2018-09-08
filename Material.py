import lighting
from Light import*
import math
from Color import Color
from Vector import Vec3
import Raytracing
from Ray import Ray
from Texture import Texture
import Sample
import abc
import MipMap

scene = None


class Material(abc.ABC):
    color = 0
    transparency = 0
    reflectivity = 0

    def shade(self, view_dir, normal, lights, hit_pos, recursion, uv, eta=1):
        raise "Use Subclass"


class UnlitMaterial (Material):

    def __init__(self, color, albedo=None):
        self.color = color
        self.albedo = albedo

    def shade(self, view_dir, normal, lights, hit_pos, recursion, uv, eta):
        if isinstance(self.albedo, Texture):
            return self.albedo.sample(uv[0], uv[1]) * self.color
        return self.color


class CheckerboardMaterial(Material):

    def __init__(self, color1=Color(1, 1, 1), color2=Color(0, 0, 0), tile_size=1):
        self.color1 = color1
        self.color2 = color2
        self.tile_size = tile_size

    def shade(self, view_dir, normal, lights, hit_pos, recursion, uv, eta=1):
        x = math.floor(hit_pos.x / self.tile_size)
        y = math.floor(hit_pos.y / self.tile_size)
        z = math.floor(hit_pos.z / self.tile_size)
        mod_x = x % 2 > 0
        mod_y = y % 2 > 0
        mod_z = z % 2 > 0
        if mod_x:
            if mod_y:
                if mod_z:
                    diffuse = self.color1
                else:
                    diffuse = self.color2
            else:
                if mod_z:
                    diffuse = self.color2
                else:
                    diffuse = self.color1
        else:
            if mod_y:
                if mod_z:
                    diffuse = self.color2
                else:
                    diffuse = self.color1
            else:
                if mod_z:
                    diffuse = self.color1
                else:
                    diffuse = self.color2
        return diffuse


class ReflectiveCheckerboardMaterial(Material):
    color1 = Color(1, 1, 1)
    color2 = Color(0, 0, 0)
    tile_size = 1

    def __init__(self, col1=Color(1, 1, 1), col2=Color(0, 0, 0), tile_size=1):
        self.color1 = col1
        self.color2 = col2
        self.tile_size = tile_size

    def shade(self, view_dir, normal, lights, hit_pos, recursion, uv, eta=1):
        x = math.floor(hit_pos.x / self.tile_size)
        y = math.floor(hit_pos.y / self.tile_size)
        z = math.floor(hit_pos.z / self.tile_size)
        mod_x = x % 2 > 0
        mod_y = y % 2 > 0
        mod_z = z % 2 > 0
        if mod_x:
            if mod_y:
                if mod_z:
                    diffuse = self.color1
                else:
                    diffuse = self.color2
            else:
                if mod_z:
                    diffuse = self.color2
                else:
                    diffuse = self.color1
        else:
            if mod_y:
                if mod_z:
                    diffuse = self.color2
                else:
                    diffuse = self.color1
            else:
                if mod_z:
                    diffuse = self.color1
                else:
                    diffuse = self.color2
        reflect_dir = view_dir.reflect(normal)
        reflection_color = Raytracing.trace(Ray(hit_pos + reflect_dir * 0.1, reflect_dir.normalize()), recursion + 1)
        diffuse_color = LambertianMaterial(diffuse).shade(view_dir, normal, lights,  hit_pos, recursion, uv)
        return 0.5 * diffuse_color + 0.5 * reflection_color


class LambertianMaterial:
    albedo = None
    normal = None

    def shade(self, view_dir, n, lights,  hit_pos, recursion, uv, eta=1):
        diffuse_color = Color(0, 0, 0)
        if isinstance(self.albedo, Texture):
            self.color = self.albedo.sample(uv[0], uv[1])
        if isinstance(self.normal, Texture):
            n = lighting.ApplyNormalMap(n, self.normal.sample(uv[0], uv[1]))
        for l in lights:
            diffuse_color += max(0, n.dotproduct(l.direction)) * self.color * l.color * l.get_attenuation((l.position - hit_pos).length()) * l.intensity
        return diffuse_color

    def __init__(self, color, albedo=None, normal=None):
        self.color = color
        self.albedo = albedo
        self.normal = normal


class PhongMaterial(Material):
    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        if isinstance(self.albedo, Texture):
            self.diffuseColor = self.albedo.sample(uv[0], uv[1])
        if isinstance(self.normal, Texture):
            normal = lighting.ApplyNormalMap(normal, self.normal.sample(uv[0], uv[1]))
        diffuse = LambertianMaterial(self.diffuseColor).shade(view_dir, normal, lights,  hit_pos, recursion, uv)
        spec = Color(0, 0, 0)
        for l in lights:
            spec += lighting.PhongNormalized(l.direction.normalize(), normal, view_dir,
                                             self.specPower) * l.color * l.intensity * self.specularColor * \
                    l.get_attenuation((hit_pos - l.position).length())
        return diffuse + spec

    def __init__(self, diff_color, spec_color, spec_power, albedo=None, normal=None):
        self.diffuseColor = diff_color
        self.specularColor = spec_color
        self.specPower = spec_power
        self.albedo = albedo
        self.normal = normal


class BlinnPhongMaterial(Material):

    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        if isinstance(self.albedo, Texture):
            self.diffuseColor = self.albedo.sample(uv[0], uv[1])
        if isinstance(self.normal, Texture):
            normal = lighting.ApplyNormalMap(normal, self.normal.sample(uv[0], uv[1]))
        diffuse = LambertianMaterial(self.diffuseColor).shade(view_dir, normal, lights,  hit_pos, recursion, uv)
        spec_color = Color(0, 0, 0)
        for l in lights:
            spec_color += lighting.BlinnPhong(-l.direction, normal, view_dir, self.specPower) * l.color * self.specularColor
        return diffuse + spec_color

    def __init__(self, diff_color, spec_color, spec_power, albedo=None, normal=None):
        self.diffuseColor = diff_color
        self.specularColor = spec_color
        self.specPower = spec_power
        self.albedo = albedo
        self.normal = normal


class PBRMaterial(Material):

    def __init__(self, color, roughness, metallic, albedo=None, normal=None):
        self.color = color
        self.roughness = roughness
        self.metallic = metallic
        self.albedo = albedo
        self.normal = normal

    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        if isinstance(self.albedo, Texture):
            self.color = self.albedo.sample(uv[0], uv[1])
        if isinstance(self.normal, Texture):
            normal = lighting.ApplyNormalMap(normal, self.normal.sample(uv[0], uv[1]))
        if isinstance(self.roughness, Texture):
            roughness = self.roughness.sample(uv[0], uv[1]).r
        else:
            roughness = self.roughness
        if isinstance(self.metallic, Texture):
            metallic = self.metallic.sample(uv[0], uv[1]).r
        else:
            metallic = self.metallic
        # 0.04 is a common F0 for dielectrics
        F0 = metallic + (1 - metallic) * 0.04
        v = ((scene.cam.position + Vec3(0, 0, 300)) - hit_pos).normalize()
        final_color = Color(0, 0, 0)
        for l in lights:
            l.direction = l.direction.normalize()
            v = -v
            h = (v + l.direction).normalize()
            F = lighting.FresnelSchlick(normal, v, F0)
            NDF = lighting.DistributionGGX(normal, h, roughness)
            G = lighting.GeometrySmith(normal, view_dir, l.direction, roughness)
            # avoid division by zero
            spec = (NDF * G * F) / max(0.00001, (4 * max(normal.dotproduct(v), 0) * max(normal.dotproduct(l.direction), 0)))
            kS = F
            kD = 1 - kS
            kD *= (1 - metallic)
            NdotL = max(normal.dotproduct(l.direction), 0)

            final_color += ((kD * self.color) / math.pi) + Color(spec * 1, spec * 1, spec * 1) * l.intensity * NdotL
            final_color += 0.5 * self.color
        return final_color


class ReflectiveMaterial(Material):

    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        reflection_ray = Ray(hit_pos, view_dir.reflect(normal))
        if self.cubemap is not None:
            reflective_color = self.cubemap.sample(reflection_ray.direction)
            return reflective_color * self.reflectivity + self.tint * (1 - self.reflectivity)
        if recursion < 8:
            reflective_color = Raytracing.trace(reflection_ray, Raytracing.Trace(0, True, 0, 8), 0, recursion + 1)
        else:
            reflective_color = Color(0, 0, 0)
        return reflective_color * self.reflectivity + self.tint * (1-self.reflectivity)

    def __init__(self, tint, reflectivity, cubemap=None):
        self.tint = tint
        self.reflectivity = reflectivity
        self.cubemap = cubemap


class TransparentMaterial (Material):

    def __init__(self, eta, transparency, sample_skybox, calculate_internal_refraction, F0=0.08):
        self.eta = eta
        self.transparency = transparency
        # 0.08 is a common value for glass
        self.F0 = F0
        self.sample_skybox = sample_skybox
        self.calculate_internal_refraction = calculate_internal_refraction

    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        r_f = lighting.FresnelSchlick(-normal, view_dir, self.F0)
        if eta == 1:
            refraction_direction = lighting.refract(-view_dir, normal, eta, self.eta)
        elif self.calculate_internal_refraction:
            refraction_direction = lighting.refract(-view_dir, normal, eta, 1)
        else:
            refraction_direction = view_dir
        if self.sample_skybox:
            refraction_color = scene.skyBox.sample(refraction_direction)
        else:
            if recursion < Material.scene.camera.trace_stack[0].max_recursion:
                if eta < self.eta:
                    refraction_color = Raytracing.trace(Ray(hit_pos - normal * 0.05, refraction_direction),
                                                        Material.scene.camera.trace_stack, recursion + 1, self.eta)
                else:
                    refraction_color = Raytracing.trace(Ray(hit_pos + normal * 0.05, refraction_direction),
                                                        Material.scene.camera.trace_stack, recursion + 1, self.eta)
            else:
                return Material.scene.skyBox.sample(refraction_direction)
        if eta < self.eta and self.sample_skybox:
            reflection_color = scene.skyBox.sample(view_dir.reflect(normal))
        elif eta < self.eta and not self.sample_skybox and recursion < 8:
            reflection_color = Raytracing.trace(Ray(hit_pos, view_dir.reflect(normal)), Material.scene.camera.trace_stack, recursion + 1)
        else:
            return refraction_color

        return (1 - r_f) * refraction_color + r_f * reflection_color


class EmissiveMaterial(Material):
    def __init__(self, color, intensity):
        self.color = color
        self.intensity = intensity

    def shade(self, view_dir, normal, lights,  hit_pos, recursion, uv, eta=1):
        return self.color * self.intensity

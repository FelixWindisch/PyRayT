from Vector import Vec3
from Color import Color
import maths
from abc import ABC
import random
import Rotate


class Object(ABC):

    def intersects(self, ray):
        raise Exception('Object is not a valid Type, use a subclass')

    def get_uv(self, hitPos):
        raise Exception('Object is not a valid Type, use a subclass')


class Sphere(Object):

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        t0 = 0
        t1 = 0

        l = ray.origin - self.center
        a = ray.direction.dotproduct(ray.direction)
        b = 2 * ray.direction.dotproduct(l)
        c = l.dotproduct(l) - pow(self.radius, 2)
        b, t0, t1 = maths.solveQuadratic(a, b, c)
        if not b:
            return False, False, False, False

        if t0 > t1:
            t0, t1 = t1, t0
        if t0 < 0:
            t0 = t1
            if t0 < 0:
                return False, False, False, False

        t = t0
        if t > 0:
            return True, ray.origin + (ray.direction * t), (
                ((ray.origin + (ray.direction * t)) - self.center).normalize()), \
                   self.get_uv(ray.origin + (ray.direction * t))
        return False, False, False, False

    def get_uv(self, hit_pos):
        n = (hit_pos - self.center).normalize()
        if n.z > 0:
            v = (n.y + 1)/2
            u = n.x / 2
        else:
            v = (n.y + 1)/2
            u = n.x/2 + 0.5
        u = min(1, max(0, u))
        v = min(1, max(0, v))
        return u, v

    def get_center(self):
        return self.center

    def get_sample(self):
        random = Vec3(random.random() * 2 - 1, random.random() * 2 - 1, random.random() * 2 - 1).normalize()
        return self.center + random * self.radius


class Plane(Object):

    def __init__(self, position, normal, material, tiling = 10):
        self.position = position
        self.normal = normal.normalize()
        self.material = material
        self.tiling = tiling

    def intersects(self, ray):
        try:
            t = ((self.position - ray.origin).dotproduct(-self.normal)) / ray.direction.dotproduct(-self.normal)
        except ZeroDivisionError:
            return False, False, False, False
        if t > 0.05:
            return True, ray.origin + ray.direction * t, -self.normal, self.get_uv(ray.origin + ray.direction * t)
        return False, False, False, False

    def get_uv(self, hit_pos):
        return hit_pos.x % self.tiling / self.tiling, hit_pos.y % self.tiling / self.tiling


class Disc(Plane):

    def __init__(self, position, normal, radius, material):
        self.position = position
        self.normal = normal
        self.radius = radius
        self.material = material

    def intersects(self, ray):
        b_hit, point, n, uv = Plane(self.position, self.normal, self.material).intersects(ray)

        if b_hit:
            distance = (self.position - point).length()
            if distance < self.radius:
                return True, point, self.normal, 0
        return False, False, False, False

    def get_sample(self):
        # Rejection sampling
        while True:
            sample_point = Vec3(random.random() * 2 - 1, random.random() * 2 - 1, 0)
            if sample_point.length() < 1:
                return self.position + self.radius * sample_point

    def get_center(self):
        return self.position


class FlatTriangle(Object):

    def __init__(self, v0, v1, v2, material):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material
        self.normal = ((v0 - v1).cross(v0 - v2)).normalize()

    def intersects(self, ray):
        a = self.v0.x - self.v1.x
        b = self.v0.x - self.v2.x
        c = ray.direction.x
        d = self.v0.x - ray.origin.x
        e = self.v0.y - self.v1.y
        f = self.v0.y - self.v2.y
        g = ray.direction.y
        h = self.v0.y - ray.origin.y
        i = self.v0.z - self.v1.z
        j = self.v0.z - self.v2.z
        k = ray.direction.z
        l = self.v0.z - ray.origin.z

        m = f * k - g * j
        n = h * k - g * l
        p = f * l - h * j
        q = g * i - e * k
        s = e * j - f * i
        try:
            inv_denom = 1/(a * m + b * q + c * s)
        except:
            return False, False, False, False
        e1 = d * m - b * n - c * p
        beta = e1 * inv_denom
        if beta < 0:
            return False, False, False, False
        r = e * l - h * i
        e2 = a * n + d * q + c * r
        gamma = e2 * inv_denom
        if gamma < 0 or beta + gamma > 1:
            return False, False, False, False
        e3 = a * p - b * r + d * s
        t = e3 * inv_denom
        if t < 0:
            return False, False, False, False
        return True, ray.origin + ray.direction * t, self.normal, 0


class SmoothTriangle(Object):
    def __init__(self, v0, n0, uv0, v1, n1, uv1, v2, n2, uv2):
        self.v0 = v0
        self.n0 = n0
        self.uv0 = uv0
        self.v1 = v1
        self.n1 = n1
        self.uv1 = uv1
        self.v2 = v2
        self.n2 = n2
        self.uv2 = uv2

    def intersects(self, ray):
        a = self.v0.x - self.v1.x
        b = self.v0.x - self.v2.x
        c = ray.direction.x
        d = self.v0.x - ray.origin.x
        e = self.v0.y - self.v1.y
        f = self.v0.y - self.v2.y
        g = ray.direction.y
        h = self.v0.y - ray.origin.y
        i = self.v0.z - self.v1.z
        j = self.v0.z - self.v2.z
        k = ray.direction.z
        l = self.v0.z - ray.origin.z

        m = f * k - g * j
        n = h * k - g * l
        p = f * l - h * j
        q = g * i - e * k
        s = e * j - f * i
        try:
            inv_denom = 1/(a * m + b * q + c * s)
        except:
            return False, False, False, False
        e1 = d * m - b * n - c * p
        beta = e1 * inv_denom
        if beta < 0:
            return False, False, False, False
        r = e * l - h * i
        e2 = a * n + d * q + c * r
        gamma = e2 * inv_denom
        if gamma < 0 or beta + gamma > 1:
            return False, False, False, False
        e3 = a * p - b * r + d * s
        t = e3 * inv_denom
        if t < 0.05:
            return False, False, False, False
        # Interpolate Normal
        n = self.n0 * (1 - beta - gamma) + self.n1 * beta + self.n2 * gamma
        # Interpolate UVs
        uv = self.uv0 * (1 - beta - gamma) + self.uv1 * beta + self.uv2 * gamma

        return True, ray.origin + ray.direction * t, n, uv


class Mesh(Object):
    def __init__(self, triangles, position, rotation, scale, material):
        for t in triangles:

            # rotation
            t.v0 = Rotate.rotate_point(t.v0, rotation)
            t.v1 = Rotate.rotate_point(t.v1, rotation)
            t.v2 = Rotate.rotate_point(t.v2, rotation)
            t.n0 = Rotate.rotate_point(t.n0, rotation)
            t.n1 = Rotate.rotate_point(t.n1, rotation)
            t.n2 = Rotate.rotate_point(t.n2, rotation)
            # scale
            t.v0 *= scale
            t.v1 *= scale
            t.v2 *= scale
            # position
            t.v0 += position
            t.v1 += position
            t.v2 += position

            t.material = material
        self.triangles = triangles
        self.material = material

    def intersects(self, ray):
        min_distance = 100000000
        nearest_triangle = None
        for t in self.triangles:
            b_hit, hit_point, hit_n, hit_uv = t.intersects(ray)
            if b_hit and (hit_point - ray.origin).length() < min_distance:
                nearest_triangle = t
                min_distance = (hit_point - ray.origin).length()
        if nearest_triangle is not None:
            b_hit, hit_point, hit_n, hit_uv = nearest_triangle.intersects(ray)
            return True, hit_point, hit_n, hit_uv
        else:
            return False, False, False, False



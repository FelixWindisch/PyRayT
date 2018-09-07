import math

class Vec3:
    x = 0
    y = 0
    z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vec3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other):
        return Vec3(self.x / other, self.y / other, self.z / other)

    def length(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

    def dotproduct(self, other):
        return self.x*other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, Vec2):
            return Vec3(self.x + other.x, self.y + other.y, self.z)
    def normalize(self):
        if self.length() == 0:
            return Vec3(0, 0, 0)
        return Vec3(self.x / self.length(), self.y / self.length(), self.z / self.length())

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def reflect(self, n):
        return self - 2 * (self.dotproduct(n) * n)

    def refract(self, N, ior):
        cosi = max(1, min(-1, self.dotproduct(N)))
        etai = 1
        etat = ior
        n = N
        if cosi < 0:
            cosi = - cosi
        else:
            etai, etat = etat, etai
            n = Vec3(0, 0, 0) - N
            eta = etai / etat
            k = 1 - eta * eta * (1 - cosi * cosi)
            if k < 0:
                return 0
            else:
                return eta * self + (eta * cosi - math.sqrt(k)) * n

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y , self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)


class Vec2:
    x = 0
    y = 0


    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index > 1:
            raise("Index out of Range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value
        if index > 1:
            raise("Index out of Range")

import math
from Vector import Vec3


def beckman(alpha, m):
    return math.exp((-pow(math.tan(alpha), 2) / pow(m,2))) / (math.pi * pow(m,2) * pow(math.cos(alpha), 4))


def refract(v, n, eta1, eta2):
    try:
        theta_c = math.asin(eta2 / eta1)
        theta_i = math.acos(n.dotproduct(v))
        if theta_i >= theta_c:
            return v.reflect(n)
    except Exception:
        total_internal_reflection = False
    eta = (eta1 / eta2)
    w = eta * (v.dotproduct(n))
    k = math.sqrt(1 + (w - eta) * (w + eta))
    return (w - k) * n - eta * v


# trowbridge-reitz GGX
def DistributionGGX(n, h, roughness):
    alpha = roughness**2
    alpha2 = alpha * alpha
    NdotH = math.fabs(n.dotproduct(h))
    NdotH2 = NdotH * NdotH
    num = alpha2
    denom = (NdotH2 * (alpha2 - 1) + 1)
    denom = math.pi * denom * denom
    return num / denom

    return (alpha**2) / (pow((n.dotproduct(h)**2)*((alpha**2)-1)+1, 2) + math.pi)


# geometry shadowing
def SchlickGGX(NdotV, k):
    return NdotV/max(0.00000000001, (NdotV*(1-k)+k))


def GeometrySmith(n, v, l, k):
    NdotV = max(n.dotproduct(-v), 0)
    NdotL = max(n.dotproduct(l), 0)
    ggx1 = SchlickGGX(NdotV, k)
    ggx2 = SchlickGGX(NdotL, k)
    return ggx1 * ggx2


def FresnelSchlick(n, v, F0):
    return F0 + ((1 - F0) * ((1 - n.dotproduct(v)) ** 5))


def CookTorrance(alpha, m, fresnel, H, V, N, L):
    G = min(1, (2*(H*N)*(V*N)) / (V * H), (2*(H*N)*(L*N)) / (V * H))
    return (beckman(alpha, m) * fresnel * G) / (4 * (V * N) * (N * L))


def Schlick(theta, eta):
    R_zero = pow((1 - eta) / (1 + eta), 2)
    return R_zero + ((1 - R_zero) * pow(1 - math.cos(theta), 5))


def SchlickMetallic(theta, eta, k):
    return (pow((eta-1), 2)+4*eta*pow((1-math.cos(theta)), 5) + pow(k, 2)) / (pow((eta+1), 2) + pow(k,2))


def Phong(light_dir, normal, view_dir, spec_power):
    reflection = light_dir.reflect(normal)
    return max(0, pow(reflection.dotproduct(view_dir), spec_power)) * (spec_power + 1 / 2)


def PhongNormalized(light_dir, normal, view_dir, spec_power):
    reflection = light_dir.reflect(normal)
    reflection = reflection.normalize()
    view_dir = view_dir.normalize()
    return max(0, pow(reflection.dotproduct(view_dir), spec_power) * ((spec_power + 2) / math.pi))


def BlinnPhong(light_dir, normal, view_dir, spec_power):
    halfVector = (light_dir + view_dir).normalize()
    return pow(normal.dotproduct(halfVector), spec_power)


def ApplyNormalMap(normal, nMap):
    nMap = Vec3(nMap.r, nMap.g, nMap.b).normalize()
    tangent = normal.cross(Vec3(1, 0, 0))
    bitangent = tangent.cross(normal)
    return (normal * nMap.z + bitangent * nMap.x + tangent * nMap.y).normalize()

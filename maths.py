import math


def solveQuadratic(a, b, c):
    discr = b * b - 4 * a * c
    x0 = x1 = -1
    if discr < 0:
        return False, False, False
    elif discr == 0:
        x0 = x1 = - 0.5 * b / a
    else:
        if b > 0:
            q = -0.5 * (b + math.sqrt(discr))
        else:
            q = -0.5 * (b - math.sqrt(discr))
            x0 = q / a
            x1 = c / q
    if x0 > x1:
        x0, x1 = x1, x0

    return True, x0, x1
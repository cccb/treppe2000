import math

H_RES = 13

def smooth_white(i, t):
    offset = (i / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    w = 0.1

    return (r, g, b, w)


def smooth_colors(i, t):
    offset = (i / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * t + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * t + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * t + 4 + offset)
    w = 0.1

    return (r, g, b, w)



def color_flow(i, t):

    p_r = (H_RES - 1) * (0.5 + 0.5 * math.sin(2.5 * t))
    p_g = (H_RES - 1) * (0.5 + 0.5 * math.sin(2.5 * t + 1.0))
    p_b = (H_RES - 1) * (0.5 + 0.5 * math.sin(2.5 * t + 2.0))

    r = 0.0
    g = 0.0
    b = 0.0

    if abs(i - p_r) < 0.5:
        r = 1.0

    if abs(i - p_g) < 0.5:
        g = 1.0

    if abs(i - p_b) < 0.5:
        b = 1.0

    return (r, g, b, 0.1)



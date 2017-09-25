import math

def smooth_white(i, t):
    offset = (i / 6.0) * (math.pi)

    r = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * t + offset)
    w = 0.1

    return (r, g, b, w)

def smooth_colors(i, t):
    offset = (i / 6.0) * (math.pi)

    r = 0.5 + 0.5 * math.cos(2.0 * t + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * t + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * t + 4 + offset)
    w = 0.1

    return (r, g, b, w)

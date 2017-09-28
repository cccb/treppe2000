import math

def smooth_white(state):
    offset = (state.v / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * state.t + offset)
    w = 0.1

    return (r, r, r, r)


def const_step(state):
    i = 11
    if state.v == i:
        return (1.0, 0, 0, 1)
    if state.v == i + 1:
        return (0, 1, 1, 0)
    return (0,0,0,0)



def const_colors(state):
    c = [(0,0,0,0), (0,0,0,0), (0,0,0,0), (0,0,0,0)]

    return c[state.v % 4]


def smooth_colors(state):
    offset = (state.v / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * state.t + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * state.t + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * state.t + 4 + offset)
    w = 0.1

    return (r, g, b, w)



def color_flow(state):

    p_r = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t))
    p_g = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t + 1.0))
    p_b = (state.v_res - 1) * (0.5 + 0.5 * math.sin(2.0 * state.t + 2.0))

    r = 0.0
    g = 0.0
    b = 0.0

    if abs(state.v - p_r) < 0.5:
        r = 1.0

    if abs(state.v - p_g) < 0.5:
        g = 1.0

    if abs(state.v - p_b) < 0.5:
        b = 1.0

    return (r, g, b, 0.1)





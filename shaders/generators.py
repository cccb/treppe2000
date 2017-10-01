

import math

from shaders import functions as fn
from shaders import oscillators as osc

def waber(freq, shift, state):

    # source 1: spatial parabola
    g0 = fn.linear_window(0, 5, state.v)
    s0 = fn.parabola(1, g0)

    f0 = fn.parabola(2, osc.saw(4.5, state.t + shift))

    w0 = fn.mix(0.2, 1.0, f0 * s0)


    # source 2: spatial parabola
    g1 = fn.linear_window(6, 14, state.v)
    s1 = fn.parabola(4, g1)

    f1 = 0.5 + 0.5 * math.sin(1 * freq * state.t + math.pi + shift)

    w1 = fn.mix(0.2, 1.0, f1) * s1


    # source 3: same
    g2 = fn.linear_window(4, 10, state.v)
    s2 = fn.parabola(1, g2)

    f2 = 0.5 + 0.5 * math.cos(0.5 * freq * state.t + math.pi * 2 + shift)

    w2 = fn.mix(0.2, 1.0, f2) * s2


    # source 4: spatial pulse
    g3 = fn.linear_window(-0.5, 4, state.v)
    s3 = fn.impulse(10, g3)

    f3 = fn.parabola(2, osc.saw(4.5, state.t + 2.5 + shift))

    w3 = fn.mix(0.1, 1.0, f3 * s3)


    return  w0 + w1 + w2 + w3


def gauge(perc, state):
    """
    Render a gauge, filled from the bottom
    """
    v_perc = 1.0 - (state.v / state.v_res)

    if v_perc <= perc:
        return 1.0

    return 0.0


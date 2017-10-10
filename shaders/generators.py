

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


def synth_adsr(a, d, s, r, t_on, t_off, v, t):
    """
    Generate envelope from synth state based on
    Attack: Time until max value
    Decay: Time until sustain is reached
    Sustain: Sustain level
    Release: Time until zero level is reached
    """

    if t_on <= 0.0:
        return 0.0

    # Release
    if t_off > t_on and t > t_off + r:
        return 0.0

    if t >= t_off and t_off > t_on:
        release_win = fn.linear_window_duration(t_off, r, t)
        release = fn.interpolate_cosine(s, 0.0, release_win)

        return release

    # Attack
    if t >= t_on and t < t_on + a:
        attack_win = fn.linear_window_duration(t_on, a, t)
        attack = fn.interpolate_cosine(0.0, v, attack_win)

        return attack

    # Decay
    if t >= t_on + a and t < t_on + a + d:
        decay_win = fn.linear_window_duration(t_on + a, d, t)
        decay = fn.interpolate_cosine(v, s, decay_win)

        return decay

    if t >= t_on:
        return s

    if t_off > t_on and t >= t_off:
        return 0.0

    return 0.0



"""
Some basic osciallators:

Oscillate between v_min and v_max
taking a given amount of time (duration).

"""

import math

def saw(v_min, v_max, duration, t):
    """Sawtooth oscillator"""
    x = (t % duration) / duration

    return v_min + x * (v_max - v_min)


def sine(v_min, v_max, duration, t):
    """Sine oscillator"""
    s = abs(v_min - v_max) / duration
    v = 0.5 + 0.5 * math.sin(s * t * (math.pi / 2))

    return v


def cosine(v_min, v_max, duration, t):
    """Cosine oscillator"""
    s = abs(v_min - v_max) / duration
    v = 0.5 + 0.5 * math.cos(s * t * (math.pi / 2))

    return v


def linear(v_min, v_max, duration, t):
    """Oscillate back and forth"""
    x = (t % duration) / duration

    if x < 0.5:
        v = v_min + (x * 2.0) * (v_max - v_min)
    else:
        v = v_max - ((x - 0.5) * 2.0) * (v_max - v_min)

    return v





"""
Some basic osciallators:

Oscillate between v_min and v_max
taking a given amount of time (duration).

"""

import math

def saw(duration, t):
    """Sawtooth oscillator"""
    x = (t % duration) / duration

    return x


def sine(freq, t):
    """Sine oscillator"""
    return 0.5 + 0.5 * math.sin(freq * t)


def cosine(freq, t):
    """Cosine oscillator"""
    return 0.5 + 0.5 * math.cos(freq * t)


def linear(v_min, v_max, duration, t):
    """Oscillate back and forth"""
    x = (t % duration) / duration

    if x < 0.5:
        v = v_min + (x * 2.0) * (v_max - v_min)
    else:
        v = v_max - ((x - 0.5) * 2.0) * (v_max - v_min)

    return v




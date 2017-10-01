import math

from shaders import oscillators as osc
from shaders import generators as gen
from shaders import functions as fn

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



def pulse(state):

    pulse_base = 1.0 - fn.impulse(8,
                                  fn.linear_window_duration(
                                    4, 1, state.t % 20.0))


    pulse_up = fn.impulse(8, fn.linear_window(pulse_base * state.v_res - 1,
                                               pulse_base * state.v_res + 8,
                                               state.v))

    return (pulse_up, 0,0,0)






def gauge_pulse(state):

    base = 0.2 * gen.waber(1, state)

    f0 = fn.impulse(12,  osc.saw(2, state.t))

    # Render gauge
    gauge = gen.gauge(f0, state)


    return (0, 0.8 * gauge, base, 0)


def pulse_wob(state):
    blue_base = 0.2 * gen.waber(1, state)

    pulse_base = 1.0 - fn.impulse(8,
                                  fn.linear_window_duration(
                                    3, 1, state.t % 10.0))


    pulse_up = fn.impulse(8, fn.linear_window(pulse_base * state.v_res - 1,
                                               pulse_base * state.v_res + 8,
                                               state.v))

    return (0, 0, blue_base, pulse_up * 0.7)


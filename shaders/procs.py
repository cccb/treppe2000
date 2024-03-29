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
    c = [(1.0,0,0,0), (0.0,1.0,0,0), (0.0,0.0,1.0,0), (0.0,0.0,0,1.0),
         (0.0,0,0,0), (0.0,1.0,0,0), (0.0,0,0.0,0), (0.0,0,0,0.0),
         (0.0,0,0,0), (0.0,0.0,0,0), (1.0,0,0.0,0), (0,0,0,0.0),
         (0.0,0,0,0), (0.0,0.0,0,0), (0.0,0,0.0,0), (0,0,0,1.0)]

    return c[state.v % 16]


def smooth_colors_old(state):
    offset = (state.v / 6.5) * math.pi

    r = 0.5 + 0.5 * math.cos(2.0 * state.t + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * state.t + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * state.t + 4 + offset)
    w = 0.1

    return (0, r, g, b)

def smooth_colors(state):
    offset = (state.v / 6.5) * math.pi
    slow = 1.0 - 0.3333333333333333333
    r = 0.5 + 0.5 * math.cos(2.0 * -state.t*slow + 2 + offset)
    g = 0.5 + 0.5 * math.cos(2.0 * -state.t*slow + 3 + offset)
    b = 0.5 + 0.5 * math.cos(2.0 * -state.t*slow + 4 + offset)
    w = 0.1
    return (r*0.071, g*0.071, b*0.071, w*0.071)



def color_flow(state):
    dimm = 0.5 # Be kind to our retinas

    pulse_len = 12.5

    # Get base color from palette
    p1 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (2.0,1.0,0.0,0.0),
          (0.5,0.20,0.25,0.0)]

    # Cycle through the palette
    cycle_period = 15 * 60 # 15 minutes
    base = fn.palette(*p1, osc.saw(cycle_period, state.t))

    # flowing pulse
    v_pos = fn.linear_window_duration(1,
                                      pulse_len,
                                      state.t % (pulse_len * 1.1)) \
                * (state.v_res + 8)

    f_pulse = fn.linear_window(-8 + v_pos, 0 + v_pos, state.v)
    pulse = 1.0 - fn.parabola(1.95, f_pulse)

    return (base[0] * pulse * dimm,
            base[1] * pulse * dimm,
            base[2] * pulse * dimm,
            0.04)


def color_flow_flow(state):
    dimm = 0.5 # Be kind to our retinas

    pulse_len = 18.5

    # Get base color from palette
    p1 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (2.0,1.0,0.0,0.0),
          (0.5,0.20,0.25,0.0)]

    # Cycle through the palette
    cycle_period = 15 * 60 # 15 minutes
    base = fn.palette(*p1, osc.saw(cycle_period, state.t))

    # flowing pulse
    v_pos = fn.linear_window_duration(1,
                                      pulse_len,
                                      state.t % (pulse_len * 1.1)) \
                * (state.v_res + 8)

    f_pulse = fn.linear_window(-8 + v_pos, 0 + v_pos, state.v)
    pulse = 1.0 - fn.parabola(5.95, f_pulse)

    # flowing pulse up
    v_pos_up = fn.linear_window_duration(1,
                                        pulse_len,
                                        -state.t % (pulse_len * 1.3)) \
                  * (state.v_res + 8)
    # v_pos_up = 1.0 - v_pos_up

    f_pulse_up = fn.linear_window(-8 + v_pos_up, 0 + v_pos_up, state.v)
    pulse_up = 1.0 - fn.parabola(5.95, f_pulse_up)

    return (base[0] * pulse_up * dimm * pulse,
            base[1] * pulse_up * dimm * pulse,
            base[2] * pulse_up * dimm * pulse,
            0.04)



def pulse(state):

    pulse_up = osc.linear(0, 13, 2, state.t)
    if state.v == pulse_up:
        return (1,0,0,0)

    return (0,0,0,0)


    pulse_base = 1.0 - fn.impulse(8,
                                  fn.linear_window_duration(
                                    0, 1, state.t % 3.0))


    pulse_up = fn.impulse(8, fn.linear_window(pulse_base * state.v_res - 1,
                                               pulse_base * state.v_res + 8,
                                               state.v))

    return (pulse_up, 0,0,0)


def gauge_pulse(state):

    base = 0.2 * gen.waber(1, 0, state)
    base2 = 0.08 * gen.waber(1, 5, state)

    f0 = fn.impulse(12, fn.linear_window_duration(5, 2, state.t % 10))
    f1 = osc.cosine(8, state.t)

    f1p = fn.mix(0.1, 0.3, f1)

    f3 = fn.clamp(0, 1, f1p + f0)

    # Render gauge
    gauge = gen.gauge(f3, state)


    # return (0.3 * gauge, 0, 0.2 * gauge + base, base2)
    return (0, 0.4 * gauge,  0.2 * gauge + base, base2)


def flow_pulse(state):
    pulse_len = 4.5
    blue_base = 0.2 * gen.waber(1, 0, state)

    # hull parabola / outer fade
    f_hull = fn.linear_window(-2, state.v_res + 1, state.v)
    hull = fn.mix(0.1, 1.0, fn.parabola(8, f_hull))

    # flowing pulse
    v_pos = fn.linear_window_duration(1, pulse_len, state.t % (pulse_len * 1.5)) * (state.v_res + 8)
    f_pulse = fn.linear_window(-8 + v_pos, 0 + v_pos, state.v)
    pulse = fn.parabola(4, f_pulse) * hull

    # flowing pulse
    v_pos2 = fn.linear_window_duration(1.4, pulse_len, state.t % (pulse_len * 1.5)) * (state.v_res + 8)
    f_pulse2 = fn.linear_window(-8 + v_pos2, 0 + v_pos2, state.v)
    pulse2 = fn.parabola(4, f_pulse2) * hull

    return (0, pulse2, blue_base, pulse)


def pulse_wob(state):
    blue_base = 0.2 * gen.waber(1, 0, state)

    pulse_base = 1.0 - fn.impulse(8,
                                  fn.linear_window_duration(
                                    4, 1, state.t % 10.0))


    pulse_up = fn.impulse(8, fn.linear_window(pulse_base * state.v_res - 1,
                                               pulse_base * state.v_res + 8,
                                               state.v))

    return (0, 0, blue_base, pulse_up * 0.7)


def random_glow(state):
    randomize = [(9, 2, 4, 8), (0, 2, 5), (3, 10, 12), (0, 3, 5, 12),
                 (4, 9), (2, 9, 11), (4, 8), (1, 5, 10, 12, 7),
                 (1,), (3, 8, 12), (9,), (2, 10, 0), (4, 11, 5, 7),
                 (0, 2, 5, 8, 12), (0, 4), (9, 12), (1, 3, 6),
                 (0, 4, 7), (9, 3, 12), (0, 5, 12)]

    duration = 1

    glow_fn = fn.impulse

    total_win_size = len(randomize) * duration

    select = math.floor((state.t % total_win_size) / duration)
    selected = randomize[select]

    pulse_t = fn.mix(0, 1, state.t % duration)

    if state.v in selected:
        pulse = fn.impulse(12, pulse_t)
        return (0, 0, 0, pulse)

    return (0,0,0,0)


def random_color_glow(state):
    colors = smooth_colors(state)
    glows = random_glow(state)

    return (0.5 * colors[0], 0.5 * colors[1], 0.5* colors[2], glows[3])



def synth_glow(state):
    synth = state.synth
    t_on = synth.t_on[state.v]
    t_off = synth.t_off[state.v]
    v = synth.v[state.v]

    envelope = gen.synth_adsr(synth.a,
                              synth.d,
                              synth.s,
                              synth.r,
                              t_on, t_off, v,
                              state.t)

    return (0, 0, 0, envelope)


def prtcls(state):
    synth = state.synth
    t_on = synth.t_on[state.v]
    t_off = synth.t_off[state.v]
    v = synth.v[state.v]

    envelope = gen.synth_adsr(0.1, 0.5, 0.7, 1.0,
                              t_on, t_off, v,
                              state.t)

    return (0, 0, 0, envelope)


def synth_color_glow(state):

    colors = smooth_colors(state)
    glows = synth_glow(state)

    return (0.5 * colors[0], 0.5 * colors[1], 0.5 * colors[2], glows[3])


def foo_pulse(state, pulse_len):
    # hull parabola / outer fade
    f_hull = fn.linear_window(-2, state.v_res + 1, state.v)
    hull = fn.mix(0.1, 1.0, fn.parabola(8, f_hull))

    # flowing pulse
    v_pos = fn.linear_window_duration(1, pulse_len, state.t % (pulse_len * 1.5)) * (state.v_res + 8)
    f_pulse = fn.linear_window(-8 + v_pos, 0 + v_pos, state.v)
    pulse = fn.parabola(4, f_pulse) * hull
    return pulse


def foo_v(state, width, phase, speed):
    h = float(state.v) / float(state.v_res)
    osc = 0.5 * (1.0 + math.sin(state.t * speed))
    osc2 = width * (0.5 + (osc*0.5))
    v = 0.5*(1.0 + math.sin(math.pi * osc2 * h))
    return v


def foo1(state):
    offset = 1.0/state.v_res
    v1 = foo_v(state, 8.0, 0.0, 0.2)
    v2 = foo_v(state, 10.0, offset, 0.3)
    v3 = foo_v(state, 8.0, offset * 2.0, 0.3)
    v4 = foo_pulse(state, 16.0)
    return (0.5 * v1, 0.2 * v2, 0.22 * v3, v4)


def krrr(state):
    randomize = [(0, 1, 2), (1, 2, 3), (2,3,4), (3,5,6), (4,5,6), (5,6,7),
                 (6,7,8),
                 (7,8,9), (8,9,10), (9,10,11), (10,11,12), (11,12,13),
                 (12,),
                 (11,12,), (10,11,12), (9,10,11), (8,9,10,), (7,8,9,),
                 (6,7,8,), (5,6,7,),
                 (4,5,6,), (3,4,5,), (2,3,4,), (1,2,3,), (1,2,0), (1,0),
                 (0,)]


    duration = 0.07

    total_win_size = len(randomize) * duration

    select = math.floor((state.t % total_win_size) / duration)
    selected = randomize[select]

    pulse_t = fn.mix(0, 1, state.t % duration)

    if state.v in selected:
        pulse = fn.impulse(12, pulse_t)
        return (1, 0, 0,0)

    return (0,0,0,0)


def palette2(state):
    pal = [
        [0.500, 0.500, 0.500, 0.0],
        [0.500, 0.500, 0.500, 0.0],
        [0.416, 0.416, 0.260, 0.0],
        [-0.042, 0.158, 0.458, 0.0],
    ]

    # Background palette
    pal_x = 1.0 - osc.linear(0.0, 1.0, state.v_res + 2, state.v)
    rgb = fn.palette(*pal, pal_x)

    rgb[0] *= 0.1
    rgb[1] *= 0.1
    rgb[2] *= 0.1
    rgb[3] = 0

    return rgb


def palette_test(state):
    p1 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (2.0,1.0,0.0,0.0),
          (0.5,0.20,0.25,0.0)]

    p2 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (1.0,1.0,1.0,0.0),
          (0.0,0.10,0.20, 0.0)]

    p3 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (1.0,1.0,1.0,0.0),
          (0.3,0.20,0.20,0.0)]

    win = fn.linear_window(0, state.v_res, state.v)

    t_win = state.t % 30
    if t_win < 10:
        return fn.palette(*p1, win - state.t)

    if t_win < 20:
        return fn.palette(*p2, win - state.t)

    if t_win < 30:
        return fn.palette(*p3, win - state.t)


def tr(state):
    colors = [
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 1.0, 1.0, 0.0),
    ]
    return colors[state.v % len(colors)]
    

def trans_pride(state):
    blue = (0.33, 0.8, 0.98, 0.0)
    pink = (0.96, 0.65, 0.72, 0.0)
    white = (0, 0, 0, 0.9)

    colors = [
        blue,
        blue,
        pink,
        pink,
        pink,
        white,
        white,
        pink,
        pink,
        pink,
        blue,
        blue,
        blue,
    ]
    rgb = colors[state.v % len(colors)]

    rgb[0] *= 0.1
    rgb[1] *= 0.1
    rgb[2] *= 0.1
    rgb[3] = 0

    return rgb


def palette_test(state):
    p1 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (2.0,1.0,0.0,0.0),
          (0.5,0.20,0.25,0.0)]

    p2 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (1.0,1.0,1.0,0.0),
          (0.0,0.10,0.20, 0.0)]

    p3 = [(0.5,0.5,0.5,0.0),
          (0.5,0.5,0.5,0.0),
          (1.0,1.0,1.0,0.0),
          (0.3,0.20,0.20,0.0)]

    win = fn.linear_window(0, state.v_res, state.v)

    t_win = state.t % 30
    if t_win < 10:
        return fn.palette(*p1, win - state.t)

    if t_win < 20:
        return fn.palette(*p2, win - state.t)

    if t_win < 30:
        return fn.palette(*p3, win - state.t)


def tr(state):
    colors = [
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (1.0, 1.0, 1.0, 0.0),
    ]
    return colors[state.v % len(colors)]


def trans_pride(state):
    blue = [0.13, 0.4, 0.98, 0.03]
    pink = [0.99, 0.15, 0.22, 0.1]
    white = [0, 0.5, 0.5, 0.4]

    colors = [
        blue,
        blue,
        pink,
        pink,
        pink,
        white,
        white,
        pink,
        pink,
        pink,
        blue,
        blue,
        blue,
    ]
    rgb = colors[state.v % len(colors)]

    rgb[0] *= 0.08
    rgb[1] *= 0.08
    rgb[2] *= 0.08
    rgb[3] *= 0.3

    return rgb


def tflow(state):
    """fade between two shaders"""
    flow = smooth_colors(state)
    pride = trans_pride(state)

    w = 120.0 # window seconds
    n = 20.0 # segments
    twin = state.t % w
    tseg = twin % (w / n)
    seg = int(twin / (w / n))
    fseg = tseg / ( w / n)

    if seg == 0:
        # fade from flow to pride
        hull = fn.interpolate_cosine(0, 1, fseg)
    elif seg < 5:
        hull = 1.0
        # keep
    elif seg == 5:
        # fade from pride to flow
        hull = fn.interpolate_cosine(1, 0, fseg)
    elif seg > 5:
        hull = 0.0

    rgb = [
        (flow[i] * (1 - hull) + pride[i] * hull)
        for i in range(4)
    ]
    return rgb



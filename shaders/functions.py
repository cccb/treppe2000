

"""
Shader function helpers (pulse, fade, etc...)

Allmost all borrowed from:
http://www.iquilezles.org/www/articles/functions/functions.htm

Some from:
https://www.khronos.org/registry/OpenGL/specs/gl/GLSLangSpec.1.40.pdf

"""

import math


def distance(a, b):
    """
    Returns the distance between a and b
    """
    return abs(b - a)


def radians(deg):
    """
    Convert degrees to radiants
    """
    return deg * math.pi / 180.0


def degrees(rad):
    """
    Convert radiants to degrees
    """
    return (rad * 180.0) / math.pi


def mix(a, b, x):
    """
    Returns the linear blend of a and b.
    """
    return (1.0 - x) * a + x * b


def clamp(l, r, x):
    """
    Clamp a value between l and r, so that
        l <= x <= r
    """
    if x < l:
        return l
    if x > r:
        return r
    return x

def step(e, x):
    """
    Returns 0.0 if x < edge, otherwise it returns 1.0.
    """
    if x < e:
        return 0.0
    return 1.0


def smoothstep(e0, e1, x):
    """
    Returns
        0.0 if x <= e0 and 1.0 if x >= e1
    and performs smooth Hermite interpolation between 0 and 1
    when
        e0 < x < e1.
    This is useful in cases where you would want a threshold
    function with a smooth transition.
    """
    x = clamp(0.0, 1.0, (x - e0) / (e1 - e0))
    return x**3 * (x * (x * 6 - 15) + 10)


def impulse(k, x):
    """
    Great for triggering behaviours or making envelopes
    for music or animation, and for anything that grows
    fast and then slowly decays. Use k to control the
    stretching o the function. Btw, it's maximum, which
    is 1.0, happens at exactly x = 1/k.
    """
    h = k * x

    return h * math.exp(1.0 - h)


def almost_identity(m, n, x):
    """
    Say you don't want to change a value unless
    it's too small and screws some of your computations up.
    Then, rather than doing a sharp conditional branch, you
    can blend your value with your threshold, and do it smoothly
    (say, with a cubic polynomial). Set m to be your threshold
    (anything above m stays unchanged), and n the value things
    will take when your value is zero. Then set

    p(0) = n
    p(m) = m
    p'(0) = 0
    p'(m) = 1

    therefore, if p(x) is a cubic, then
    p(x) = (2n-m)(x/m)^3 + (2m-3n)(x/m)^2 + n
    """
    if x > m:
        return x;

    a = 2.0 * n - m
    b = 2.0*m - 3.0*n
    t = x/m

    return (a*t + b)*t*t + n;



def cubic_pulse(c, w, x):
    """
    Of course you found yourself doing

        smoothstep(c-w,c,x)-smoothstep(c,c+w,x)

    very often, probably cause you were trying to isolate
    some features. Then this cubicPulse() is your friend.

    Also, why not, you can use it as a cheap
    replacement for a gaussian.
    """
    x = abs(x - c)

    if x > w:
        return 0.0

    x /= w

    return 1.0 - x**2 * (3.0 - 2.0 * x)


def exp_step(n, w, x):
    """
    A natural attenuation is an exponential of a linearly
    decaying quantity.
    """
    return math.exp(-k * pow(x,n))


def parabola(k, x):
    """
    A nice choice to remap the 0..1 interval into 0..1,
    such that the corners are remapped to 0 and the center to 1.

    In other words,
        parabola(0) =  parabola(1) = 0,
    and
        parabola(1/2) = 1
    """
    return pow(4.0 * x * (1.0 - x), k)


def gain(k, x):
    """
    Remapping the unit interval into the unit interval by
    expanding the sides and compressing the center, and keeping
    1/2 mapped to 1/2, that can be done with the gain() function.

    This was a common function in RSL tutorials (the Renderman
    Shading Language). k=1 is the identity curve, k<1 produces the
    classic gain() shape, and k>1 produces "s" shaped curces. The
    curves are symmetric (and inverse) for k=a and k=1/a.
    """
    n = x
    if x < 0.5:
        n = 1.0 - x

    a = 0.5 * pow(2.0 * n, k)

    if x < 0.5:
        return a

    return 1.0 - a


def power_curve(a, b, x):
    """
    A nice choice to remap the 0..1 interval into 0..1, such that
    the corners are remapped to 0. Very useful to skew the shape
    one side or the other in order to make leaves, eyes, and many
    other interesting shapes

    Note that k is chosen such that pcurve() reaches exactly 1 at
    its maximum for illustration purposes, but in many applications
    the curve needs to be scaled anyways so the slow computation of
    k can be simply avoided.
    """
    k = pow(a + b, a + b) / (pow(a, a) * pow(b, b))

    return k * pow( x, a ) * pow( 1.0-x, b );


def linear_window(l, r, x):
    """
    Returns a linear transition between 0 and 1 in a window
    of length r - l;
    """
    if x < l or x > r:
        return 0.0

    return (x - l) / abs(r - l)


def linear_window_duration(onset, width, x):
    """
    Returns a linear transition between 0 and 1 in a window
    of length width, after onset time.
    """
    return linear_window(onset, onset + width, x)


def interpolate_cosine(y0, y1, x):
    """
    Make a simple cosine interpolation.
    """
    x2 = 0.5 * (1.0 - math.cos(x * math.pi))
    return y0 * (1 - x2) + y1 * x2

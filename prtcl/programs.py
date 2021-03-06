
"""
Particle programs
"""

import random

from prtcl import particle

FPS = 30

FLOOR = particle.Particle((0,0), fixed=True)

def random_push(space):

    if len(list(space.sample1d())) == 0:
        space.add_particle(particle.Particle((0, 0),
                                             (0, random.random() * 12.0),
                                              collides=False))
    space.update()

    return space

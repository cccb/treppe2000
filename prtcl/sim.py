#!/usr/bin/env python3

import time
import random

import space
import particle


FPS = 30

FLOOR = particle.Particle((0,0), fixed=True)

def simulate_debug(space):
    space.reset()
    t0 = time.time()
    i = 0
    while True:
        t = time.time() - t0

        if i % (1 * FPS) == 0:
            space.add_particle(particle.Particle((0, 0),
                                                 (0, random.random() * 20.0),
                                                  collides=False))

        # if i % 16 == 0:
        #   FLOOR.collides = False

        # if i % 25 == 0:
        #    FLOOR.collides = True


        space.update()
        space.print_state()
        time.sleep(1.0/FPS)

        i += 1


if __name__ == "__main__":
    s = space.Space(9.81)

    s.add_particle(FLOOR)

    simulate_debug(s)


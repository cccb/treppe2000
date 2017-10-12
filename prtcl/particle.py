
import math

class Particle:
    def __init__(self, pos, v=(0,0), m=1.0, r=1.0, fixed=False, collides=True):
        self.r = r # Radius

        self.m = m # Mass

        self.x = pos[0]
        self.y = pos[1]

        self.vx = v[0]
        self.vy = v[1]

        self.space = None

        self.fixed = fixed
        self.collides = collides


    def _distance(self, x, y):
        return math.sqrt((self.x - x)**2 +
                         (self.y - y)**2)


    def _collide(self, x, y):
        if not self.collides:
            return None

        # Collide with others
        others = self.space.particles - {self}
        for p in others:
            if not p.collides:
                continue
            if p._distance(x, y) < self.r:
                return p

        return None


    def on_death(self):
        self.space.remove_particle(self)


    def update(self, dt):

        if self.fixed:
            return

        # Apply gravity
        vy = self.vy + dt * self.space.g

        # Advance
        x = self.x + dt * self.vx
        y = self.y + dt * self.vy

        # Collide
        if self._collide(x, y):
            self.vx = 0
            self.vy = 0
            return

        self.vy = vy
        self.x = x
        self.y = y

        # Are we still alive?
        if self.y < -1:
            self.on_death()

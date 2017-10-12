import time


class Space:

    def __init__(self, g=9.81, fps=30):
        """Initialize world"""
        self.g = -g
        self.particles = set()

        self.i = 0
        self.fps = fps

        self.t = None


    def add_particle(self, p):
        """Register particle in world"""
        self.particles.add(p)
        p.space = self

        return self


    def remove_particle(self, p):
        """Unregister particle"""
        self.particles = self.particles - {p}
        p.space = None

        return self


    def update(self):
        if self.t == None:
            self.t = time.time()
            return

        dt = time.time() - self.t

        for p in self.particles:
            p.update(dt)

        self.t = time.time()
        self.i += 1


    def clear(self):
        self.particles = {}


    def reset(self):
        self.t = None


    def print_state(self):
        for i, p in enumerate(self.particles):
            print("P({}) x = {}, {}, y = {}, {}".format(i,
                                                        p.x, round(p.x),
                                                        p.y, round(p.y)))

        print("-----------------------------------------------")


    def sample1d(self):
        """Get particles mapped to discrete stairs"""
        return (round(p.y) for p in self.particles if p.y >= 0.0)


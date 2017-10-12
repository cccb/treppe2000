import time


class Space:

    def __init__(self, g):
        """Initialize world"""
        self.g = -g
        self.particles = set()

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



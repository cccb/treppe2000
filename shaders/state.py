
import time
from collections import namedtuple


ShaderState = namedtuple("ShaderState", [
    "t", "u", "v", "h_res", "v_res",
    "synth"
])


class SynthState:

    def __init__(self, resolution):
        """Initialize Synth State"""
        self.resolution = resolution
        self.reset()


    def reset(self):
        """Initialize state vectors"""
        # Timing
        self.t0 = time.time()

        self.t_on = [0.0 for _ in range(0, self.resolution)]
        self.t_off = [0.0 for _ in range(0, self.resolution)]

        # Velocity
        self.v = [0.0 for _ in range(0, self.resolution)]

        # Parameters
        self.a = 0.03
        self.d = 0.3
        self.s = 0.5
        self.r = 0.5


    def _map_channel(self, channel):
        mapped_channel = int(channel % self.resolution)
        return mapped_channel


    def on(self, channel, velocity=1.0):
        """Activate Channel"""
        mapped_channel = self._map_channel(channel)

        t = time.time() - self.t0

        t_on = self.t_on[mapped_channel]
        t_off = self.t_off[mapped_channel]

        # Check if channel is already on
        if t_on < t_off:
            return

        self.t_on[mapped_channel] = t
        self.t_off[mapped_channel] = 0.0
        self.v[mapped_channel] = velocity


    def off(self, channel):
        """Release Channel"""
        mapped_channel = self._map_channel(channel)
        self.t_off[mapped_channel] = time.time() - self.t0


    def hit(self, channel, velocity=1.0, duration=0.5):
        """Hit a channel"""
        mapped_channel = self._map_channel(channel)
        self.on(channel, velocity) # Activate
        self.t_off[mapped_channel] = (time.time() - self.t0) + duration


    def set_params(a, d, s, r):
        self.a = a
        self.d = d
        self.s = s
        self.r = r

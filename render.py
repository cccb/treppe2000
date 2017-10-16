#!/usr/bin/env python3

"""
Initial implementation in python
"""

import socket
import time
import inspect
import argparse
import binascii

from shaders import procs, state
from treppe import protocol


CHANNELS_ACTIVE = 13

SYNTH = state.SynthState(CHANNELS_ACTIVE)


def open_socket(host="localhost", port=2334):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, int(port)))

    return sock


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shader")
    parser.add_argument("-H", "--host", default="localhost")
    parser.add_argument("-p", "--port", default=3123)
    parser.add_argument("-f", "--fps", default=60)

    return parser.parse_args()


def get_shaders():
    return {name: proc
            for name, proc in inspect.getmembers(procs, inspect.isfunction)
            if not name.startswith("_")}


def list_shaders(shaders_available):
    print("Shaders available:")
    for name, _ in shaders_available.items():
        print("    {}".format(name))


def render_loop(conn, shader, fps):
    """
    Rendering loop for a shader
    """
    t0 = time.time()
    fps = float(fps)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        t = time.time() - t0
        # Make shader state
        frame = []
        for i in range(0, CHANNELS_ACTIVE):
            s = state.ShaderState(t=t,
                                  u=0,
                                  v=i,
                                  h_res=1,
                                  v_res=CHANNELS_ACTIVE,
                                  synth=SYNTH)

            # Draw strip
            frame.append(shader(s))

        sock.sendto(protocol.cmd_frame_rgbw16(frame), conn)
        time.sleep(1.0/fps)




def main(args):
    shaders_available = get_shaders()
    shader = shaders_available.get(args.shader)
    if not shader:
        list_shaders(shaders_available)
        return

    print("Sending data to {}:{}".format(args.host, args.port))
    render_loop((args.host, int(args.port)), shader, args.fps)


if __name__ == "__main__":
    args = parse_args()
    main(args)


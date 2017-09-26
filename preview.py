#!/usr/bin/env python3

import sys
import time
import math
import argparse
import inspect

import pygame

from shaders import procs, state

CHANNELS_ACTIVE = 13

WIDTH = 300
HEIGHT = 800


def get_shaders():
    return {name: proc
            for name, proc in inspect.getmembers(procs, inspect.isfunction)
            if not name.startswith("_")}


def list_shaders(shaders_available):
    print("Shaders available:")
    for name, _ in shaders_available.items():
        print("    {}".format(name))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shader")

    return parser.parse_args()


def draw_strip(ctx, i, color):
    y = 20 + i * 50

    rect_up = (10, y, 280, 10)
    rect_dn = (10, y + 20, 280, 10)

    pygame.draw.rect(ctx, color, rect_up)
    pygame.draw.rect(ctx, color, rect_dn)


def _encode_rgbw(rgbw, bits):
    rgb = (min(rgbw[0] + rgbw[3], 1.0),
           min(rgbw[1] + rgbw[3], 1.0),
           min(rgbw[2] + rgbw[3], 1.0))

    return (round(rgb[0] * 255.0),
            round(rgb[1] * 255.0),
            round(rgb[2] * 255.0))



def render(ctx, t, proc):

    for i in range(0, CHANNELS_ACTIVE):
        # Make shader state
        s = state.ShaderState(t=t,
                              u=0,
                              v=i,
                              h_res=1,
                              v_res=CHANNELS_ACTIVE)

        # draw strip
        rgbw = proc(s)

        color = _encode_rgbw(rgbw, 8)
        draw_strip(ctx, i, color)


def main(args):
    shaders_available = get_shaders()
    shader = shaders_available.get(args.shader)

    if not shader:
        list_shaders(shaders_available)
        return

    pygame.init()

    display = pygame.display.set_mode((300, 800), 0, 32)

    t0 = time.time()

    while 42:
        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();

        t = time.time() - t0
        display.fill((0,0,0))
        render(display, t, shader)
        pygame.display.update()


if __name__ == "__main__":
    args = parse_args()

    main(args)


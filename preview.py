#!/usr/bin/env python3

import sys
import time
import math
import argparse
import inspect
import random
import socket
import selectors

import pygame

from treppe import protocol

DEFAULT_PORT = 3123

WIDTH = 300

CHANNELS_ACTIVE = 13

HEIGHT = CHANNELS_ACTIVE * 50 + 20

def open_socket(host="localhost", port=2334):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, int(port)))
    sock.setblocking(False)
    return sock


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)
    parser.add_argument("-t", "--gracetime", default=1.5, type=int)

    return parser.parse_args()


def draw_strip(ctx, i, color):
    y = 20 + i * 50

    rect_up = (10, y, 280, 10)
    rect_dn = (10, y + 20, 280, 10)

    pygame.draw.rect(ctx, color, rect_up)
    pygame.draw.rect(ctx, color, rect_dn)


def _map_rgbw(rgbw):
    rgb = (min(rgbw[0] + 0.5*rgbw[3], 1.0),
           min(rgbw[1] + 0.5*rgbw[3], 1.0),
           min(rgbw[2] + 0.5*rgbw[3], 1.0))

    return (round(rgb[0] * 255.0),
            round(rgb[1] * 255.0),
            round(rgb[2] * 255.0))


def render(ctx, frame):

    for i in range(0, CHANNELS_ACTIVE):
        color = _map_rgbw(frame[i])

        draw_strip(ctx, i, color)


def main(args):

    pygame.init()
    sock_a = open_socket(port=args.port)
    sock_b = open_socket(port=args.port+1)

    print("Listening on 0.0.0.0:{}".format(args.port))
    print("Listening on 0.0.0.0:{} (priority)".format(args.port+1))

    display = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    t0 = time.time()
    i = 0

    framebuffer = [(0, 0, 0, 0)
                   for _ in range(0, protocol.CHANNELS_AVAILABLE)]

    render(display, framebuffer)
    pygame.display.update()

    source = protocol.demultiplex_sockets(
        protocol.receive_sockets(sock_a, sock_b),
        1.5)

    for data in source:
        # check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # Read from socket
        packet = protocol.decode_packet(data)
        if packet.cmd == protocol.CMD_SET_DIRECT:
            framebuffer[packet.flags] = protocol.decode_rgbw16(
                packet.payload[:8])
        elif packet.cmd == protocol.CMD_FRAME:
            framebuffer = packet.payload
        elif packet.cmd == protocol.CMD_INVALID:
            print("ERROR: Received invalid data.")

        render(display, framebuffer)
        pygame.display.update()


if __name__ == "__main__":
    args = parse_args()

    main(args)


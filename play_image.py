#!/usr/bin/env python3

"""
Play a png file line by line
"""

import time
import socket
import argparse

from PIL import Image

from treppe import protocol


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host", default="localhost")
    parser.add_argument("-c", "--crap", default=False, action="store_true")
    parser.add_argument("-p", "--port", type=int, default=3123)
    parser.add_argument("-f", "--fps", type=int, default=30)
    parser.add_argument("-l", "--leds", type=int, default=16)
    parser.add_argument("filename", nargs=1)

    return parser.parse_args()


def _decode_rgba(rgba):
    return (rgba[0] / 255.0,
            rgba[1] / 255.0,
            rgba[2] / 255.0,
            1.0 - (rgba[3] / 255.0))


def _get_col(image, row, max_width):
    data = []
    for i in range(0, max_width):
        try:
            data.append(_decode_rgba(image.getpixel((row, i))))
        except IndexError:
            data.append((0,0,0,0))

    return data


def play_image(conn, filename, fps, crap, leds):
    image = Image.open(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        for x in range(image.width):
            frame = _get_col(image, x, leds)
            if crap:
                sock.sendto(protocol.encode_frame_crap8(frame), conn)
            else:
                sock.sendto(protocol.cmd_frame_rgbw16(frame), conn)

            time.sleep(1.0 / fps)



def main(args):
    conn = (args.host, args.port)
    play_image(conn,
               args.filename[0],
               args.fps,
               args.crap,
               args.leds)


if __name__ == "__main__":
    args = parse_args()
    main(args)



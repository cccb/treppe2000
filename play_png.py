
"""
Play a png file line by line
"""

import time
import socket

from PIL import Image

from treppe import protocol



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


def play_image(conn, filename, fps):
    image = Image.open(filename)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        for x in range(image.width):
            frame = _get_col(image, x, 13)
            sock.sendto(protocol.cmd_frame_rgbw16(frame), conn)

            time.sleep(1.0 / fps)





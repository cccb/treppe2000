#!/usr/bin/env python3

"""
UDP Server for treppe2000
"""

import time
import socket
import argparse

import serial

from treppe import protocol
from treppe import olsndots

LISTEN_PORT_DEFAULT = 3123

SERIAL_PORT_DEFAULT = "/dev/ttyUSB0"
SERIAL_BAUD_DEFAULT = 1000000

CHANNELS_ACTIVE = 13
CHANNELS_AVAILABLE = 16

CHANNEL_MAPPING = [7,6,5,4,1,0,9,8,11,10,15,14,13,3,12,2]


def _open_socket(port):
    """
    Open UDP socket and bind to port.

    :param port: Bind the socket to this port
    :type port: int

    :returns: A bound socket
    :rtype: socket.socket
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", port))

    return s


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen-port", default=LISTEN_PORT_DEFAULT)
    parser.add_argument("-p", "--serial-port", default=SERIAL_PORT_DEFAULT)
    parser.add_argument("-b", "--baudrate", default=SERIAL_BAUD_DEFAULT)

    return parser.parse_args()


def _encode_rgbw16(rgbw):
    """Encode rgbw value as little endian"""
    return round(rgbw[0] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[1] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[2] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[3] * 65535.0).to_bytes(2, "little")

def _encode_frame(frame_data):
    """
    Frame data: [(r,g,b,w), ...]

    The driver (maybe) expects a flat layout of rgbw data (0..65535)
    Let's try this.
    """
    return [v*65535.0 for pixel in frame for v in pixel]


def _write_frame(boards, frame):

    num_boards = len(boards)
    frame_size = len(frame)
    sub_frame_size = frame_size / num_boards

    mapped_frame = [frame[channel] for channel in CHANNEL_MAPPING]

    sub_frames = [mapped_frame[i:i + sub_frame_size]
                  for i in range(0, frame_size, sub_frame_size)]

    for i, board in enumerate(boards):
        sub_frame = sub_frames[i]
        board.send_framebuffer(_encode_frame(sub_frame))

        time.sleep(20e-6)


def recv_loop(boards, sock):

    while 42:
        packet = protocol.receive(sock)

        if packet.cmd == protocol.CMD_SET_DIRECT:
            print("This command is currently not supported")
            pass
        elif packet.cmd == protocol.CMD_FRAME:
            _write_frame(boards, packet.payload)

        time.sleep(20e-6)


def main(args):
    sock = _open_socket(args.listen_port)

    boards = [
        olsndots.Olsndot(0x23420001),
        olsndots.Olsndot(0x23420002),
    ]

    driver = olsndots.Driver(args.serial_port, devices=boards)

    recv_loop(boards, sock)


if __name__ == "__main__":
    args = _parse_args()
    main(args)


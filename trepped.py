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

CHANNEL_MAPPING = [14,12,11,10,7,6,9,8,14,14,5,4,1,0,3,2]


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
    s.setblocking(False)
    return s


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--listen-port", default=LISTEN_PORT_DEFAULT)
    parser.add_argument("-p", "--serial-port", default=SERIAL_PORT_DEFAULT)
    parser.add_argument("-b", "--baudrate", default=SERIAL_BAUD_DEFAULT)
    parser.add_argument("-t", "--gracetime", default=1.5, type=float)

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

    The driver (maybe) expects a flat layout of wrgb data (0..65535)
    Let's try this.
    """
    frame = [round(v*65535.0)
             for (r, g, b, w) in frame_data
             for v in (w, r, g, b)]

    return frame


def _write_frame(boards, frame):
    # FIXME: This kind of sucks.
    num_boards = len(boards)
    frame_size = len(frame)
    if frame_size % 2 != 0:
        return

    sub_frame_size = int(frame_size / num_boards)

    if len(frame) < max(CHANNEL_MAPPING) + 1:
        return # invalid data

    mapped_frame = [frame[channel] for channel in CHANNEL_MAPPING]

    sub_frames = [mapped_frame[i:i + sub_frame_size]
                  for i in range(0, frame_size, sub_frame_size)]

    for i, board in enumerate(boards):
        sub_frame = sub_frames[i]
        board.send_framebuf(_encode_frame(sub_frame))

        time.sleep(20e-6)


def recv_loop(boards, source):
    for data in source:
        packet = protocol.decode_packet(data)

        if packet.cmd == protocol.CMD_SET_DIRECT:
            print("This command is currently not supported")
            pass
        elif packet.cmd == protocol.CMD_FRAME:
            _write_frame(boards, packet.payload)

        time.sleep(20e-6)


def initialize_boards(serial_port, devices):
    """
    Initialize boards.
    This can fail. So, as long we don't have a
    driver - we repeat this.
    """
    print("Waiting for boards...")
    while True:
        try:
            driver = olsndots.Driver(serial_port, devices=devices)
            print("Drivers initialized.")
            return driver
        except:
            time.sleep(1)


def main(args):
    print("Listening on 0.0.0.0:{}".format(args.listen_port))
    print("Listening on 0.0.0.0:{} (priority)".format(args.listen_port+1))
    print("Gracetime: {} s".format(args.gracetime))

    sock_a = _open_socket(args.listen_port)
    sock_b = _open_socket(args.listen_port+1)

    boards = [
        olsndots.Olsndot(0x23420001),
        olsndots.Olsndot(0x23420002),
    ]

    driver = initialize_boards(args.serial_port, boards)

    source = protocol.demultiplex_sockets(
        protocol.receive_sockets(sock_a, sock_b),
        args.gracetime)

    recv_loop(boards, source)


if __name__ == "__main__":
    args = _parse_args()
    main(args)


#!/usr/bin/env python3

"""
UDP Server for treppe2000
"""

import time
import socket
import argparse

import serial

from treppe import protocol

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


def _write_frame(conn, frame):

    for i, rgbw in enumerate(frame):
        channel = CHANNEL_MAPPING[i]
        update = bytes([0x23, channel]) + _encode_rgbw16(rgbw)
        conn.write(update)
        time.sleep(20e-6)


def recv_loop(conn, sock):

    while 42:
        packet = protocol.receive(sock)

        if packet.cmd == protocol.CMD_SET_DIRECT:
            conn.write(b"\x23" + packet.flags + packet.payload)
        elif packet.cmd == protocol.CMD_FRAME:
            _write_frame(conn, packet.payload)

        time.sleep(20e-6)


def main(args):
    sock = _open_socket(args.listen_port)

    conn = serial.Serial(args.serial_port, args.baudrate)
    recv_loop(conn, sock)


if __name__ == "__main__":
    args = _parse_args()
    main(args)


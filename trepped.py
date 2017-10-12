#!/usr/bin/env python3

"""
UDP Server for treppe2000

Protocol
--------

Commands:

0x23 - Set Channel to 16 bit RGBW value (Direct to serial)
0x42 - Set frame with RGB(W) values


Flags:

Channel 0x00 - 0x10 (stair 0 - 16)

Frame 0x01 RGB
      0x02 RGBW
      0x04 8 Bit
      0x08 16 Bit (Big Endian)


Frame:

16 * RGB(A) Values


[1 Byte Cmd, 1 Byte Frame, Payload]

"""

import collections
import socket


CHANNELS_AVAILABLE = 16


CMD_INVALID = 0x00
CMD_SET_DIRECT = 0x23
CMD_FRAME = 0x42

FLAG_RGB = 0x01
FLAG_RGBA = 0x02

FLAG_BITS_8 = 0x04
FLAG_BITS_16 = 0x08


EMPTY_FRAME = [(0, 0, 0, 0) for _ in range(0, CHANNELS_AVAILABLE)]

DecodeResult = collections.namedtuple("DecodeResult", [
                                      "cmd",
                                      "flags",
                                      "payload"])



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


def _receive(sock):
    """
    Read and decode packet from socket.

    :param sock: The socket to read from
    :type sock: socket.socket

    :returns: The decoded command
    :rtype: DecodeResult
    """
    data = sock.recv(2048)

    cmd = data[0]
    flags = data[1]
    payload_data = data[2:]
    payload = b"\x00"

    # Check if this packet is valid
    if len(payload_data) != _expected_payloadlen(cmd, flags):
        return DecodeResult(CMD_INVALID, 0x00, payload)

    # Decode payload
    if cmd == CMD_SET_DIRECT:
        payload = payload_data[:8] # RRGGBBWW
    elif cmd == CMD_FRAME:
        payload = _decode_frame(payload_data, flags)

    return DecodeResult(cmd, flags, payload)


def _expected_payloadlen(cmd, flags):
    """
    Calculate expected data length for a given
    command with flags
    """
    channels = 0
    if cmd == CMD_SET_DIRECT:
        return 8

    if cmd == CMD_FRAME:
        channels = CHANNELS_AVAILABLE

    width = 0
    if flags & FLAG_RGB:
        width = 3
    elif flags & FLAG_RGBA:
        width = 4

    if flags & FLAG_BITS_16:
        width *= 2

    return channels * width


def _decode_rgbw8(payload):
    r = float(int.from_bytes(payload[0], "big")) / 255.0
    g = float(int.from_bytes(payload[1], "big")) / 255.0
    b = float(int.from_bytes(payload[2], "big")) / 255.0
    w = float(int.from_bytes(payload[3], "big")) / 255.0

    return (r, g, b, w)


def _decode_rgbw16(payload):
    r = float(int.from_bytes(payload[0:2], "big")) / 65535.0
    g = float(int.from_bytes(payload[2:4], "big")) / 65535.0
    b = float(int.from_bytes(payload[4:6], "big")) / 65535.0
    a = float(int.from_bytes(payload[6:8], "big")) / 65535.0

    return (r, g, b, w)


def _decode_rgb8(payload):
    r = float(int.from_bytes(payload[0], "big")) / 255.0
    g = float(int.from_bytes(payload[1], "big")) / 255.0
    b = float(int.from_bytes(payload[2], "big")) / 255.0

    return (r, g, b, 0.0)


def _decode_rgb16(payload):
    r = float(int.from_bytes(payload[0:2], "big")) / 65535.0
    g = float(int.from_bytes(payload[2:4], "big")) / 65535.0
    b = float(int.from_bytes(payload[4:6], "big")) / 65535.0

    return (r, g, b, 0.0)


def _decode_frame(data, flags):
    if flags & FLAG_RGB:
        if flags & FLAG_BITS_8:
            return _decode_frame_rgb8(data)
        else:
            return _decode_frame_rgb16(data)

    elif flags & FLAG_RGBA:
        if flags & FLAG_BITS_8:
            return _decode_frame_rgba8(data)
        else:
            return _decode_frame_rgba16(data)


def _decode_frame_rgb8(data):
    return [_decode_rgb8(data[i:i+3]) for i in range(0, len(data), 3)]

def _decode_frame_rgbw8(data):
    return [_decode_rgbw8(data[i:i+4]) for i in range(0, len(data), 4)]

def _decode_frame_rgb16(data):
    return [_decode_rgb16(data[i:i+6]) for i in range(0, len(data), 6)]

def _decode_frame_rgbw16(data):
    return [_decode_rgbw16(data[i:i+8]) for i in range(0, len(data), 8)]



def main():
    sock = _open_socket(2334)

    while 42:
        action = _receive(sock)
        print(action)


if __name__ == "__main__":
    main()


"""
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
import time

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


def receive(sock):
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

    # Decode payload
    if cmd == CMD_SET_DIRECT:
        payload = payload_data[:8] # RRGGBBWW
    elif cmd == CMD_FRAME:
        try:
            payload = decode_frame(payload_data, flags)
        except:
            return DecodeResult(CMD_INVALID, 0x00, None)

    return DecodeResult(cmd, flags, payload)


def encode_rgb8(r, g, b):
    return bytes([int(r * 255.0),
                  int(g * 255.0),
                  int(b * 255.0)])


def encode_rgbw8(r, g, b, w):
    return bytes([int(r * 255.0),
                  int(g * 255.0),
                  int(b * 255.0),
                  int(w * 255.0)])


def encode_rgb16(r, g, b):
    return int(r * 65535.0).to_bytes(2, "big") + \
           int(g * 65535.0).to_bytes(2, "big") + \
           int(b * 65535.0).to_bytes(2, "big")


def encode_rgbw16(r, g, b, w):
    return int(r * 65535.0).to_bytes(2, "big") + \
           int(g * 65535.0).to_bytes(2, "big") + \
           int(b * 65535.0).to_bytes(2, "big") + \
           int(w * 65535.0).to_bytes(2, "big")


def decode_rgbw8(payload):
    r = float(int(payload[0])) / 255.0
    g = float(int(payload[1])) / 255.0
    b = float(int(payload[2])) / 255.0
    w = float(int(payload[3])) / 255.0

    return (r, g, b, w)


def decode_rgbw16(payload):
    r = float(int.from_bytes(payload[0:2], "big")) / 65535.0
    g = float(int.from_bytes(payload[2:4], "big")) / 65535.0
    b = float(int.from_bytes(payload[4:6], "big")) / 65535.0
    a = float(int.from_bytes(payload[6:8], "big")) / 65535.0

    return (r, g, b, w)


def decode_rgb8(payload):
    r = float(int(payload[0])) / 255.0
    g = float(int(payload[1])) / 255.0
    b = float(int(payload[2])) / 255.0

    return (r, g, b, 0.0)


def decode_rgb16(payload):
    r = float(int.from_bytes(payload[0:2], "big")) / 65535.0
    g = float(int.from_bytes(payload[2:4], "big")) / 65535.0
    b = float(int.from_bytes(payload[4:6], "big")) / 65535.0

    return (r, g, b, 0.0)


def decode_frame(data, flags):
    if flags & FLAG_RGB:
        if flags & FLAG_BITS_8:
            return decode_frame_rgb8(data)
        else:
            return decode_frame_rgb16(data)

    elif flags & FLAG_RGBA:
        if flags & FLAG_BITS_8:
            return decode_frame_rgba8(data)
        else:
            return decode_frame_rgba16(data)


def decode_frame_rgb8(data):
    return [decode_rgb8(data[i:i+3]) for i in range(0, len(data), 3)]

def decode_frame_rgbw8(data):
    return [decode_rgbw8(data[i:i+4]) for i in range(0, len(data), 4)]

def decode_frame_rgb16(data):
    return [decode_rgb16(data[i:i+6]) for i in range(0, len(data), 6)]

def decode_frame_rgbw16(data):
    return [decode_rgbw16(data[i:i+8]) for i in range(0, len(data), 8)]


def _pad_frame_rgb(frame):
    if len(frame) < CHANNELS_AVAILABLE:
        frame = frame + [(0, 0, 0)
                         for _ in range(0, CHANNELS_AVAILABLE - len(frame))]
    return frame


def _pad_frame_rgbw(frame):
    if len(frame) < CHANNELS_AVAILABLE:
        frame = frame + [(0, 0, 0, 0)
                         for _ in range(0, CHANNELS_AVAILABLE - len(frame))]
    return frame


def encode_frame_rgb8(frame):
    frame = _pad_frame_rgb(frame)

    return b"".join(encode_rgb8(*rgb)
                    for rgb in frame[:CHANNELS_AVAILABLE])


def encode_frame_rgbw8(frame):
    frame = _pad_frame_rgbw(frame)

    return b"".join(encode_rgbw8(*rgbw)
                    for rgbw in frame[:CHANNELS_AVAILABLE])


def encode_frame_rgb16(frame):
    frame = _pad_frame_rgb(frame)

    return b"".join(encode_rgb16(*rgb)
                    for rgb in frame[:CHANNELS_AVAILABLE])


def encode_frame_rgbw16(frame):
    frame = _pad_frame_rgbw(frame)

    return b"".join(encode_rgbw16(*rgbw)
                    for rgbw in frame[:CHANNELS_AVAILABLE])


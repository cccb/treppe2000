#!/usr/bin/env python3

"""
Initial implementation in python
"""

import time
import inspect
import argparse

import serial

from shaders import procs, state

import binascii


SERIAL_PORT_DEFAULT = "/dev/ttyUSB0"
SERIAL_BAUD_DEFAULT = 1000000

CHANNELS_ACTIVE = 13
CHANNELS_AVAILABLE = 16

CHANNEL_MAPPING = [0,1,2,3,4,5,13,12,11,10,9,8,7,6,14,15]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--shader")
    parser.add_argument("-p", "--serial-port", default=SERIAL_PORT_DEFAULT)
    parser.add_argument("-b", "--baudrate", default=SERIAL_BAUD_DEFAULT)

    return parser.parse_args()

def get_shaders():
    return {name: proc
            for name, proc in inspect.getmembers(procs, inspect.isfunction)
            if not name.startswith("_")}


def list_shaders(shaders_available):
    print("Shaders available:")
    for name, _ in shaders_available.items():
        print("    {}".format(name))


def _encode_rgbw_8(rgbw):
    """Encode a sigle rgbw value"""
    return bytes([
        round(rgbw[0] * 255.0),
        round(rgbw[1] * 255.0),
        round(rgbw[2] * 255.0),
        round(rgbw[3] * 255.0),
    ])


def _encode_rgbw_10(rgbw):
    """Encode rgbw value as little endian"""
    return round(rgbw[0] * 1024.0).to_bytes(2, "little") + \
           round(rgbw[1] * 1024.0).to_bytes(2, "little") + \
           round(rgbw[2] * 1024.0).to_bytes(2, "little") + \
           round(rgbw[3] * 1024.0).to_bytes(2, "little")


def _encode_rgbw_16(rgbw):
    """Encode rgbw value as little endian"""
    return round(rgbw[0] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[1] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[2] * 65535.0).to_bytes(2, "little") + \
           round(rgbw[3] * 65535.0).to_bytes(2, "little")


def _encode_rgbw(rgbw, channel_bits=10):
    """
    Encode rgbw data
    """
    if channel_bits == 16:
        return _encode_rgbw_16(rgbw)
    if channel_bits == 10:
        return _encode_rgbw_10(rgbw)
    elif channel_bits == 8:
        return _encode_rgbw_8(rgbw)

    raise RuntimeError("Invalid bits per channel.")


def encode_frame(rgbw_data, channel_bits=10):
    """
    Make frame from rgbw data

    :param rgbw_data: List of Tuples with rgbw values,
                      where values are 0.0 <= x <= 1.0

    :param channel_bits: Use 10 bits or 8 bits per channel
    """
    frame = bytes()

    for rgbw in rgbw_data:
        frame += _encode_rgbw(rgbw, channel_bits)

    # Pad up frame
    pad = CHANNELS_AVAILABLE - len(rgbw_data)
    frame += pad * _encode_rgbw((0, 0, 0, 0), channel_bits)

    return frame


def update(conn, frame):
    """
    Send frame via serial

    A frame of rgbw data
    """
    conn.write(frame)
    time.sleep(20e-6)


def render_loop(conn, shader):
    """
    Rendering loop for a shader
    """
    t0 = time.time()

    while True:
        t = time.time() - t0
        # Make shader state
        for i in range(0, CHANNELS_AVAILABLE):
            s = state.ShaderState(t=t,
                                  u=0,
                                  v=i,
                                  h_res=1,
                                  v_res=CHANNELS_ACTIVE)

            # Map channel
            channel = CHANNEL_MAPPING[i]

            # Draw strip
            rgbw_data = shader(s)
            frame = bytes([0x23, channel]) + _encode_rgbw(rgbw_data, 16)

            update(conn, frame)

        time.sleep(1.0/100.0)


def main(args):
    shaders_available = get_shaders()
    shader = shaders_available.get(args.shader)
    if not shader:
        list_shaders(shaders_available)
        return

    conn = serial.Serial(args.serial_port, args.baudrate)
    render_loop(conn, shader)



if __name__ == "__main__":
    args = parse_args()
    main(args)


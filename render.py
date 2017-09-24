
"""
Initial implementation in python
"""

import time

import serial

SERIAL_PORT="/dev/ttyUSB1"
SERIAL_BAUD=1000000


CHANNELS_ACTIVE=13
CHANNELS_AVAILABLE=16



def _int_to_big_endian(n):
    """Encode n as big endian"""


def _encode_rgbw_8(rgbw):
    """Encode a sigle rgbw value"""
    return bytes([
        round(rgbw[0] * 255.0),
        round(rgbw[1] * 255.0),
        round(rgbw[2] * 255.0),
        round(rgbw[3] * 255.0),
    ])


def _encode_rgbw_10(rgbw):
    """Encode rgbw value as big endian"""
    return round(rgbw[0] * 1024.0).to_bytes(2, "big") + \
           round(rgbw[1] * 1024.0).to_bytes(2, "big") + \
           round(rgbw[2] * 1024.0).to_bytes(2, "big") + \
           round(rgbw[3] * 1024.0).to_bytes(2, "big")


def _encode_rgbw_16(rgbw):
    """Encode rgbw value as big endian"""
    return round(rgbw[0] * 65535.0).to_bytes(2, "big") + \
           round(rgbw[1] * 65535.0).to_bytes(2, "big") + \
           round(rgbw[2] * 65535.0).to_bytes(2, "big") + \
           round(rgbw[3] * 65535.0).to_bytes(2, "big")


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
        rgbw_data = [shader(i, t)
                     for i in range(0, CHANNELS_ACTIVE)]

        frame = encode_frame(rgbw_data)
        update(conn, frame)

        time.sleep(1.0/60.0)


def smooth_colors(i, t):

    r = 0.5 + 0.5 * math.sin(t * 0.5 + i * math.pi/4)
    g = 0.5 + 0.5 * math.sin(t * 0.5 + i * math.pi/3)
    b = 0.5 + 0.5 * math.sin(t * 0.5 + i * math.pi/2)
    w = 0.5 + 0.5 * math.sin(t * 0.5 + i * math.pi/1)

    return (r, g, b, w)


def main():
    conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD)

    render_loop(conn, smooth_colors)



if __name__ == "__main__":
    main()



from treppe import protocol


def test_decode_frame_rgb8():

    rgb8_payload = b"\xff\x7f\x00" * protocol.CHANNELS_AVAILABLE
    rgbw_data = protocol.decode_frame_rgb8(rgb8_payload)

    rgbw = rgbw_data[0]
    assert rgbw[0] == 1.0
    assert round(rgbw[1], 1) == 0.5
    assert rgbw[2] == 0.0
    assert rgbw[3] == 0.0


def test_decode_frame_rgbw8():

    rgb8_payload = b"\xff\x7f\x00\xff" * protocol.CHANNELS_AVAILABLE
    rgbw_data = protocol.decode_frame_rgbw8(rgb8_payload)

    rgbw = rgbw_data[0]

    assert rgbw[0] == 1.0
    assert round(rgbw[1], 1) == 0.5
    assert rgbw[2] == 0.0
    assert rgbw[3] == 1.0


def test_encode_frame_rgb8():
    frame = [(1.0, 0.5, 0.0) for _ in range(0, 3)]
    encoded = protocol.encode_frame_rgb8(frame)

    assert encoded[0] == 0xff
    assert encoded[1] == 0x7f
    assert encoded[2] == 0x00

    assert len(encoded) == protocol.CHANNELS_AVAILABLE * 3


def test_encode_frame_rgbw8():
    frame = [(1.0, 0.5, 0.0, 0.5) for _ in range(0, 3)]
    encoded = protocol.encode_frame_rgbw8(frame)

    assert encoded[0] == 0xff
    assert encoded[1] == 0x7f
    assert encoded[2] == 0x00
    assert encoded[3] == 0x7f

    assert len(encoded) == protocol.CHANNELS_AVAILABLE * 4


def test_encode_frame_rgb16():
    frame = [(1.0, 0.5, 0.0) for _ in range(0, 3)]
    encoded = protocol.encode_frame_rgb16(frame)

    assert len(encoded) == protocol.CHANNELS_AVAILABLE * 6 # RRGGBB


def test_encode_frame_rgbw16():
    frame = [(1.0, 0.5, 0.0, 0.5) for _ in range(0, 3)]
    encoded = protocol.encode_frame_rgbw16(frame)

    assert len(encoded) == protocol.CHANNELS_AVAILABLE * 8 # RRGGBBWW



def test_encode_decode_frame_rgb8():
    frame = [(1.0, 0.5, 0.0) for _ in range(0, 3)]

    encoded = protocol.encode_frame_rgb8(frame)
    decoded = protocol.decode_frame_rgb8(encoded)

    assert len(decoded) == protocol.CHANNELS_AVAILABLE

    assert decoded[0][0] == 1.0
    assert round(decoded[0][1], 1) == 0.5

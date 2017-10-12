
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

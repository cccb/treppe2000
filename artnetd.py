import time
import sys
import socket

sys.path.insert(0, './python_artnet/')

from python_artnet import Artnet


ARTNET_BIND_IP = "0.0.0.0"
ARTNET_UNIVERSE = 0


TREPPE_HOST = "127.0.0.1"
TREPPE_PORT = 3124 # default priority port

def receive(artnet):
    """Receive RGBW data from ArtNet"""
    buf = artnet.readBuffer()
    if not buf:
        return
    packet = buf[ARTNET_UNIVERSE]
    if not packet.data:
        return

    dmx = packet.data
    if not dmx:
        return
    seq = packet.sequence
    print("Received data: ", seq, end="")
    print(*dmx)
   
    return rgbw16
            

def dmx_rgb_to_rgb_frame(dmx):
    """
    Map the dmx channels in xlight format to the
    treppe RGBW16 format.
    """
    # Map values to 0..1 
    return [float(x) / 255.0 for x in dmx]
    


def main():
    """
    Artnet Receiver for treppe2000
    """
    artnet = Artnet(ARTNET_BIND_IP, DEBUG=True)
    conn = (TREPPE_HOST, TREPPE_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            dmx = receive(artnet)
            if dmx:
                frame = dmx_rgb_to_rgb_frame(dmx)
                cmd = protocol.cmd_frame_rgb8(frame)
                sock.sendto(protocol.encode_frame_rgb8(frame), conn)

            time.sleep(0.1)
        except KeyboardInterrupt:
            break

    artnet.close()


if __name__ == "__main__":
    main()


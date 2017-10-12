#!/usr/bin/env python3

"""
UDP Server for treppe2000
"""

import socket

from treppe import protocol


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


def main():
    sock = _open_socket(2334)

    while 42:
        action = protocol.receive(sock)
        print(action)


if __name__ == "__main__":
    main()


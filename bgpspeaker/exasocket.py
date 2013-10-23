"""
Unix socket to communicate with ExaBGP.

Author: Quentin Loos <contact@quentinloos.be>
"""

import socket

SOCKET = "/tmp/exabgp.sock"


def send(command):
    """
    Send the specified command through the socket.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET)
    sock.sendall(command)

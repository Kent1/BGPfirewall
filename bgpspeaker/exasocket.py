"""
Author: Quentin Loos <contact@quentinloos.be>
"""

import socket

SOCKET = "/tmp/exabgp.sock"

def send(command):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET)
    sock.sendall(command)

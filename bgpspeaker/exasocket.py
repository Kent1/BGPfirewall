"""
Unix socket to communicate with ExaBGP.

Author: Quentin Loos <contact@quentinloos.be>
"""

import socket
import logging
logger = logging.getLogger('bgpspeaker')

SOCKET = '/tmp/exabgp.sock'


def send(command):
    """
    Send the specified command through the socket.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(SOCKET)
        sock.sendall(command)
        sock.close()
        logger.info('bgp command sent')
    except Exception, e:
        print e
        logger.error(e)
        return -1
    return 0

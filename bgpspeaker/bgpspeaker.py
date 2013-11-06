"""
A set of functions to generate commands for ExaBGP and pass them to the socket.

Author: Quentin Loos <contact@quentinloos.be>
"""
# Python import
import logging
logger = logging.getLogger('BGPFirewall')

# My import
import exasocket


def _list_as_string(list):
    """
    Given a list, return a string representation of it

    >>> _list_as_string(['22', '80'])
    [ 22 80 ]
    """
    string = '[ '
    for element in list:
        string += str(element) + ' '
    return string + ']'


def update_flow(match, then, withdraw=False):
    """
    Sends a BGP update containing flow rule with specified params
    to the bgpspeaker.

    :param dict match: dictionnary with match components.
    :param str then: string representing the then action.
    :param bool withdraw: Is the flow should be withdrawn ?
    """
    if withdraw:
        announce = 'withdraw'
    else:
        announce = 'announce'
    announce += ' flow route {\nmatch {\n'

    for key, value in match.items():
        if value:
            if isinstance(value, str) or isinstance(value, unicode):
                announce += '%s %s;\n' % (key, value)
            elif len(value) == 1:
                announce += '%s %s;\n' % (key, value[0])
            else:
                announce += '%s %s;\n' % (key, _list_as_string(value))

    announce += '}\nthen {\n'
    announce += then
    announce += ';\n}\n}\n'

    announce = announce.replace('\n', '\\n')

    logger.info('Send configuration to the socket :\n' + announce)
    return exasocket.send(announce)

"""
Functions generating commands for ExaBGP and pass them to the socket.

Author: Quentin Loos <contact@quentinloos.be>
"""

import exasocket


def list_as_string(list):
    """
    Given a list, return a string representation of it

    >>> list_as_string(['22', '80'])
    [ 22 80 ]
    """
    string = '[ '
    for element in list:
        string += str(element) + ' '
    return string + ']'


def update_flow(route, match, then, withdraw=False):
    """
    Sends a BGP update containing flow rule with specified params
    to the bgpspeaker.

    :param route: dictionnary with route parameters.
    :param match: dictionnary with match components.
    :param then: string representing the then action.
    :param withdraw: Is the flow should be withdrawn ?
    """
    announce = ''
    if withdraw:
        announce = 'withdraw'
    else:
        announce = 'announce'
    announce +=  ' flow route {\n'

    for key, value in route.items():
        if value:
            announce += '%s %s;\n' % (key, value)

    announce += 'match {\n'

    for key, value in match.items():
        if value:
            if isinstance(value, str):
                announce += '%s %s;\n' % (key, value)
            elif len(value) == 1:
                announce += '%s %s;\n' % (key, value[0])
            else:
                announce += '%s %s;\n' % (key, list_as_string(value))

    announce += '}\nthen {\n'
    announce += then
    announce += ';\n}\n}\n'

    print announce
    exasocket.send(announce.replace('\n', '\\n'))

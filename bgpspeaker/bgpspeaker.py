"""
Author: Quentin Loos <contact@quentinloos.be>
"""

import exasocket


def list_as_string(list):
    string = '[ '
    for element in list:
        string += str(element) + ' '
    return string + ']'


def announce_flow(route, match, then):
    """Announce BGP flow rule with param specified in args dictionary."""
    announce = "announce flow route {\n"

    for key, value in route.items():
        if value:
            announce += "%s %s;\n" % (key, value)

    announce += "match {\n"

    for key, value in match.items():
        if value:
            if len(value) == 1:
                announce += "%s %s;\n" % (key, value[0])
            else:
                announce += "%s %s;\n" % (key, list_as_string(value))

    announce += "}\nthen {\n"
    announce += then
    announce += ";\n}\n}\n"

    print announce
    exasocket.send(announce.replace('\n', '\\n'))

"""
Author: Quentin Loos <contact@quentinloos.be>
"""

import exasocket


def announce_flow(args):
    """Announce BGP flow rule with param specified in args dictionary."""
    print args
    announce = "announce flow route {\nmatch {\n"
    if args['source']:
        announce += "source %s;\n" % args['source']
    if args['destination']:
        announce += "destination %s;\n" % args['destination']
    if args['port']:
        announce += "%s;\n" % args['port']
    if args['protocol']:
        announce += "protocol %s;\n" % args['protocol']
    if args['packet-length']:
        announce += "packet-length %s;\n" % args['packet-length']
    if args['dscp']:
        announce += "dscp %s;\n" % args['dscp']
    if args['icmp-type']:
        announce += "icmp-type %s;\n" % args['icmp-type']
    if args['icmp-code']:
        announce += "icmp-code %s;\n" % args['icmp-code']
    if args['tcp-flag']:
        announce += "tcp-flags %s;\n" % args['tcp-flag']
    if args['fragment']:
        announce += "fragment %s;\n" % args['fragment']
    announce += "}\nthen {\ndiscard;\n}\n}\n"""
    print announce
    exasocket.send(announce.replace('\n', '\\n'))

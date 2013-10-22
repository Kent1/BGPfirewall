"""
Flow rule models

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.db import models

import bgpspeaker


class Route(object):

    ACTIVE   = 1
    ERROR    = 2
    EXPIRED  = 3
    PENDING  = 4
    INACTIVE = 5

    STATUS = (
        (ACTIVE, "Active"),
        (ERROR, "Error"),
        (EXPIRED, "Expired"),
        (PENDING, "Pending"),
        (INACTIVE, "Inactive"),
    )


class Then(object):

    TRAFFICRATE    = "rate-limit"
    DISCARD        = "discard"
    SAMPLE         = "action sample"
    TERMINAL       = "action terminal"
    SAMPLETERMINAL = "action sample-terminal"
    REDIRECT       = "redirect"
    TRAFFICMARKING = "mark"

    ACTIONS = (
        (TRAFFICRATE, "Traffic-rate"),
        (DISCARD, "Discard"),
        (SAMPLE, "Sample"),
        (TERMINAL, "Terminal"),
        (SAMPLETERMINAL, "Sample & Terminal"),
        (REDIRECT, "Redirect"),
        (TRAFFICMARKING, "Traffic Marking"),
    )


class Flow(models.Model):

    """This class represents a BGP flow specification (RFC 5575)."""

    name         = models.CharField(max_length=50)
    description  = models.TextField(blank=True, null=True)

    # TODO user

    filed        = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status       = models.IntegerField(choices=Route.STATUS, default=Route.PENDING)
    expires      = models.DateTimeField()

    # Match
    match        = models.OneToOneField("Match")

    # Then
    then         = models.CharField(max_length=30, choices=Then.ACTIONS)
    then_value   = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        bgpspeaker.announce_flow(self.to_dictionary())
        super(Flow, self).save(*args, **kwargs)

    def to_dictionary(self):
        dictionary = {}
        dictionary['name'] = self.name
        dictionary['description'] = self.description
        dictionary.update(self.match.to_dictionary())
        dictionary['then'] = self.get_then_display()
        if(self.then == Then.TRAFFICRATE or
           self.then == Then.REDIRECT or
           self.then == Then.TRAFFICMARKING):
            dictionary['then'] += ' ' + str(self.then_value)
        return dictionary


class Match(models.Model):

    """This class represents the "match" condition of a BGP flow spec."""

    destination = models.CharField("Destination IP Address", max_length=43, blank=True, null=True)
    source      = models.CharField("Source IP Address", max_length=43, blank=True, null=True)

    def to_dictionary(self):
        dictionary = {}
        dictionary['source']        = self.source
        dictionary['destination']   = self.destination
        dictionary['protocol']      = [p.protocol for p in self.protocol_set.all()]
        dictionary['port']          = self.port_set.all()
        dictionary['packet-length'] = self.packetlength_set.all()
        dictionary['dscp']          = self.dscp_set.all()
        dictionary['icmp-type']     = [i.icmp_type for i in self.icmp_set.all()]
        dictionary['icmp-code']     = [i.icmp_code for i in self.icmp_set.all()]
        dictionary['tcp-flag']      = [t.tcp_flag for t in self.tcpflag_set.all()]
        dictionary['fragment']      = [f.fragment for f in self.fragment_set.all()]
        return dictionary


class Protocol(models.Model):

    """Protocol model."""

    PROTOCOLS = (
        (1, "ICMP"),
        (2, "IGMP"),
        (6, "TCP"),
        (8, "EGP"),
        (17, "UDP"),
        (46, "RSVP"),
        (47, "GRE"),
        (50, "ESP"),
        (51, "AH"),
        (58, "ICMPv6"),
        (89, "OSPF"),
        (94, "IPIP"),
        (103, "PIM"),
        (132, "SCTP"),
    )

    flow     = models.ForeignKey(Match)
    protocol = models.IntegerField(choices=PROTOCOLS)

    def __unicode__(self):
        return self.get_protocol_display()


class Port(models.Model):

    """Port model.
    You can specify if it is the source port, the destination port or both.
    """

    SRC  = "source-port"
    DST  = "destination-port"
    BOTH = "port"

    DIRECTION = (
        (SRC, "Source port"),
        (DST, "Destination port"),
        (BOTH, "Source & destination ports"),
    )

    flow        = models.ForeignKey(Match)
    port_number = models.CharField(max_length=50)
    direction   = models.IntegerField(choices=DIRECTION)

    def __unicode__(self):
        return '%s %s' % (self.get_direction_display, self.port_number)


class PacketLength(models.Model):

    flow          = models.ForeignKey(Match)
    packet_length = models.IntegerField(max_length=65536)

    def __unicode__(self):
        return self.packet_length


class DSCP(models.Model):

    flow  = models.ForeignKey(Match)
    dscp  = models.IntegerField("DSCP", max_length=64)

    def __unicode__(self):
        return self.dscp


class ICMP(models.Model):

    """ICMP

    A complete list can be found here : http://www.nthelp.com/icmp.html
    """

    ICMP_TYPES = (
        (0, "Echo reply"),
        (3, "Destination unreacheable"),
        (4, "Source Quench"),
        (5, "Redirect"),
        (8, "Echo Request"),
        (9, "Router Advertisement"),
        (10, "Router Solicitation"),
        (11, "Time Exceeded"),
        (12, "Parameter Problem"),
        (13, "Timestamp Request"),
        (14, "Timestamp Reply"),
        (15, "Information Request"),
        (16, "Information Response"),
        (17, "Address Mask Request"),
        (18, "Address Mask Reply"),
    )

    flow      = models.ForeignKey(Match)
    icmp_type = models.IntegerField("ICMP Type", max_length=255, choices=ICMP_TYPES)
    icmp_code = models.SmallIntegerField("ICMP Code", max_length=255)

    def __unicode__(self):
        if icmp_code:
            return '%s (%s)' % (self.get_icmp_type_display(), self.icmp_code)
        else:
            return '%s' % self.get_icmp_type_display()


class TCPFlag(models.Model):

    """TCP flag like SYN or ACK.

        0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
      +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
      |               |                       | U | A | P | R | S | F |
      | Header Length |        Reserved       | R | C | S | S | Y | I |
      |               |                       | G | K | H | T | N | N |
      +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
    """

    TCP_FLAGS = (
        (1, "FIN"),
        (2, "SYN"),
        (4, "RST"),
        (8, "PUSH"),
        (16, "ACK"),
        (32, "URGENT"),
    )

    flow     = models.ForeignKey(Match)
    tcp_flag = models.SmallIntegerField("TCP Flag", max_length=32, choices=TCP_FLAGS)

    def __unicode__(self):
        return self.get_tcp_flag_display()


class Fragment(models.Model):

    DONTFRAGMENT  = 1
    ISAFRAGMENT   = 2
    FIRSTFRAGMENT = 4
    LASTFRAGMENT  = 8

    FRAGMENTS = (
        (DONTFRAGMENT, "Don't fragment"),
        (ISAFRAGMENT, "Is a fragment"),
        (FIRSTFRAGMENT, "First fragment"),
        (LASTFRAGMENT, "Last fragment"),
    )

    flow     = models.ForeignKey(Match)
    fragment = models.SmallIntegerField(max_length=8, choices=FRAGMENTS)

    def __unicode__(self):
        return self.get_fragment_display()

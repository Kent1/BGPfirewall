"""
Flow rule models

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.db import models
from multiselectfield.models import MultiSelectField

from flow import TCPFlag, Fragment


class Flow(models.Model):

    """This class represents a BGP flow specification (RFC 5575)."""

    ACTIVE   = 1
    ERROR    = 2
    EXPIRED  = 3
    PENDING  = 4
    INACTIVE = 5

    ROUTE_STATUS = (
        (ACTIVE, "Active"),
        (ERROR, "Error"),
        (EXPIRED, "Expired"),
        (PENDING, "Pending"),
        (INACTIVE, "Inactive"),
    )

    name         = models.CharField(max_length=50)
    description  = models.TextField(null=True)

    # TODO user

    filed        = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status       = models.IntegerField(choices=ROUTE_STATUS, default=PENDING)
    expires      = models.DateField()

    match        = models.OneToOneField("Match")
    then         = models.OneToOneField("Then")

    def __unicode__(self):
        return self.name


class Match(models.Model):

    """This class represents the "match" condition of a BGP flow spec."""

    destination = models.CharField("Destination IP Address", max_length=43, blank=True, null=True)
    source      = models.CharField("Source IP Address", max_length=43, blank=True, null=True)

    tcp_flag    = MultiSelectField("TCP flag", max_length=3, choices=TCPFlag.TCP_FLAGS, blank=True, null=True)
    fragment    = MultiSelectField(max_length=250, blank=True, choices=Fragment.FRAGMENTS)

class Then(models.Model):

    """This class represents the "then" action of a BGP flow spec."""

    TRAFFICRATE    = 1
    DISCARD        = 2
    SAMPLE         = 3
    TERMINAL       = 4
    SAMPLETERMINAL = 5
    REDIRECT       = 6
    TRAFFICMARKING = 7

    THEN = (
        (TRAFFICRATE, "Traffic-rate"),
        (DISCARD, "Discard"),
        (SAMPLE, "Sample"),
        (TERMINAL, "Terminal"),
        (SAMPLETERMINAL, "Sample & Terminal"),
        (REDIRECT, "Redirect"),
        (TRAFFICMARKING, "Traffic Marking"),
    )

    action = models.IntegerField(choices=THEN)
    value  = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.get_action_display() + ' ' + str(self.value)


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

    match    = models.ForeignKey(Match)
    protocol = models.IntegerField(choices=PROTOCOLS)

    def __unicode__(self):
        return self.protocol


class Port(models.Model):

    """Port model.
    You can specify if it is the source port, the destination port or both.
    """

    SRC  = 1
    DST  = 2
    BOTH = 3

    DIRECTION = (
        (SRC, "Source port"),
        (DST, "Destination port"),
        (BOTH, "Source & destination ports"),
    )

    match       = models.ForeignKey(Match)
    port_number = models.CharField(max_length=50)
    direction   = models.IntegerField(choices=DIRECTION)

    def __unicode__(self):
        return '%s (%s)' % (self.port_number, self.get_direction_display)


class PacketLength(models.Model):

    match         = models.ForeignKey(Match)
    packet_length = models.IntegerField(max_length=65536)

    def __unicode__(self):
        return self.get_operator_display() + self.get_packet_length_display()


class DSCP(models.Model):

    match = models.ForeignKey(Match)
    dscp  = models.IntegerField(max_length=64)

    def __unicode__(self):
        return self.get_operator_display() + self.get_dscp_display()


class ICMPType(models.Model):

    """ICMP Type

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

    match     = models.ForeignKey(Match)
    icmp_type = models.IntegerField(max_length=255, choices=ICMP_TYPES)

    def __unicode__(self):
        return '%s' % self.get_icmp_type_display()


class ICMPCode(models.Model):

    icmp_type = models.ForeignKey(ICMPType)
    icmp_code = models.SmallIntegerField(max_length=255)

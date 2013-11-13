"""
Flow rule models

Author: Quentin Loos <contact@quentinloos.be>
"""
# Python import
import ipaddr
import datetime
import logging
logger = logging.getLogger('bgpspeaker')

# Django import
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import ValidationError

# My import


class Route(object):

    """Constants used to indicate the status of the flow."""

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

    """Choices set of then action."""

    ACCEPT         = "accept"
    TRAFFICRATE    = "rate-limit"
    DISCARD        = "discard"
    SAMPLE         = "action sample"
    TERMINAL       = "action terminal"
    SAMPLETERMINAL = "action sample-terminal"
    REDIRECT       = "redirect"
    TRAFFICMARKING = "mark"

    ACTIONS = (
        (ACCEPT, "Accept"),
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

    name         = models.CharField(max_length=50, unique=True)
    description  = models.TextField(blank=True, null=True)

    filed        = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status       = models.IntegerField(choices=Route.STATUS,
                                       default=Route.INACTIVE)
    active       = models.BooleanField(default=False)
    expires      = models.DateTimeField(
                    default=timezone.now() + datetime.timedelta(days=1))

    # Match
    destination = models.CharField(
        "Destination IP Address",max_length=43, blank=True, null=True)
    source      = models.CharField(
        "Source IP Address",  max_length=43, blank=True, null=True)

    # Then
    then_action  = models.CharField(max_length=30, choices=Then.ACTIONS,
                                    default=Then.ACCEPT)
    then_value   = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def match(self):
        """Return a dictionary including match components."""
        match = {}
        match['source']           = self.source
        match['destination']      = self.destination
        match['protocol']         = [p.protocol for p in self.protocol_set.all()]
        match['port']             = [p.port_number for p in self.port_set.all().filter(direction=Port.BOTH)]
        match['source-port']      = [p.port_number for p in self.port_set.all().filter(direction=Port.SRC)]
        match['destination-port'] = [p.port_number for p in self.port_set.all().filter(direction=Port.DST)]
        match['packet-length']    = [p.packet_length for p in self.packetlength_set.all()]
        match['dscp']             = [d.dscp for d in self.dscp_set.all()]
        match['icmp-type']        = [i.icmp_type for i in self.icmp_set.all()]
        match['icmp-code']        = [i.icmp_code for i in self.icmp_set.all()]
        match['tcp-flags']        = [t.tcp_flag for t in self.tcpflag_set.all()]
        match['fragment']         = [f.fragment for f in self.fragment_set.all()]
        return match

    def then(self):
        """Return a string with then_action and then_value."""
        result = self.then_action
        if self.then_value:
            result += ' ' + str(self.then_value)
        return result

    def has_expired(self):
        """Return True if the flow has expired."""
        if self.expires < timezone.now():
            return True
        return False


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

    flow     = models.ForeignKey(Flow)
    protocol = models.IntegerField(choices=PROTOCOLS)

    def __unicode__(self):
        return self.get_protocol_display()


class Port(models.Model):

    """Port model.
    You can specify for a port number if it is the source port,
    the destination port or both.
    """

    SRC  = "source-port"
    DST  = "destination-port"
    BOTH = "port"

    DIRECTION = (
        (SRC, "Source port"),
        (DST, "Destination port"),
        (BOTH, "Source & destination ports"),
    )

    flow        = models.ForeignKey(Flow)
    port_number = models.CharField(max_length=50)
    direction   = models.CharField(max_length=50,
                                   choices=DIRECTION, default=BOTH)

    def __unicode__(self):
        return '%s' % self.port_number


class PacketLength(models.Model):

    """Packet length model."""

    flow          = models.ForeignKey(Flow)
    packet_length = models.CharField(max_length=65536)

    def __unicode__(self):
        return '%s' % self.packet_length


class DSCP(models.Model):

    """DSCP model."""

    flow  = models.ForeignKey(Flow)
    dscp  = models.CharField("DSCP", max_length=64)

    def __unicode__(self):
        return '%s' % self.dscp


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

    flow      = models.ForeignKey(Flow)
    icmp_type = models.IntegerField("ICMP Type",
                                    max_length=255, choices=ICMP_TYPES)
    icmp_code = models.SmallIntegerField("ICMP Code", max_length=255)

    def __unicode__(self):
        if self.icmp_code:
            return '%s (%s)' % (self.get_icmp_type_display(), self.icmp_code)
        else:
            return '%s' % self.get_icmp_type_display()


class TCPFlag(models.Model):

    """TCP flag like SYN or ACK."""

    TCP_FLAGS = (
        (1, "FIN"),
        (2, "SYN"),
        (4, "RST"),
        (8, "PUSH"),
        (16, "ACK"),
        (32, "URGENT"),
    )

    flow     = models.ForeignKey(Flow)
    tcp_flag = models.SmallIntegerField("TCP Flag",
                                        max_length=32, choices=TCP_FLAGS)

    def __unicode__(self):
        return self.get_tcp_flag_display()


class Fragment(models.Model):

    """Fragment type model."""

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

    flow     = models.ForeignKey(Flow)
    fragment = models.SmallIntegerField(max_length=8, choices=FRAGMENTS)

    def __unicode__(self):
        return self.get_fragment_display()

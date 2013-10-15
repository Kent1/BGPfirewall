"""
Flow rule models

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.db import models
from multiselectfield.models import MultiSelectField

FRAGMENTS = (
    (1, "Don't fragment"),
    (2, "Is a fragment"),
    (4, "First fragment"),
    (8, "Last fragment"),
)


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

    # TODO Add a correct field or model for IP prefix.
    destination   = models.CharField("Destination IP Address", max_length=43)
    source        = models.CharField("Source IP Address", max_length=43)
    protocol      = models.ManyToManyField("Protocol", blank=True, null=True)
    port          = models.ManyToManyField("Port", blank=True, null=True, related_name="port")
    dest_port     = models.ManyToManyField("Port", blank=True, null=True, related_name="destport")
    src_port      = models.ManyToManyField("Port", blank=True, null=True, related_name="srcport")
    icmp_type     = models.ManyToManyField("ICMPType", blank=True, null=True, verbose_name="ICMP Type")
    icmp_code     = models.ManyToManyField("ICMPCode", blank=True, null=True, verbose_name="ICMP Code")
    # TODO Use OpBitmask like the RFC for TCP flag and DSCP
    tcp_flag      = models.ManyToManyField("TCPFlag", blank=True, null=True, verbose_name="TCP flag")
    packet_length = models.ManyToManyField("PacketLength", blank=True, null=True)
    dscp          = models.ManyToManyField("DSCP", blank=True, null=True, verbose_name="DSCP")
    #fragment      = models.ManyToManyField("Fragment", blank=True, null=True)
    fragment      = MultiSelectField(max_length=250, blank=True, choices=FRAGMENTS)

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
    value  = models.IntegerField()

class OpValue(models.Model):

    """Abstract class for modeling an octet operator or value like defined
    in RFC 5575.

      0   1   2   3   4   5   6   7
    +---+---+---+---+---+---+---+---+
    | e | a |  len  | 0 |lt |gt |eq |
    +---+---+---+---+---+---+---+---+
    """

    EQ = 1
    LT = 2
    GT = 3
    LE = 4
    GE = 5

    OPERATORS = (
        (EQ, "="),
        (LT, "<"),
        (GT, ">"),
        (LE, "<="),
        (GE, ">="),
    )

    operator = models.IntegerField(choices=OPERATORS)

    class Meta:
        abstract = True


class Protocol(OpValue):

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

    protocol = models.IntegerField(choices=PROTOCOLS)

    def __unicode__(self):
        return self.get_operator_display() + self.get_protocol_display()


class Port(OpValue):

    port_number = models.IntegerField(max_length=65536)

    def __unicode__(self):
        return self.get_operator_display() + self.get_port_number_display()


class PacketLength(OpValue):

    packet_length = models.IntegerField(max_length=65536)

    def __unicode__(self):
        return self.get_operator_display() + self.get_packet_length_display()


class DSCP(OpValue):

    dscp = models.IntegerField(max_length=64)

    def __unicode__(self):
        return self.get_operator_display() + self.get_dscp_display()


class ICMPType(OpValue):

    """ICMP type class inherits from OpValue.

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

    icmp_type = models.IntegerField(max_length=255, choices=ICMP_TYPES)

    def __unicode__(self):
        return self.get_operator_display() + self.get_icmp_type_display()


class ICMPCode(OpValue):

    """ICMP code class inherits from OpValue.

    A complete list can be found here : http://www.nthelp.com/icmp.html
    """

    icmp_code = models.SmallIntegerField(max_length=255)

    def __unicode__(self):
        return self.get_operator_display() + self.get_icmp_code_display()


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

    tcp_flag = models.SmallIntegerField(max_length=32, choices=TCP_FLAGS)

    def __unicode__(self):
        return self.get_tcp_flag_display()


class Fragment(models.Model):

    FRAGMENTS = (
        (1, "Don't fragment"),
        (2, "Is a fragment"),
        (4, "First fragment"),
        (8, "Last fragment"),
    )

    fragment = models.SmallIntegerField(max_length=8, choices=FRAGMENTS)

    def __unicode__(self):
        return self.get_fragment_display()

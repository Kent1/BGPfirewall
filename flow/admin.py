from django.contrib import admin
from flow.models import *


class ProtocolInLine(admin.StackedInline):
    model = Protocol
    extra = 1


class PortInLine(admin.StackedInline):
    model = Port
    extra = 1


class PacketLengthInLine(admin.StackedInline):
    model = PacketLength
    extra = 1


class DSCPInLine(admin.StackedInline):
    model = DSCP
    extra = 1


class ICMPInLine(admin.StackedInline):
    model = ICMP
    extra = 1


class TCPFlagInLine(admin.StackedInline):
    model = TCPFlag
    extra = 1


class FragmentInLine(admin.StackedInline):
    model = Fragment
    extra = 1


class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        ('IP addresses', {'fields': ['destination', 'source']}),
    ]
    inlines = [ProtocolInLine, PortInLine, PacketLengthInLine, DSCPInLine, ICMPInLine, TCPFlagInLine, FragmentInLine]


class FlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status')
    fieldsets = [
        ('Route',  {'fields': ['name', 'description', 'expires']}),
        ('Match',  {'fields': ['match']}),
        ('Then',   {'fields': ['then', 'then_value']}),
    ]

admin.site.register(Flow, FlowAdmin)
admin.site.register(Match, MatchAdmin)

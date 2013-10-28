from django.contrib import admin
from flow.models import *


class ProtocolInline(admin.StackedInline):

    model = Protocol
    extra = 1


class PortInline(admin.StackedInline):

    model = Port
    extra = 1


class PacketLengthInline(admin.StackedInline):

    model = PacketLength
    extra = 1


class DSCPInline(admin.StackedInline):

    model = DSCP
    extra = 1


class ICMPInline(admin.StackedInline):

    model = ICMP
    extra = 1


class TCPFlagInline(admin.StackedInline):

    model = TCPFlag
    extra = 1


class FragmentInline(admin.StackedInline):

    model = Fragment
    extra = 1

class FlowAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'status')
    fieldsets = [
        ('Route',  {'fields': ['name', 'description', 'expires', 'active']}),
        ('Match',  {'fields': ['source', 'destination']}),
        ('Then',   {'fields': ['then', 'then_value']}),
    ]
    inlines = [ProtocolInline, PortInline, PacketLengthInline, DSCPInline, ICMPInline, TCPFlagInline, FragmentInline]

admin.site.register(Flow, FlowAdmin)

# Python import
import celery
import logging
logger = logging.getLogger('BGPFirewall')

# Django import
from django.contrib import admin

# My import
from flow.models import *
from flow.forms import FlowForm
from flow import tasks
from flow import signals


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

    form = FlowForm
    list_display = ('name', 'description', 'status')
    fieldsets = [
        ('Route',
            {
                'description': '',
                'fields': ['name', 'description', 'expires', 'active']
            }
        ),
        ('Then',
            {
                'description': '',
                'fields': [('then_action', 'then_value')]
            }
        ),
        ('Match',
            {
                'description': '',
                'fields': ['source', 'destination']
            }
        ),
    ]
    inlines = [ProtocolInline, PortInline, PacketLengthInline, DSCPInline, ICMPInline, TCPFlagInline, FragmentInline]

    # def save_model(self, request, obj, form, change):
    #     super(FlowAdmin, self).save_model(request, obj, form, change)

    # def delete_model(self, request, obj):
    #     super(FlowAdmin, self).delete_model(request, obj)

admin.site.register(Flow, FlowAdmin)

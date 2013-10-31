from django.contrib import admin
from flow.models import *
from flow.forms import FlowForm
from flow import tasks
import logging
logger = logging.getLogger('BGPFirewall')


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
                'fields': [('then', 'then_value')]
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

    def save_model(self, request, obj, form, change):
        obj.save()
        then = obj.then
        if obj.then_value:
            then +=' ' + obj.then_value
        if obj.active:
            if obj.status == Route.INACTIVE or obj.status == Route.ERROR:
                # If we want to active the flow
                obj.status = Route.PENDING
                obj.save(update_fields=['status'])
                logger.info('Announce flow ' + obj.name)
                tasks.announce.apply_async((obj, obj.match(), then), countdown=3)
        else:
            if obj.status == Route.ACTIVE or obj.status == Route.ERROR:
                # If we want to desactive the flow
                obj.status = Route.PENDING
                obj.save(update_fields=['status'])
                logger.info('Withdraw flow ' + obj.name)
                tasks.withdraw.apply_async((obj, obj.match(), then), countdown=3)

    def delete_model(self, request, obj):
        if obj.active:
            tasks.withdraw.apply_async((obj, obj.match(), then), countdown=3)
        obj.save()

admin.site.register(Flow, FlowAdmin)

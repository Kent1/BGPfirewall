from django.contrib import admin
from flow.models import *
from flow.forms import FlowForm
from flow import tasks
import logging
logger = logging.getLogger('BGPFirewall')
import celery


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

    def save_model(self, request, obj, form, change):

        if change:
            oldflow = Flow.objects.get(pk=obj.pk)
        super(FlowAdmin, self).save_model(request, obj, form, change)

        if change:
            # Modify existing flow
            if obj.status in (Route.ACTIVE,):
                # The flow was activated
                if obj.active:
                    # Modify it
                    tasks.modify(oldflow, obj)
                    obj.status = Route.PENDING
                else:
                    # Withdraw it
                    tasks.withdraw.delay(oldflow, oldflow.match(), oldflow.then())
                    obj.status = Route.PENDING
            elif obj.status in (Route.INACTIVE,):
                # If the flow was not activated
                if obj.active:
                    # And we want to activate it
                    tasks.announce.delay(obj, obj.match(), obj.then())
                    obj.status = Route.PENDING

        else:
            # Create new flow
            if obj.active:
                # Announce it
                tasks.announce.delay(obj, obj.match(), obj.then())
                obj.status = Route.PENDING

        # Add withdraw task.

    def delete_model(self, request, obj):
        if obj.status != Route.INACTIVE:
            tasks.withdraw.delay(obj, obj.match(), obj.then())
        super(FlowAdmin, self).delete_model(request, obj)

admin.site.register(Flow, FlowAdmin)

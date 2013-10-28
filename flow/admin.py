from django.contrib import admin
from flow.models import *
from flow.forms import FlowForm, MatchForm


class FlowAdmin(admin.ModelAdmin):
    form = FlowForm
    list_display = ('name', 'description', 'status')
    fieldsets = [
        ('Route',  {'fields': ['name', 'description', 'expires', 'active']}),
        ('Match',  {'fields': ['source', 'destination', 'protocol', ('port_number', 'direction')]}),
        ('Advanced Match', {'classes': ['collapse'], 'fields' : ['packet_length', 'dscp', ('icmp_type', 'icmp_code'), 'tcp_flag', 'fragment']}),
        ('Then',   {'fields': ['then', 'then_value']}),
    ]

admin.site.register(Flow, FlowAdmin)

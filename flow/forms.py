"""
Forms of Flows

Author: Quentin Loos <contact@quentinloos.be>
"""
import ipaddr
from django import forms
from flow.models import Then

from flow.models import *


class FlowForm(forms.ModelForm):

    class Meta:
        model = Flow

    # TODO in django 1.6, the labels, help_texts and error_messages options were added to Meta.
    Flow._meta.get_field('source').help_text = u'The source address can be a network, e.g. 10.2.14.0/24'
    Flow._meta.get_field('destination').help_text = u'The destination address can be a network, e.g. 10.2.14.0/24'
    Port._meta.get_field('port_number').help_text = u'The port number can be an expression, like (12 & >23)'
    PacketLength._meta.get_field('packet_length').help_text = u'The packet length can be an expression, like (12 & >23)'
    DSCP._meta.get_field('dscp').help_text = u'The DSCP can be an expression, like (12 & >23)'
    ICMP._meta.get_field('icmp_code').help_text = u'The icmp code is an integer'


    def clean_source(self):
        if self.cleaned_data['source']:
            try:
                address = ipaddr.IPNetwork(self.cleaned_data['source'])
            except ValueError:
                raise forms.ValidationError(
                    'Invalid network address format for source component')
            return str(address)

    def clean_destination(self):
        if self.cleaned_data['destination']:
            try:
                address = ipaddr.IPNetwork(self.cleaned_data['destination'])
            except ValueError:
                raise forms.ValidationError(
                    'Invalid network address format for destination component')
            return str(address)

    def clean(self):
        cleaned_data = super(FlowForm, self).clean()
        then = cleaned_data.get("then")

        if then:
            if(then == Then.TRAFFICRATE or then == Then.REDIRECT or
               then == Then.TRAFFICMARKING):
                if(not cleaned_data['then_value']):
                    raise forms.ValidationError('A value is required')
            else:
                cleaned_data['then_value'] == ''
        return cleaned_data

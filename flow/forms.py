"""
Forms of Flows

Author: Quentin Loos <contact@quentinloos.be>
"""
from django import forms
from django.contrib.admin import widgets
from django.forms.models import inlineformset_factory

from models import *


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol


class PortForm(forms.ModelForm):

    class Meta:
        model = Port


class PacketLengthForm(forms.ModelForm):

    class Meta:
        model = PacketLength


class DSCPForm(forms.ModelForm):

    class Meta:
        model = DSCP


class ICMPForm(forms.ModelForm):

    class Meta:
        model = ICMP


class TCPFlagForm(forms.ModelForm):

    class Meta:
        model = TCPFlag


class FragmentForm(forms.ModelForm):

    class Meta:
        model = Fragment


class MatchForm(forms.ModelForm):

    class Meta:
        model = Match


class FlowForm(forms.ModelForm):

    match         = MatchForm()
    source        = match.fields['source']
    destination   = match.fields['destination']
    protocol      = ProtocolForm().fields['protocol']
    port          = PortForm()
    port_number   = port.fields['port_number']
    direction     = port.fields['direction']
    packet_length = PacketLengthForm().fields['packet_length']
    dscp          = DSCPForm().fields['dscp']
    icmp          = ICMPForm()
    icmp_type     = icmp.fields['icmp_type']
    icmp_code     = icmp.fields['icmp_code']
    tcp_flag      = TCPFlagForm().fields['tcp_flag']
    fragment      = FragmentForm().fields['fragment']

    class Meta:
        model = Flow
        fields = [
            'name',
            'description',
            'expires',
            'source',
            'destination',
            'protocol',
            'port_number',
            'direction',
            'packet_length',
            'dscp',
            'icmp_type',
            'icmp_code',
            'tcp_flag',
            'fragment',
            'then',
            'then_value'
        ]

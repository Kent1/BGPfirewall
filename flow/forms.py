"""
Forms of Flows

Author: Quentin Loos <contact@quentinloos.be>
"""
import ipaddr
from django import forms

from flow.models import Flow


class FlowForm(forms.ModelForm):

    class Meta:
        model = Flow

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

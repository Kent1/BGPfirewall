"""
Forms of Neighbor

Author: Quentin Loos <contact@quentinloos.be>
"""
from django import forms

from models import Neighbor


class NeighborForm(forms.ModelForm):

    class Meta:
        model   = Neighbor
        exclude = ('enable')

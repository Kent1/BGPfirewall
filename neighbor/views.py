"""
Views for neighbor

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from neighbor.models import Neighbor
from neighbor.forms import NeighborForm


class ListView(generic.ListView):

    """
    list all current neighbors.
    Template: neighbor_list.html
    """
    model               = Neighbor
    context_object_name = 'neighbors'

    def get_queryset(self):
        """Return all configured neighbors."""
        return Neighbor.objects.all()


class DetailView(generic.DetailView):

    """
    Detailled view of a given neighbor.
    Template: neighbor_detail.html
    """
    model               = Neighbor
    context_object_name = 'neighbor'


class CreateView(generic.CreateView):

    """
    Neighbor creating view.
    Template: neighbor_form.html
    """
    model       = Neighbor
    form_class  = NeighborForm
    success_url = reverse_lazy('neighbor_list')

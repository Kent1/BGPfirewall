from django.shortcuts import render, get_object_or_404
from django.views import generic

from neighbor.models import Neighbor

class ListView(generic.ListView):
    """Index view."""
    context_object_name = 'neighbors'

    def get_queryset(self):
        """Return all configured neighbors."""
        return Neighbor.objects.all()

class DetailView(generic.DetailView):
    """Detailled view of a given neighbor."""
    model = Neighbor

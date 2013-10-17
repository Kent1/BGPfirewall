"""
Views for flows

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.views import generic

from flow.models import Flow


class ListView(generic.ListView):

    """
    Index view.
    Template: flow_detail.html
    """
    model               = Flow
    context_object_name = 'flows'

    def get_queryset(self):
        """Return all configured flows."""
        return Flow.objects.all()


class DetailView(generic.DetailView):

    """
    Detailled view of a given flow.
    Template: flow_list.html
    """
    model               = Flow
    context_object_name = 'flow'

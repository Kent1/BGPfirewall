"""
Views for flows

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from flow.models import Flow
from flow.forms import FlowForm


class ListView(generic.ListView):

    """
    List all current flows.
    Template: flow_list.html
    """
    model               = Flow
    context_object_name = 'flows'

    def get_queryset(self):
        """Return all configured flows."""
        return Flow.objects.all()


class DetailView(generic.DetailView):

    """
    Detailled view of a given flow.
    Template: flow_detail.html
    """
    model               = Flow
    context_object_name = 'flow'


class CreateView(generic.CreateView):

    """
    Flow creating view.
    Template: flow_form.html
    """
    model       = Flow
    form_class  = FlowForm
    success_url = reverse_lazy('flow_list')

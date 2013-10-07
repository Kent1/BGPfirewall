from django.shortcuts import render, get_object_or_404

from neighbor.models import Neighbor

def index(request):
    """Index view of neighbor.
    This view display a list of all configured neighbor.
    """

    neighbors = Neighbor.objects.all()
    context = {
        'neighbors': neighbors,
    }
    return render(request, 'neighbor/index.html', context)

def detail(request, neighbor_id):
    """Detail view of a neighbor."""
    neighbor = get_object_or_404(Neighbor, pk=neighbor_id)
    return render(request, 'neighbor/detail.html', {'neighbor': neighbor})
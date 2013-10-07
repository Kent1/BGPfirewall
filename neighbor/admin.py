from django.contrib import admin
from neighbor.models import Neighbor

class NeighborAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'enable')

admin.site.register(Neighbor, NeighborAdmin)

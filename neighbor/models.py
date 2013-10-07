from django.db import models


class Neighbor(models.Model):

    """This class represents a neighbor in BGP.
    It inherits from Neighbor of ExaBGP.
    """

    name          = models.CharField(max_length=50)
    description   = models.CharField(max_length=500, blank=True)

    # IP Addresses
    router_id     = models.GenericIPAddressField()
    local_address = models.GenericIPAddressField()
    peer_address  = models.GenericIPAddressField()

    passive       = models.BooleanField(default=False)

    # AS numbers
    peer_as       = models.PositiveIntegerField()
    local_as      = models.PositiveIntegerField()

    enable        = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

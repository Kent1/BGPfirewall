from django.db import models


class Neighbor(models.Model):

    """This class represents a neighbor in BGP.
    It inherits from Neighbor of ExaBGP.
    """

    name          = models.CharField(max_length=50)
    description   = models.CharField(max_length=500, blank=True)

    # IP Addresses
    router_id     = models.CharField(max_length=150)
    local_address = models.CharField(max_length=150)
    peer_address  = models.CharField(max_length=150)

    passive       = models.BooleanField(default=False)

    # AS numbers
    peer_as       = models.IntegerField()
    local_as      = models.IntegerField()

    enable        = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

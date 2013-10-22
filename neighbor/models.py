"""
Neighbor models

Author: Quentin Loos <contact@quentinloos.be>
"""
from django.db import models


class Neighbor(models.Model):

    """This class represents a neighbor in BGP."""

    name          = models.CharField(max_length=50)
    description   = models.TextField(blank=True, null=True)

    # IP Addresses
    router_id     = models.GenericIPAddressField('Router ID')
    local_address = models.GenericIPAddressField('Local IP address')
    peer_address  = models.GenericIPAddressField('Peer IP address')

    passive       = models.BooleanField(default=False)

    # AS numbers
    peer_as       = models.PositiveIntegerField('Peer AS number')
    local_as      = models.PositiveIntegerField('Local AS number')

    enable        = models.BooleanField(default=False)

    def connect(self):
        """Enable BGP connection with the neighbor. Add neighbor to ExaBGP."""
        self.enable = True

    def disconnect(self):
        """Disconnect the neighbor."""
        self.enable = False

    def enable_changed(self):
        """Return True if enable has changed."""
        if self.pk is not None:
            orig = Neighbor.objects.get(pk=self.pk)
            if orig.enable != self.enable:
                # If enable has changed
                return True
        return False

    def save(self, *args, **kwargs):
        if self.enable_changed():
            if self.enable:
                # Try to connect with the neighbor
                self.connect()
            else:
                self.disconnect()
        super(Neighbor, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if not self.enable:
            # Try to disconnect with the neighbor
            pass
        super(Neighbor, self).delete(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Neighbor"
        verbose_name_plural = "Neighbors"

"""
Signal functions.

Author: Quentin Loos <contact@quentinloos.be>
"""
# Django import
from django.utils import timezone
from django.db.models import signals
from django.dispatch import receiver

# My import
from flow.models import Flow, Route
from flow import tasks


@receiver(signals.pre_save, sender=Flow)
def presave(sender, instance, **kwargs):
    """This function is called before a flow is saved.
    It withdraws flow if a flow already existing before and was active.
    """
    instance.status = Route.PENDING

    if not instance.pk:
        return

    # Existing flow
    oldflow = Flow.objects.get(pk=instance.pk)

    # Modify existing flow
    if oldflow.status in (Route.ACTIVE,):
        # The flow was active
        # Withdraw it
        tasks.withdraw.delay(oldflow, oldflow.match(), oldflow.then())


@receiver(signals.post_save, sender=Flow)
def postsave(sender, instance, created, **kwargs):
    """This function is called after a flow is saved.
    It announces the flow if it is active and schedules
    expire task at the expire datetime.
    """
    # Create new flow
    if instance.active:
        # Announce it
        tasks.announce.delay(instance)

        # Add withdraw task.
        tasks.expire.apply_async((instance,),
            countdown=(instance.expires - timezone.now()).total_seconds())


@receiver(signals.pre_delete, sender=Flow)
def predelete(sender, instance, **kwargs):
    """This function is called before a flow is deleted.
    It withdraw the flow if it was active.
    """
    # Existing flow
    oldflow = Flow.objects.get(pk=instance.pk)

    if instance.status != Route.INACTIVE:
        tasks.delete.delay(oldflow, oldflow.match(), oldflow.then())

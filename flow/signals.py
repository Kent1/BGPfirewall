# Django import
from django.db.models import signals
from django.dispatch import receiver

# My import
from flow.models import Flow, Route
from flow import tasks


@receiver(signals.pre_save, sender=Flow)
def presave(sender, instance, **kwargs):
    instance.status = Route.PENDING

    if not instance.pk:
        return

    # Existing flow
    oldflow = Flow.objects.get(pk=instance.pk)

    # Modify existing flow
    if oldflow.status  in (Route.ACTIVE,):
        # The flow was activated
        # Withdraw it
        tasks.withdraw.delay(oldflow, oldflow.match(), oldflow.then())

@receiver(signals.post_save, sender=Flow)
def postsave(sender, instance, created, **kwargs):
    # Create new flow
    if instance.active:
        # Announce it
        tasks.announce.delay(instance)

    # Add withdraw task.

@receiver(signals.pre_delete, sender=Flow)
def postdelete(sender, instance, **kwargs):
    # Existing flow
    oldflow = Flow.objects.get(pk=instance.pk)

    if instance.status != Route.INACTIVE:
        tasks.delete.delay(oldflow, oldflow.match(), oldflow.then())

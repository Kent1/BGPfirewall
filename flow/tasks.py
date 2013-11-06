# Python import
from celery import task
from celery.utils.log import get_task_logger
from celery import chain
import logging
logger = logging.getLogger('BGPFirewall')

# Django import
from flow.models import Route

# My import
import bgpspeaker


@task(max_retries=3)
def announce(flow):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends announce route command via a socket.
    Update status of the flow to ACTIVE if there are no error
    """
    try:
        bgpspeaker.update_flow(flow.match(), flow.then())
        flow.status = Route.ACTIVE
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        raise announce.retry(exc=e, countdown=10)
    finally:
        flow.save(update_fields=['status'])

@task(max_retries=3)
def withdraw(flow, match, then):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends withdraw route command via a socket.
    """
    try:
        bgpspeaker.update_flow(match, then, withdraw=True)
        flow.status = Route.INACTIVE
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        raise announce.retry(exc=e, countdown=10)
    finally:
        flow.save(update_fields=['status'])

@task(max_retries=3)
def delete(flow, match, then):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends withdraw route command via a socket.
    This function doesn't update status fields, compared to withdraw task.
    """
    try:
        bgpspeaker.update_flow(match, then, withdraw=True)
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        flow.save()
        raise announce.retry(exc=e, countdown=10)

@task(max_retries=3)
def expire(flow):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends withdraw route command via a socket.
    This function set status field to EXPIRED
    """
    if not flow.has_expired():
        return
    try:
        bgpspeaker.update_flow(flow.match(), flow.then(), withdraw=True)
        flow.status = Route.EXPIRED
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        raise announce.retry(exc=e, countdown=10)
    finally:
        flow.save(update_fields=['status'])

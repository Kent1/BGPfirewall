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

def modify(oldflow, newflow):
    #group(withdraw.s(oldflow), announce.s(newflow))()
    chain(withdraw.si(oldflow, oldflow.match(), oldflow.then()), announce.si(newflow, newflow.match(), newflow.then()))()

@task(max_retries=3)
def expire(flow, match, then):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends withdraw route command via a socket.
    """
    if not flow.has_expired():
        return
    try:
        bgpspeaker.update_flow(match, then, withdraw=True)
        flow.status = Route.EXPIRED
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        raise announce.retry(exc=e, countdown=10)
    finally:
        flow.save(update_fields=['status'])

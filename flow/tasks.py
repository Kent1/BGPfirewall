from celery import task
from celery.utils.log import get_task_logger
from flow.models import Route
import logging
logger = logging.getLogger('BGPFirewall')

import bgpspeaker

@task(max_retries=3)
def announce(flow, match, then):
    """
    Asynchronous task. It transmit information to the bgpspeaker
    who sends announce route command via a socket.
    """
    try:
        bgpspeaker.update_flow(match, then)
        flow.status = Route.ACTIVE
    except ValueError, e:
        logger.error('Error ' + e)
        flow.status = Route.ERROR
        raise announce.retry(exc=e)
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
        raise announce.retry(exc=e)
    finally:
        flow.save(update_fields=['status'])

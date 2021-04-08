# -*- coding: utf-8 -*-

from sentry_sdk import capture_message
from ..tasks import celery
from .models import Voter
from .helper import calculate_post_vote, calculate_post_kill


@celery.task(name='base.common.health_check_task', rate_limit='10/s')
def health_check_task():
    capture_message('Health check task')
    return "Health check task finished successfully"


@celery.task(name='voter.add_task', rate_limit='20/s')
def add_task(payload):
    """
    Add user deciding to db.
    :param payload:
    :return:
    """

    Voter.add(payload)

    # Update redis for deciding
    update_post_deciding.delay(payload)

    return "Done"


@celery.task(name='voter.update_post_deciding_task', rate_limit='20/s')
def update_post_deciding(payload):
    """
    Update vote, kill for a post. Update redis. Update DB if need.
    :param payload:
    :return:
    """

    post_id = payload['postId']
    vote = payload['vote']
    kill = payload['kill']

    if vote:
        calculate_post_vote(post_id, vote)

    if kill:
        calculate_post_kill(post_id, kill)

    return "Done"

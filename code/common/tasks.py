# -*- coding: utf-8 -*-

from sentry_sdk import capture_message
from ..tasks import celery
from .models import Logs


@celery.task(name='base.common.health_check_task', rate_limit='10/s')
def health_check_task():
    capture_message('Health check task')
    return "Health check task finished successfully"

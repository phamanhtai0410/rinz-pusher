import traceback

from sentry_sdk import capture_exception

from src.tasks import celery
from src.utils import log_any


@celery.task(name='tasks.name', rate_limit='100/s')
def name_task(*args, **kwargs):
    try:
        log_any("")
    except Exception as e:
        capture_exception(e)
        traceback.print_exception(e)
    return "success"

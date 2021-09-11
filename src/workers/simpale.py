import traceback

from sentry_sdk import capture_exception

from src.tasks import celery
from src.utils.logger import Logger


@celery.task(name='tasks.name', rate_limit='100/s')
def name_task(*args, **kwargs):
    try:
        Logger.debug("")
    except:
        capture_exception()
        traceback.print_exc()
    return "success"

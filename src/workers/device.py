import traceback

from sentry_sdk import capture_exception

from src.exceptions.handler import handle_exception
from src.models.device import Device
from src.tasks import celery
from src.utils.logger import Logger


@celery.task(name='push.tasks.insert_device', rate_limit='100/s')
@handle_exception()
def insert_device_task(device):
    Device.add(device)

from src.exceptions.handler import handle_exception
from src.models.device import Device
from src.tasks import celery


@celery.task(name='push.tasks.user.insert_notification', rate_limit='100/s')
@handle_exception()
def insert_notifications_task(notifications: list):
    Device.add_many(notifications)
    return 'success'

from bson import ObjectId

from src.enums.service import ServiceForNoification
from src.exceptions.handler import handle_exception
from src.extensions import redis_global
from src.helpers.user import count_notification
from src.models.notification import Notification
from src.tasks import celery
from src.utils.logger import Logger


@celery.task(name='push.tasks.user.insert_notification', rate_limit='100/s')
@handle_exception()
def insert_notifications_task(users: list, notification: dict):
    Logger.debug(users)
    for user_id in users:
        count_notification(
            user_id=user_id,
            from_service=notification.get('from_service')
        )
    notifications = [{
        'user_id': x,
        **notification
    } for x in users]
    Notification.add_many(notifications)
    return 'success'


@celery.task(name='push.tasks.user.insert_notification', rate_limit='100/s')
@handle_exception()
def mark_notification_task(user_id: int, notification_id: str, from_service: str, bulk_id=None):
    filter = {
        'user_id': user_id,
        'has_marked': False
    }
    if bulk_id:
        filter['bulk_id'] = bulk_id
    else:
        if notification_id != "*":
            filter['_id'] = ObjectId(notification_id)

    if from_service != ServiceForNoification.RINZ:
        filter['from_service'] = from_service

    if notification_id == '*':
        count_notification(
            user_id=user_id,
            from_service=from_service,
            number=0,
        )
    else:
        count_notification(
            user_id=user_id,
            from_service=from_service,
            number=-1,
        )

    Notification.update_many(filter=filter, update_data={
        'has_marked': True
    })

    return 'success'

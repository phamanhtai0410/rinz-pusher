from src.exceptions.handler import handle_exception
from src.helpers.firebase import gen_key_topic_for_user
from src.models.notification import Notification
from src.workers.device import insert_device_task, remove_device_task
from src.workers.firebase import firebase_subscribe_task, firebase_unsubscribe_task
from src.workers.user import mark_notification_task


class UserService(object):

    @staticmethod
    @handle_exception()
    def login_device(device: dict):
        # record device
        insert_device_task(device)
        user_id = device.get('user_id')
        fcm_token = device.get('fcm_token')

        # gen topic name
        topic = gen_key_topic_for_user(user_id=user_id)
        # TODO add delay
        firebase_subscribe_task(topic, [fcm_token])

    @staticmethod
    @handle_exception()
    def logout_device(device: dict):
        user_id = device.get('user_id')
        fcm_token = device.get('fcm_token')
        # remove status or device
        remove_device_task(user_id=user_id, fcm_token=fcm_token)
        # gen name for topic
        topic = gen_key_topic_for_user(user_id=user_id)

        # TODO add delay
        firebase_unsubscribe_task(topic, [fcm_token])

    @staticmethod
    @handle_exception(default=[])
    def get_notifications(user_id: int, limit: int, offset: int, from_service: str):
        notifications = Notification.get_by_filter(
            filter={
                'user_id': user_id,
                'from_service': from_service
            },
            options={
                'limit': limit,
                'offset': offset,
                'sort': {
                    'created_time': -1
                }
            }
        )
        return notifications

    @staticmethod
    @handle_exception()
    def mark_notification(user_id: int, notification_id: str, from_service: str, bulk_id=None):
        """
            mark notification of user; if notification = * => mark all
        """
        mark_notification_task(user_id=user_id, notification_id=notification_id, from_service=from_service, bulk_id=bulk_id)

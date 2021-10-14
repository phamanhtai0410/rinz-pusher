from src.exceptions.handler import handle_exception
from src.helpers.firebase import gen_key_topic_for_user
from src.workers.firebase import firebase_send_topic_use_condition


class FirebaseService(object):

    @staticmethod
    def gen_condition_for_users(users: list):
        topics = [gen_key_topic_for_user(user_id=x) for x in users]
        # read docs here https://firebase.google.com/docs/cloud-messaging
        return ' || '.join([f"'{x}' in topics" for x in topics])

    @classmethod
    @handle_exception()
    def send_message_to_users(cls, users: list, notification: dict):
        topic = None
        condition = None
        if len(users) == 1:
            topic = gen_key_topic_for_user(user_id=users[0])
        else:
            condition = cls.gen_condition_for_users(users)

        firebase_send_topic_use_condition(
            condition=condition,
            topic=topic,
            notification=notification
        )

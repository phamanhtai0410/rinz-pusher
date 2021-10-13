from src.exceptions.handler import handle_exception


class FirebaseService(object):

    @staticmethod
    def gen_condition_for_users(users: list):
        return ''

    @classmethod
    @handle_exception()
    def send_message_to_users(cls, users: list, notification: dict):
        print()

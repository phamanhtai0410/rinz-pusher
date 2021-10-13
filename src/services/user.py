from src.exceptions.handler import handle_exception


class UserService(object):

    @staticmethod
    @handle_exception
    def login_device(user_id: int, device: dict):
        print()
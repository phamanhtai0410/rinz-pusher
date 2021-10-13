from src.exceptions.handler import handle_exception


class UserService(object):

    @staticmethod
    @handle_exception
    def update_device(device: dict):
        user_id = device.get('user_id')

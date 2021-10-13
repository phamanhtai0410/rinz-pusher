from flask import g

from src.decorators.handle_response import handle_response
from src.decorators.load_body import load_data
from src.schemas.device import DeviceSchema
from src.schemas.notification import NotificationSchema
from src.utils.logger import Logger


@handle_response()
@load_data(NotificationSchema)
def send_to_user_controller():
    data = g.data
    Logger.debug(data)
    return {}


@handle_response()
@load_data(DeviceSchema)
def login_device_controller():
    data = g.data
    # update_device_of_user(data)
    return {}


@handle_response()
@load_data(DeviceSchema)
def logout_device_controller():
    data = g.data
    return {}

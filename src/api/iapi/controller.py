from flask import g

from src.decorators.handle_response import handle_response
from src.decorators.load_body import load_data
from src.schemas.device import DeviceSchema
from src.schemas.notification import NotificationSchema
from src.services.firebase import FirebaseService
from src.services.user import UserService
from src.utils.generator import gen_oid
from src.workers.user import insert_notifications_task


@handle_response()
@load_data(NotificationSchema)
def send_to_user_controller():
    data = g.data
    users = data.get('users', [])
    del data['users']
    data['bulk_id'] = gen_oid()
    # data['navigate']['no_record'] = True
    insert_notifications_task.delay(users=users, notification=data)
    FirebaseService.send_message_to_users(users, data)
    return {}


@handle_response()
@load_data(NotificationSchema)
def send_to_user_no_record_controller():
    data = g.data
    users = data.get('users', [])
    del data['users']
    data['navigate']['no_record'] = True
    FirebaseService.send_message_to_users(users, data)
    return {}


@handle_response()
@load_data(DeviceSchema)
def login_device_controller():
    device = g.data
    UserService.login_device(device=device)
    return {}


@handle_response()
@load_data(DeviceSchema)
def logout_device_controller():
    device = g.data
    UserService.logout_device(device=device)
    return {}

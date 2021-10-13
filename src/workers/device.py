from src.exceptions.handler import handle_exception
from src.models.device import Device
from src.tasks import celery


@celery.task(name='push.tasks.insert_device', rate_limit='100/s')
@handle_exception()
def insert_device_task(device):
    Device.add(device)
    return 'success'


@celery.task(name='push.tasks.remove_device', rate_limit='100/s')
@handle_exception()
def remove_device_task(user_id, fcm_token):
    Device.update_one(filter={
        'user_id': user_id,
        'fcm_token': fcm_token,
        'has_logout': False
    }, update_data={
        'has_logout': True
    })
    return 'success'

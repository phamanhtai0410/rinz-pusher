from src.enums.service import ServiceForNoification
from src.exceptions.handler import handle_exception
from src.extensions import redis_global


def gen_key_count_notification_of_user(user_id: int, from_service: str):
    return f'rz_notifications:counter:{user_id}:{from_service}'


@handle_exception()
def count_notification(user_id: int, from_service: str, number: int = 1):
    if from_service != ServiceForNoification.RINZ:
        _count_key = gen_key_count_notification_of_user(user_id=user_id, from_service=from_service)
        if number == 0:
            redis_global.set(_count_key, 0)
        else:
            redis_global.incr(_count_key, number)

    count_key = gen_key_count_notification_of_user(user_id=user_id, from_service=ServiceForNoification.RINZ)
    if number == 0:
        redis_global.set(count_key, 0)
    else:
        redis_global.incr(count_key, number)


@handle_exception(default=0)
def get_total_notifications(user_id: int, from_service: str):
    count_key = gen_key_count_notification_of_user(user_id=user_id, from_service=from_service)
    number = redis_global.get(count_key)
    return int(number)

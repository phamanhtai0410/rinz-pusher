from src.exceptions.handler import handle_exception
from src.tasks import celery
from firebase_admin import messaging

from src.utils.format import dumps
from src.utils.logger import Logger


@celery.task(name='push.tasks.firebase.subscribe', rate_limit='100/s')
@handle_exception()
def firebase_subscribe_task(topic: str, tokens: list):
    response = messaging.subscribe_to_topic(tokens, topic)
    Logger.debug(response)
    return 'success'


@celery.task(name='push.tasks.firebase.unsubscribe', rate_limit='100/s')
@handle_exception()
def firebase_unsubscribe_task(topic: str, tokens: list):
    response = messaging.unsubscribe_from_topic(tokens, topic)
    Logger.debug(response)
    return 'success'


@celery.task(name='push.tasks.firebase.send_topic_use_condition', rate_limit='100/s')
def firebase_send_topic_use_condition(condition, topic, notification):
    _message = notification.get('message')
    preview = _message.get('preview', {})
    payload = notification.get('payload', {})
    payload["navigate"] = dumps(notification.get('navigate', {}))
    payload["bulk_id"] = notification.get('bulk_id', '')

    data_payload = {}
    for x in payload.keys():
        data_payload[x] = payload[x]
    Logger.debug('condition', condition, data_payload, topic)
    if preview.get("image"):
        message = messaging.Message(
            notification=messaging.Notification(
                title=preview.get('title'),
                body=preview.get('description'),
                image=preview.get("image"),
            ),
            data=data_payload,
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(
                aps=messaging.Aps(mutable_content=1)
            ), fcm_options=messaging.APNSFCMOptions(
                image=preview.get("image"))),
            # condition=condition,
        )
    else:
        message = messaging.Message(
            notification=messaging.Notification(
                title=preview.get('title'),
                body=preview.get('description'),
            ),
            data=data_payload,
            apns=messaging.APNSConfig(payload=messaging.APNSPayload(
                aps=messaging.Aps(mutable_content=1)
            )),
            # condition=condition,
        )
    if topic:
        message.topic = topic
    if condition:
        message.condition = condition
    response = messaging.send(message)
    Logger.debug(response)
    return "success"

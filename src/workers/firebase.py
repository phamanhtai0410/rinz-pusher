from src.exceptions.handler import handle_exception
from src.tasks import celery
from firebase_admin import messaging

from src.utils.format import dumps


@celery.task(name='push.tasks.firebase.subscribe', rate_limit='100/s')
@handle_exception()
def firebase_subscribe_task(topic: str, tokens: list):
    messaging.subscribe_to_topic(tokens, topic)
    return 'success'


@celery.task(name='push.tasks.firebase.unsubscribe', rate_limit='100/s')
@handle_exception()
def firebase_unsubscribe_task(topic: str, tokens: list):
    messaging.unsubscribe_from_topic(tokens, topic)
    return 'success'


@celery.task(name='push.tasks.firebase.send_topic_use_condition', rate_limit='100/s')
def firebase_send_topic_use_condition(condition, notification):
    _message = notification.get('message')
    preview = _message.get('preview', {})
    payload = notification.get('payload', {})
    payload["navigate"] = dumps(notification.get('navigate', {}))
    payload["_id"] = notification.get('_id', '')

    data_payload = {}
    for x in payload.keys():
        data_payload[x] = payload[x]

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
            condition=condition,
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
            condition=condition,
        )
    messaging.send(message)
    return "success"

from flask import g, request

from src.decorators import auth_user
from src.decorators.handle_response import handle_response
from src.decorators.load_body import load_data
from src.enums.service import ServiceEnum
from src.schemas.notification import NotificationsResponseSchema, MarkNotificationSchema, MarkFirebaseSchema
from src.services.user import UserService


@handle_response()
@auth_user()
def get_notifications_controller(user_info):
    user_id = user_info.get('id')
    limit = request.args.get('limit', type=int, default=20)
    offset = request.args.get('offset', type=int, default=0)
    from_service = request.args.get('from_service', type=str)
    if from_service not in ServiceEnum.enums():
        return NotificationsResponseSchema.load_response({})
    notifications = UserService.get_notifications(
        user_id=user_id,
        limit=limit,
        offset=offset,
        from_service=from_service
    )
    return NotificationsResponseSchema.load_response({
        'notifications': notifications,
        'has_ended': True if len(notifications) < limit else False
    })


@handle_response()
@load_data(MarkNotificationSchema)
@auth_user()
def mark_notification_controller(user_info):
    data = g.data
    user_id = user_info.get('id')
    from_service = data.get('from_service')
    notification_id = data.get('notification_id')

    UserService.mark_notification(
        user_id=user_id,
        from_service=from_service,
        notification_id=notification_id
    )

    return {}


@handle_response()
@load_data(MarkFirebaseSchema)
@auth_user()
def mark_notification_controller(user_info):
    data = g.data
    user_id = user_info.get('id')
    from_service = data.get('from_service')
    bulk_id = data.get('bulk_id')

    UserService.mark_notification(
        user_id=user_id,
        from_service=from_service,
        notification_id=None,
        bulk_id=bulk_id
    )

    return {}

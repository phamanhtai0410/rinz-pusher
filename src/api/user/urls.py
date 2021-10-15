from flask import Blueprint

from src.api.user.controller import get_notifications_controller, \
    mark_notification_controller, mark_notification_by_bulk_controller, get_new_notification

rest_user = Blueprint('rest_user', __name__, url_prefix='/user')

rest_user.add_url_rule('notifications', methods=['GET'], view_func=get_notifications_controller)

rest_user.add_url_rule('mark', methods=['PUT'], view_func=mark_notification_controller)

rest_user.add_url_rule('mark_by_bulk', methods=['PUT'], view_func=mark_notification_by_bulk_controller)

rest_user.add_url_rule('new', methods=['GET'], view_func=get_new_notification)

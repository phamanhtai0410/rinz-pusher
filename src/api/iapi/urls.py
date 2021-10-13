from flask import Blueprint

from src.api.iapi.controller import send_to_user_controller, login_device_controller, logout_device_controller

rest_iapi = Blueprint('rest_iapi', __name__, url_prefix='/iapi')

rest_iapi.add_url_rule('user', methods=['POST'], view_func=send_to_user_controller)

rest_iapi.add_url_rule('user/login', methods=['POST'], view_func=login_device_controller)

rest_iapi.add_url_rule('user/logout', methods=['POST'], view_func=logout_device_controller)

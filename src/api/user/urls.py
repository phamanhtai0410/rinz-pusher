from flask import Blueprint

from src.api.user.controller import send_to_user_controller

rest_user = Blueprint('rest_user', __name__, url_prefix='/user')

rest_user.add_url_rule('', methods=['POST'], view_func=send_to_user_controller)

from flask import Blueprint

from src.api.common.controller import cl_health_check

rest_service = Blueprint('rest_service', __name__, url_prefix='/common')

rest_service.add_url_rule('health_check', methods=['GET'], view_func=cl_health_check)

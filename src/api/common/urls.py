from flask import Blueprint

from src.api.common.controller import cl_health_check

rest_service = Blueprint('rest_service', __name__, url_prefix='/common')


@rest_service.route('/health_check', methods=['GET'])
def health_check():
    return cl_health_check()

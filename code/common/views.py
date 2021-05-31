# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort, g
from flask_expects_json import expects_json

from code.utils import make_cross_domain_response, log_any
from ..constants import AppConstants

rest_service = Blueprint('rest_service', __name__, url_prefix='/common')


@rest_service.route('/health_check', methods=['GET'])
def health_check():
    # capture_message('Health check route voter service')
    log_any("call health_check")
    payload = {
        "info": "log health_check"
    }
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'TheCuaTui Health Check base service',
                                       'error_code': AppConstants.NOT_E}, 200)


# method != GET
schema = {
    'type': 'object',
    'properties': {
        'description': {'type': 'string'},
        'images': {'type': 'array'},
        'videos': {'type': 'array'},
        'tags': {'type': 'array'},
        'categories': {'type': 'array'},
        'files': {'type': 'array'}
    },
    'required': ['description']
}


@rest_service.route('/schema', methods=['POST'])
@expects_json(schema)
def test():
    """
    Save test internal sevrice call.
    """
    # data here
    data = g.data
    log_any(data)
    return make_cross_domain_response(
        {'status': AppConstants.STATUS_OK, 'msg': 'success', 'error_code': AppConstants.NOT_E})

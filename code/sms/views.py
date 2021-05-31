# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort, g
from flask_expects_json import expects_json

from code.utils import make_cross_domain_response, log_any
from ..constants import AppConstants
from ..workers import send_phone_task

rest_sms = Blueprint('rest_sms', __name__, url_prefix='/sms')

#
# @rest_sms.route('/health_check', methods=['GET'])
# def health_check():
#     # capture_message('Health check route voter service')
#     log_any("call health_check")
#     payload = {
#         "info": "log health_check"
#     }
#     return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'TheCuaTui Health Check base service',
#                                        'error_code': AppConstants.NOT_E}, 200)
#

# method != GET
sms_schema = {
    'type': 'object',
    'properties': {
        'phone': {'type': 'string'},
        'code': {'type': 'string'},
        'user_id': {'type': 'number'},
    },
    'required': ['phone', 'code', 'user_id']
}


@rest_sms.route('/send_code', methods=['POST'])
@expects_json(sms_schema)
def send_code():
    phone = g.data.get('phone')
    code = g.data.get('code')
    user_id = g.data.get('user_id')
    send_phone_task.delay(code=code, phone=phone, user_id=user_id)
    return make_cross_domain_response(
        {
            'status': AppConstants.STATUS_OK,
            'msg': 'success',
            'error_code': AppConstants.NOT_E
        })

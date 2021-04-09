# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort

from code.utils import make_cross_domain_response, log_any
from ..constants import AppConstants
from .tasks import add_task


rest_service = Blueprint('rest_service', __name__, url_prefix='/v1/comment')


@rest_service.route('/common/health_check', methods=['GET'])
def health_check():
    #capture_message('Health check route voter service')
    log_any("call health_check")
    payload = {
        "info": "log health_check"
    }
    add_task(payload)
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'TheCuaTui Health Check base service', 'error_code': AppConstants.NOT_E}, 200)


@rest_service.route('/iapi/test', methods=['POST'])
def test():
    """
    Save test internal sevrice call.
    """
    log_any("call /iapi/test")
    return make_cross_domain_response({'status': AppConstants.STATUS_OK, 'msg': 'success', 'error_code': AppConstants.NOT_E})
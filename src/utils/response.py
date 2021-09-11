from datetime import datetime

from flask import jsonify


def make_response(data: dict = {}, msg: str = '', error_code: str = '', status: int = 1):
    result = {
        'data': data,
        'msg': msg,
        'error_code': error_code,
        'status': status,
        'version': 'v1',
        'time': datetime.utcnow().timestamp()
    }

    return jsonify(result), 200

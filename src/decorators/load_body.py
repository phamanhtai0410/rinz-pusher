# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, abort, jsonify, g
from marshmallow import ValidationError


def load_data(BaseSchema):
    """
    Decorator to load data from request
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.method == 'GET':
                request_data = request.args.to_dict()
            else:
                request_data = request.get_json()
            schema = BaseSchema()
            try:
                result = schema.load(request_data)
                g.data = result
            except ValidationError as err:
                return jsonify({
                    'error_code': 'INVALID',
                    'status': 0,
                    'msg': err.messages,
                    'data': {}
                }), 400
            return f(*args, **kwargs)

        return wrapper

    return decorator

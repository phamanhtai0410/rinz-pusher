# -*- coding: utf-8 -*-
from functools import wraps
from flask import request, g
from marshmallow import ValidationError

from src.exceptions.missing import ExceptionMissing


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
                errors = err.messages
                msg = ''
                if isinstance(errors, str):
                    msg = errors
                if isinstance(errors, list) and isinstance(errors[0], dict):
                    field, msg = errors[0].items()[0]
                if isinstance(errors, dict) and len(errors.items()) > 0:
                    field, msg = list(errors.items())[0]
                    if isinstance(msg, list):
                        msg = msg[0]
                if not msg:
                    msg = str(errors)
                raise ExceptionMissing(message=msg, errors=errors)
            except:
                raise
            return f(*args, **kwargs)

        return wrapper

    return decorator

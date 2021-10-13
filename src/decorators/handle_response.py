
from functools import wraps
from src.utils.response import make_response

from src.exceptions.handler import request_exception
from flask import jsonify
from flask.globals import request
from src.decorators import cache_request


def handle_response(cahing=False, timeout=604800, default=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            @request_exception(default=default)
            def run_controller():
                @cache_request(
                    keep_timeout=timeout,
                    key_prefix=request.path
                )
                def run_with_cache():
                    return f(*args, **kwargs)
                if cahing:
                    data = run_with_cache()
                else:
                    data = f(*args, **kwargs)
                return make_response(data)

            return jsonify(run_controller()), 200
        return wrapper

    return decorator

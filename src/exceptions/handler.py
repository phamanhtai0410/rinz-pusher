import traceback
from functools import wraps

import sentry_sdk

from src.constants import Constants
from src.utils.response import make_response
from src.exceptions import BadRequestException


def request_exception(default: dict = {}):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except BadRequestException as e:
                return e.response
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()
                if default:
                    return make_response(data=default)
                return make_response(
                    status=Constants.STATUS_NOT_OK,
                    msg=Constants.MSG_UNKNOWN_ERROR,
                    error_code=Constants.ERROR_SERVER
                )

        return wrapper

    return decorator


def handle_exception(default=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()
                return default

        return wrapper

    return decorator

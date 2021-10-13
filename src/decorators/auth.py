# -*- coding: utf-8 -*-
from functools import wraps

from src.exceptions.auth import ExceptionRequiredAuth
from src.extensions import redis_global
from flask import request
from sentry_sdk import capture_exception
import jwt
import traceback

from src.utils.response import make_response


def verify_token():
    rq_user_token = request.headers.get('Authorization')
    if not rq_user_token or 'Bearer ' not in rq_user_token:
        return None

    rq_user_token = rq_user_token.split(' ')[1]
    # Get user token on Redis user info
    token_existed = redis_global.get("token:{}".format(rq_user_token))
    user_info = None
    if token_existed:  # In case user info exists, decode it
        try:
            user_info = jwt.decode(rq_user_token, algorithm="RS256", options={"verify_signature": False})
        except:
            traceback.print_exc()
            capture_exception()

    return user_info


def auth_user():
    """
    Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request:  # Outside flask app context
                decorated_kwargs = {**kwargs, 'user_info': None}
                return f(*args, **decorated_kwargs)
            user_info = verify_token()
            if not user_info:
                raise ExceptionRequiredAuth

            decorated_kwargs = {**kwargs, 'user_info': user_info.get('payload', {})}
            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator


def get_user():
    """
    Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request:  # Outside flask app context
                decorated_kwargs = {**kwargs, 'user_info': {}}
                return f(*args, **decorated_kwargs)
            user_info = verify_token()
            if not user_info:
                user_info = {}
            decorated_kwargs = {**kwargs, 'user_info': user_info.get('payload', {})}
            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator

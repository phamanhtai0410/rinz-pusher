# -*- coding: utf-8 -*-
import json
from functools import wraps

import sentry_sdk

from src.config import DefaultConfig
from src.extensions import redis_cluster
import traceback

from src.utils.format import json_decode_hook, dumps, load_json

CACHE_TIMEOUT_FACTOR = 1


def get_data_by_key(_key):
    try:
        if DefaultConfig.CACHING:
            return redis_cluster.get(_key)
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
    return None


def set_data_by_key(_key, _payload):
    try:
        if DefaultConfig.CACHING:
            return redis_cluster.setex(_key, 86400, dumps(_payload))
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
    return None


# timeout=1 week
def cache_id(timeout=604800, key_prefix='common', keep_timeout=False):
    """
        - Input:
            + key_prefix: name of model(table or collection).
        - Output:
            + dict or None

    """
    if timeout is None:
        timeout = 300

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = "%s%s:id:%s" % (DefaultConfig.CACHE_SUB, key_prefix, args[0])
            output = get_data_by_key(key)
            if output:
                return json.loads(output, object_hook=json_decode_hook)

            output = f(*args, **kwargs)
            # Set data to redis
            set_data_by_key(key, output)
            return output

        return wrapper

    return decorator


# timeout = 1 day
def cache_filter(timeout=86400, key_prefix='common', key_fields=[], options=[], keep_timeout=False):
    """
        - Input:
            + key_prefix: name of model(table or collection).
            + key_fields:  key of filter
            + options: ex: limit, offset, sort, ...
        - Output:
            + result of filter
    """
    if timeout is None:
        timeout = 86400

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            _filter = dict()

            # TODO sort keys

            key_fields.sort()

            for key_field in key_fields:
                _filter[key_field] = kwargs.get(key_field)

            _options = kwargs.get('options', {})

            for option in options:
                _filter[option] = _options.get(option)

            key = "%s%s:%s" % (DefaultConfig.CACHE_SUB,
                               key_prefix, dumps(_filter))

            output = get_data_by_key(key)

            if output:
                return load_json(output)

            output = f(*args, **kwargs)

            set_data_by_key(key, output)

            return output

        return wrapper

    return decorator

# timeout=1 week


def cache_request(timeout=604800, key_prefix='url', keep_timeout=False):
    """
        - Input:
            + key_prefix: name of model(table or collection).
        - Output:
            + dict or None

    """
    if timeout is None:
        timeout = 604800

    if not keep_timeout:
        timeout *= CACHE_TIMEOUT_FACTOR

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = "%s:requests:%s" % (DefaultConfig.PREFIX, key_prefix)
            output = get_data_by_key(key)
            if output:
                return load_json(output)

            output = f(*args, **kwargs)
            # Set data to redis
            set_data_by_key(key, output)
            return output

        return wrapper

    return decorator

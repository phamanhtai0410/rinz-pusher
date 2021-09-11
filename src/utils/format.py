import json
import traceback
from datetime import datetime, date

import sentry_sdk
from bson import ObjectId


def is_oid(oid):
    return ObjectId.is_valid(oid)


def load_json(string: str):
    try:
        return json.loads(string, object_hook=json_decode_hook)
    except:
        traceback.print_exc()
        sentry_sdk.capture_exception()
    return {}


def dumps(payload: object = {}):
    try:
        return json.dumps(payload, default=json_encode_hook)
    except:
        traceback.print_exc()
        sentry_sdk.capture_exception()
    return ''


def json_decode_hook(obj):
    if '__datetime__' in obj:
        return datetime.strptime(obj['as_str'], "%Y%m%dT%H:%M:%S.%f")
    if b'__datetime__' in obj:
        return datetime.strptime(obj[b'as_str'], "%Y%m%dT%H:%M:%S.%f")
    return obj


def json_encode_hook(obj):
    if isinstance(obj, datetime):
        obj = {'__datetime__': True, 'as_str': obj.strftime("%Y%m%dT%H:%M:%S.%f")}
    if isinstance(obj, ObjectId):
        obj = str(obj)
    return obj


def json_encode_response(obj):
    if isinstance(obj, datetime):
        obj = obj.timestamp()
    if isinstance(obj, ObjectId):
        obj = str(obj)
    return obj


def id_response(obj):
    try:
        if isinstance(obj, ObjectId):
            return str(obj)
    except:
        traceback.print_exc()
        sentry_sdk.capture_exception()
    return obj


def datetime_response(obj):
    try:
        if isinstance(obj, datetime):
            return obj.timestamp()
    except:
        traceback.print_exc()
        sentry_sdk.capture_exception()

    return obj


def make_response_dict(data):
    dict_string = json.dumps(data, default=json_encode_response)
    return json.loads(dict_string)


def get_current_time():
    return datetime.utcnow()

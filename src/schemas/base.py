import traceback
from datetime import datetime

import sentry_sdk
from marshmallow import pre_load, fields


class Trim(fields.Field):
    def __init__(self, inner, *args, **kwargs):
        self.inner = inner
        super().__init__(*args, **kwargs)

    def _bind_to_schema(self, field_name, parent):
        super()._bind_to_schema(field_name, parent)
        self.inner._bind_to_schema(field_name, parent)

    def _deserialize(self, value, *args, **kwargs):
        if hasattr(value, 'strip'):
            value = value.strip()
        return self.inner._deserialize(value, *args, **kwargs)

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)


class BaseQuery():
    @pre_load
    def load_limit_and_offset(self, in_data, **kwargs):
        if in_data.get('limit'):
            try:
                in_data['limit'] = int(in_data['limit'])
            except:
                traceback.print_exc()
                in_data['limit'] = 20
        if in_data.get('offset'):
            try:
                in_data['offset'] = int(in_data['offset'])
            except:
                traceback.print_exc()
                in_data['offset'] = 0
        return in_data


class BaseResponse():
    @pre_load
    def load_id(self, in_data, **kwargs):
        if in_data.get('_id'):
            in_data['_id'] = str(in_data['_id'])
        return in_data

    @pre_load
    def load_datetime(self, in_data, **kwargs):
        for key, value in in_data.items():
            if isinstance(value, datetime):
                in_data[key] = value.timestamp()
        return in_data

    @classmethod
    def load_response(cls, payload: dict = {}):
        try:
            try:
                result = cls().load(payload)
                return result
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()
                return {}
        except:
            sentry_sdk.capture_exception()
            traceback.print_exc()

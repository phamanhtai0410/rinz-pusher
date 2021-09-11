import traceback

from marshmallow import Schema, fields, ValidationError, INCLUDE, EXCLUDE, pre_load

from src.schemas.base import BaseResponse, BaseQuery
from src.utils.format import is_oid, id_response


class Example(Schema, BaseQuery):
    class Meta:
        unknown = INCLUDE

    limit = fields.Int()
    offset = fields.Int(missing=0)
    type = fields.String()
    _id = fields.String(validate=is_oid, error_messages={
        'invalid': '_id must be a objectId as string'
    })

    def handle_error(self, exc, data, **kwargs):
        """Log and raise our custom exception when (de)serialization fails."""
        print(exc.messages)


class ExampleResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.String()
    created_time = fields.Float()

from marshmallow import Schema, fields, EXCLUDE, validate

from src.enums.platform import PlatformEnum


class DeviceSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    device_id = fields.Str(required=True)
    fcm_token = fields.Str(required=True)
    user_id = fields.Int(required=True)
    platform = fields.Str(required=True, validate=validate.OneOf(PlatformEnum.enums()))

from marshmallow import Schema, fields, EXCLUDE, validate, validates, ValidationError, validates_schema

from src.enums.screen import ScreenRZMusicEnum
from src.enums.service import ServiceEnum


class NavigationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    screen = fields.Str(missing='')
    payload = fields.Dict(missing={}, allow_none=True)
    is_local = fields.Bool(missing=True)
    href = fields.URL(allow_none=True, missing='')


class PreviewMessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True)
    image = fields.Str(missing='', allow_none=True)
    description = fields.Str(required=True)


class MessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True)
    description = fields.Str(required=True)
    image = fields.Str(required=True)
    item_id = fields.Str(allow_none=True, missing='')
    item_type = fields.Str(allow_none=True, missing='')
    preview = fields.Nested(PreviewMessageSchema(), required=True)


class NotificationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    user_id = fields.Int(required=True)

    from_service = fields.Str(required=True, validate=validate.OneOf([
        ServiceEnum.RINZ_MUSIC
    ]))

    navigate = fields.Nested(NavigationSchema(), required=True)

    message = fields.Nested(MessageSchema(), required=True)

    @validates_schema
    def validate_navigate(self, value, **kwargs):
        navigate = value.get('navigate', {})
        if navigate.get('is_local'):
            if value.get('from_service') == ServiceEnum.RINZ_MUSIC:
                screens = ScreenRZMusicEnum.enums()
                if navigate.get('screen') not in screens:
                    raise ValidationError({
                        'navigate': [
                            f'screen must be in {screens}'
                        ]
                    })
        else:
            print('navigate', navigate)
            if not navigate.get('href'):
                raise ValidationError({
                    'navigate': [
                        f'href must be required'
                    ]
                })

from marshmallow import Schema, fields, EXCLUDE, validate, validates, ValidationError, validates_schema

from src.enums.screen import ScreenRZMusicEnum
from src.enums.service import ServiceEnum, ServiceForNoification
from src.schemas.base import BaseResponse
from src.utils.validates import is_not_blank, is_oid_or_all


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

    title = fields.Str(required=True,
                       validate=is_not_blank,
                       error_messages={
                           'validator_failed': 'Must be not empty'
                       })

    image = fields.Str(missing='', allow_none=True)

    description = fields.Str(required=True,
                             validate=is_not_blank,
                             error_messages={
                                 'validator_failed': 'Must be not empty'
                             })


class MessageSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(required=True,
                       validate=is_not_blank,
                       error_messages={
                           'validator_failed': 'Must be not empty'
                       })
    description = fields.Str(required=True,
                             validate=is_not_blank,
                             error_messages={
                                 'validator_failed': 'Must be not empty'
                             })
    image = fields.URL(required=True,
                       validate=is_not_blank,
                       error_messages={
                           'validator_failed': 'Must be not empty'
                       })
    item_id = fields.Str(allow_none=True, missing='')
    item_type = fields.Str(allow_none=True, missing='')
    preview = fields.Nested(PreviewMessageSchema(), required=True)


class NotificationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    users = fields.List(fields.Int(), required=True,
                        validate=is_not_blank,
                        error_messages={
                            'validator_failed': 'Must be not empty'
                        })

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
            if not navigate.get('href'):
                raise ValidationError({
                    'navigate': [
                        f'href must be required'
                    ]
                })


class NotificationResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Str()
    user_id = fields.Int()
    from_service = fields.Str()
    navigate = fields.Nested(NavigationSchema(), required=True)
    message = fields.Nested(MessageSchema(), required=True)
    has_marked = fields.Bool()
    created_time = fields.Float()


class NotificationsResponseSchema(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    notifications = fields.List(fields.Nested(NotificationResponseSchema()), missing=[])
    has_ended = fields.Bool(missing=True)


class MarkNotificationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    from_service = fields.Str(required=True, validate=validate.OneOf(ServiceForNoification.enums()))
    notification_id = fields.Str(required=True,
                                 validate=is_oid_or_all,
                                 error_messages={
                                     'validator_failed': 'Must be a objectid or "*"'
                                 })

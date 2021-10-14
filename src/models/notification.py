from pymodm import fields

from src.models.base import BaseMG


class Notification(BaseMG):
    class Meta:
        collection_name = 'rz_notifications'
        final = True
        ignore_unknown_fields = True

    _id = fields.ObjectIdField(primary_key=True)
    user_id = fields.IntegerField(required=True)
    has_marked = fields.BooleanField(default=False)
    navigate = fields.DictField(required=True)
    message = fields.DictField(required=True)
    from_service = fields.CharField(required=True)

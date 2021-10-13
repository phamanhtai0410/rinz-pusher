from pymodm import fields

from src.models.base import BaseMG


class Device(BaseMG):
    class Meta:
        collection_name = 'rz_devices'
        final = True
        ignore_unknown_fields = True

    _id = fields.ObjectIdField(primary_key=True)
    user_id = fields.IntegerField(required=True)
    fcm_token = fields.CharField(required=True)
    platform = fields.CharField(required=True)
    device_id = fields.CharField(required=True)
    has_logout = fields.BooleanField(default=False)


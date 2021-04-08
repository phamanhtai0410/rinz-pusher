import traceback
from pymodm import MongoModel, fields
from sentry_sdk import capture_exception


class Base(MongoModel):
    createdBy = fields.CharField(default='')
    updatedBy = fields.CharField(default='')
    createdDate = fields.DateTimeField(default=None)
    updatedDate = fields.DateTimeField(default=None)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def find(cls, raw_dict):
        try:
            return cls.objects.raw(raw_dict)
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return []

    @classmethod
    def find_one(cls, _filter):
        try:
            return cls.objects.get(_filter)
        except cls.DoesNotExist:
            return None
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return None

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.objects.get({'_id': fields.ObjectId(id)})
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return None

    @classmethod
    def get_by_list_ids(cls, list_ids):
        try:
            return cls.objects.raw({'_id': {'$in': [fields.ObjectId(id) for id in list_ids]}})
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return []

    @classmethod
    def delete_with_filter(cls, raw_dict):
        cls.objects.raw(raw_dict).delete()

    @classmethod
    def delete_by_id(cls, id):
        cls.objects.raw({'_id': fields.ObjectId(id)}).delete()

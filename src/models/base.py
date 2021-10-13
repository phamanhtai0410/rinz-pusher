import json
import traceback
from datetime import datetime

import sentry_sdk
import sqlalchemy
from bson import ObjectId
from pymodm import fields, MongoModel
from sqlalchemy import inspect, text
from sqlalchemy.types import TypeDecorator
from sentry_sdk import capture_exception
from traceback import print_exc
from src.decorators.cache import cache_id, cache_filter
from src.utils.format import get_current_time
from src.utils.validates import is_oid

SIZE = 10000


class JsonType(TypeDecorator):
    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Base():
    #
    # @classmethod
    # def commit_db(cls):
    #     try:
    #         db.session.commit()
    #     except Exception as e:
    #         db.session.rollback()
    #         capture_exception(e)
    #         print_exc()
    #
    # @classmethod
    # def insert(cls, payload):
    #     try:
    #         db.session.add(payload)
    #         db.session.commit()
    #         return payload
    #     except:
    #         db.session.rollback()
    #         capture_exception()
    #         print_exc()

    def to_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    @classmethod
    def get_by_id(cls, _id, with_cache=True):
        if with_cache:
            @cache_id(key_prefix=cls.__tablename__)
            def get_cache_by_id(with_id):
                value = cls.query.filter_by(id=with_id).first()
                if value:
                    return value.to_dict()
                return {}

            return get_cache_by_id(_id)
        row = cls.query.filter_by(id=_id).first()
        if row:
            return row.to_dict()
        return {}

    @classmethod
    def get_by_filter(cls,
                      filter={},
                      options={},
                      with_cache=True):
        def get_db():
            _option_keys = options.keys()
            if 'limit' in _option_keys and 'offset' in _option_keys and 'order_by' in _option_keys:
                values = cls.query.filter_by(**filter).order_by(text(options.get('order_by'))) \
                    .offset(options.get('offset')).limit(options.get('limit'))
            elif 'limit' in _option_keys and 'offset' in _option_keys:
                values = cls.query.filter_by(**filter).offset(
                    options.get('offset')).limit(options.get('limit'))
            else:
                values = cls.query.filter_by(**filter).all()
            return [x.to_dict() for x in values]

        if with_cache:
            _keys = filter.keys()
            __option_keys = options.keys()

            @cache_filter(
                key_prefix=cls.__tablename__,
                key_fields=_keys,
                options=__option_keys)
            def get_cache_by_filter(*args, **kwargs):
                return get_db()

            return get_cache_by_filter(**filter, options=options)
        return get_db()

    @classmethod
    def get_one(cls, filter={}, options={}, with_cache=True):
        def get_db():
            value = cls.query.filter_by(**filter).first()
            if value:
                return value.to_dict()
            return {}

        if with_cache:
            _keys = filter.keys()
            __option_keys = options.keys()

            @cache_filter(
                key_prefix=cls.__tablename__,
                key_fields=_keys,
                options=__option_keys)
            def get_cache_by_filter(*args, **kwargs):
                return get_db()

            return get_cache_by_filter(**filter, options=options)
        return get_db()


class BaseMG(MongoModel):
    created_by = fields.CharField(default='', blank=True)
    updated_by = fields.CharField(default='', blank=True)
    created_time = fields.DateTimeField(default=None)
    updated_time = fields.DateTimeField(default=None)

    @classmethod
    def update_many(cls,
                    filter: dict,
                    update_data: dict):
        try:
            _keys = update_data.keys()
            _delete_keys = ['created_by',
                            'created_time',
                            '_id']
            for _key in _delete_keys:
                if _key in _keys:
                    del update_data[_key]
            update_data['updated_time'] = datetime.utcnow()
            return cls.objects.raw(filter).update({
                '$set': update_data
            })
        except cls.DoesNotExist:
            return []
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return []

    @classmethod
    def update_one(cls,
                   filter: dict,
                   update_data: dict):
        try:
            _keys = update_data.keys()
            _delete_keys = ['created_by', 'created_time', '_id']
            for _key in _delete_keys:
                if _key in _keys:
                    del update_data[_key]
            update_data['updated_time'] = datetime.utcnow()
            return cls.objects.raw(filter).update({
                '$set': update_data
            })
        except cls.DoesNotExist:
            return {}
        except Exception as e:
            capture_exception(e)
            traceback.print_exc()
            return {}

    @classmethod
    def add(cls, payload):
        _init = {}
        for field in cls._mongometa.get_fields():
            if field.mongo_name == '_id':
                if not isinstance(payload.get('_id'), ObjectId):
                    if is_oid(payload.get(field.mongo_name)):
                        _init[field.mongo_name] = ObjectId(
                            payload.get(field.mongo_name))
                    else:
                        _init[field.mongo_name] = ObjectId()
                else:
                    _init[field.mongo_name] = payload.get(
                        field.mongo_name, ObjectId())
            else:
                if field.mongo_name in ['created_time', 'updated_time']:
                    if not isinstance(field.mongo_name, datetime):
                        if isinstance(field.mongo_name, (float, int)):
                            _init[field.mongo_name] = datetime.fromtimestamp(
                                payload.get(field.mongo_name, field.default))
                        else:
                            _init[field.mongo_name] = get_current_time().timestamp()
                else:
                    _init[field.mongo_name] = payload.get(
                        field.mongo_name, field.default)
        return cls(**_init).save()

    def to_dict(self):
        _dict = self.to_son().to_dict()
        if '_id' in _dict.keys():
            _dict['_id'] = str(_dict['_id'])
        return _dict

    @classmethod
    def get_one(cls,
                filter: dict = {},
                with_cache=True):
        try:
            _keys = filter.keys()

            def get_db():
                value = cls.objects.get(filter)
                if value:
                    return value.to_dict()
                return {}

            if with_cache:
                @cache_filter(
                    key_prefix=cls.Meta.collection_name,
                    key_fields=_keys,
                    options=[])
                def get_cache_by_filter(*args, **kwargs):
                    return get_db()

                return get_cache_by_filter(
                    **filter,
                    options=[])
            return get_db()

        except cls.DoesNotExist:
            return {}
        except:
            capture_exception()
            traceback.print_exc()
            return {}

    @classmethod
    def get_by_filter(cls,
                      filter: dict = {},
                      options={},
                      with_cache=True):
        try:
            _keys = filter.keys()
            __option_keys = options.keys()

            def get_db():
                _query = [{
                    '$match': filter
                }]
                if 'sort' in __option_keys:
                    _query.append({
                        '$sort': options.get('sort')
                    })
                if 'offset' in __option_keys:
                    _query.append({
                        '$skip': options.get('offset')
                    })
                if 'limit' in __option_keys:
                    _query.append({
                        '$limit': options.get('limit')
                    })
                values = cls.objects.aggregate(*_query)
                return list(values)

            if with_cache:
                @cache_filter(
                    key_prefix=cls.Meta.collection_name,
                    key_fields=_keys,
                    options=__option_keys)
                def get_cache_by_filter(*args, **kwargs):
                    return get_db()

                return get_cache_by_filter(
                    **filter,
                    options=options
                )
            return get_db()
        except cls.DoesNotExist:
            return {}
        except:
            capture_exception()
            traceback.print_exc()
            return {}

    @classmethod
    def get_by_id(cls,
                  _id: str,
                  with_cache=True):
        try:
            def get_db():
                try:
                    value = cls.objects.get({'_id': fields.ObjectId(_id)})
                    if value:
                        return value.to_dict()
                except cls.DoesNotExist:
                    return {}
                except:
                    sentry_sdk.capture_exception()
                    traceback.print_exc()
                return {}

            if with_cache:
                @cache_id(
                    key_prefix=cls.Meta.collection_name)
                def get_cache_by_id(with_id):
                    return get_db()

                return get_cache_by_id(_id)
            return get_db()
        except:
            capture_exception()
            traceback.print_exc()
            return {}

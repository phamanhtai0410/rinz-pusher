import json
import sqlalchemy
from sqlalchemy import inspect, desc, text
from sqlalchemy.types import TypeDecorator
from sentry_sdk import capture_exception
from traceback import print_exception
from src.decorators import cache_id, cache_filter
from src.extensions import db

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

    @classmethod
    def commit_db(cls):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            capture_exception(e)
            print_exception(e)

    @classmethod
    def insert(cls, payload):
        try:
            db.session.add(payload)
            db.session.commit()
            return payload
        except Exception as e:
            db.session.rollback()
            capture_exception(e)
            print_exception(e)

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
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_by_filter(cls, _filter={}, _options={}, with_cache=True, cache_keys=[]):
        def get_db():
            _option_keys = _options.keys()
            if 'limit' in _option_keys and 'offset' in _option_keys and 'order_by' in _option_keys:
                values = cls.query.filter_by(**_filter).order_by(text(_options.get('order_by'))) \
                    .offset(_options.get('offset')).limit(_options.get('limit'))
            elif 'limit' in _option_keys and 'offset' in _option_keys:
                values = cls.query.filter_by(**_filter).offset(
                    _options.get('offset')).limit(_options.get('limit'))
            else:
                values = cls.query.filter_by(**_filter).all()
            return [x.to_dict() for x in values]

        if with_cache:
            _keys = _filter.keys()
            __option_keys = _options.keys()

            @cache_filter(key_prefix=cls.__tablename__, key_fields=cache_keys, options=__option_keys)
            def get_cache_by_filter(*args, **kwargs):
                return get_db()

            return get_cache_by_filter(**_filter, options=_options)
        return get_db()

    @classmethod
    def get_one_by_filter(cls, _filter={}, _options={}, with_cache=True, cache_keys=[]):
        def get_db():
            value = cls.query.filter_by(**_filter).first()
            if value:
                return value.to_dict()
            return {}

        if with_cache:
            _keys = _filter.keys()
            __option_keys = _options.keys()

            @cache_filter(key_prefix=cls.__tablename__, key_fields=cache_keys, options=__option_keys)
            def get_cache_by_filter(*args, **kwargs):
                return get_db()

            return get_cache_by_filter(**_filter, options=_options)
        return get_db()

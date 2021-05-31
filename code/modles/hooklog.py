from datetime import datetime

from code.extensions import db

from sqlalchemy import Column

from code.modles.base import JsonType
from code.utils import get_current_time


class HookLog(db.Model):
    """
    Example Logger model
    """

    __tablename__ = 'hook_logs'
    LOG_LENGTH = 500

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    from_service = Column(db.String(LOG_LENGTH))
    to_service = Column(db.String(LOG_LENGTH))
    data = Column(JsonType(), default={})
    response = Column(db.String(5000), default={})
    headers = Column(JsonType(), default={})
    url = Column(db.String(LOG_LENGTH))
    created_date = Column(db.DateTime, default=get_current_time)

    @staticmethod
    def add(payload):
        payload = {
            'from_service': payload.get("from_service", ''),
            'to_service': payload.get("to_service"),
            'data': payload.get("data", {}),
            'response': payload.get('response', ''),
            'headers': payload.get("headers", {}),
            'url': payload.get("url", ''),
            'created_date': datetime.utcnow(),
        }
        hook_log = HookLog(**payload)
        db.session.add(hook_log)
        db.session.commit()
        return hook_log


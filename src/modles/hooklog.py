from datetime import datetime

from src.extensions import db

from sqlalchemy import Column

from src.modles.base import JsonType, Base
from src.utils import get_current_time


class HookLog(db.Model, Base):
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
        return HookLog.insert(hook_log)


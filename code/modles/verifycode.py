from datetime import datetime

from sqlalchemy import Column

from code.extensions import db
from code.utils import get_current_time


class VerifyCode(db.Model):
    """
    Example Logger model
    """

    __tablename__ = 'verify_codes'
    LOG_LENGTH = 500

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = Column(db.Integer)
    code_number = Column(db.String(LOG_LENGTH))
    phone_number = Column(db.String(LOG_LENGTH))
    created_date = Column(db.DateTime, default=get_current_time)

    @staticmethod
    def add(payload):
        payload = {
            'user_id': payload.get("user_id"),
            'code_number': payload.get("code_number"),
            'phone_number': payload.get("phone_number"),
            'created_date': datetime.utcnow(),
        }
        hook_log = VerifyCode(**payload)
        db.session.add(hook_log)
        db.session.commit()
        return hook_log

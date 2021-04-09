# -*- coding: utf-8 -*-

from sqlalchemy import Column
from ..extensions import db
from ..utils import get_current_time


class Logs(db.Model):
    """
    CREATE TABLE logs(id INT AUTO_INCREMENT PRIMARY KEY, info VARCHAR(500), created_time DATETIME)
    """

    __tablename__ = 'logs'
    LOG_LENGTH = 500

    id = Column(db.Integer, primary_key=True)
    info = Column(db.String(LOG_LENGTH), nullable=False, unique=True)
    created_time = Column(db.DateTime, default=get_current_time)

    @classmethod
    def save(cls, info):
        # Add record with phone, otp, type
        log = Logs()
        log.info = info
        log.created_time = get_current_time()
        db.session.add(log)
        db.session.commit()

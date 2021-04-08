# -*- coding: utf-8 -*-
from datetime import datetime
from bson import ObjectId
from pymodm import fields
from ..base.model import Base


class Logger(Base):
    """
    Example Logger model
    """

    class Meta:
        collection_name = 'logger'
        final = True

    _id = fields.ObjectIdField(primary_key=True)
    event = fields.CharField(default='', blank=True)
    description = fields.CharField(default='', blank=True)

    @staticmethod
    def add(payload):
        return Logger(_id=ObjectId(), event=payload['event'], description=payload['description'], 
            createdDate=datetime.utcnow(), updatedDate=datetime.utcnow()).save()


class Voter(Base):
    """
    Example Logger model
    """

    class Meta:
        collection_name = 'voter'
        final = True

    _id = fields.ObjectIdField(primary_key=True)
    userId = fields.CharField(default='', blank=False)
    postId = fields.CharField(default='', blank=False)
    vote = fields.IntegerField(default='', blank=True)
    kill = fields.IntegerField(default='', blank=True)
    status = fields.BooleanField(default=True, blank=True)

    @staticmethod
    def add(payload):
        return Voter(_id=ObjectId(), userId=payload['userId'], postId=payload['postId'],
                      vote=payload['vote'], kill=payload['kill'], createdDate=datetime.utcnow(),
                      updatedDate=datetime.utcnow()).save()


    @staticmethod
    def get_voter(user_id, post_id):
        return Voter.find({'userId': user_id, 'postId': post_id})
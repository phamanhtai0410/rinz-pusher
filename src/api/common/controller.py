# -*- coding: utf-8 -*-
from datetime import datetime
from src.decorators.handle_response import handle_response
from src.exceptions import ExceptionNotFound

from bson import ObjectId
from flask import g

from src.decorators.load_body import load_data
from src.schemas import Example
from src.schemas.example import ExampleResponse
from src.utils.logger import Logger


@handle_response()
@load_data(Example)
def cl_health_check():
    data = g.data
    Logger.debug("call health_check", data)
    if data:
        raise ExceptionNotFound

    return ExampleResponse.load_response({
        '_id': ObjectId(),
        'created_time': datetime.utcnow()
    })

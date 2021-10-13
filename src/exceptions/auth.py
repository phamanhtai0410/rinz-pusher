# -*- coding: utf-8 -*-

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionRequiredAuth(BadRequestException):
    def __init__(self, response=make_response(
        error_code='ERROR_AUTH',
        status=Constants.STATUS_NOT_OK,
        msg='Auth is required'
    ), *args: object) -> None:
        super().__init__(*args)
        self.response = response

    pass

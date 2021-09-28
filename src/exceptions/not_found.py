# -*- coding: utf-8 -*-

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExeceptionNotFound(BadRequestException):
    def __init__(self, message=Constants.MSG_NOT_FOUND, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code=Constants.ERROR_NOT_FOUND,
            status=Constants.MSG_NOT_FOUND,
            msg=message
        )
    pass

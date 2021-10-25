from .common import rest_service
from .iapi import rest_iapi
from .user import rest_user
from .wowza import rest_wowza

rest_app = (
    rest_service,
    rest_user,
    rest_iapi,
    rest_wowza
)

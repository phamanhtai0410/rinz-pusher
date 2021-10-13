from .common import rest_service
from .user import rest_user

rest_app = (
    rest_service,
    rest_user
)

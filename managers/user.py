import jwt
from datetime import datetime

from validators import UserValidator
from repositories import UserRepository
from serializers import UserSerializer
from models import User
from exceptions import SanicException

from configurations.settings import AUTH_SECRET


class UserManager:

    _user = None

    def __init__(self) -> None:
        pass

    @staticmethod
    async def signup_user(payload):
        UserValidator.validate_signup_params(payload)
        user = await UserRepository.get_or_create_user(payload)
        return UserSerializer.serialize_user(user)

    @staticmethod
    async def login_user(payload):
        UserValidator.validate_login_params(payload)
        user = await User.authenticate(**payload)
        if user is None:
            raise SanicException("Invalid credentials", status_code=400)
        token = jwt.encode(
            {"user_id": str(user.static_id), "timestamp": str(datetime.now())},
            key=AUTH_SECRET,
        )
        return token

    @classmethod
    async def change_password(cls, payload):
        user = cls._user
        UserValidator.validate_change_password(payload)
        user.set_password(payload.get("password"))
        await user.save()

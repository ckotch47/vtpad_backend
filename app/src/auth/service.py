from fastapi.security import OAuth2PasswordBearer

from ..common.crypto import verify_password, create_access_token
from ..users.service import UserService
from .dto import *



class AuthService:
    @staticmethod
    async def authenticate_user(user: AuthUserDto):
        this_user = await UserService.get_user_by_mail(user.mail)
        if not this_user:
            return None

        if not await verify_password(user.password, this_user.password):
            return 'not password'

        return await create_access_token({"mail": this_user.mail, "id": str(this_user.id)})

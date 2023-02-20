from .dto import *
from .model import *
from ..common.crypto import *


class UserService:
    @staticmethod
    async def create_user(user: RegisterUserDto):
        return await UserModel.create(
            username=user.username,
            mail=user.mail,
            password=await get_password_hash(user.password),
        )

    @staticmethod
    async def get_user_by_mail(user_mail: str):
        return await UserModel.get_or_none(mail=user_mail)

    @staticmethod
    async def get_user_by_id(user_payload: dict):
        return await UserModel.get_or_none(id=user_payload.get('id'))

    @staticmethod
    async def update_user(dto: UpdateUserDto, user: dict):
        # self_user = await UserModel.filter(id=user.get('id')).get()
        await UserModel.filter(id=user.get('id')).update(username=dto.username)
        return await UserService.get_user_by_id(user)

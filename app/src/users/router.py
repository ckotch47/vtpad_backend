from fastapi import APIRouter, Depends
from .dto import *
from .service import UserService

from ..common.crypto import bearer, user_payload

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"message": "Not found"}},
)


@router.post('')
async def register_user(user: RegisterUserDto):
    return await UserService.create_user(user)


@router.get('', dependencies=[Depends(bearer)])
async def get_user(token: str = Depends(bearer)):
    return await UserService.get_user_by_id(user_payload(token))


@router.patch('', dependencies=[Depends(bearer)])
async def update_user(user: UpdateUserDto, token: str = Depends(bearer)):
    return await UserService.update_user(user, user_payload(token))

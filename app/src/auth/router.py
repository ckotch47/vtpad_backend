from fastapi import Depends, APIRouter, HTTPException
from .dto import *
from .service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"message": "Not found"}},
)


@router.post('')
async def auth(user: AuthUserDto):
    return await AuthService.authenticate_user(user)

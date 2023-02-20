from fastapi import APIRouter, Depends
from .service import PadService
from .dto import *
from ..common.crypto import bearer, user_payload
from ..spacesuser.service import SpacesUserService

router = APIRouter(
    prefix='/pad',
    tags=['pad'],
    responses={404: {"message": "Not found"}},
)


@router.get('/{space_id}', dependencies=[Depends(bearer)])
async def get_pad(space_id: str):
    return await PadService.get_pad(space_id)


@router.post('/{space_id}', dependencies=[Depends(bearer)])
async def create_pad(space_id: str, item: CreatePadDto):
    return await PadService.create_pad(space_id, item)


@router.put('/{pad_id}', dependencies=[Depends(bearer)])
async def update_pad(pad_id: str, item: UpdatePadDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_pad(user_payload(token), pad_id)
    return await PadService.update_pad(pad_id, item)


@router.delete('/{pad_id}', dependencies=[Depends(bearer)])
async def delete_pad(pad_id: str, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_pad(user_payload(token), pad_id)
    return await PadService.delete_pad(pad_id)


@router.patch('/{pad_id}', dependencies=[Depends(bearer)])
async def update_sort_pad(pad_id: str, dto: UpdateSortPadDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_pad(user_payload(token), pad_id)
    return await PadService.update_sort_pad(pad_id, dto)

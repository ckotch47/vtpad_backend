from fastapi import APIRouter, Depends

from .dto import *
from .service import ItemsService
from ..common.crypto import bearer, user_payload
from ..space.service import SpaceService
from ..spacesuser.service import SpacesUserService

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"message": "Not found"}},
)


@router.get('/{pad_id}', dependencies=[Depends(bearer)])
async def get_items(pad_id: str):
    return await ItemsService.get_items(pad_id)


@router.post('/{pad_id}', dependencies=[Depends(bearer)])
async def create_item(pad_id: str, item: CreateItemDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_pad(user_payload(token), pad_id)
    return await ItemsService.create_item(pad_id, item)


@router.put('/{item_id}', dependencies=[Depends(bearer)])
async def update_item(item_id: str, item: UpdateItemDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_items(user_payload(token), item_id)
    return await ItemsService.update_item(item_id, item)


@router.delete('/{item_id}', dependencies=[Depends(bearer)])
async def delete_item(item_id: str, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_items(user_payload(token), item_id)
    return await ItemsService.delete_item(item_id)


@router.patch('/{item_id}', dependencies=[Depends(bearer)])
async def update_path_item(item_id: str, dto: UpdateSortItemDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_items(user_payload(token), item_id)
    return await ItemsService.update_path_item(item_id, dto)

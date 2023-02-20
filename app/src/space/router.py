from fastapi import APIRouter, Depends, HTTPException
from .service import SpaceService
from .dto import *
from ..common.crypto import bearer, user_payload

router = APIRouter(
    prefix="/space",
    tags=["space"],
    responses={404: {"message": "Not found"}},
)


@router.get('', dependencies=[Depends(bearer)])
async def get_space(token: str = Depends(bearer)):
    return await SpaceService.get_space(user_payload(token))


@router.post('', dependencies=[Depends(bearer)])
async def create_space(space: CreateSpaceDto, token: str = Depends(bearer)):
    return await SpaceService.create_space(space, user_payload(token))


@router.get('/{space_id}', dependencies=[Depends(bearer)])
async def get_space_by_id(space_id: str, token: str = Depends(bearer)):
    return await SpaceService.get_space_by_id(user_payload(token), space_id)


@router.get('/{space_id}/users', dependencies=[Depends(bearer)])
async def get_space_by_id(space_id: str):
    return await SpaceService.get_user_for_space(space_id)


@router.put('/{space_id}', dependencies=[Depends(bearer)])
async def update_space(space_id: str, space: UpdateSpaceDto, token: str = Depends(bearer)):
    await SpaceService.check_owner(user_payload(token), space_id)
    return await SpaceService.update_space(space_id, space)


@router.put('/{space_id}/user', dependencies=[Depends(bearer)])
async def update_space_user(space_id: str, mail: AddUserSpaceDto, token: str = Depends(bearer)):
    await SpaceService.check_owner(user_payload(token), space_id)
    return await SpaceService.add_user_space(space_id, mail, user_payload(token))


@router.delete('/{space_id}/user/{user_id}', dependencies=[Depends(bearer)])
async def delete_space_user_id(space_id: str, user_id: str, token: str = Depends(bearer)):
    await SpaceService.check_owner(user_payload(token), space_id)
    return await SpaceService.delete_user_from_space(user_id, space_id, user_payload(token))


@router.patch('/{space_id}/user/{user_id}', dependencies=[Depends(bearer)])
async def update_user_rules_in_space(space_id: str, user_id: str,
                                     dto: UpdateUserRulesForSpaceDto, token: str = Depends(bearer)):
    await SpaceService.check_owner(user_payload(token), space_id)
    return await SpaceService.update_user_rules_in_space(space_id, user_id, dto)


@router.delete('/{space_id}', dependencies=[Depends(bearer)])
async def delete_space(space_id: str, token: str = Depends(bearer)):
    await SpaceService.check_owner(user_payload(token), space_id)
    return await SpaceService.delete_space(space_id)


@router.get('/{space_id}/all_runs')
async def get_all_runs_spaces(space_id: str):
    return await SpaceService.get_all_runs_spaces(space_id)

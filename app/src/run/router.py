from fastapi import APIRouter, Depends
from .service import RunService
from .dto import *
from ..common.crypto import bearer, user_payload
from ..spacesuser.service import SpacesUserService

router = APIRouter(
    prefix="/runs",
    tags=["runs"],
    responses={404: {"message": "Not found"}},
)


@router.post('/{pad_id}', dependencies=[Depends(bearer)])
async def create_run(pad_id: str, run: CreateRunDto, token: str = Depends(bearer)):
    await SpacesUserService.check_right_edit_pad(user_payload(token), pad_id)
    return await RunService.create_run(pad_id, run)


@router.delete('/{run_id}', dependencies=[Depends(bearer)])
async def delete_run(run_id: str, token: str = Depends(bearer)):
    await SpacesUserService.check_tight_runs(user_payload(token), run_id)
    return await RunService.delete_run(run_id)


@router.get('/items/{run_id}', dependencies=[Depends(bearer)])
async def get_items_fro_run(run_id: str):
    return await RunService.get_items_fro_run(run_id)


@router.get('/{run_id}', dependencies=[Depends(bearer)])
async def get_run(run_id: str):
    return await RunService.get_run(run_id)


@router.get('/all/{pad_id}', dependencies=[Depends(bearer)])
async def get_all_run(pad_id: str):
    return await RunService.get_all_run(pad_id)


@router.patch('/{run_id}', dependencies=[Depends(bearer)])
async def update_run(run_id: str, name: str, token: str = Depends(bearer)):
    await SpacesUserService.check_right_runs(user_payload(token), run_id)
    return await RunService.update_run(run_id, name)

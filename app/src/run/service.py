from asyncio import sleep
from datetime import datetime

from .model import RunModel
from ..runitems import RunItemsService
from .dto import *


class RunService:
    @staticmethod
    async def create_run(pad_id: str, run: CreateRunDto):
        temp = await RunModel.create(
            name=run.name,
            date=datetime.now(),
            pads_id=pad_id
        )
        await RunItemsService.create_run_item(temp.id)
        return temp

    @staticmethod
    async def get_items_fro_run(run_id: str):
        return await RunItemsService.get_item_for_run(run_id)

    @staticmethod
    async def get_all_run(pad_id: str):
        return await RunModel.filter(pads_id=pad_id).order_by('-date')

    @staticmethod
    async def delete_run(run_id: str):
        return bool(await RunModel.filter(id=run_id).delete())

    @staticmethod
    async def get_run(run_id: str):
        return await RunModel.filter(id=run_id).first()

    @staticmethod
    async def update_run(run_id: str, name: str):
        return bool(await RunModel.filter(id=run_id).update(name=name))
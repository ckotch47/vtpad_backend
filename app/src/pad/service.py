from .model import PadModel
from .dto import *


class PadService:
    @staticmethod
    async def create_pad(space_id: str, pad: CreatePadDto):
        last_sort = await PadModel.filter(spaces_id=space_id).order_by('-sort').first()
        try:
            sort = ((last_sort.sort / 1000) + 1) * 1000
        except:
            sort = 1000

        temp = await PadModel.create(
            name=pad.name,
            sort=sort,
            spaces_id=space_id
        )
        return {
            'id': temp.id,
            'name': temp.name,
            'sort': temp.sort,
            'item': []
        }

    @staticmethod
    async def get_pad(space_id: str):
        temp = await PadModel.filter(spaces_id=space_id).order_by('sort')
        return temp

    @staticmethod
    async def update_pad(pad_id: str, pad: UpdatePadDto):
        return bool(await PadModel.filter(id=pad_id).update(name=pad.name))

    @staticmethod
    async def delete_pad(pad_id: str):
        temp = bool(await PadModel.filter(id=pad_id).delete())
        if not temp:
            return temp

    @staticmethod
    async def update_sort_pad(pad_id: str, dto: UpdateSortPadDto):
        temp = None
        if dto.sortBeforeId:
            temp = await PadModel.filter(id=dto.sortBeforeId).get()
            temp1 = await PadModel.filter(id=pad_id).get()
            await PadModel.filter(id=dto.sortBeforeId).update(sort=temp1.sort)
            await PadModel.filter(id=pad_id).update(sort=temp.sort)
        if dto.sortAfterId:
            temp = await PadModel.filter(id=dto.sortAfterId).get()
            temp1 = await PadModel.filter(id=pad_id).get()
            await PadModel.filter(id=dto.sortAfterId).update(sort=temp1.sort)
            await PadModel.filter(id=pad_id).update(sort=temp.sort)

        try:
            print(str(temp.spaces_id))
            return await PadService.get_pad(str(temp.spaces_id))
        except:
            return True

from .model import ItemsModel
from .dto import *
from fastapi import HTTPException


class ItemsService:
    @staticmethod
    async def create_item(pad_id: str, item: CreateItemDto):
        main_id = item.mainId
        try:
            last_sort = await ItemsModel.filter(pad_id=pad_id, mainId=main_id).order_by('-sort').first()
            try:
                sort = ((last_sort.sort / 1000) + 1) * 1000
            except:
                sort = 1000

            temp = await ItemsModel.create(
                text=item.text,
                sort=sort,
                pad_id=pad_id,
                mainId=main_id
            )
            return {
                'id': temp.id,
                'text': temp.text,
                'sort': temp.sort,
                'subItem': []
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{e}')

    @staticmethod
    async def get_items(pad_id: str):
        try:
            temp = await ItemsModel.filter(pad_id=pad_id, mainId=None).order_by('sort')
            res = []
            for i in temp:
                try:
                    sub_item = await ItemsModel.filter(mainId=i.id).order_by('sort')
                except:
                    sub_item = []
                res.append({
                    'id': i.id,
                    'text': i.text,
                    'sort': i.sort,
                    'subItem': sub_item
                })
            return res
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{e}')

    @staticmethod
    async def update_item(item_id: str, item: UpdateItemDto):
        try:
            return bool(await ItemsModel.filter(id=item_id).update(text=item.text))

        except Exception as e:
                raise HTTPException(status_code=500, detail=f'{e}')

    @staticmethod
    async def delete_item(item_id: str):
        try:
            await ItemsModel.filter(id=item_id).delete()
            return bool(await ItemsModel.filter(mainId=item_id).delete())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'{e}')

    @staticmethod
    async def update_path_item(item_id: str, dto: UpdateSortItemDto):
        temp = None
        if dto.sortBeforeId:
            temp = await ItemsModel.filter(id=dto.sortBeforeId).get()
            temp1 = await ItemsModel.filter(id=item_id).get() #.update(sort=(temp.sort - 1))
            await ItemsModel.filter(id=dto.sortBeforeId).update(sort=temp1.sort)
            await ItemsModel.filter(id=item_id).update(sort=temp.sort)
        if dto.sortAfterId:
            temp = await ItemsModel.filter(id=dto.sortAfterId).get()
            temp1 = await ItemsModel.filter(id=item_id).get()
            await ItemsModel.filter(id=dto.sortAfterId).update(sort=temp1.sort)
            await ItemsModel.filter(id=item_id).update(sort=temp.sort)

        try:
            return await ItemsService.get_items(str(temp.pad_id))
        except:
            return True
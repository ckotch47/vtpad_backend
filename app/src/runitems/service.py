from typing import Union

from tortoise import Tortoise

from .model import RunItemsModel
from .dto import *

class RunItemsService:
    @staticmethod
    async def create_run_item(run_id: str):
        conn = Tortoise.get_connection("default")
        run = await conn.execute_query_dict(f"SELECT * FROM runmodel WHERE id='{run_id}'")
        pad = run[0].get('pads_id')
        items: [RunItemsModel] = await conn.execute_query_dict(f"SELECT * FROM itemsmodel WHERE pad_id='{pad}'")
        temp = []
        for item in items:
            await RunItemsModel.create(
                            itemId=item.get('id'),
                            run_id=run_id
                        )
        return temp

    @staticmethod
    async def get_item_for_run(run_id: str):
        conn = Tortoise.get_connection("default")
        res = []
        main_items = await conn.execute_query_dict(f"SELECT * FROM itemsmodel LEFT JOIN runitemsmodel ON itemsmodel.id = runitemsmodel.\"itemId\"  WHERE itemsmodel.\"mainId\" IS NULL AND runitemsmodel.run_id = '{run_id}' ORDER BY itemsmodel.sort ASC")
        for main_item in main_items:
            sub_item = await conn.execute_query_dict(f"SELECT * FROM itemsmodel LEFT JOIN runitemsmodel ON itemsmodel.id = runitemsmodel.\"itemId\"  WHERE itemsmodel.\"mainId\"='{main_item.get('itemId')}' AND runitemsmodel.run_id = '{run_id}' ORDER BY itemsmodel.sort ASC")
            main_item['subItem'] = sub_item
            res.append(main_item)
        return res

    @staticmethod
    async def update_run_item(item_id: str, state: State):
        return bool(await RunItemsModel.filter(id=item_id).update(state=state))

    @staticmethod
    async def get_count_state_item(run_id: str, state: Union[str, None]):
        if type(state) is str:
            return await RunItemsModel.filter(run_id=run_id, state=state).count()
        else:
            return await RunItemsModel.filter(run_id=run_id).count()

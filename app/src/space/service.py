from typing import List

from fastapi import HTTPException
from tortoise import Tortoise

from .model import SpaceModel
from .dto import *
from ..pad.model import PadModel
from ..pad.service import PadService
from ..run.service import RunService
from ..runitems import RunItemsService
from ..spacesuser.model import SpacesUserModel, SpacesUserRole
from ..users.model import UserModel


class SpaceService:
    @staticmethod
    async def create_space(space: CreateSpaceDto, user: dict):
        last_sort = await SpaceService.get_space(user, 'DESC')
        last_sort = last_sort[0].get('sort')
        this_user = await UserModel.filter(id=user.get('id')).get_or_none()
        if not this_user:
            return None

        try:
            sort = ((last_sort / 1000) + 1) * 1000
        except:
            sort = 1000

        temp = await SpaceModel.create(
            name=space.name,
            sort=sort
        )

        await SpacesUserModel.create(
            userId=this_user.id,
            spaceId=temp.id,
            role=SpacesUserRole.owner)

        await PadModel.create(
            name='Pad',
            sort=1000,
            spaces_id=temp.id
        )

        return temp

    @staticmethod
    async def get_space_by_id(user: dict, space_id: str):
        return await SpaceModel.filter(id=space_id).get()

    @staticmethod
    async def get_user_for_space(space_id: str):
        conn = Tortoise.get_connection("default")
        return await conn.execute_query_dict(
            f'SELECT "userId", "spaceId", role, "right", username, avatar_id, mail, filepath FROM spacesusermodel '
            f'LEFT JOIN usermodel on spacesusermodel."userId" = usermodel.id '
            f'LEFT JOIN filemodel f on usermodel.avatar_id = f.id '
            f'WHERE spacesusermodel."spaceId" = \'{space_id}\''
            f'ORDER BY spacesusermodel.role DESC')


    @staticmethod
    async def get_space(user: dict, order='ASC'):
        this_user = await UserModel.filter(id=user.get('id')).get_or_none()
        conn = Tortoise.get_connection("default")
        sql = f'SELECT  "spaceId" as id, role, "right", name, sort FROM spacesusermodel ' \
              f'LEFT JOIN spacemodel s on spacesusermodel."spaceId" = s.id ' \
              f'WHERE spacesusermodel."userId" = \'' + str(this_user.id) + f'\' ORDER BY s.sort {order} '
        return await conn.execute_query_dict(sql)

    @staticmethod
    async def update_space(space_id: str, space: UpdateSpaceDto):
        return bool(await SpaceModel.filter(id=space_id).update(name=space.name))

    @staticmethod
    async def add_user_space(space_id: str, dto: AddUserSpaceDto, user: dict):
        self_user = await UserModel.filter(mail=dto.mail).first()
        if not self_user.id:
            return None
        temp = await SpacesUserModel.filter(userId=self_user.id, spaceId=space_id)
        print(temp)
        if temp != []:
            return None
        await SpacesUserModel.create(
            userId=self_user.id,
            spaceId=space_id,
            role=SpacesUserRole.collaborator)
        return await SpaceService.get_user_for_space(space_id)

    @staticmethod
    async def delete_space(space_id: str):
        temp = bool(await SpaceModel.filter(id=space_id).delete())
        await SpacesUserModel.filter(spaceId=space_id).delete()
        return temp

    @staticmethod
    async def delete_user_from_space(user_id: str, space_id: str, user: dict):
        self_user = await UserModel.filter(id=user.get('id')).get()
        if self_user.id == user_id:
            return 'no delete self'
        space = await SpacesUserModel.filter(userId=user_id, spaceId=space_id).get()
        if space.role == SpacesUserRole.owner:
            return 'no delete owner'
        await SpacesUserModel.filter(userId=user_id, spaceId=space_id).delete()
        return await SpaceService.get_user_for_space(space_id)

    @staticmethod
    async def check_owner(user_payload: dict, space_id: str):
        user = await UserModel.filter(id=user_payload.get('id')).get()
        space_user = await SpacesUserModel.filter(userId=user.id, spaceId=space_id).get()
        if space_user.role != SpacesUserRole.owner:
            raise HTTPException(status_code=403, detail="not have rule")
        else:
            return True

    @staticmethod
    async def update_user_rules_in_space(space_id: str, user_id: str, dto: UpdateUserRulesForSpaceDto):
        temp: dict = (await SpacesUserModel.filter(spaceId=space_id, userId=user_id).get()).right
        print(temp)
        if dto.editPads is not None:
            temp['editPads'] = dto.editPads
        if dto.editRuns is not None:
            temp['editRuns'] = dto.editRuns
        if dto.editItems is not None:
            temp['editItems'] = dto.editItems
        if dto.editNotes is not None:
            temp['editNotes'] = dto.editNotes

        await SpacesUserModel.filter(spaceId=space_id, userId=user_id).update(right=temp)
        return await SpaceService.get_user_for_space(space_id)

    @staticmethod
    async def get_all_runs_spaces(space_id):
        conn = Tortoise.get_connection('default')
        space = await SpaceService.get_space_by_id({}, space_id)

        pad: dict = await PadService.get_pad(space_id)

        res = []

        for i in pad:
            runs = []
            run = await RunService.get_all_run(i.id)
            for j in run:
                runs.append({
                    "name": j.name,
                    "id": j.id,
                    "date": j.date,
                    "itemsCount": {
                        "pass": await RunItemsService.get_count_state_item(j.id, 'pass'),
                        "fail": await RunItemsService.get_count_state_item(j.id, 'fail'),
                        "all": await RunItemsService.get_count_state_item(j.id, None)
                    }
                })
            res.append({
                "padId": i.id,
                "padName": i.name,
                "run": runs
            })

        return {
            "spaceId": space.id,
            "spaceName": space.name,
            "pad": res
        }

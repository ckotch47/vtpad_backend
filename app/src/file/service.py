import shutil

from fastapi import UploadFile
from .model import FileModel
from ..users.model import UserModel


class FileService:
    @staticmethod
    async def save_file(file: UploadFile, user: dict):
        file_location = f'uploads/{file.filename}'
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        avatar = await FileModel.create(filepath=file_location)
        await UserModel.filter(id=user.get('id')).update(avatar=avatar)
        temp = await UserModel.filter(id=user.get('id')).get()
        return temp

    @staticmethod
    async def get_file(file_id: str):
        return await FileModel.filter(id=file_id).get()

from typing import Union

from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    username: Union[str, None]

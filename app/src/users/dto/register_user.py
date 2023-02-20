from typing import Union

from pydantic import BaseModel


class RegisterUserDto(BaseModel):
    username: Union[str, None]
    mail: str
    password: str

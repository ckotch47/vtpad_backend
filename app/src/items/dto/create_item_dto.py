from typing import Union

from pydantic import BaseModel


class CreateItemDto(BaseModel):
    text: Union[str, None]
    mainId: Union[str, None]

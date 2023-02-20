from pydantic import BaseModel
from typing import Union


class UpdateSortPadDto(BaseModel):
    sortAfterId: Union[str, None]
    sortBeforeId: Union[str, None]

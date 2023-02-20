from typing import Union

from pydantic import BaseModel


class UpdateSortItemDto(BaseModel):
    sortAfterId: Union[str, None]
    sortBeforeId: Union[str, None]
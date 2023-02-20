from typing import Union

from pydantic import BaseModel


class UpdateUserRulesForSpaceDto(BaseModel):
    editPads: Union[bool, None]
    editItems: Union[bool, None]
    editRuns: Union[bool, None]
    editNotes: Union[bool, None]


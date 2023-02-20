from enum import Enum

from pydantic import BaseModel


class State(str, Enum):
    PASS = 'pass'
    FAIL = 'fail'


class UpdateRunItemDto(BaseModel):
    state: State = None

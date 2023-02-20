from pydantic import BaseModel


class CreatePadDto(BaseModel):
    name: str


from pydantic import BaseModel



class UpdatePadDto(BaseModel):
    name: str


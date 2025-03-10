from pydantic import BaseModel

class Codigo(BaseModel):
    codigo: str
    orden: int
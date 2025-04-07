from pydantic import BaseModel

class TiposNecesidades(BaseModel):
    tipos_necesidad: list[int]
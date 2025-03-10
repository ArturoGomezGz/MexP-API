from pydantic import BaseModel

class Sal(BaseModel):
    sal: str
    unidad: int
    tipoUnidad: str
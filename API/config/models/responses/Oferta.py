from pydantic import BaseModel

class Oferta(BaseModel):
    escala: int
    descuento: float
    porcentaje: float
    unitario: float
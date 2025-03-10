from pydantic import BaseModel
from typing import Optional

class FacturaProducto(BaseModel):
    idProducto: int
    nombre: str
    presentacion: str
    solicitado: float
    cantidad: int
    precioUnitario: float
    lote: str
    caducidad: Optional[str]